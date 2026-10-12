package net.zerog.tweaks.machine;
import com.mojang.serialization.MapCodec;
import net.minecraft.core.*;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
public final class GasSeparatorBlock extends BaseEntityBlock {
    public GasSeparatorBlock(Properties p){super(p);registerDefaultState(stateDefinition.any().setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,Direction.NORTH));}
    @Override protected void createBlockStateDefinition(net.minecraft.world.level.block.state.StateDefinition.Builder<Block,BlockState> b){b.add(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING);}
    @Override public BlockState getStateForPlacement(net.minecraft.world.item.context.BlockPlaceContext c){return defaultBlockState().setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,c.getHorizontalDirection().getOpposite());}
    @Override protected BlockState rotate(BlockState s,Rotation r){return s.setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,r.rotate(s.getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING)));}
    @Override protected BlockState mirror(BlockState s,Mirror m){return s.rotate(m.getRotation(s.getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING)));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(GasSeparatorBlock::new);}
    @Override protected RenderShape getRenderShape(BlockState s){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos p,BlockState s){return new GasSeparatorBlockEntity(p,s);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level l,BlockState s,BlockEntityType<T> t){return l.isClientSide?null:createTickerHelper(t,GasSeparatorRegistry.TYPE.get(),GasSeparatorBlockEntity::tick);}
    @Override protected ItemInteractionResult useItemOn(ItemStack stack,BlockState s,Level l,BlockPos p,Player player,InteractionHand hand,BlockHitResult hit){
        if(stack.getCapability(net.neoforged.neoforge.capabilities.Capabilities.FluidHandler.ITEM)!=null&&l.getBlockEntity(p) instanceof GasSeparatorBlockEntity be&&!be.terminalFace(hit.getDirection())){
            if(!l.isClientSide)net.neoforged.neoforge.fluids.FluidUtil.interactWithFluidHandler(player,hand,be.fluid(hit.getDirection()));
            return ItemInteractionResult.sidedSuccess(l.isClientSide);
        }return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
    }
    @Override protected InteractionResult useWithoutItem(BlockState s,Level l,BlockPos p,Player player,BlockHitResult hit){
        if(player instanceof ServerPlayer server&&l.getBlockEntity(p) instanceof GasSeparatorBlockEntity be)server.openMenu(new SimpleMenuProvider((id,inv,user)->new GasSeparatorMenu(id,inv,be),Component.translatable(getDescriptionId())),buf->buf.writeBlockPos(p));
        return InteractionResult.sidedSuccess(l.isClientSide);
    }
    @Override protected void onRemove(BlockState s,Level l,BlockPos p,BlockState next,boolean moving){
        if(!s.is(next.getBlock())&&!l.isClientSide&&l.getBlockEntity(p) instanceof GasSeparatorBlockEntity be)for(int i=0;i<2;i++)popResource(l,p,be.cards.getStackInSlot(i).copy());
        super.onRemove(s,l,p,next,moving);
    }
}
