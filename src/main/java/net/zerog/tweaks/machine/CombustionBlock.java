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
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.network.chat.Component;
import net.minecraft.world.phys.BlockHitResult;

public final class CombustionBlock extends BaseEntityBlock {
    public CombustionBlock(Properties properties){super(properties);registerDefaultState(stateDefinition.any().setValue(BlockStateProperties.HORIZONTAL_FACING,net.minecraft.core.Direction.NORTH).setValue(BlockStateProperties.LIT,false));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(CombustionBlock::new);}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> builder){builder.add(BlockStateProperties.HORIZONTAL_FACING,BlockStateProperties.LIT);}
    @Override public BlockState getStateForPlacement(BlockPlaceContext context){return defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,context.getHorizontalDirection().getOpposite());}
    @Override protected RenderShape getRenderShape(BlockState state){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos pos,BlockState state){return new CombustionBlockEntity(pos,state);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){return level.isClientSide?null:createTickerHelper(type,CombustionRegistry.TYPE.get(),CombustionBlockEntity::tick);}
    @Override protected ItemInteractionResult useItemOn(ItemStack stack,BlockState state,Level level,BlockPos pos,Player player,InteractionHand hand,BlockHitResult hit){
        if(!stack.is(CombustionRegistry.FLUX_MODULE.get()))return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        if(!level.isClientSide&&level.getBlockEntity(pos) instanceof CombustionBlockEntity be){
            if(be.installModule()){if(!player.getAbilities().instabuild)stack.shrink(1);player.displayClientMessage(Component.translatable("message.zerog_tweaks.generator_module_installed",be.upgrades(),be.capacity()),true);}
            else player.displayClientMessage(Component.translatable("message.zerog_tweaks.generator_module_limit"),true);
        }return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }
    @Override protected InteractionResult useWithoutItem(BlockState state,Level level,BlockPos pos,Player player,BlockHitResult hit){
        if(player instanceof ServerPlayer server&&level.getBlockEntity(pos) instanceof CombustionBlockEntity be)server.openMenu(new SimpleMenuProvider((id,inventory,p)->new CombustionMenu(id,inventory,be),Component.translatable("block.zerog_tweaks.combustion_generator")),buf->buf.writeBlockPos(pos));
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
    @Override protected void onRemove(BlockState state,Level level,BlockPos pos,BlockState next,boolean moving){
        if(!state.is(next.getBlock())&&!level.isClientSide&&level.getBlockEntity(pos) instanceof CombustionBlockEntity be){
            net.minecraft.world.Containers.dropItemStack(level,pos.getX()+.5,pos.getY()+.5,pos.getZ()+.5,be.fuel.extractItem(0,64,false));
            int modules=be.removeModulesForDrop();if(modules>0)net.minecraft.world.Containers.dropItemStack(level,pos.getX()+.5,pos.getY()+.5,pos.getZ()+.5,new ItemStack(CombustionRegistry.FLUX_MODULE.get(),modules));
            be.stored=0;be.burn=0;
        }super.onRemove(state,level,pos,next,moving);
    }
}
