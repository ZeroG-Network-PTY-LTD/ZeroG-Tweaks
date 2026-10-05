package net.zerog.tweaks.power;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.phys.BlockHitResult;
import net.zerog.tweaks.machine.CombustionRegistry;

public final class PowerBlock extends BaseEntityBlock {
    public PowerBlock(Properties p){super(p);registerDefaultState(stateDefinition.any().setValue(BlockStateProperties.HORIZONTAL_FACING,net.minecraft.core.Direction.NORTH));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(PowerBlock::new);}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> b){b.add(BlockStateProperties.HORIZONTAL_FACING);}
    @Override public BlockState getStateForPlacement(BlockPlaceContext c){return defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,c.getHorizontalDirection().getOpposite());}
    @Override protected RenderShape getRenderShape(BlockState s){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos p,BlockState s){return new PowerBlockEntity(p,s);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level l,BlockState s,BlockEntityType<T> t){return l.isClientSide?null:createTickerHelper(t,PowerRegistry.TYPE.get(),PowerBlockEntity::tick);}
    @Override protected ItemInteractionResult useItemOn(ItemStack stack,BlockState s,Level l,BlockPos p,Player player,InteractionHand hand,BlockHitResult hit){
        if(!stack.is(CombustionRegistry.FLUX_MODULE.get()))return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        if(!l.isClientSide&&l.getBlockEntity(p) instanceof PowerBlockEntity be){if(be.installModule()){if(!player.getAbilities().instabuild)stack.shrink(1);player.displayClientMessage(Component.literal("Flux modules: "+be.modules()+" / 3"),true);}else player.displayClientMessage(Component.literal("Maximum 3 flux modules"),true);}
        return ItemInteractionResult.sidedSuccess(l.isClientSide);
    }
    @Override protected InteractionResult useWithoutItem(BlockState s,Level l,BlockPos p,Player player,BlockHitResult hit){if(player instanceof ServerPlayer server&&l.getBlockEntity(p) instanceof PowerBlockEntity be)server.openMenu(new SimpleMenuProvider((id,inv,who)->new PowerMenu(id,inv,be),s.getBlock().getName()),buf->buf.writeBlockPos(p));return InteractionResult.sidedSuccess(l.isClientSide);}
    @Override protected void onRemove(BlockState s,Level l,BlockPos p,BlockState next,boolean moving){if(!s.is(next.getBlock())&&!l.isClientSide&&l.getBlockEntity(p) instanceof PowerBlockEntity be){Containers.dropItemStack(l,p.getX()+.5,p.getY()+.5,p.getZ()+.5,be.fuel.extractItem(0,64,false));int modules=be.takeModules();if(modules>0)Containers.dropItemStack(l,p.getX()+.5,p.getY()+.5,p.getZ()+.5,new ItemStack(CombustionRegistry.FLUX_MODULE.get(),modules));}super.onRemove(s,l,p,next,moving);}
}
