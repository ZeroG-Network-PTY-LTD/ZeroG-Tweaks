package net.zerog.tweaks.machine;
import net.minecraft.world.entity.player.*;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.SlotItemHandler;
public final class ProcessingMenu extends AbstractContainerMenu {
    public final ProcessingBlockEntity machine;private final ContainerData data;
    public ProcessingMenu(int id,Inventory inv,ProcessingBlockEntity be){super(ProcessingRegistry.MENU.get(),id);machine=be;
        for(int i=0;i<be.kind.inputCount;i++)addSlot(new SlotItemHandler(be.inventory,i,16+i*20,36));
        addSlot(new SlotItemHandler(be.inventory,be.kind.catalyst(),16,72));
        for(int i=0;i<be.kind.outputCount;i++)addSlot(new SlotItemHandler(be.inventory,be.kind.output()+i,120+i*20,36));
        for(int i=0;i<3;i++)addSlot(new SlotItemHandler(be.inventory,be.kind.upgrades()+i,120+i*20,72));
        for(int r=0;r<3;r++)for(int c=0;c<9;c++)addSlot(new Slot(inv,9+r*9+c,16+c*18,126+r*18));for(int c=0;c<9;c++)addSlot(new Slot(inv,c,16+c*18,184));
        data=inv.player.level().isClientSide?new SimpleContainerData(20):new ContainerData(){public int get(int i){return switch(i){case 0->be.stored&65535;case 1->be.stored>>>16;case 2->be.progress;case 3->be.casingTier();case 4->be.speedQuarter();case 5->be.getLevel().getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get(),be.input(),be.getLevel()).map(h->be.duration(h.value())).orElse(0);case 6->cost(be)&65535;case 7->cost(be)>>>16;default->i>=14&&i<20?be.itemMode(net.minecraft.core.Direction.values()[i-14]):i>=8&&i<14&&be.faceDisabled(net.minecraft.core.Direction.values()[i-8])?1:0;};}public void set(int i,int v){}public int getCount(){return 20;}};addDataSlots(data);
    }
    public int value(int i){return data.get(i);}public int energy(){return(value(0)&65535)|(value(1)<<16);}
    private static int cost(ProcessingBlockEntity be){return be.getLevel().getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get(),be.input(),be.getLevel()).map(h->be.energyCost(h.value())).orElse(0);}
    public int jobCost(){return(value(6)&65535)|(value(7)<<16);}
    @Override public boolean clickMenuButton(Player player,int id){if(player.level().isClientSide||!stillValid(player))return false;if(id>=100&&id<112)machine.setFaceDisabled(net.minecraft.core.Direction.values()[(id-100)%6],id<106);else if(id>=200&&id<230)machine.setItemMode(net.minecraft.core.Direction.values()[(id-200)/5],(id-200)%5);else return false;broadcastChanges();return true;}
    @Override public boolean stillValid(Player p){return !machine.isRemoved()&&p.level()==machine.getLevel()&&p.level().getBlockEntity(machine.getBlockPos())==machine&&p.distanceToSqr(machine.getBlockPos().getCenter())<=64;}
    @Override public ItemStack quickMoveStack(Player p,int n){
        if(!stillValid(p)||n<0||n>=slots.size()||!slots.get(n).hasItem())return ItemStack.EMPTY;
        var slot=slots.get(n);var s=slot.getItem();var copy=s.copy();int machineSlots=machine.kind.slots();
        if(n<machineSlots){if(!moveItemStackTo(s,machineSlots,slots.size(),true))return ItemStack.EMPTY;}
        else{
            boolean moved;
            // Recipe materials can also be legacy upgrades. Never silently install
            // an ingredient as an upgrade, including when its operating slots are full.
            if(machine.inventory.isItemValid(machine.kind.catalyst(),s)){
                moved=moveItemStackTo(s,machine.kind.catalyst(),machine.kind.catalyst()+1,false);
            }else if(machine.inventory.isItemValid(0,s)){
                moved=moveItemStackTo(s,0,machine.kind.inputCount,false);
            }else{
                moved=false;
                for(int i=machine.kind.upgrades();i<machineSlots;i++)if(machine.inventory.isItemValid(i,s)){
                    moved=moveItemStackTo(s,i,i+1,false);break;
                }
            }
            if(!moved)return ItemStack.EMPTY;
        }
        if(s.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(p,s);return copy;
    }
}
