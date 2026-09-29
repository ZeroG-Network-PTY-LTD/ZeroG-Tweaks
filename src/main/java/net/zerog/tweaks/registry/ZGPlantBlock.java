package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.PushReaction;

/**
 * Decorative cross-billboard plant (Cinder Cap, Emberthorn, Frostfern,
 * Ghostbloom, Lunar/Rust Lichen, Pyrevine, Solflower, Starbloom).
 *
 * Registered as plain full cubes these rendered black/shadowed when placed:
 * an opaque full cube claims its entire light cell, so the billboard sampled
 * ~0 light. BushBlock keeps the cell light-transparent (propagatesSkylightDown
 * = true) so the sprite renders at full surface brightness, with no
 * collision and a pop-off when the support block is removed.
 */
public class ZGPlantBlock extends BushBlock {
    public ZGPlantBlock(BlockBehaviour.Properties props) {
        super(props.sound(SoundType.GRASS).noOcclusion().pushReaction(PushReaction.DESTROY));
    }

    @Override
    public com.mojang.serialization.MapCodec<ZGPlantBlock> codec() {
        return simpleCodec(ZGPlantBlock::new);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return true; // accept any solid support so planet terrain works
    }
}