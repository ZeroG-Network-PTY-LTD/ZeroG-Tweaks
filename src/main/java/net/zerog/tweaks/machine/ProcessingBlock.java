package net.zerog.tweaks.machine;
import com.mojang.serialization.MapCodec;
import net.minecraft.core.*;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.phys.BlockHitResult;
public final class ProcessingBlock extends BaseEntityBlock {
    public ProcessingBlock(Properties p){super(p);registerDefaultState(stateDefinition.any().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.NORTH));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(ProcessingBlock::new);}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> b){b.add(BlockStateProperties.HORIZONTAL_FACING);}
    @Override public BlockState getStateForPlacement(BlockPlaceContext c){return defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,c.getHorizontalDirection().getOpposite());}
    @Override protected BlockState rotate(BlockState s,Rotation r){return s.setValue(BlockStateProperties.HORIZONTAL_FACING,r.rotate(s.getValue(BlockStateProperties.HORIZONTAL_FACING)));}
    @Override protected BlockState mirror(BlockState s,Mirror m){return s.rotate(m.getRotation(s.getValue(BlockStateProperties.HORIZONTAL_FACING)));}
    @Override protected RenderShape getRenderShape(BlockState s){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos p,BlockState s){return new ProcessingBlockEntity(p,s);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level l,BlockState s,BlockEntityType<T> t){return l.isClientSide?null:createTickerHelper(t,ProcessingRegistry.TYPE.get(),ProcessingBlockEntity::tick);}
    @Override protected InteractionResult useWithoutItem(BlockState s,Level l,BlockPos p,Player player,BlockHitResult hit){if(player instanceof ServerPlayer server&&l.getBlockEntity(p) instanceof ProcessingBlockEntity be)server.openMenu(new SimpleMenuProvider((id,inv,user)->new ProcessingMenu(id,inv,be),Component.translatable(s.getBlock().getDescriptionId())),buf->buf.writeBlockPos(p));return InteractionResult.sidedSuccess(l.isClientSide);}
    @Override protected void onRemove(BlockState s,Level l,BlockPos p,BlockState next,boolean moving){if(!s.is(next.getBlock())&&!l.isClientSide&&l.getBlockEntity(p) instanceof ProcessingBlockEntity be)be.dropContents();super.onRemove(s,l,p,next,moving);}
}
