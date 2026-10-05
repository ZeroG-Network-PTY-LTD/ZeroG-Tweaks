package net.zerog.tweaks.genetics;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;

/** Verified existing recipe: one thread -> one woven silk. No pattern consumption or invented FE. */
public final class SilkWeaverRuntime {
    public static void tick(Object object){
        if(!(object instanceof BlockEntity be)||!(be.getLevel() instanceof ServerLevel))return;
        var inv=GeneticsRuntime.inventory(be);var input=inv.getStackInSlot(0);var output=inv.getStackInSlot(3);
        try {
            var reset=be.getClass().getMethod("resetProgress");
            var recipe=GeneticsRuntime.product("woven_silk");
            if(!GeneticsRuntime.item(input,"silk_thread")||recipe.isEmpty()
                ||!output.isEmpty()&&(!ItemStack.isSameItemSameComponents(output,recipe)||output.getCount()>=output.getMaxStackSize())){
                reset.invoke(be);return;
            }
            int progress=(Integer)be.getClass().getMethod("getProgress").invoke(be);
            if(progress<199){be.getClass().getMethod("tickProgress").invoke(be);return;}
            inv.extractItem(0,1,false);
            inv.setStackInSlot(3,recipe.copyWithCount(output.getCount()+1));reset.invoke(be);be.setChanged();
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified Silk Weaver API changed",ex);}
    }
    private SilkWeaverRuntime(){}
}
