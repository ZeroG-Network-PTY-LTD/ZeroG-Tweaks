package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Decorative cross-billboard plant (Cinder Cap, Emberthorn, Frostfern,
 * Ghostbloom, Lunar/Rust Lichen, Pyrevine, Solflower, Starbloom).
 *
 * Registered as plain full cubes these rendered black/shadowed when placed:
 * an opaque full cube claims its entire light cell, so the billboard sampled
 * ~0 light. BushBlock keeps the cell light-transparent (propagatesSkylightDown
 * = true) so the sprite renders at full surface brightness, and pops off when
 * the support block is removed.
 *
 * Walk-through like vanilla plants: noCollission() and instabreak() are set here in
 * the constructor, so they apply whatever properties BlockInit passes in (the old
 * registrations passed stone properties, which made the plants solid).
 */
public class ZGPlantBlock extends BushBlock {
    public ZGPlantBlock(BlockBehaviour.Properties props) {
        super(props.sound(SoundType.GRASS).noCollission().instabreak().noOcclusion().pushReaction(PushReaction.DESTROY));
    }

    /** Plant-sized outline (like a fern) instead of a full cube; subclasses narrow it further. */
    protected static final VoxelShape PLANT_SHAPE = Block.box(2.0, 0.0, 2.0, 14.0, 13.0, 14.0);

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return PLANT_SHAPE;
    }

    @Override
    public com.mojang.serialization.MapCodec<ZGPlantBlock> codec() {
        return simpleCodec(ZGPlantBlock::new);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        // any solid-topped planet surface (stone/regolith/sand) plus vanilla dirt/farmland;
        // air/non-sturdy tops are rejected so plants pop off like vanilla instead of floating
        return ZGPlantSupport.canSupport(state, level, pos);
    }
}