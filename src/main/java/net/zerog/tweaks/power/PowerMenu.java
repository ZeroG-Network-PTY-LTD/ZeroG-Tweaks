package net.zerog.tweaks.power;

import net.minecraft.world.entity.player.*;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;

public final class PowerMenu extends AbstractContainerMenu {
    private final PowerBlockEntity generator;private final ContainerData data;private final int machineSlots;
    public PowerMenu(int id,Inventory inv,BlockEntity block){
        super(PowerRegistry.MENU.get(),id);if(!(block instanceof PowerBlockEntity be))throw new IllegalArgumentException("Missing power generator");generator=be;machineSlots=be.solar()?0:1;
        if(machineSlots>0)addSlot(new SlotItemHandler(be.fuel,0,26,44));
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inv,9+row*9+col,8+col*18,112+row*18));
        for(int col=0;col<9;col++)addSlot(new Slot(inv,col,8+col*18,170));
        data=inv.player.level().isClientSide?new SimpleContainerData(12):new ContainerData(){
            public int get(int i){int value=switch(i/2){case 0->be.stored;case 1->be.capacity();case 2->be.burn;case 3->be.burnTotal;case 4->be.rate;case 5->be.modules();default->0;};return i%2==0?value&65535:value>>>16;}
            public void set(int i,int value){}public int getCount(){return 12;}
        };addDataSlots(data);
    }
    public int value(int i){return(data.get(i*2)&65535)|((data.get(i*2+1)&65535)<<16);}
    public boolean solar(){return machineSlots==0;}
    @Override public boolean stillValid(Player p){return !generator.isRemoved()&&p.level()==generator.getLevel()&&p.level().getBlockEntity(generator.getBlockPos())==generator&&p.distanceToSqr(generator.getBlockPos().getCenter())<=64;}
    @Override public ItemStack quickMoveStack(Player p,int index){if(!stillValid(p)||index<0||index>=slots.size())return ItemStack.EMPTY;var slot=slots.get(index);if(!slot.hasItem())return ItemStack.EMPTY;var stack=slot.getItem();var copy=stack.copy();if(index<machineSlots){if(!moveItemStackTo(stack,machineSlots,slots.size(),true))return ItemStack.EMPTY;}else if(machineSlots==0||!moveItemStackTo(stack,0,machineSlots,false))return ItemStack.EMPTY;if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(p,stack);return copy;}
}
