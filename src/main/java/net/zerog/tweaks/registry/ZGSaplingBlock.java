package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.SaplingBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.PushReaction;

/**
 * ZeroG sapling (Charwood / Gildwood / Hoarwood / Shardwood).
 *
 * Vanilla SaplingBlock's ground check only accepts the dirt family; the
 * planets' stone/regolith/sand surfaces rejected it. Same light-cell rule
 * as {@link ZGPlantBlock}: light-transparent, no collision, pop-off.
 */
public class ZGSaplingBlock extends SaplingBlock {
    public ZGSaplingBlock(TreeGrower grower, BlockBehaviour.Properties props) {
        super(grower, props.sound(SoundType.GRASS).noOcclusion().pushReaction(PushReaction.DESTROY));
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return true; // grow on planet stone/regolith/sand, not just dirt
    }
}