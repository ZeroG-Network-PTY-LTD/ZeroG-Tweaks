package net.zerog.tweaks.worldgen;

import com.mojang.datafixers.util.Either;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
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
 * (surface above the ocean floor) or the surface varies by more than max_height_difference.
 */
public class DryLandJigsawStructure extends Structure {
    public static final MapCodec<DryLandJigsawStructure> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            settingsCodec(instance),
            StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
            Codec.intRange(0, 20).optionalFieldOf("size", 1).forGetter(s -> s.maxDepth),
            Codec.intRange(-64, 64).optionalFieldOf("start_height", 0).forGetter(s -> s.startHeight),
            Codec.intRange(1, 128).optionalFieldOf("max_distance_from_center", 80).forGetter(s -> s.maxDistanceFromCenter),
            Codec.intRange(0, 64).optionalFieldOf("max_height_difference", 4).forGetter(s -> s.maxHeightDifference)
    ).apply(instance, DryLandJigsawStructure::new));

    private static final int SAMPLES = 5;

    private final Holder<StructureTemplatePool> startPool;
    private final int maxDepth;
    private final int startHeight;
    private final int maxDistanceFromCenter;
    private final int maxHeightDifference;

    public DryLandJigsawStructure(StructureSettings settings, Holder<StructureTemplatePool> startPool, int maxDepth,
                                  int startHeight, int maxDistanceFromCenter, int maxHeightDifference) {
        super(settings);
        this.startPool = startPool;
        this.maxDepth = maxDepth;
        this.startHeight = startHeight;
        this.maxDistanceFromCenter = maxDistanceFromCenter;
        this.maxHeightDifference = maxHeightDifference;
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        var chunk = context.chunkPos();
        Optional<GenerationStub> stub = JigsawPlacement.addPieces(context, startPool, Optional.empty(), maxDepth,
                new BlockPos(chunk.getMinBlockX(), startHeight, chunk.getMinBlockZ()), false,
                Optional.of(Heightmap.Types.WORLD_SURFACE_WG), maxDistanceFromCenter, PoolAliasLookup.EMPTY,
                DimensionPadding.ZERO, LiquidSettings.APPLY_WATERLOGGING);
        if (stub.isEmpty()) return Optional.empty();
        // build the pieces now (the stub would build them later anyway) so the real footprint can be checked
        StructurePiecesBuilder pieces = stub.get().getPiecesBuilder();
        if (!isDryAndLevel(context, pieces.getBoundingBox())) return Optional.empty();
        return Optional.of(new GenerationStub(stub.get().position(), Either.right(pieces)));
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
