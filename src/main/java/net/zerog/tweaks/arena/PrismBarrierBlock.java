package net.zerog.tweaks.arena;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.HalfTransparentBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Prism barrier: the translucent cyan wall that seals the arena entrance while the Sentinel fight runs.
 * Unbreakable in survival, drops nothing, never placed by worldgen (the arena places and clears it).
 */
public class PrismBarrierBlock extends HalfTransparentBlock {
    public PrismBarrierBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected float getShadeBrightness(BlockState state, BlockGetter level, BlockPos pos) {
        return 1.0F;
    }

    @Override
    protected boolean propagatesSkylightDown(BlockState state, BlockGetter level, BlockPos pos) {
        return true;
    }
}
