package net.zerog.tweaks.machine;

import net.minecraft.core.Direction;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.IItemHandler;
import net.zerog.tweaks.genetics.GeneticsRuntime;

/** Face permissions wrap the verified machine filters, never replace processing rules. */
public final class LegacyMachineSides {
    private static final java.util.Map<String,Integer> OUTPUTS=java.util.Map.of(
        "stardust_smelter",2,"starmetal_smelter",3,"silk_weaver",3,
        "gravitational_centrifuge",1,"centrifuge",1,"frame_assembler",2,
        "frame_component_assembler",2,"frame_infusion_altar",3,"infusion_altar",2);
    public static boolean supports(BlockEntity be){return be!=null&&(GeneticsRuntime.handles(GeneticsRuntime.id(be))||OUTPUTS.containsKey(GeneticsRuntime.id(be)));}
    public static boolean supportsFamily(BlockEntity be,int family){return supports(be)&&(family==0||family==1&&(GeneticsRuntime.handles(GeneticsRuntime.id(be))||GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be)))||family==2&&GeneticsRuntime.handles(GeneticsRuntime.id(be)));}
    private static String key(int family){return switch(family){case 1->"power";case 2->"fluid";default->"item";};}
    public static int mode(BlockEntity be,int face){
        int family=face/6,index=face%6;int[] modes=GeneticsRuntime.state(be).getIntArray(key(family)+"_modes");
        int value=index>=0&&index<modes.length?modes[index]:(family==1?1:0);
        return family==1?value==3?3:1:Math.clamp(value,0,3);
    }
    private static int revision(BlockEntity be,int face){if(face<0)return 0;int[] values=GeneticsRuntime.state(be).getIntArray(key(face/6)+"_revisions");int index=face%6;return index<values.length?values[index]:0;}
    public static boolean command(BlockEntity be,Player player,int button){
        if(!supports(be)||player.level().isClientSide||be.isRemoved()||player.level()!=be.getLevel()
            ||!player.level().hasChunkAt(be.getBlockPos())||player.level().getBlockEntity(be.getBlockPos())!=be
            ||player.distanceToSqr(be.getBlockPos().getCenter())>64||button<500||button>=572)return false;
        int family=(button-500)/24,face=(button-500)/4,next=(button-500)%4;
        if(!supportsFamily(be,family)||family==1&&next!=1&&next!=3)return false;
        if(mode(be,face)!=next){
            int[] modes=new int[6],epochs=new int[6];
            for(int i=0;i<6;i++){modes[i]=mode(be,family*6+i);epochs[i]=revision(be,family*6+i);}
            modes[face%6]=next;epochs[face%6]++;var state=GeneticsRuntime.state(be);
            state.putIntArray(key(family)+"_modes",modes);state.putIntArray(key(family)+"_revisions",epochs);
            be.setChanged();be.getLevel().invalidateCapabilities(be.getBlockPos());
        }
        return true;
    }
    public static IItemHandler items(BlockEntity be,Direction side){
        int face=side==null?-1:side.ordinal(),selected=face<0?0:mode(be,face),epoch=revision(be,face);
        // A null provider lets vanilla hoppers fall back to the legacy Container.
        // Off therefore exposes an inert zero-slot capability, not that fallback.
        boolean genetics=GeneticsRuntime.handles(GeneticsRuntime.id(be));
        IItemHandler base=genetics?GeneticsRuntime.automation(be):GeneticsRuntime.legacyAutomation(be);
        int output=genetics?3:OUTPUTS.getOrDefault(GeneticsRuntime.id(be),base.getSlots());
        return new IItemHandler(){
            private boolean live(){return selected!=3&&!be.isRemoved()&&(face<0||mode(be,face)==selected&&revision(be,face)==epoch);}
            private boolean valid(int slot){return live()&&slot>=0&&slot<base.getSlots();}
            public int getSlots(){return selected==3?0:base.getSlots();}
            public ItemStack getStackInSlot(int slot){return valid(slot)?base.getStackInSlot(slot):ItemStack.EMPTY;}
            public int getSlotLimit(int slot){return valid(slot)?base.getSlotLimit(slot):0;}
            public boolean isItemValid(int slot,ItemStack stack){return valid(slot)&&selected!=2&&base.isItemValid(slot,stack);}
            public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){return isItemValid(slot,stack)?base.insertItem(slot,stack,simulate):stack;}
            public ItemStack extractItem(int slot,int count,boolean simulate){return valid(slot)&&selected!=1&&(selected==0||slot>=output)?base.extractItem(slot,count,simulate):ItemStack.EMPTY;}
        };
    }
    public static net.neoforged.neoforge.energy.IEnergyStorage energy(BlockEntity be,Direction side){
        int face=side==null?-1:6+side.ordinal(),epoch=revision(be,face);
        if(!supportsFamily(be,1)||face>=0&&mode(be,face)==3)return null;
        var base=GeneticsRuntime.energy(be);
        return new net.neoforged.neoforge.energy.IEnergyStorage(){
            private boolean live(){return !be.isRemoved()&&(face<0||mode(be,face)==1&&revision(be,face)==epoch);}
            public int receiveEnergy(int n,boolean simulate){return live()?base.receiveEnergy(n,simulate):0;}
            public int extractEnergy(int n,boolean simulate){return 0;}
            public int getEnergyStored(){return live()?base.getEnergyStored():0;}
            public int getMaxEnergyStored(){return base.getMaxEnergyStored();}
            public boolean canReceive(){return live();}public boolean canExtract(){return false;}
        };
    }
    public static net.neoforged.neoforge.fluids.capability.IFluidHandler fluids(BlockEntity be,Direction side){
        int face=side==null?-1:12+side.ordinal(),selected=face<0?0:mode(be,face),epoch=revision(be,face);
        if(!supportsFamily(be,2)||selected==3)return null;
        var base=new net.zerog.tweaks.genetics.GeneticsTank(be);
        return new net.neoforged.neoforge.fluids.capability.IFluidHandler(){
            private boolean live(){return !be.isRemoved()&&(face<0||mode(be,face)==selected&&revision(be,face)==epoch);}
            public int getTanks(){return 1;}
            public net.neoforged.neoforge.fluids.FluidStack getFluidInTank(int tank){return tank==0&&live()?base.getFluidInTank(0):net.neoforged.neoforge.fluids.FluidStack.EMPTY;}
            public int getTankCapacity(int tank){return tank==0?base.getTankCapacity(0):0;}
            public boolean isFluidValid(int tank,net.neoforged.neoforge.fluids.FluidStack fluid){return live()&&selected!=2&&base.isFluidValid(tank,fluid);}
            public int fill(net.neoforged.neoforge.fluids.FluidStack fluid,FluidAction action){return live()&&selected!=2?base.fill(fluid,action):0;}
            public net.neoforged.neoforge.fluids.FluidStack drain(int n,FluidAction action){return live()&&selected!=1?base.drain(n,action):net.neoforged.neoforge.fluids.FluidStack.EMPTY;}
            public net.neoforged.neoforge.fluids.FluidStack drain(net.neoforged.neoforge.fluids.FluidStack fluid,FluidAction action){return live()&&selected!=1?base.drain(fluid,action):net.neoforged.neoforge.fluids.FluidStack.EMPTY;}
        };
    }
    private LegacyMachineSides(){}
}
