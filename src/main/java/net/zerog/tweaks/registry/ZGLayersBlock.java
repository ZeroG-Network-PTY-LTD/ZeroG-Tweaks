package net.zerog.tweaks.registry;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.SnowLayerBlock;
import net.minecraft.world.level.block.state.BlockState;

/** Eight-layer deposits matching the authored blockstates, shapes and loot tables. */
public class ZGLayersBlock extends SnowLayerBlock {
    private static final MapCodec<SnowLayerBlock> CODEC = simpleCodec(ZGLayersBlock::new);
    public ZGLayersBlock(Properties props) { super(props); }
    @Override public MapCodec<SnowLayerBlock> codec() { return CODEC; }

    // Share vanilla stacking/support, not vanilla snow's light-driven melting.
    // Ash and crater dust must not disappear next to lamps.
    @Override protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {}
}
