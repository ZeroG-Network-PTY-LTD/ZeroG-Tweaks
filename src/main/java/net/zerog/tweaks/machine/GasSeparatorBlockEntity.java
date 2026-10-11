package net.zerog.tweaks.machine;
import net.minecraft.core.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.fluids.*;
import net.neoforged.neoforge.fluids.capability.*;
import net.neoforged.neoforge.fluids.capability.templates.FluidTank;
import net.zerog.tweaks.registry.ZGGases;
/** Three independent single-fluid tanks. Work commits atomically at completion. */
public final class GasSeparatorBlockEntity extends BlockEntity {
    public static final int CAPACITY=16000,ENERGY_CAPACITY=200000;
    public int stored,progress;
    private int lastWater,lastEnergy,lastTicks;
    private final int[] roles={0,1,0,0,3,2};
    private final boolean[] power={true,true,true,true,true,true};
    public final FluidTank water=tank(0),hydrogen=tank(1),oxygen=tank(2);
    public final ItemStackHandler cards=new ItemStackHandler(2){
        @Override public int getSlotLimit(int slot){return 1;}
        @Override public boolean isItemValid(int slot,ItemStack s){return MachineUpgradeCards.tier(s,slot==0?MachineUpgradeCards.Family.ACCELERATION:MachineUpgradeCards.Family.ENERGY_COIL)>0;}
        @Override protected void onContentsChanged(int slot){progress=0;setChanged();}
    };
    private FluidTank tank(int id){return new FluidTank(CAPACITY,s->s.is(id==0?Fluids.WATER:id==1?ZGGases.HYDROGEN.fluid().get():ZGGases.OXYGEN.fluid().get())){@Override protected void onContentsChanged(){setChanged();}};}
    public GasSeparatorBlockEntity(BlockPos p,BlockState s){super(GasSeparatorRegistry.TYPE.get(),p,s);}
    public boolean live(){return level!=null&&!isRemoved()&&level.getBlockEntity(worldPosition)==this;}
    public int role(Direction side){return roles[side.ordinal()];}
    public boolean power(Direction side){return power[side.ordinal()];}
    public void cycle(Direction side){roles[side.ordinal()]=(roles[side.ordinal()]+1)%4;setChanged();}
    public void togglePower(Direction side){power[side.ordinal()]=!power[side.ordinal()];setChanged();}
    public int speed(){return 100+MachineUpgradeCards.tier(cards.getStackInSlot(0),MachineUpgradeCards.Family.ACCELERATION)*MachineUpgradeConfig.SPEED_PERCENT_PER_TIER.get();}
    public int duration(){return Math.max(1,(GasProductionConfig.TICKS.get()*100+speed()-1)/speed());}
    public int cost(){int saving=MachineUpgradeCards.tier(cards.getStackInSlot(1),MachineUpgradeCards.Family.ENERGY_COIL)*MachineUpgradeConfig.ENERGY_SAVING_PER_TIER.get();return (GasProductionConfig.ENERGY.get()*(100-saving)+99)/100;}
    public int status(){if(water.getFluidAmount()<GasProductionConfig.WATER.get())return 1;if(stored<cost())return 2;if(hydrogen.getSpace()<GasProductionConfig.WATER.get()*2||oxygen.getSpace()<GasProductionConfig.WATER.get())return 3;return 0;}
    public static void tick(Level l,BlockPos p,BlockState s,GasSeparatorBlockEntity be){be.work();}
    public void work(){
        if(!live()||level.isClientSide)return;
        int amount=GasProductionConfig.WATER.get(),energy=cost(),ticks=duration();
        if(lastWater!=amount||lastEnergy!=energy||lastTicks!=ticks){progress=0;lastWater=amount;lastEnergy=energy;lastTicks=ticks;}
        if(status()!=0)return;
        if(++progress>=ticks){
            // Single server-thread commit, after all three tanks and FE were checked.
            water.drain(amount,IFluidHandler.FluidAction.EXECUTE);
            hydrogen.fill(new FluidStack(ZGGases.HYDROGEN.fluid().get(),amount*2),IFluidHandler.FluidAction.EXECUTE);
            oxygen.fill(new FluidStack(ZGGases.OXYGEN.fluid().get(),amount),IFluidHandler.FluidAction.EXECUTE);
            stored-=energy;progress=0;
        }setChanged();
    }
    public IEnergyStorage energy(Direction side){return new IEnergyStorage(){
        public int receiveEnergy(int max,boolean simulate){if(max<=0||!live()||!power(side))return 0;int n=Math.min(max,Math.min(10000,ENERGY_CAPACITY-stored));if(!simulate){stored+=n;setChanged();}return n;}
        public int extractEnergy(int max,boolean simulate){return 0;}
        public int getEnergyStored(){return live()?stored:0;}public int getMaxEnergyStored(){return ENERGY_CAPACITY;}
        public boolean canReceive(){return live()&&power(side);}public boolean canExtract(){return false;}
    };}
    public IFluidHandler fluid(Direction side){return new IFluidHandler(){
        private FluidTank assigned(){return switch(role(side)){case 1->water;case 2->hydrogen;case 3->oxygen;default->null;};}
        public int getTanks(){return 1;}public int getTankCapacity(int i){return i==0?CAPACITY:0;}
        public FluidStack getFluidInTank(int i){var t=assigned();return i==0&&live()&&t!=null?t.getFluid().copy():FluidStack.EMPTY;}
        public boolean isFluidValid(int i,FluidStack s){return i==0&&live()&&role(side)==1&&s.is(Fluids.WATER);}
        public int fill(FluidStack s,FluidAction a){return isFluidValid(0,s)?water.fill(s,a):0;}
        public FluidStack drain(int n,FluidAction a){var t=assigned();return n>0&&live()&&role(side)>=2&&t!=null?t.drain(n,a):FluidStack.EMPTY;}
        public FluidStack drain(FluidStack s,FluidAction a){var t=assigned();return live()&&role(side)>=2&&t!=null?t.drain(s,a):FluidStack.EMPTY;}
    };}
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider r){super.saveAdditional(tag,r);tag.putInt("FE",stored);tag.putInt("Progress",progress);tag.putInt("LastWater",lastWater);tag.putInt("LastEnergy",lastEnergy);tag.putInt("LastTicks",lastTicks);tag.put("Water",water.writeToNBT(r,new CompoundTag()));tag.put("Hydrogen",hydrogen.writeToNBT(r,new CompoundTag()));tag.put("Oxygen",oxygen.writeToNBT(r,new CompoundTag()));tag.put("Cards",cards.serializeNBT(r));tag.putIntArray("FluidRoles",roles);for(int i=0;i<6;i++)tag.putBoolean("Power"+i,power[i]);}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider r){super.loadAdditional(tag,r);stored=Math.max(0,Math.min(ENERGY_CAPACITY,tag.getInt("FE")));water.readFromNBT(r,tag.getCompound("Water"));hydrogen.readFromNBT(r,tag.getCompound("Hydrogen"));oxygen.readFromNBT(r,tag.getCompound("Oxygen"));cards.deserializeNBT(r,tag.getCompound("Cards"));progress=Math.max(0,tag.getInt("Progress"));lastWater=tag.getInt("LastWater");lastEnergy=tag.getInt("LastEnergy");lastTicks=tag.getInt("LastTicks");var saved=tag.getIntArray("FluidRoles");for(int i=0;i<6;i++){if(saved.length==6)roles[i]=Math.max(0,Math.min(3,saved[i]));if(tag.contains("Power"+i))power[i]=tag.getBoolean("Power"+i);}sanitize(water,Fluids.WATER);sanitize(hydrogen,ZGGases.HYDROGEN.fluid().get());sanitize(oxygen,ZGGases.OXYGEN.fluid().get());}
    private static void sanitize(FluidTank t,net.minecraft.world.level.material.Fluid f){if(!t.isEmpty()&&!t.getFluid().is(f))t.setFluid(FluidStack.EMPTY);else if(t.getFluidAmount()>CAPACITY)t.setFluid(t.getFluid().copyWithAmount(CAPACITY));}
}
