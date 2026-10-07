package net.zerog.tweaks.machine;

import java.util.Arrays;
import java.util.function.IntSupplier;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.*;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.ItemStackHandler;

/** Normal visible stacks plus component-aware bounded input reserves. */
public class CompactInventory extends ItemStackHandler {
    private final int inputs;
    private final IntSupplier tier;
    private final int[] reserve;
    private final ItemStack[] types;
    public CompactInventory(int slots,int inputs,IntSupplier tier){
        super(slots);this.inputs=inputs;this.tier=tier;
        reserve=new int[inputs];types=new ItemStack[inputs];Arrays.fill(types,ItemStack.EMPTY);
    }
    public int total(int slot){return slot<inputs?super.getStackInSlot(slot).getCount()+reserve[slot]:super.getStackInSlot(slot).getCount();}
    public boolean acceptsStoredType(int slot,ItemStack stack){return slot>=inputs||reserve[slot]==0||ItemStack.isSameItemSameComponents(types[slot],stack);}
    public int capacity(ItemStack stack){return tier.getAsInt()>0?64+148*Math.min(6,tier.getAsInt()):Math.min(64,stack.isEmpty()?64:stack.getMaxStackSize());}
    private void refill(int slot){
        if(slot>=inputs||reserve[slot]==0||types[slot].isEmpty())return;
        var visible=super.getStackInSlot(slot);
        if(!visible.isEmpty()&&!ItemStack.isSameItemSameComponents(visible,types[slot]))return;
        int add=Math.min(reserve[slot],Math.min(64,types[slot].getMaxStackSize())-visible.getCount());
        if(add<=0)return;
        var next=types[slot].copyWithCount(visible.getCount()+add);
        reserve[slot]-=add;if(reserve[slot]==0)types[slot]=ItemStack.EMPTY;
        super.setStackInSlot(slot,next);
    }
    @Override public ItemStack getStackInSlot(int slot){refill(slot);return super.getStackInSlot(slot);}
    @Override public void setStackInSlot(int slot,ItemStack stack){
        if(slot<inputs&&reserve[slot]>0&&!stack.isEmpty()&&!ItemStack.isSameItemSameComponents(stack,types[slot]))
            throw new IllegalArgumentException("Recover stored input before replacing its item type");
        if(slot<inputs&&stack.getCount()>Math.min(64,stack.getMaxStackSize()))
            throw new IllegalArgumentException("Insert compact inputs through the handler, not oversized stacks");
        super.setStackInSlot(slot,stack);refill(slot);
    }
    @Override public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){
        if(slot>=inputs)return super.insertItem(slot,stack,simulate);
        if(stack.isEmpty()||!isItemValid(slot,stack))return stack;
        var visible=super.getStackInSlot(slot);
        if(!visible.isEmpty()&&!ItemStack.isSameItemSameComponents(visible,stack)
                ||reserve[slot]>0&&!ItemStack.isSameItemSameComponents(types[slot],stack))return stack;
        int accepted=Math.min(stack.getCount(),Math.max(0,capacity(stack)-total(slot)));
        if(accepted==0)return stack;
        if(!simulate){
            int count=total(slot)+accepted,shown=Math.min(count,Math.min(64,stack.getMaxStackSize()));
            reserve[slot]=count-shown;types[slot]=reserve[slot]>0?stack.copyWithCount(1):ItemStack.EMPTY;
            super.setStackInSlot(slot,stack.copyWithCount(shown));
        }
        return accepted==stack.getCount()?ItemStack.EMPTY:stack.copyWithCount(stack.getCount()-accepted);
    }
    @Override public ItemStack extractItem(int slot,int amount,boolean simulate){
        if(slot>=inputs)return super.extractItem(slot,amount,simulate);
        if(amount<=0)return ItemStack.EMPTY;
        // Simulation never refills or dirties storage.
        var visible=super.getStackInSlot(slot);
        if(!visible.isEmpty()&&reserve[slot]>0&&!ItemStack.isSameItemSameComponents(visible,types[slot])){
            var result=super.extractItem(slot,amount,simulate);if(!simulate)refill(slot);return result;
        }
        var type=visible.isEmpty()?types[slot]:visible;
        if(type.isEmpty())return ItemStack.EMPTY;
        int taken=Math.min(amount,Math.min(total(slot),Math.min(64,type.getMaxStackSize())));
        var result=type.copyWithCount(taken);
        if(!simulate){
            int count=total(slot)-taken,shown=Math.min(count,Math.min(64,type.getMaxStackSize()));
            reserve[slot]=count-shown;types[slot]=reserve[slot]>0?type.copyWithCount(1):ItemStack.EMPTY;
            super.setStackInSlot(slot,shown==0?ItemStack.EMPTY:type.copyWithCount(shown));
        }return result;
    }
    @Override public CompoundTag serializeNBT(HolderLookup.Provider lookup){
        var tag=super.serializeNBT(lookup);var entries=new ListTag();
        for(int i=0;i<inputs;i++)if(reserve[i]>0){var entry=new CompoundTag();entry.putInt("Slot",i);entry.putInt("Count",reserve[i]);entry.put("Type",types[i].save(lookup));entries.add(entry);}
        tag.put("CompactReserve",entries);return tag;
    }
    @Override public void deserializeNBT(HolderLookup.Provider lookup,CompoundTag tag){
        Arrays.fill(reserve,0);Arrays.fill(types,ItemStack.EMPTY);super.deserializeNBT(lookup,tag);
        for(var value:tag.getList("CompactReserve",Tag.TAG_COMPOUND)){
            var entry=(CompoundTag)value;int slot=entry.getInt("Slot");if(slot<0||slot>=inputs)continue;
            var type=ItemStack.parseOptional(lookup,entry.getCompound("Type"));if(type.isEmpty())continue;
            types[slot]=type.copyWithCount(1);reserve[slot]=Math.clamp(entry.getInt("Count"),0,952);
        }
        for(int i=0;i<inputs;i++)refill(i);
    }
}
