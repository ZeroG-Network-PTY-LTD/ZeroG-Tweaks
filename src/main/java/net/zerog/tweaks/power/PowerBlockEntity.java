package net.zerog.tweaks.power;

import net.minecraft.core.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

public final class PowerBlockEntity extends BlockEntity {
    public int stored,burn,burnTotal,rate;
    private int modules,activeFuelRate;
    private int disabledOutputs;
    private int disabledFuel=63&~(1<<Direction.UP.ordinal());
    private final int[] fuelEpoch=new int[6];
    public boolean fuelDisabled(Direction side){return solar()||side!=null&&(disabledFuel&(1<<side.ordinal()))!=0;}
    public void setFuelDisabled(Direction side,boolean disabled){
        if(solar()||side==null||fuelDisabled(side)==disabled)return;
        disabledFuel=disabled?disabledFuel|(1<<side.ordinal()):disabledFuel&~(1<<side.ordinal());
        fuelEpoch[side.ordinal()]++;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);
    }
    public net.neoforged.neoforge.items.IItemHandler fuelFor(Direction side){
        if(fuelDisabled(side))return null;
        int epoch=side==null?0:fuelEpoch[side.ordinal()];
        return new net.neoforged.neoforge.items.IItemHandler(){
            private boolean valid(int slot){return slot==0&&!isRemoved()&&!fuelDisabled(side)&&(side==null||fuelEpoch[side.ordinal()]==epoch);}
            public int getSlots(){return 1;}
            public ItemStack getStackInSlot(int slot){return valid(slot)?fuel.getStackInSlot(slot):ItemStack.EMPTY;}
            public int getSlotLimit(int slot){return valid(slot)?fuel.getSlotLimit(slot):0;}
            public boolean isItemValid(int slot,ItemStack stack){return valid(slot)&&fuel.isItemValid(slot,stack);}
            public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){return isItemValid(slot,stack)?fuel.insertItem(slot,stack,simulate):stack;}
            public ItemStack extractItem(int slot,int count,boolean simulate){return ItemStack.EMPTY;}
        };
    }
    private final int[] outputEpoch=new int[6];
    public boolean outputDisabled(Direction side){return (disabledOutputs&(1<<side.ordinal()))!=0;}
    public void setOutputDisabled(Direction side,boolean disabled){
        if(outputDisabled(side)==disabled)return;
        disabledOutputs=disabled?disabledOutputs|(1<<side.ordinal()):disabledOutputs&~(1<<side.ordinal());
        outputEpoch[side.ordinal()]++;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);
    }
    public IEnergyStorage energyFor(Direction side){
        if(side==null)return energy;
        int epoch=outputEpoch[side.ordinal()];
        return new IEnergyStorage(){
            private boolean valid(){return !isRemoved()&&!outputDisabled(side)&&epoch==outputEpoch[side.ordinal()];}
            public int receiveEnergy(int n,boolean simulate){return 0;}
            public int extractEnergy(int n,boolean simulate){return valid()?energy.extractEnergy(n,simulate):0;}
            public int getEnergyStored(){return valid()?stored:0;}
            public int getMaxEnergyStored(){return capacity();}
            public boolean canReceive(){return false;}
            public boolean canExtract(){return valid();}
        };
    }
    public PowerBlockEntity(BlockPos pos,BlockState state){super(PowerRegistry.TYPE.get(),pos,state);}
    public boolean solar(){return getBlockState().is(BlockInit.SOLAR_ARRAY.get());}
    public int modules(){return modules;}
    public int capacity(){return (int)Math.min(Integer.MAX_VALUE,(long)PowerConfig.BUFFER.get()*(1+modules));}
    public boolean installModule(){if(modules>=3)return false;modules++;setChanged();return true;}
    public int takeModules(){int n=modules;modules=0;return n;}
    /** GUI view of the existing module count: no second inventory or duplicated refunds. */
    public final ItemStackHandler moduleInput=new ItemStackHandler(1){
        @Override public int getSlotLimit(int slot){return 3;}
        @Override public ItemStack getStackInSlot(int slot){return modules==0?ItemStack.EMPTY:new ItemStack(net.zerog.tweaks.machine.CombustionRegistry.FLUX_MODULE.get(),modules);}
        @Override public boolean isItemValid(int slot,ItemStack stack){return slot==0&&stack.is(net.zerog.tweaks.machine.CombustionRegistry.FLUX_MODULE.get());}
        private boolean canReduceTo(int count){return stored<=(long)PowerConfig.BUFFER.get()*(1+count);}
        @Override public void setStackInSlot(int slot,ItemStack stack){
            if(slot!=0||!stack.isEmpty()&&!isItemValid(slot,stack)||stack.getCount()>3)return;
            int count=stack.isEmpty()?0:stack.getCount();if(!canReduceTo(count))return;
            modules=count;setChanged();
        }
        @Override public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){
            if(!isItemValid(slot,stack))return stack;int n=Math.min(3-modules,stack.getCount());
            if(!simulate&&n>0){modules+=n;setChanged();}return stack.copyWithCount(stack.getCount()-n);
        }
        @Override public ItemStack extractItem(int slot,int count,boolean simulate){
            if(slot!=0||count<=0)return ItemStack.EMPTY;int n=Math.min(count,modules);
            while(n>0&&!canReduceTo(modules-n))n--;
            if(n==0)return ItemStack.EMPTY;if(!simulate){modules-=n;setChanged();}
            return new ItemStack(net.zerog.tweaks.machine.CombustionRegistry.FLUX_MODULE.get(),n);
        }
    };
    public final ItemStackHandler fuel=new ItemStackHandler(1){
        @Override public boolean isItemValid(int slot,ItemStack stack){return !solar()&&stack.is(ItemInit.FUSION_DUST.get());}
        @Override protected void onContentsChanged(int slot){setChanged();}
    };
    public final IEnergyStorage energy=new IEnergyStorage(){
        public int receiveEnergy(int n,boolean simulate){return 0;}
        public int extractEnergy(int n,boolean simulate){int actual=Math.max(0,Math.min(Math.min(n,PowerConfig.TRANSFER.get()),stored));if(!simulate&&actual>0){stored-=actual;setChanged();}return actual;}
        public int getEnergyStored(){return stored;}public int getMaxEnergyStored(){return capacity();}
        public boolean canReceive(){return false;}public boolean canExtract(){return true;}
    };
    public static double dimensionMultiplier(String id){return switch(id){case "zerog_tweaks:moon"->PowerConfig.MOON.get();case "zerog_tweaks:eidolon"->PowerConfig.EIDOLON.get();case "zerog_tweaks:solvane"->PowerConfig.SOLVANE.get();default->1.0;};}
    public int solarRate(Level level){
        if(!level.dimensionType().hasSkyLight()||!level.isDay()
            ||level.getBlockState(worldPosition.above()).getLightBlock(level,worldPosition.above())>0
            ||!level.canSeeSky(worldPosition.above())||level.isThundering())return 0;
        double weather=level.isRaining()?PowerConfig.RAIN.get():1.0;
        return (int)Math.min(capacity(),Math.floor(PowerConfig.SOLAR_RATE.get()*dimensionMultiplier(level.dimension().location().toString())*weather*(1+modules*.25)));
    }
    public static void tick(Level level,BlockPos pos,BlockState state,PowerBlockEntity be){
        if(level.isClientSide)return;
        if(be.solar()){be.rate=be.solarRate(level);int n=Math.min(be.rate,Math.max(0,be.capacity()-be.stored));if(n>0){be.stored+=n;be.setChanged();net.zerog.tweaks.machine.MachineActivity.work(level,pos,"solar_array");}}
        else {
            if(be.burn==0&&be.stored<be.capacity()&&be.fuel.getStackInSlot(0).is(ItemInit.FUSION_DUST.get())){
                be.activeFuelRate=PowerConfig.FUSION_RATE.get();be.burn=be.burnTotal=PowerConfig.FUSION_TICKS.get();be.fuel.extractItem(0,1,false);be.setChanged();
            }
            be.rate=be.burn>0?(int)Math.min(be.capacity(),(long)be.activeFuelRate*(4+be.modules)/4):0;
            // Pause rather than destroy paid-for fuel while output storage is blocked.
            if(be.burn>0&&be.stored<=be.capacity()-be.rate){be.stored+=be.rate;be.burn--;be.setChanged();net.zerog.tweaks.machine.MachineActivity.work(level,pos,"fusion_reactor");}
        }
        int remaining=PowerConfig.TRANSFER.get();
        for(Direction side:Direction.values()){
            if(be.outputDisabled(side))continue;
            if(!level.hasChunkAt(pos.relative(side)))continue;
            var sink=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos.relative(side),side.getOpposite());if(sink==null)continue;
            int offered=Math.min(remaining,be.stored),accepted=Math.clamp(sink.receiveEnergy(offered,true),0,offered);
            int n=Math.clamp(sink.receiveEnergy(accepted,false),0,accepted);be.stored-=n;remaining-=n;if(n>0)be.setChanged();if(remaining==0)break;
        }
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putInt("fuel_disabled",disabledFuel);tag.putInt("power_disabled",disabledOutputs);tag.putInt("modules",modules);tag.putInt("energy",stored);tag.putInt("burn",burn);tag.putInt("burn_total",burnTotal);tag.putInt("fuel_rate",activeFuelRate);tag.put("fuel",fuel.serializeNBT(lookup));}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);disabledFuel=tag.contains("fuel_disabled")?tag.getInt("fuel_disabled")&63:63&~(1<<Direction.UP.ordinal());for(int i=0;i<6;i++)fuelEpoch[i]++;disabledOutputs=tag.getInt("power_disabled")&63;for(int i=0;i<6;i++)outputEpoch[i]++;modules=Math.clamp(tag.getInt("modules"),0,3);stored=Math.clamp(tag.getInt("energy"),0,capacity());burn=Math.clamp(tag.getInt("burn"),0,1000000);burnTotal=Math.clamp(tag.getInt("burn_total"),burn,1000000);activeFuelRate=Math.clamp(tag.getInt("fuel_rate"),1,100000);fuel.deserializeNBT(lookup,tag.getCompound("fuel"));}
}
