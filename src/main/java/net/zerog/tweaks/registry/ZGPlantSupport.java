package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;

/** Ground rule for ZeroG plants: vanilla dirt family + any sturdy planet surface. */
public final class ZGPlantSupport {
    private ZGPlantSupport() {}

    public static boolean canSupport(BlockState ground, BlockGetter level, BlockPos pos) {
        return ground.is(BlockTags.DIRT) || ground.is(Blocks.FARMLAND)
                || ground.isFaceSturdy(level, pos, Direction.UP);
    }
}
