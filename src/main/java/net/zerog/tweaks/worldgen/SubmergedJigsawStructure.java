package net.zerog.tweaks.worldgen;

import com.mojang.datafixers.util.Either;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pools.DimensionPadding;
import net.minecraft.world.level.levelgen.structure.pools.JigsawPlacement;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.minecraft.world.level.levelgen.structure.pools.alias.PoolAliasLookup;
import net.minecraft.world.level.levelgen.structure.templatesystem.LiquidSettings;

/** Bounded single-room ocean-floor ruins; never falls back to a dry island or surface platform. */
public final class SubmergedJigsawStructure extends Structure {
    public static final MapCodec<SubmergedJigsawStructure> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
            settingsCodec(i),
            StructureTemplatePool.CODEC.fieldOf("start_pool").forGetter(s -> s.startPool),
            Codec.intRange(0, 12).optionalFieldOf("max_height_difference", 6).forGetter(s -> s.heightTolerance)
    ).apply(i, SubmergedJigsawStructure::new));

    private final Holder<StructureTemplatePool> startPool;
    private final int heightTolerance;

    public SubmergedJigsawStructure(StructureSettings settings, Holder<StructureTemplatePool> pool, int tolerance) {
        super(settings); startPool = pool; heightTolerance = tolerance;
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        var chunk = context.chunkPos();
        var stub = JigsawPlacement.addPieces(context, startPool, Optional.empty(), 1,
                new BlockPos(chunk.getMinBlockX(), -1, chunk.getMinBlockZ()), false,
                Optional.of(Heightmap.Types.OCEAN_FLOOR_WG), 48, PoolAliasLookup.EMPTY,
                DimensionPadding.ZERO, LiquidSettings.APPLY_WATERLOGGING);
        if (stub.isEmpty()) return Optional.empty();
        var anchor = stub.get().position();
        if (!context.validBiome().test(context.chunkGenerator().getBiomeSource().getNoiseBiome(
                QuartPos.fromBlock(anchor.getX()), QuartPos.fromBlock(anchor.getY()),
                QuartPos.fromBlock(anchor.getZ()), context.randomState().sampler()))) return Optional.empty();
        var pieces = stub.get().getPiecesBuilder();
        if (pieces.isEmpty()) return Optional.empty();
        var bounds = pieces.getBoundingBox();
        int lowest = Integer.MAX_VALUE, highest = Integer.MIN_VALUE;
        for (int ix = 0; ix < 5; ix++) for (int iz = 0; iz < 5; iz++) {
            int x = bounds.minX() + (bounds.maxX() - bounds.minX()) * ix / 4;
            int z = bounds.minZ() + (bounds.maxZ() - bounds.minZ()) * iz / 4;
            int floor = context.chunkGenerator().getFirstFreeHeight(x, z, Heightmap.Types.OCEAN_FLOOR_WG,
                    context.heightAccessor(), context.randomState());
            int surface = context.chunkGenerator().getFirstFreeHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG,
                    context.heightAccessor(), context.randomState());
            // Require a genuine fluid column and water above even the antenna; no guaranteed placement fallback.
            if (surface <= floor || bounds.maxY() >= surface - 1) return Optional.empty();
            var column = context.chunkGenerator().getBaseColumn(x, z, context.heightAccessor(), context.randomState());
            if (!column.getBlock(bounds.maxY() + 1).getFluidState().is(net.minecraft.tags.FluidTags.WATER))
                return Optional.empty();
            lowest = Math.min(lowest, floor); highest = Math.max(highest, floor);
        }
        if (highest - lowest > heightTolerance) return Optional.empty();
        return Optional.of(new GenerationStub(anchor, Either.right(pieces)));
    }

    @Override public StructureType<?> type() { return ZGStructures.SUBMERGED_JIGSAW.get(); }
}
