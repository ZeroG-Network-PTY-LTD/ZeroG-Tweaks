package net.zerog.tweaks.genetics;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;

/** Two independently typed tanks: honey at T3, starlight catalyst at T6. */
public final class AlvearyFluids implements IFluidHandler {
    private final BlockEntity be;
    public AlvearyFluids(BlockEntity be){this.be=be;}
    private String key(int tank){return "fluid"+tank;}
    public int getTanks(){return 2;}
    public FluidStack getFluidInTank(int tank){if(tank<0||tank>1)return FluidStack.EMPTY;var state=AlvearyRuntime.state(be);var id=ResourceLocation.tryParse(state.getString(key(tank)));int n=state.getInt(key(tank)+"_amount");if(id==null||n<=0||!BuiltInRegistries.FLUID.containsKey(id))return FluidStack.EMPTY;return new FluidStack(BuiltInRegistries.FLUID.get(id),Math.min(getTankCapacity(tank),n));}
    public int getTankCapacity(int tank){return tank==0?(AlvearyRuntime.tier(be)>=3?8000:0):tank==1&&AlvearyRuntime.tier(be)>=6?4000:0;}
    public boolean isFluidValid(int tank,FluidStack fluid){if(getTankCapacity(tank)==0)return false;var id=BuiltInRegistries.FLUID.getKey(fluid.getFluid());return id.getNamespace().equals("zerog_tweaks")&&!id.getPath().startsWith("flowing_")&&(tank==0?id.getPath().endsWith("_honey"):id.getPath().equals("liquid_starlight"));}
    public int fill(FluidStack resource,FluidAction action){for(int tank=0;tank<2;tank++)if(isFluidValid(tank,resource)){var old=getFluidInTank(tank);if(!old.isEmpty()&&!FluidStack.isSameFluidSameComponents(old,resource))return 0;int n=Math.max(0,Math.min(resource.getAmount(),getTankCapacity(tank)-old.getAmount()));if(action.execute()&&n>0){var state=AlvearyRuntime.state(be);state.putString(key(tank),BuiltInRegistries.FLUID.getKey(resource.getFluid()).toString());state.putInt(key(tank)+"_amount",old.getAmount()+n);be.setChanged();}return n;}return 0;}
    public FluidStack drain(FluidStack resource,FluidAction action){for(int i=0;i<2;i++)if(FluidStack.isSameFluidSameComponents(getFluidInTank(i),resource))return drainTank(i,resource.getAmount(),action);return FluidStack.EMPTY;}
    public FluidStack drain(int amount,FluidAction action){for(int i=0;i<2;i++)if(!getFluidInTank(i).isEmpty())return drainTank(i,amount,action);return FluidStack.EMPTY;}
    public FluidStack drainTank(int tank,int amount,FluidAction action){var fluid=getFluidInTank(tank);int n=Math.max(0,Math.min(amount,fluid.getAmount()));if(n==0)return FluidStack.EMPTY;var result=fluid.copyWithAmount(n);if(action.execute()){AlvearyRuntime.state(be).putInt(key(tank)+"_amount",fluid.getAmount()-n);if(fluid.getAmount()==n)AlvearyRuntime.state(be).remove(key(tank));be.setChanged();}return result;}
}
