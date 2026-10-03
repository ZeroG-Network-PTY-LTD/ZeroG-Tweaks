package net.zerog.tweaks.worldgen;

import com.mojang.datafixers.util.Either;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePiecesBuilder;
import net.minecraft.world.level.levelgen.structure.pools.DimensionPadding;
import net.minecraft.world.level.levelgen.structure.pools.JigsawPlacement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.levelgen.structure.pools.alias.PoolAliasLookup;
import net.minecraft.world.level.levelgen.structure.templatesystem.LiquidSettings;

/**
 * A surface jigsaw structure that only generates on dry, fairly level ground.
 *
 * Planet terrain (Cerulon etc.) has oceans inside land biomes, so a plain minecraft:jigsaw boss arena could land in
 * the sea. This builds the jigsaw exactly like vanilla (start projected to WORLD_SURFACE_WG, start_height added on
 * top), then samples a 5x5 grid over the finished bounding box and rejects the spot if any sample is under water
 * (surface above the ocean floor) or the surface varies by more than max_height_difference. With search_radius set,
 * it tries nearby spots before giving up (needed when the placement allows only one arena per world).
 */
public class DryLandJigsawStructure extends Structure {
    public static final MapCodec<DryLandJigsawStructure> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            settingsCodec(instance),
            StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
            Codec.intRange(0, 20).optionalFieldOf("size", 1).forGetter(s -> s.maxDepth),
            Codec.intRange(-64, 64).optionalFieldOf("start_height", 0).forGetter(s -> s.startHeight),
            Codec.intRange(1, 128).optionalFieldOf("max_distance_from_center", 80).forGetter(s -> s.maxDistanceFromCenter),
            Codec.intRange(0, 64).optionalFieldOf("max_height_difference", 4).forGetter(s -> s.maxHeightDifference),
            Codec.intRange(0, 80).optionalFieldOf("search_radius", 0).forGetter(s -> s.searchRadius)
    ).apply(instance, DryLandJigsawStructure::new));

    private static final int SAMPLES = 5;
    private static final int SEARCH_STEP = 16;

    private final Holder<StructureTemplatePool> startPool;
    private final int maxDepth;
    private final int startHeight;
    private final int maxDistanceFromCenter;
    private final int maxHeightDifference;
    private final int searchRadius;

    public DryLandJigsawStructure(StructureSettings settings, Holder<StructureTemplatePool> startPool, int maxDepth,
                                  int startHeight, int maxDistanceFromCenter, int maxHeightDifference, int searchRadius) {
        super(settings);
        this.startPool = startPool;
        this.maxDepth = maxDepth;
        this.startHeight = startHeight;
        this.maxDistanceFromCenter = maxDistanceFromCenter;
        this.maxHeightDifference = maxHeightDifference;
        this.searchRadius = searchRadius;
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        var chunk = context.chunkPos();
        // search_radius > 0 (one-per-world placements such as concentric_rings): try spots on a 16-block grid around the
        // chunk, nearest first, so a single placement that lands on water still finds the closest dry ground. Capped at 80:
        // pieces must stay within 8 chunks of the start chunk to be referenced (80 + a 47-wide template <= 128)
        List<int[]> offsets = new ArrayList<>();
        for (int ox = -searchRadius; ox <= searchRadius; ox += SEARCH_STEP) {
            for (int oz = -searchRadius; oz <= searchRadius; oz += SEARCH_STEP) {
                if (ox * ox + oz * oz <= searchRadius * searchRadius) offsets.add(new int[] {ox, oz});
            }
        }
        offsets.sort(Comparator.comparingInt(o -> o[0] * o[0] + o[1] * o[1]));
        for (int[] o : offsets) {
            Optional<GenerationStub> stub = JigsawPlacement.addPieces(context, startPool, Optional.empty(), maxDepth,
                    new BlockPos(chunk.getMinBlockX() + o[0], startHeight, chunk.getMinBlockZ() + o[1]), false,
                    Optional.of(Heightmap.Types.WORLD_SURFACE_WG), maxDistanceFromCenter, PoolAliasLookup.EMPTY,
                    DimensionPadding.ZERO, LiquidSettings.APPLY_WATERLOGGING);
            if (stub.isEmpty() || !isValidBiomeAt(context, stub.get().position())) continue;
            // build the pieces now (the stub would build them later anyway) so the real footprint can be checked
            StructurePiecesBuilder pieces = stub.get().getPiecesBuilder();
            if (isDryAndLevel(context, pieces.getBoundingBox())) {
                return Optional.of(new GenerationStub(stub.get().position(), Either.right(pieces)));
            }
        }
        return Optional.empty();
    }

    /** Same test Structure#generate applies to the returned stub; checked per candidate so the search skips water biomes. */
    private static boolean isValidBiomeAt(GenerationContext context, BlockPos pos) {
        return context.validBiome().test(context.chunkGenerator().getBiomeSource().getNoiseBiome(QuartPos.fromBlock(pos.getX()),
                QuartPos.fromBlock(pos.getY()), QuartPos.fromBlock(pos.getZ()), context.randomState().sampler()));
    }

    private boolean isDryAndLevel(GenerationContext context, BoundingBox box) {
        var generator = context.chunkGenerator();
        int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
        for (int i = 0; i < SAMPLES; i++) {
            for (int k = 0; k < SAMPLES; k++) {
                int x = box.minX() + (box.maxX() - box.minX()) * i / (SAMPLES - 1);
                int z = box.minZ() + (box.maxZ() - box.minZ()) * k / (SAMPLES - 1);
                int surface = generator.getFirstFreeHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG,
                        context.heightAccessor(), context.randomState());
                int floor = generator.getFirstFreeHeight(x, z, Heightmap.Types.OCEAN_FLOOR_WG,
                        context.heightAccessor(), context.randomState());
                if (surface > floor) return false; // fluid on top
                min = Math.min(min, surface);
                max = Math.max(max, surface);
            }
        }
        return max - min <= maxHeightDifference;
    }

    @Override
    public StructureType<?> type() {
        return ZGStructures.DRY_LAND_JIGSAW.get();
    }
}
