package net.zerog.tweaks.machine;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;

public final class CombustionMenu extends AbstractContainerMenu {
    private final CombustionBlockEntity generator;
    private final ContainerData data;
    public CombustionMenu(int id,Inventory inventory,BlockEntity block){
        super(CombustionRegistry.MENU.get(),id);if(!(block instanceof CombustionBlockEntity be))throw new IllegalArgumentException("Missing combustion generator");generator=be;
        addSlot(new SlotItemHandler(be.fuel,0,48,36));
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inventory,9+row*9+col,8+col*18,102+row*18));
        for(int col=0;col<9;col++)addSlot(new Slot(inventory,col,8+col*18,160));
        data=inventory.player.level().isClientSide?new SimpleContainerData(7):new ContainerData(){
            public int get(int i){return switch(i){case 0->be.stored&65535;case 1->be.stored>>>16;case 2->be.burn;case 3->be.burnTotal;case 4->be.upgrades();case 5->be.outputQuarterFE();case 6->be.capacity()/1000;default->0;};}
            public void set(int i,int v){}public int getCount(){return 7;}
        };addDataSlots(data);
    }
    public int value(int index){return data.get(index);}
    public int energy(){return (value(0)&65535)|(value(1)<<16);}
    public int capacity(){return value(6)*1000;}
    @Override public boolean stillValid(Player player){return !generator.isRemoved()&&player.level()==generator.getLevel()&&player.level().hasChunkAt(generator.getBlockPos())&&player.level().getBlockEntity(generator.getBlockPos())==generator&&player.distanceToSqr(generator.getBlockPos().getCenter())<=64;}
    @Override public ItemStack quickMoveStack(Player player,int index){
        if(!stillValid(player)||index<0||index>=slots.size())return ItemStack.EMPTY;var slot=slots.get(index);if(!slot.hasItem())return ItemStack.EMPTY;
        var stack=slot.getItem();var copy=stack.copy();if(index==0){if(!moveItemStackTo(stack,1,slots.size(),true))return ItemStack.EMPTY;}
        else if(!moveItemStackTo(stack,0,1,false))return ItemStack.EMPTY;
        if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(player,stack);return copy;
    }
}
