package net.zerog.tweaks.registry;

import javax.annotation.Nullable;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * ZeroG kelp (Glowkelp): kelp semantics — underwater column that grows
 * upward from a solid floor while the head's AGE < 25, body plants stack
 * beneath, head bonemeal-able, pops off when the water/support leaves.
 */
public class ZGKelpBlock extends GrowingPlantHeadBlock {
    public static final int MAX_AGE_25 = 25;
    private static final VoxelShape SHAPE = Block.box(1.0, 0.0, 1.0, 15.0, 16.0, 15.0);

    public ZGKelpBlock(BlockBehaviour.Properties props) {
        super(props.sound(SoundType.WET_GRASS).noOcclusion().pushReaction(PushReaction.DESTROY),
                Direction.UP, SHAPE, true, 0.14);
    }

    @Override
    public com.mojang.serialization.MapCodec<ZGKelpBlock> codec() {
        return simpleCodec(ZGKelpBlock::new);
    }

    @Override
    protected boolean canGrowInto(BlockState state) {
        // vanilla kelp: only water counts (this keeps the art's water behavior)
        return state.is(Blocks.WATER);
    }

    @Override
    protected Block getBodyBlock() {
        return BlockInit.GLOWKELP_PLANT.get();
    }

    @Override
    protected int getBlocksToGrowWhenBonemealed(RandomSource random) {
        return 1;
    }

    @Override
    public ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state) {
        return new ItemStack(BlockInit.GLOWKELP.get().asItem());
    }
}