package net.zerog.tweaks.machine;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.item.context.BlockPlaceContext;

public final class CombustionBlock extends BaseEntityBlock {
    public CombustionBlock(Properties properties){super(properties);registerDefaultState(stateDefinition.any().setValue(BlockStateProperties.HORIZONTAL_FACING,net.minecraft.core.Direction.NORTH).setValue(BlockStateProperties.LIT,false));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(CombustionBlock::new);}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> builder){builder.add(BlockStateProperties.HORIZONTAL_FACING,BlockStateProperties.LIT);}
    @Override public BlockState getStateForPlacement(BlockPlaceContext context){return defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,context.getHorizontalDirection().getOpposite());}
    @Override protected RenderShape getRenderShape(BlockState state){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos pos,BlockState state){return new CombustionBlockEntity(pos,state);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){return level.isClientSide?null:createTickerHelper(type,CombustionRegistry.TYPE.get(),CombustionBlockEntity::tick);}
    @Override protected void onRemove(BlockState state,Level level,BlockPos pos,BlockState next,boolean moving){if(!state.is(next.getBlock())&&level.getBlockEntity(pos) instanceof CombustionBlockEntity be)net.minecraft.world.Containers.dropItemStack(level,pos.getX()+.5,pos.getY()+.5,pos.getZ()+.5,be.fuel.getStackInSlot(0));super.onRemove(state,level,pos,next,moving);}
}
