package net.zerog.tweaks.genetics;

import java.util.List;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.zerog.tweaks.power.PowerConfig;

/** Power gate around verified addon recipes; no replacement recipe catalogue. */
public final class LegacyMachinePower {
    public static int cost(String id){return id.equals("centrifuge")?PowerConfig.CENTRIFUGE_COST.get():PowerConfig.STARMETAL_COST.get();}
    public static boolean before(BlockEntity be){
        var state=GeneticsRuntime.state(be);state.remove("paid_tick_cost");
        if(!ready(be)||state.getInt("energy")<cost(GeneticsRuntime.id(be)))return false;
        try {
            state.putInt("paid_tick_cost",cost(GeneticsRuntime.id(be)));
            state.putInt("before_progress",(Integer)be.getClass().getMethod("getProgress").invoke(be));
            state.putInt("before_input_count",GeneticsRuntime.inventory(be).getStackInSlot(0).getCount());
            return true;
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified addon progress API changed",ex);}
    }
    public static void after(BlockEntity be){
        var state=GeneticsRuntime.state(be);int cost=state.getInt("paid_tick_cost");if(cost==0)return;
        try {
            int progress=(Integer)be.getClass().getMethod("getProgress").invoke(be);
            if(progress>state.getInt("before_progress")||GeneticsRuntime.inventory(be).getStackInSlot(0).getCount()<state.getInt("before_input_count")){
                state.putInt("energy",Math.max(0,state.getInt("energy")-cost));be.setChanged();
                net.zerog.tweaks.machine.MachineActivity.work(be.getLevel(),be.getBlockPos(),GeneticsRuntime.id(be));
            }
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified addon progress API changed",ex);}
        finally{state.remove("paid_tick_cost");state.remove("before_progress");state.remove("before_input_count");}
    }
    public static boolean ready(BlockEntity be){
        try {
            var inv=GeneticsRuntime.inventory(be);String id=GeneticsRuntime.id(be);
            var families=Class.forName("com.zerog.aeroapiary.ZeroGSlotFamilies");List<ItemStack> products;int start,end;
            if(id.equals("centrifuge")){
                var method=families.getDeclaredMethod("centrifugeProducts",ItemStack.class);method.setAccessible(true);
                @SuppressWarnings("unchecked") var values=(List<ItemStack>)method.invoke(null,inv.getStackInSlot(0).copy());products=values;start=1;end=6;
            }else{
                var method=families.getDeclaredMethod("starmetal",ItemStack.class,ItemStack.class);method.setAccessible(true);
                var product=(ItemStack)method.invoke(null,inv.getStackInSlot(0).copy(),inv.getStackInSlot(2).copy());
                products=product.isEmpty()?List.of():List.of(product);start=end=3;
            }
            if(products.isEmpty())return false;
            var reserved=new ItemStackHandler(end-start+1);
            for(int i=start;i<=end;i++)reserved.setStackInSlot(i-start,inv.getStackInSlot(i).copy());
            for(var product:products){
                // Reserve whole stacks, matching the addon's deposit boundary; never mutate live outputs.
                boolean placed=false;
                for(int i=0;i<reserved.getSlots();i++)if(reserved.insertItem(i,product.copy(),true).isEmpty()){
                    reserved.insertItem(i,product.copy(),false);placed=true;break;
                }
                if(!placed)return false;
            }
            return true;
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified addon recipe API changed",ex);}
    }
    private LegacyMachinePower(){}
}
