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
 * get a Key Altar in their centre, so every vault has exactly that many keys. If a layout has too few rooms it is
 * rebuilt (up to 10 tries). Rooms keep their centre 3x3 free for the altar (vault room brief).
 */
public class ConcordVaultStructure extends Structure {
    public static final MapCodec<ConcordVaultStructure> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            settingsCodec(instance),
            StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
            Codec.intRange(1, 20).fieldOf("size").forGetter(s -> s.size),
            Codec.intRange(-128, 0).fieldOf("start_height").forGetter(s -> s.startHeight),
            Codec.intRange(1, 128).fieldOf("max_distance_from_center").forGetter(s -> s.maxDistance),
            Codec.intRange(0, 16).fieldOf("key_rooms").forGetter(s -> s.keyRooms)
    ).apply(instance, ConcordVaultStructure::new));

    /** Room templates are 17 x 17; corridors, caps and the shaft are narrower; the chamber is 67 wide. */
    public static final int ROOM_SIZE = 15, CHAMBER_SIZE = 60;
    private static final int TRIES = 10;

    private final Holder<StructureTemplatePool> startPool;
    private final int size, startHeight, maxDistance, keyRooms;

    public ConcordVaultStructure(StructureSettings settings, Holder<StructureTemplatePool> startPool, int size, int startHeight,
                                 int maxDistance, int keyRooms) {
        super(settings);
        this.startPool = startPool;
        this.size = size;
        this.startHeight = startHeight;
        this.maxDistance = maxDistance;
        this.keyRooms = keyRooms;
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
            List<BoundingBox> rooms = rooms(pieces);
            if (best == null || rooms.size() > bestRooms.size()) {
                best = new GenerationStub(stub.get().position(), Either.right(pieces));
                bestRooms = rooms;
            }
            if (rooms.size() >= keyRooms) break;
        }
        if (best == null) return Optional.empty();
        StructurePiecesBuilder pieces = best.getPiecesBuilder();
        List<BoundingBox> pick = new ArrayList<>(bestRooms);
        for (int i = pick.size() - 1; i > 0; i--) java.util.Collections.swap(pick, i, context.random().nextInt(i + 1));
        for (BoundingBox room : pick.subList(0, Math.min(keyRooms, pick.size()))) {
            pieces.addPiece(new KeyAltarPiece(new BlockPos(room.minX() + room.getXSpan() / 2, room.minY() + 1,
                    room.minZ() + room.getZSpan() / 2)));
        }
        return Optional.of(best);
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
