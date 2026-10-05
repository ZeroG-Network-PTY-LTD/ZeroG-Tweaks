package net.zerog.tweaks.travel;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.Containers;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.server.level.ServerPlayer;
import net.zerog.tweaks.registry.ZGOrientedBlock;

public final class SurvivalGateBlock extends ZGOrientedBlock implements EntityBlock {
    public SurvivalGateBlock(Properties properties){super(properties);}
    @Override public BlockEntity newBlockEntity(BlockPos pos,BlockState state){return new SurvivalGateBlockEntity(pos,state);}
    @Override public void setPlacedBy(Level level,BlockPos pos,BlockState state,LivingEntity placer,ItemStack stack){super.setPlacedBy(level,pos,state,placer,stack);if(placer instanceof ServerPlayer player&&level.getBlockEntity(pos) instanceof SurvivalGateBlockEntity gate)gate.claim(player);}
    @Override protected void onRemove(BlockState state,Level level,BlockPos pos,BlockState replacement,boolean moving){
        if(!state.is(replacement.getBlock())&&level.getBlockEntity(pos) instanceof SurvivalGateBlockEntity gate&&!level.isClientSide){
            for(int i=0;i<gate.upgrades.getSlots();i++)Containers.dropItemStack(level,pos.getX()+.5,pos.getY()+.5,pos.getZ()+.5,gate.upgrades.getStackInSlot(i));
        }super.onRemove(state,level,pos,replacement,moving);
    }
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){return level.isClientSide?null:(l,p,s,b)->{if(b instanceof SurvivalGateBlockEntity gate)gate.tick();};}
}
