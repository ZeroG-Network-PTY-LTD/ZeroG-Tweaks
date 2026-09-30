package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Starbloom / Ghostbloom / Solflower — vanilla {@link FlowerBlock}: small
 * flower hitbox, random XZ offset, suspicious-stew effect, pottable, bee
 * pollination (minecraft:flowers tag). Also grows on planet stone.
 */
public class ZGFlowerBlock extends FlowerBlock {
    public ZGFlowerBlock(Holder<MobEffect> stewEffect, float seconds, BlockBehaviour.Properties props) {
        super(stewEffect, seconds, props.noCollission().instabreak());
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return ZGPlantSupport.canSupport(state, level, pos);
    }
}
