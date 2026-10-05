package net.zerog.tweaks.storage;

import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.fluids.FluidStack;

public final class StorageTankMenu extends AbstractContainerMenu {
    public final StorageTankBlockEntity tank;private final ContainerData data;
    public StorageTankMenu(int id,Inventory inventory,BlockEntity entity){super(StorageTankRegistry.MENU.get(),id);if(!(entity instanceof StorageTankBlockEntity be))throw new IllegalArgumentException("Missing storage tank");tank=be;for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inventory,9+row*9+col,8+18*col,124+18*row));for(int col=0;col<9;col++)addSlot(new Slot(inventory,col,8+18*col,182));data=inventory.player.level().isClientSide?new SimpleContainerData(9):new ContainerData(){public int get(int i){return i==0?tank.tank.getFluidAmount()&65535:i==1?tank.tank.getFluidAmount()>>>16:i==2?BuiltInRegistries.FLUID.getId(tank.tank.getFluid().getFluid()):tank.modes[i-3];}public void set(int i,int value){}public int getCount(){return 9;}};addDataSlots(data);}
    public int amount(){return(data.get(0)&65535)|((data.get(1)&65535)<<16);}public int mode(int face){return data.get(3+face);}public FluidStack fluid(){var fluid=BuiltInRegistries.FLUID.byId(data.get(2)&65535);return amount()==0||fluid==null?FluidStack.EMPTY:new FluidStack(fluid,amount());}
    @Override public boolean stillValid(Player player){return !tank.isRemoved()&&tank.getLevel()==player.level()&&player.level().hasChunkAt(tank.getBlockPos())&&player.level().getBlockEntity(tank.getBlockPos())==tank&&player.distanceToSqr(tank.getBlockPos().getCenter())<=64;}
    @Override public boolean clickMenuButton(Player player,int id){if(player.level().isClientSide||!stillValid(player)||id<0||id>=6)return false;tank.cycle(Direction.values()[id]);broadcastChanges();return true;}
    @Override public ItemStack quickMoveStack(Player player,int index){if(!stillValid(player)||index<0||index>=slots.size())return ItemStack.EMPTY;var slot=slots.get(index);if(!slot.hasItem())return ItemStack.EMPTY;var stack=slot.getItem();var original=stack.copy();if(!moveItemStackTo(stack,index<27?27:0,index<27?36:27,false))return ItemStack.EMPTY;if(stack.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();return original;}
}
