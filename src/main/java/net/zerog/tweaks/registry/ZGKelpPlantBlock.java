package net.zerog.tweaks.registry;

import javax.annotation.Nullable;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.GrowingPlantBodyBlock;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Glowkelp body (column between head and floor): pops off when water or the
 * support leaves, no collision, wet-grass sounds.
 */
public class ZGKelpPlantBlock extends GrowingPlantBodyBlock {
    public ZGKelpPlantBlock(BlockBehaviour.Properties props) {
        super(props.sound(SoundType.WET_GRASS).noOcclusion().pushReaction(PushReaction.DESTROY),
                Direction.UP, Block.box(1.0, 0.0, 1.0, 15.0, 16.0, 15.0), true);
    }

    @Override
    public com.mojang.serialization.MapCodec<ZGKelpPlantBlock> codec() {
        return simpleCodec(ZGKelpPlantBlock::new);
    }

    @Override
    protected GrowingPlantHeadBlock getHeadBlock() {
        return BlockInit.GLOWKELP.get();
    }

    @Override
    protected Block getBodyBlock() {
        return BlockInit.GLOWKELP_PLANT.get();
    }

    @Override
    public ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state) {
        return new ItemStack(BlockInit.GLOWKELP.get().asItem());
    }
}