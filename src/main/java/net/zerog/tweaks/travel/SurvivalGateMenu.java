package net.zerog.tweaks.travel;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;

public final class SurvivalGateMenu extends AbstractContainerMenu {
    public final SurvivalGateBlockEntity gate;
    private final ContainerData data;
    public SurvivalGateMenu(int id,Inventory inventory,BlockEntity entity){
        super(SurvivalGates.MENU.get(),id);
        if(!(entity instanceof SurvivalGateBlockEntity controller))throw new IllegalArgumentException("Missing gate controller");gate=controller;
        for(int i=0;i<4;i++){final int slot=i;addSlot(new SlotItemHandler(gate.upgrades,i,18+i*20,137){
            @Override public boolean mayPickup(Player player){return player.level().isClientSide?value(5)==1:player instanceof ServerPlayer server&&gate.mayControl(server);}
            @Override public boolean mayPlace(ItemStack stack){if(!inventory.player.level().isClientSide)return inventory.player instanceof ServerPlayer server&&gate.mayControl(server)&&gate.upgrades.isItemValid(slot,stack);var id=net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem());int tier=value(0),available=tier>=6?4:tier>=5?3:tier>=3?2:tier>=1?1:0;return value(5)==1&&slot<available&&id.getNamespace().equals("zerog_tweaks")&&java.util.List.of("refracting_lens","cryo_core","star_map_fragment","capacity_coil").contains(id.getPath());}
        });}
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inventory,9+row*9+col,46+col*18,170+row*18));
        for(int col=0;col<9;col++)addSlot(new Slot(inventory,col,46+col*18,228));
        data=inventory.player.level().isClientSide?new SimpleContainerData(7):new ContainerData(){
            public int get(int i){return switch(i){case 0->gate.formedTier();case 1->gate.stored/10000;case 2->gate.capacity()/10000;case 3->gate.selected;case 4->gate.countdown;case 5->inventory.player instanceof ServerPlayer p&&gate.mayControl(p)?1:0;case 6->gate.returnPlatform?1:0;default->0;};}
            public void set(int i,int value){}public int getCount(){return 7;}
        };addDataSlots(data);
    }
    public int value(int index){return data.get(index);}
    @Override public boolean stillValid(Player player){return !gate.isRemoved()&&player.level()==gate.getLevel()&&player.distanceToSqr(gate.getBlockPos().getX()+.5,gate.getBlockPos().getY()+.5,gate.getBlockPos().getZ()+.5)<=64;}
    @Override public boolean clickMenuButton(Player player,int button){
        if(!(player instanceof ServerPlayer server)||!stillValid(player))return false;
        if(button==101){gate.confirm(server);return true;}
        if(!gate.mayControl(server))return false;
        if(button==100)return gate.engage(server);
        if(button==102){gate.preview(server);return true;}
        if(button==103){gate.cancel();return true;}
        if(button>=0&&button<SurvivalGateBlockEntity.destinations().size()&&gate.countdown==0&&gate.canReach(SurvivalGateBlockEntity.destinations().get(button))){gate.selected=button;gate.setChanged();return true;}return false;
    }
    @Override public ItemStack quickMoveStack(Player player,int index){
        if(index<0||index>=slots.size()||!(player instanceof ServerPlayer server)||!gate.mayControl(server))return ItemStack.EMPTY;Slot slot=slots.get(index);if(!slot.hasItem()||!slot.mayPickup(player))return ItemStack.EMPTY;
        ItemStack stack=slot.getItem(),copy=stack.copy();
        if(index<4){if(!moveItemStackTo(stack,4,slots.size(),true))return ItemStack.EMPTY;}
        else if(!moveItemStackTo(stack,0,4,false))return ItemStack.EMPTY;
        if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(player,stack);return copy;
    }
}
