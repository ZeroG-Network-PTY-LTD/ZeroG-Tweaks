package net.zerog.tweaks.genetics;

import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;

/** A real 27-slot handler, not a visual overlay over seven legacy slots. */
public final class AlvearyMenu extends AbstractContainerMenu {
    public final BlockEntity machine;public final int legacySlots;private final ContainerData data;private int page;
    public AlvearyMenu(int id,Inventory inv,BlockEntity be){super(AlvearyRegistry.MENU.get(),id);if(be==null||AlvearyRuntime.tier(be)==0)throw new IllegalArgumentException("Not a supported controller");machine=be;var original=GeneticsRuntime.inventory(be);legacySlots=original.getSlots();
        if(!inv.player.level().isClientSide)AlvearyRuntime.migrate(be);
        data=inv.player.level().isClientSide?new SimpleContainerData(11):new ContainerData(){public int get(int i){var state=AlvearyRuntime.state(be);return switch(i){case 0->AlvearyRuntime.tier(be);case 1->AlvearyRuntime.status(be);case 2->AlvearyRuntime.FRAME_CAPACITY[AlvearyRuntime.tier(be)];case 3->state.getInt("progress");case 4->AlvearyRuntime.cycle(be);case 5->AlvearyRuntime.energy(be).getEnergyStored()/100;case 6->new AlvearyFluids(be).getFluidInTank(0).getAmount();case 7->new AlvearyFluids(be).getFluidInTank(1).getAmount();case 8->(int)(AlvearyRuntime.productivity(be)*100);case 9->page;case 10->(state.getBoolean("eject")?1:0)|(state.getBoolean("void")?2:0);default->0;};}public void set(int i,int v){}public int getCount(){return 11;}};addDataSlots(data);
        for(int i=0;i<legacySlots;i++){final int index=i;int grid=i>=AlvearyRuntime.outputStart(be)?i-AlvearyRuntime.outputStart(be):i-2;int x=i<2?17:140+grid%3*18;int y=i==0?27:i==1?55:23+(grid%9)/3*18;addSlot(new SlotItemHandler(original,i,x,y){
            @Override public boolean isActive(){return index==0||index==1&&!getItem().isEmpty()||index>=AlvearyRuntime.outputStart(be)&&(index-AlvearyRuntime.outputStart(be))/9==value(9)||index>=2&&index<AlvearyRuntime.outputStart(be)&&value(9)==outputPages();}
            @Override public boolean mayPickup(Player player){return isActive();}
            @Override public boolean mayPlace(ItemStack stack){return index==0&&(!AlvearyRuntime.species(stack).isEmpty()||ProductiveBeeGenes.read(stack).size()==5);}
            @Override public int getMaxStackSize(){return index==0?1:64;}
            @Override public void setChanged(){super.setChanged();be.setChanged();}
        });}
        var frames=AlvearyRuntime.frames(be);for(int i=0;i<27;i++){final int index=i;addSlot(new SlotItemHandler(frames,i,12+i%9*18,99+i/9*18){@Override public boolean mayPlace(ItemStack stack){return index<value(2)&&AlvearyRuntime.isFrame(stack);}@Override public int getMaxStackSize(){return 1;}});}
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inv,9+row*9+col,48+col*18,169+row*18));for(int col=0;col<9;col++)addSlot(new Slot(inv,col,48+col*18,227));
    }
    public int value(int i){return data.get(i);}public int outputPages(){return Math.max(1,(legacySlots-AlvearyRuntime.outputStart(machine)+8)/9);}public int pages(){return outputPages()+1;}public boolean recoveryPage(){return value(9)==outputPages();}
    @Override public boolean stillValid(Player player){return !machine.isRemoved()&&machine.getLevel()==player.level()&&player.level().hasChunkAt(machine.getBlockPos())&&player.level().getBlockEntity(machine.getBlockPos())==machine&&player.distanceToSqr(machine.getBlockPos().getCenter())<=64;}
    @Override public boolean clickMenuButton(Player player,int id){if(player.level().isClientSide||!stillValid(player))return false;var state=AlvearyRuntime.state(machine);
        if(id==0&&AlvearyRuntime.tier(machine)>=3)state.putBoolean("eject",!state.getBoolean("eject"));else if(id==1)AlvearyRuntime.sort(machine);else if(id==2)page=(page+1)%pages();else if(id==3)state.putBoolean("void",false);else if(id==4&&player.isShiftKeyDown())state.putBoolean("void",true);else return false;machine.setChanged();broadcastChanges();return true;}
    @Override public ItemStack quickMoveStack(Player player,int index){if(index<0||index>=slots.size()||!stillValid(player))return ItemStack.EMPTY;var slot=slots.get(index);if(!slot.hasItem()||!slot.mayPickup(player))return ItemStack.EMPTY;var stack=slot.getItem();var old=stack.copy();int playerStart=legacySlots+27;
        if(index<playerStart){if(!moveItemStackTo(stack,playerStart,slots.size(),true))return ItemStack.EMPTY;}else if(AlvearyRuntime.isFrame(stack)){if(!moveItemStackTo(stack,legacySlots,legacySlots+value(2),false))return ItemStack.EMPTY;}else if(!moveItemStackTo(stack,0,1,false))return ItemStack.EMPTY;
        if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(player,stack);return old;}
}
