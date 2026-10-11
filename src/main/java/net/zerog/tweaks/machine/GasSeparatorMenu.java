package net.zerog.tweaks.machine;
import net.minecraft.core.Direction;
import net.minecraft.world.entity.player.*;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.SlotItemHandler;
public final class GasSeparatorMenu extends AbstractContainerMenu {
    public final GasSeparatorBlockEntity machine;
    private final ContainerData data;
    public GasSeparatorMenu(int id,Inventory inv,GasSeparatorBlockEntity be){super(GasSeparatorRegistry.MENU.get(),id);machine=be;
        addSlot(new SlotItemHandler(be.cards,0,18,106));addSlot(new SlotItemHandler(be.cards,1,42,106));
        for(int r=0;r<3;r++)for(int c=0;c<9;c++)addSlot(new Slot(inv,9+r*9+c,18+c*18,164+r*18));for(int c=0;c<9;c++)addSlot(new Slot(inv,c,18+c*18,222));
        data=inv.player.level().isClientSide?new SimpleContainerData(26):new ContainerData(){
            public int get(int i){return switch(i){case 0->be.stored&65535;case 1->be.stored>>>16;case 2->be.water.getFluidAmount();case 3->be.hydrogen.getFluidAmount();case 4->be.oxygen.getFluidAmount();case 5->be.progress;case 6->be.duration();case 7->be.cost()&65535;case 8->be.cost()>>>16;case 9->be.status();case 10->GasProductionConfig.WATER.get();case 11->GasProductionConfig.ENERGY.get()&65535;case 12->GasProductionConfig.ENERGY.get()>>>16;case 13->GasProductionConfig.TICKS.get();default->i<20?be.role(Direction.values()[i-14]):be.power(Direction.values()[i-20])?1:0;};}
            public void set(int i,int v){}public int getCount(){return 26;}};addDataSlots(data);
    }
    public int value(int i){return data.get(i);}public int energy(){return(value(0)&65535)|(value(1)<<16);}public int cost(){return(value(7)&65535)|(value(8)<<16);}public int baseCost(){return(value(11)&65535)|(value(12)<<16);}
    @Override public boolean stillValid(Player p){return machine.live()&&p.level()==machine.getLevel()&&p.distanceToSqr(machine.getBlockPos().getCenter())<=64;}
    @Override public boolean clickMenuButton(Player p,int id){if(p.level().isClientSide||!stillValid(p))return false;if(id>=0&&id<6)machine.cycle(Direction.values()[id]);else if(id>=10&&id<16)machine.togglePower(Direction.values()[id-10]);else return false;broadcastChanges();return true;}
    @Override public ItemStack quickMoveStack(Player p,int n){if(!stillValid(p)||n<0||n>=slots.size())return ItemStack.EMPTY;var slot=slots.get(n);if(!slot.hasItem())return ItemStack.EMPTY;var stack=slot.getItem();var copy=stack.copy();if(n<2){if(!moveItemStackTo(stack,2,slots.size(),true))return ItemStack.EMPTY;}else{int target=MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.ACCELERATION)>0?0:MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.ENERGY_COIL)>0?1:-1;if(target<0||!moveItemStackTo(stack,target,target+1,false))return ItemStack.EMPTY;}if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(p,stack);return copy;}
}
