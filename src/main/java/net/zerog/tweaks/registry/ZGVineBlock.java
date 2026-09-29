package net.zerog.tweaks.registry;

import net.minecraft.world.level.block.VineBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.PushReaction;

/**
 * ZeroG vine (Pyrevine): full vanilla vine semantics by extension —
 * attaches to any sturdy face, grows randomly into open air beside its
 * support, pops off when the last face detaches, sheared by shears,
 * destroyed (not dragged) by pistons.
 *
 * codec(): not overridden — VineBlock's own codec creates a plain VineBlock,
 * which is correct for our identical-state subclass.
 */
public class ZGVineBlock extends VineBlock {
    public ZGVineBlock(BlockBehaviour.Properties props) {
        super(props.sound(SoundType.GRASS).noOcclusion().pushReaction(PushReaction.DESTROY).randomTicks());
    }
}