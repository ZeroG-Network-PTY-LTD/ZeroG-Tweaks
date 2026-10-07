package net.zerog.tweaks.genetics;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.*;
import net.zerog.tweaks.machine.*;

/** Two independent persistent card sockets; the addon's sixteen inventory indices stay untouched. */
public final class LegacyMachineCards {
    public static boolean supports(BlockEntity be){String id=GeneticsRuntime.id(be);return GeneticsRuntime.handles(id)||GeneticsRuntime.legacyPowered(id);}
    public static IItemHandlerModifiable inventory(BlockEntity be){return new IItemHandlerModifiable(){
        private ItemStackHandler read(){var h=new ItemStackHandler(2);var tag=GeneticsRuntime.state(be).getCompound("cards").copy();tag.putInt("Size",2);h.deserializeNBT(be.getLevel().registryAccess(),tag);return h;}
        private void save(ItemStackHandler h){GeneticsRuntime.state(be).put("cards",h.serializeNBT(be.getLevel().registryAccess()));be.setChanged();if(!be.getLevel().isClientSide)resetJob(be);}
        public int getSlots(){return 2;}
        public int getSlotLimit(int slot){return 1;}
        public ItemStack getStackInSlot(int slot){return read().getStackInSlot(slot).copy();}
        public boolean isItemValid(int slot,ItemStack stack){return supports(be)&&slot>=0&&slot<2&&MachineUpgradeCards.tier(stack,slot==0?MachineUpgradeCards.Family.ACCELERATION:MachineUpgradeCards.Family.ENERGY_COIL)>0;}
        public void setStackInSlot(int slot,ItemStack stack){var h=read();if(ItemStack.matches(h.getStackInSlot(slot),stack))return;h.setStackInSlot(slot,stack.copy());save(h);}
        public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){if(!isItemValid(slot,stack))return stack;var h=read();if(!h.getStackInSlot(slot).isEmpty())return stack;int count=Math.min(1,stack.getCount());if(!simulate){h.setStackInSlot(slot,stack.copyWithCount(count));save(h);}return stack.copyWithCount(stack.getCount()-count);}
        public ItemStack extractItem(int slot,int count,boolean simulate){var h=read();var result=h.extractItem(slot,count,simulate);if(!simulate&&!result.isEmpty())save(h);return result;}
    };}
    public static int speed(BlockEntity be){return 100+Math.min(150,MachineUpgradeCards.tier(inventory(be).getStackInSlot(0),MachineUpgradeCards.Family.ACCELERATION)*MachineUpgradeConfig.SPEED_PERCENT_PER_TIER.get());}
    public static int saving(BlockEntity be){return Math.min(30,MachineUpgradeCards.tier(inventory(be).getStackInSlot(1),MachineUpgradeCards.Family.ENERGY_COIL)*MachineUpgradeConfig.ENERGY_SAVING_PER_TIER.get());}
    public static boolean installed(BlockEntity be){return speed(be)>100||saving(be)>0;}
    public static void resetJob(BlockEntity be){
        GeneticsRuntime.cancel(be);var state=GeneticsRuntime.state(be);state.remove("card_job");state.remove("card_elapsed");state.remove("card_paid");state.remove("card_units");state.remove("card_carry");
        if(GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be)))try{be.getClass().getMethod("resetProgress").invoke(be);}catch(ReflectiveOperationException ex){throw new IllegalStateException(ex);}
    }
    public static java.util.List<SlotItemHandler> slots(BlockEntity be){var inv=inventory(be);return java.util.List.of(new SlotItemHandler(inv,0,228,159),new SlotItemHandler(inv,1,228,195));}
    /** Null means this is not a card transfer; ordinary recipes keep their original routing. */
    public static ItemStack quickMove(AbstractContainerMenu menu,BlockEntity be,Player player,int index){
        if(index<0||index>=menu.slots.size())return ItemStack.EMPTY;
        var slot=menu.getSlot(index);var source=slot.getItem();
        int cardStart=menu.slots.size()-2,playerStart=cardStart-36;
        if(index<cardStart&&!(index>=playerStart&&source.getItem() instanceof MachineUpgradeCards.Card))return null;
        if(be.isRemoved()||player.level()!=be.getLevel()||player.distanceToSqr(be.getBlockPos().getCenter())>64||player.level().getBlockEntity(be.getBlockPos())!=be)return ItemStack.EMPTY;
        var before=source.copy();var rest=source.copy();
        if(index>=cardStart)player.getInventory().add(rest);
        else {var cards=inventory(be);for(int i=0;i<2;i++)if(cards.isItemValid(i,rest)){rest=cards.insertItem(i,rest,false);break;}}
        if(rest.getCount()==before.getCount())return ItemStack.EMPTY;
        slot.setByPlayer(rest);slot.onTake(player,rest);return before;
    }
    public static void drop(BlockEntity be){if(!supports(be)||be.getLevel()==null||be.getLevel().isClientSide)return;var inv=inventory(be);for(int i=0;i<2;i++){var stack=inv.extractItem(i,64,false);if(!stack.isEmpty())net.minecraft.world.Containers.dropItemStack(be.getLevel(),be.getBlockPos().getX()+.5,be.getBlockPos().getY()+.5,be.getBlockPos().getZ()+.5,stack);}}
    private LegacyMachineCards(){}
}
