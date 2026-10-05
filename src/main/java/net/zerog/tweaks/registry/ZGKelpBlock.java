package net.zerog.tweaks.registry;

import com.mojang.serialization.MapCodec;
import javax.annotation.Nullable;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.LiquidBlockContainer;
import net.minecraft.world.level.block.NetherVines;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.level.material.FluidState;
import net.minecraft.world.level.material.Fluids;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Glowkelp (head) — ZeroG counterpart of vanilla {@code kelp}.
 * Always waterlogged, grows upward through water sources (14% per random
 * tick), must be placed in a full water source, cannot sit on magma.
 */
public class ZGKelpBlock extends GrowingPlantHeadBlock implements LiquidBlockContainer {
    public static final MapCodec<ZGKelpBlock> CODEC = simpleCodec(ZGKelpBlock::new);
    protected static final VoxelShape SHAPE = Block.box(0.0, 0.0, 0.0, 16.0, 9.0, 16.0);

    public ZGKelpBlock(BlockBehaviour.Properties props) {
        super(props, Direction.UP, SHAPE, true, 0.14);
    }

    @Override
    public MapCodec<ZGKelpBlock> codec() {
        return CODEC;
    }

    @Override
    protected boolean canGrowInto(BlockState state) {
        return state.is(Blocks.WATER) && state.getFluidState().isSource() && state.getFluidState().getAmount()==8;
    }

    @Override
    protected Block getBodyBlock() {
        return BlockInit.GLOWKELP_PLANT.get();
    }

    @Override
    protected boolean canAttachTo(BlockState state) {
        return !state.is(Blocks.MAGMA_BLOCK);
    }

    @Override
    public boolean canPlaceLiquid(@Nullable Player player, BlockGetter level, BlockPos pos, BlockState state, Fluid fluid) {
        return false;
    }

    @Override
    public boolean placeLiquid(LevelAccessor level, BlockPos pos, BlockState state, FluidState fluidState) {
        return false;
    }

    @Override
    protected int getBlocksToGrowWhenBonemealed(RandomSource random) {
        return NetherVines.getBlocksToGrowWhenBonemealed(random);
    }

    @Nullable
    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        FluidState fluid = ctx.getLevel().getFluidState(ctx.getClickedPos());
        return fluid.is(FluidTags.WATER) && fluid.getAmount() == 8 ? super.getStateForPlacement(ctx) : null;
    }

    @Override
    protected FluidState getFluidState(BlockState state) {
        return Fluids.WATER.getSource(false);
    }
}
