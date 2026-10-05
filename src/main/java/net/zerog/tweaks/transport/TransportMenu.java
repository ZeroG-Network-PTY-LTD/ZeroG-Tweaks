package net.zerog.tweaks.transport;

import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;
import net.zerog.tweaks.machine.CombustionBlockEntity;

public final class TransportMenu extends AbstractContainerMenu {
    public final BlockEntity machine;public final int machineSlots,playerStart;private final ContainerData data;private final TransportBlockEntity inventoryOwner;private boolean transferTransaction;private boolean recovery;
    public boolean itemFamily(){return machine instanceof TransportBlockEntity t&&t.supports("item");}
    public boolean fluidFamily(){return machine instanceof TransportBlockEntity t&&t.supports("fluid");}
    public boolean recoveryVisible(){return value(16)==1;}
    public TransportMenu(int id,Inventory inv,BlockEntity be){super(TransportMenus.MENU.get(),id);machine=be;
        if(!(be instanceof TransportBlockEntity)&&!(be instanceof CombustionBlockEntity))throw new IllegalArgumentException("Not a supported machine");
        inventoryOwner=be instanceof TransportBlockEntity t?t.owner():null;
        var handler=be instanceof TransportBlockEntity t&&t.owner()!=null?t.owner().items:be instanceof TransportBlockEntity t?t.items:((CombustionBlockEntity)be).fuel;machineSlots=handler.getSlots();
        boolean itemStorage=!(be instanceof TransportBlockEntity t)||t.supports("item");
        for(int i=0;i<machineSlots;i++)addSlot(new SlotItemHandler(handler,i,8+i*18,72){@Override public boolean mayPlace(ItemStack stack){return itemStorage&&super.mayPlace(stack);}@Override public boolean isActive(){return itemStorage||recoveryVisible();}});
        if(be instanceof TransportBlockEntity t){for(int i=0;i<9;i++)addSlot(ghost(t.ghostItems,i,8+i*18,104));for(int i=0;i<3;i++)addSlot(ghost(t.ghostFluids,i,8+i*18,136));}playerStart=slots.size();
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inv,9+row*9+col,8+col*18,176+row*18));
        for(int col=0;col<9;col++)addSlot(new Slot(inv,col,8+col*18,234));
        data=inv.player.level().isClientSide?new SimpleContainerData(17):new ContainerData(){
            public int get(int i){var owner=be instanceof TransportBlockEntity t?t.owner():null;int energy=owner!=null?owner.stored:be instanceof CombustionBlockEntity c?c.stored:0;return switch(i){case 0->energy&65535;case 1->energy>>>16;case 2->owner!=null?owner.tank.getFluidAmount():be instanceof CombustionBlockEntity c?c.burn:0;case 3->be instanceof TransportBlockEntity t?t.redstone:0;case 4->be instanceof TransportBlockEntity t?t.routing:0;case 5->be instanceof TransportBlockEntity t?t.blacklist?1:0:0;case 12->be instanceof TransportBlockEntity t&&t.matchTags?1:0;case 13->be instanceof TransportBlockEntity t&&t.matchComponents?1:0;case 14->be.getBlockState().hasProperty(TransportBlock.MODE)?be.getBlockState().getValue(TransportBlock.MODE).ordinal():-1;case 15->be instanceof TransportBlockEntity t?t.colour:-1;case 16->recovery?1:0;default->be instanceof TransportBlockEntity t&&i>=6&&i<12?t.modes[i-6]:0;};}
            public void set(int i,int v){}public int getCount(){return 17;}};addDataSlots(data);
    }
    private Slot ghost(net.neoforged.neoforge.items.ItemStackHandler handler,int index,int x,int y){return new SlotItemHandler(handler,index,x,y){@Override public boolean mayPickup(Player player){return false;}@Override public boolean mayPlace(ItemStack stack){return false;}@Override public boolean isActive(){return y==104?itemFamily():fluidFamily();}};}
    @Override public void clicked(int slot,int button,net.minecraft.world.inventory.ClickType type,Player player){if(!player.level().isClientSide&&!stillValid(player))return;if(slot>=machineSlots&&slot<playerStart&&machine instanceof TransportBlockEntity t){if(player.level().isClientSide||type!=net.minecraft.world.inventory.ClickType.PICKUP||!slots.get(slot).isActive())return;int index=slot-machineSlots;var template=button==1?ItemStack.EMPTY:getCarried().copyWithCount(1);if(index<9)t.ghostItems.setStackInSlot(index,template);else if(template.isEmpty()||net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(template).isPresent())t.ghostFluids.setStackInSlot(index-9,template);t.setChanged();broadcastChanges();return;}
        if(remoteFactor()>0&&!player.level().isClientSide&&!player.getAbilities().instabuild){if(slot<0||type!=net.minecraft.world.inventory.ClickType.PICKUP&&type!=net.minecraft.world.inventory.ClickType.QUICK_MOVE&&type!=net.minecraft.world.inventory.ClickType.SWAP)return;paidTransfer(player,()->super.clicked(slot,button,type,player));}else super.clicked(slot,button,type,player);}
    private int remoteFactor(){return inventoryOwner==null||inventoryOwner==machine?0:inventoryOwner.getLevel()==machine.getLevel()?1:2;}
    private boolean paidTransfer(Player player,Runnable action){if(transferTransaction||remoteFactor()==0||player.level().isClientSide||player.getAbilities().instabuild){action.run();return true;}if(!stillValid(player))return false;
        var before=new java.util.ArrayList<ItemStack>();for(int i=0;i<machineSlots;i++)before.add(inventoryOwner.items.getStackInSlot(i).copy());var playerBefore=new java.util.ArrayList<ItemStack>();for(int i=0;i<player.getInventory().getContainerSize();i++)playerBefore.add(player.getInventory().getItem(i).copy());var carried=getCarried().copy();int energy=inventoryOwner.stored;
        transferTransaction=true;try{action.run();}finally{transferTransaction=false;}
        // Component-specific net movement counts swaps, but not rearranging the shared buffer itself.
        var types=new java.util.ArrayList<ItemStack>();for(var stack:before)if(!stack.isEmpty()&&types.stream().noneMatch(t->ItemStack.isSameItemSameComponents(t,stack)))types.add(stack);for(int i=0;i<machineSlots;i++){var stack=inventoryOwner.items.getStackInSlot(i);if(!stack.isEmpty()&&types.stream().noneMatch(t->ItemStack.isSameItemSameComponents(t,stack)))types.add(stack.copy());}
        int moved=0;for(var type:types){int old=0,now=0;for(int i=0;i<machineSlots;i++){if(ItemStack.isSameItemSameComponents(type,before.get(i)))old+=before.get(i).getCount();var stack=inventoryOwner.items.getStackInSlot(i);if(ItemStack.isSameItemSameComponents(type,stack))now+=stack.getCount();}moved+=Math.abs(old-now);}int fee=moved*2*remoteFactor();
        if(fee>energy){for(int i=0;i<machineSlots;i++)inventoryOwner.items.setStackInSlot(i,before.get(i));for(int i=0;i<playerBefore.size();i++)player.getInventory().setItem(i,playerBefore.get(i));setCarried(carried);inventoryOwner.stored=energy;broadcastFullState();return false;}inventoryOwner.stored=energy-fee;inventoryOwner.setChanged();broadcastChanges();return true;
    }
    public int value(int i){return data.get(i);}public int energy(){return (value(0)&65535)|((value(1)&65535)<<16);}
    @Override public boolean stillValid(Player player){return !machine.isRemoved()&&(!(machine instanceof TransportBlockEntity t)||inventoryOwner!=null&&t.owner()==inventoryOwner)&&machine.getLevel()==player.level()&&player.level().getBlockEntity(machine.getBlockPos())==machine&&player.distanceToSqr(machine.getBlockPos().getCenter())<=64;}
    @Override public boolean clickMenuButton(Player player,int id){if(player.level().isClientSide||!stillValid(player)||!(machine instanceof TransportBlockEntity t))return false;
        if(id==6){if(itemFamily())return false;recovery=!recovery;broadcastChanges();return true;}
        if(id>=2&&id<=5&&!itemFamily()&&!fluidFamily())return false;
        if(id==0)t.redstone=(t.redstone+1)%4;else if(id==1)t.routing=(t.routing+1)%3;else if(id==2)t.blacklist=!t.blacklist;else if(id==3)t.matchTags=!t.matchTags;else if(id==4)t.matchComponents=!t.matchComponents;else if(id==5){for(int i=0;i<9;i++)t.ghostItems.setStackInSlot(i,ItemStack.EMPTY);for(int i=0;i<3;i++)t.ghostFluids.setStackInSlot(i,ItemStack.EMPTY);t.itemFilter="";t.fluidFilter="";}else if(id>=10&&id<16)t.cycleFace(net.minecraft.core.Direction.values()[id-10]);else if(id>=20&&id<26)t.priorities[id-20]=t.priorities[id-20]>=10?-10:t.priorities[id-20]+1;else return false;t.setChanged();broadcastChanges();return true;}
    @Override public ItemStack quickMoveStack(Player player,int i){if(!transferTransaction&&remoteFactor()>0&&!player.level().isClientSide){var result=new ItemStack[]{ItemStack.EMPTY};return paidTransfer(player,()->result[0]=quickMoveRaw(player,i))?result[0]:ItemStack.EMPTY;}return quickMoveRaw(player,i);}
    private ItemStack quickMoveRaw(Player player,int i){if(i<0||i>=slots.size()||!stillValid(player)||i>=machineSlots&&i<playerStart)return ItemStack.EMPTY;var slot=slots.get(i);if(!slot.hasItem())return ItemStack.EMPTY;var stack=slot.getItem();var old=stack.copy();if(i<machineSlots){if(!moveItemStackTo(stack,playerStart,slots.size(),true))return ItemStack.EMPTY;}else if(!moveItemStackTo(stack,0,machineSlots,false))return ItemStack.EMPTY;if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();slot.onTake(player,stack);return old;}
}
