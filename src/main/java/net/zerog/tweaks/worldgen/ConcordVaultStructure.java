package net.zerog.tweaks.worldgen;

import com.mojang.datafixers.util.Either;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.PoolElementStructurePiece;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePiecesBuilder;
import net.minecraft.world.level.levelgen.structure.pools.DimensionPadding;
import net.minecraft.world.level.levelgen.structure.pools.JigsawPlacement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.levelgen.structure.pools.alias.PoolAliasLookup;
import net.minecraft.world.level.levelgen.structure.templatesystem.LiquidSettings;

/**
 * The Concord Vault: the Prism Sentinel's chamber deep under Cerulon with corridors and rooms branching off it like a
 * mineshaft (a jigsaw from start_pool, start_height blocks below the surface), reached by a stair shaft from a shrine.
 *
 * After the layout is built, key_rooms of the rooms (pieces at least ROOM_SIZE wide both ways, other than the chamber)
 * get a Key Altar in their centre, so every vault has exactly that many keys, scattered (pickKeyRooms). A layout must
 * have at least min_rooms rooms, so most rooms hold no key; smaller layouts are rebuilt (up to TRIES times, then the
 * largest one is used). Rooms keep their centre 3x3 free for the altar (vault room brief).
 */
public class ConcordVaultStructure extends Structure {
    public static final MapCodec<ConcordVaultStructure> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            settingsCodec(instance),
            StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
            Codec.intRange(1, 20).fieldOf("size").forGetter(s -> s.size),
            Codec.intRange(-128, 0).fieldOf("start_height").forGetter(s -> s.startHeight),
            Codec.intRange(1, 128).fieldOf("max_distance_from_center").forGetter(s -> s.maxDistance),
            Codec.intRange(0, 16).fieldOf("key_rooms").forGetter(s -> s.keyRooms),
            Codec.intRange(0, 64).optionalFieldOf("min_rooms", 0).forGetter(s -> s.minRooms)
    ).apply(instance, ConcordVaultStructure::new));

    /** Room templates are 17 x 17; corridors, caps and the shaft are narrower; the chamber is 67 wide. */
    public static final int ROOM_SIZE = 15, CHAMBER_SIZE = 60;
    private static final int TRIES = 20;

    private final Holder<StructureTemplatePool> startPool;
    private final int size, startHeight, maxDistance, keyRooms, minRooms;

    public ConcordVaultStructure(StructureSettings settings, Holder<StructureTemplatePool> startPool, int size, int startHeight,
                                 int maxDistance, int keyRooms, int minRooms) {
        super(settings);
        this.startPool = startPool;
        this.size = size;
        this.startHeight = startHeight;
        this.maxDistance = maxDistance;
        this.keyRooms = keyRooms;
        this.minRooms = Math.max(minRooms, keyRooms);
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        var chunk = context.chunkPos();
        GenerationStub best = null;
        List<BoundingBox> bestRooms = List.of();
        for (int attempt = 0; attempt < TRIES; attempt++) {
            Optional<GenerationStub> stub = JigsawPlacement.addPieces(context, startPool, Optional.empty(), size,
                    new BlockPos(chunk.getMinBlockX(), startHeight, chunk.getMinBlockZ()), false,
                    Optional.of(Heightmap.Types.WORLD_SURFACE_WG), maxDistance, PoolAliasLookup.EMPTY,
                    DimensionPadding.ZERO, LiquidSettings.IGNORE_WATERLOGGING);
            if (stub.isEmpty()) continue;
            StructurePiecesBuilder pieces = stub.get().getPiecesBuilder();
            // Vanilla createReferences only discovers starts within eight chunks.
            // Jigsaw's own radius is centred on its rotated start template instead
            // of the start chunk, so an intact layout can otherwise escape it.
            var shift = fitToReferenceWindow(pieces, chunk);
            if (shift.isEmpty()) continue;
            List<BoundingBox> rooms = rooms(pieces);
            if (best == null || rooms.size() > bestRooms.size()) {
                best = new GenerationStub(stub.get().position().offset(shift.get()), Either.right(pieces));
                bestRooms = rooms;
            }
            if (rooms.size() >= minRooms) break;
        }
        if (best == null || bestRooms.size() < keyRooms) return Optional.empty();
        StructurePiecesBuilder pieces = best.getPiecesBuilder();
        BlockPos chamber = chamberCentre(pieces);
        for (BlockPos altar : pickKeyRooms(bestRooms, chamber, keyRooms, context.random())) {
            pieces.addPiece(new KeyAltarPiece(altar));
        }
        return Optional.of(best);
    }

    /** Translate the whole connected jigsaw, before adding keyed pieces. Never crop rooms. */
    private static Optional<BlockPos> fitToReferenceWindow(StructurePiecesBuilder pieces, net.minecraft.world.level.ChunkPos chunk) {
        var bounds = pieces.build().calculateBoundingBox();
        int minX = chunk.getMinBlockX() - 128, maxX = chunk.getMaxBlockX() + 128;
        int minZ = chunk.getMinBlockZ() - 128, maxZ = chunk.getMaxBlockZ() + 128;
        if (bounds.getXSpan() > maxX - minX + 1 || bounds.getZSpan() > maxZ - minZ + 1) return Optional.empty();
        int dx = bounds.minX() < minX ? minX - bounds.minX() : bounds.maxX() > maxX ? maxX - bounds.maxX() : 0;
        int dz = bounds.minZ() < minZ ? minZ - bounds.minZ() : bounds.maxZ() > maxZ ? maxZ - bounds.maxZ() : 0;
        if (dx != 0 || dz != 0) {
            for (var piece : pieces.build().pieces()) {
                piece.move(dx, 0, dz);
                if (piece instanceof PoolElementStructurePiece pool) {
                    // PoolElement.move shifts boxes and template position, but not
                    // junction metadata. Keep that metadata in the same world space.
                    pool.getJunctions().replaceAll(j -> new net.minecraft.world.level.levelgen.structure.pools.JigsawJunction(
                            j.getSourceX() + dx, j.getSourceGroundY(), j.getSourceZ() + dz, j.getDeltaY(), j.getDestProjection()));
                }
            }
        }
        return Optional.of(new BlockPos(dx, 0, dz));
    }

    /**
     * Scatters the keys: the first goes in one of the rooms farthest from the chamber, each next one in the room that is
     * farthest from the chamber and every key already placed (with a little randomness so layouts differ). Returns the
     * altar spot (centre, floor + 1) of each chosen room.
     */
    public static List<BlockPos> pickKeyRooms(List<BoundingBox> rooms, BlockPos chamber, int keys, net.minecraft.util.RandomSource random) {
        List<BlockPos> centres = new ArrayList<>();
        for (BoundingBox r : rooms) centres.add(new BlockPos(r.minX() + r.getXSpan() / 2, r.minY() + 1, r.minZ() + r.getZSpan() / 2));
        List<BlockPos> chosen = new ArrayList<>();
        List<BlockPos> anchors = new ArrayList<>(List.of(chamber));
        while (chosen.size() < keys && !centres.isEmpty()) {
            BlockPos pick = null;
            double bestScore = -1;
            for (BlockPos c : centres) {
                double nearest = Double.MAX_VALUE;
                for (BlockPos a : anchors) nearest = Math.min(nearest, horizontalDistance(c, a));
                double score = nearest * (0.75 + random.nextDouble() * 0.5);   // +-25%: spread out, not always the same rooms
                if (score > bestScore) { bestScore = score; pick = c; }
            }
            chosen.add(pick);
            anchors.add(pick);
            centres.remove(pick);
        }
        return chosen;
    }

    private static double horizontalDistance(BlockPos a, BlockPos b) {
        return Math.hypot(a.getX() - b.getX(), a.getZ() - b.getZ());
    }

    /** Centre of the chamber piece (the one wider than CHAMBER_SIZE). */
    private static BlockPos chamberCentre(StructurePiecesBuilder pieces) {
        for (StructurePiece piece : pieces.build().pieces()) {
            BoundingBox b = piece.getBoundingBox();
            if (Math.min(b.getXSpan(), b.getZSpan()) >= CHAMBER_SIZE) return b.getCenter();
        }
        return pieces.build().calculateBoundingBox().getCenter();
    }

    /** The room pieces of a built layout (wide in both directions, not the chamber). */
    public static List<BoundingBox> rooms(StructurePiecesBuilder pieces) {
        List<BoundingBox> rooms = new ArrayList<>();
        for (StructurePiece piece : pieces.build().pieces()) {
            if (!(piece instanceof PoolElementStructurePiece)) continue;
            BoundingBox b = piece.getBoundingBox();
            int min = Math.min(b.getXSpan(), b.getZSpan()), max = Math.max(b.getXSpan(), b.getZSpan());
            if (min >= ROOM_SIZE && max < CHAMBER_SIZE) rooms.add(b);
        }
        return rooms;
    }

    @Override
    public StructureType<?> type() {
        return ZGStructures.CONCORD_VAULT.get();
    }
}
