package net.zerog.tweaks.genetics;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;

/** Catalyst tank is persisted beside the existing machine inventory, never in a global cache. */
public final class GeneticsTank implements IFluidHandler {
    public static final int CAPACITY=4000,DOSE=250;
    private final BlockEntity be;
    public GeneticsTank(BlockEntity be){this.be=be;}
    private String key(){return GeneticsRuntime.state(be).getString("fluid");}
    public int amount(){return Math.max(0,Math.min(CAPACITY,GeneticsRuntime.state(be).getInt("fluid_amount")));}
    public String kind(){var id=ResourceLocation.tryParse(key());if(id==null)return "";String path=id.getPath();if(path.equals("cosmic_jelly"))return "cosmic_jelly";if(path.equals("royal_jelly"))return "royal_jelly";if(path.equals("honey")||path.endsWith("_honey"))return "honey";return "";}
    public boolean ready(){return amount()>=DOSE&&(GeneticsRuntime.id(be).equals("geno_station")?kind().equals("honey"):kind().equals("royal_jelly")||kind().equals("cosmic_jelly"));}
    public void consume(){drain(DOSE,FluidAction.EXECUTE);}
    public int getTanks(){return 1;}
    public FluidStack getFluidInTank(int tank){var id=ResourceLocation.tryParse(key());if(id==null||amount()==0||!BuiltInRegistries.FLUID.containsKey(id))return FluidStack.EMPTY;return new FluidStack(BuiltInRegistries.FLUID.get(id),amount());}
    public int getTankCapacity(int tank){return CAPACITY;}
    public boolean isFluidValid(int tank,FluidStack stack){if(tank!=0||stack.isEmpty())return false;var id=BuiltInRegistries.FLUID.getKey(stack.getFluid());if(!id.getNamespace().equals("zerog_tweaks")&&!id.getNamespace().equals("aeroapiary")&&!id.getNamespace().equals("productivebees"))return false;String name=id.getPath();return !name.startsWith("flowing_")&&(GeneticsRuntime.id(be).equals("geno_station")?(name.equals("honey")||name.endsWith("_honey")):name.equals("royal_jelly")||name.equals("cosmic_jelly"));}
    public int fill(FluidStack resource,FluidAction action){if(!isFluidValid(0,resource))return 0;String id=BuiltInRegistries.FLUID.getKey(resource.getFluid()).toString();if(amount()>0&&!key().equals(id))return 0;int accepted=Math.max(0,Math.min(resource.getAmount(),CAPACITY-amount()));if(action.execute()&&accepted>0){GeneticsRuntime.state(be).putString("fluid",id);GeneticsRuntime.state(be).putInt("fluid_amount",amount()+accepted);be.setChanged();}return accepted;}
    public FluidStack drain(FluidStack resource,FluidAction action){return FluidStack.isSameFluidSameComponents(resource,getFluidInTank(0))?drain(resource.getAmount(),action):FluidStack.EMPTY;}
    public FluidStack drain(int requested,FluidAction action){var fluid=getFluidInTank(0);int n=Math.max(0,Math.min(requested,amount()));if(fluid.isEmpty()||n==0)return FluidStack.EMPTY;var result=fluid.copyWithAmount(n);if(action.execute()){GeneticsRuntime.state(be).putInt("fluid_amount",amount()-n);if(amount()==0)GeneticsRuntime.state(be).remove("fluid");be.setChanged();}return result;}
}
