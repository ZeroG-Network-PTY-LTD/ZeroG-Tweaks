package net.zerog.tweaks.genetics;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.block.entity.BlockEntity;

/** Existing comb outputs, now gated by a persistent vanilla-duration furnace fire. */
public final class StardustSmelterRuntime {
    public static final int TICKS=201;
    public static final String BURN="stardust_burn",TOTAL="stardust_burn_total";
    public static int fuelTicks(ItemStack stack){return stack.isEmpty()?0:Math.max(0,stack.getBurnTime(RecipeType.SMELTING));}
    public static ItemStack result(ItemStack input){
        try{
            var method=Class.forName("com.zerog.aeroapiary.ZeroGSlotFamilies").getDeclaredMethod("stardust",ItemStack.class,ItemStack.class);
            method.setAccessible(true);return ((ItemStack)method.invoke(null,input.copy(),ItemStack.EMPTY)).copy();
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified Stardust recipe API changed",ex);}
    }
    public static void tick(Object object){
        if(!(object instanceof BlockEntity be)||!(be.getLevel() instanceof ServerLevel))return;
        var state=GeneticsRuntime.state(be);var inv=GeneticsRuntime.inventory(be);
        int burn=Math.max(0,state.getInt(BURN));
        boolean hot=burn>0;if(hot){burn--;state.putInt(BURN,burn);be.setChanged();}
        var input=inv.getStackInSlot(0);var output=inv.getStackInSlot(2);var result=result(input);
        boolean fits=!result.isEmpty()&&(output.isEmpty()?result.getCount()<=Math.min(inv.getSlotLimit(2),result.getMaxStackSize()):
            ItemStack.isSameItemSameComponents(output,result)&&output.getCount()+result.getCount()<=Math.min(inv.getSlotLimit(2),output.getMaxStackSize()));
        try{
            var reset=be.getClass().getMethod("resetProgress");
            if(!fits){reset.invoke(be);state.remove("stardust_input");return;}
            var fingerprint=input.copyWithCount(1).save(be.getLevel().registryAccess());
            if(state.contains("stardust_input")&&!state.get("stardust_input").equals(fingerprint))reset.invoke(be);
            state.put("stardust_input",fingerprint);
            if(!hot){
                var fuel=inv.getStackInSlot(1);int duration=fuelTicks(fuel);
                var remainder=fuel.getCraftingRemainingItem();
                // A stacked container-bearing fuel cannot overwrite its remaining fuel stack.
                if(duration<=0||!remainder.isEmpty()&&fuel.getCount()!=1){reset.invoke(be);be.setChanged();return;}
                inv.extractItem(1,1,false);
                if(!remainder.isEmpty())inv.setStackInSlot(1,remainder.copy());
                state.putInt(TOTAL,duration);state.putInt(BURN,duration-1);hot=true;
            }
            int progress=(Integer)be.getClass().getMethod("getProgress").invoke(be);
            net.zerog.tweaks.machine.MachineActivity.work(be.getLevel(),be.getBlockPos(),"stardust_smelter");
            if(progress<TICKS-1)be.getClass().getMethod("tickProgress").invoke(be);
            else{inv.extractItem(0,1,false);inv.setStackInSlot(2,result.copyWithCount(output.getCount()+result.getCount()));reset.invoke(be);state.remove("stardust_input");}
            be.setChanged();
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified Stardust progress API changed",ex);}
    }
    private StardustSmelterRuntime(){}
}
