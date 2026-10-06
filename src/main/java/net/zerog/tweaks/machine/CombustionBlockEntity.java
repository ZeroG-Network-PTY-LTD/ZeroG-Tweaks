package net.zerog.tweaks.machine;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.capabilities.Capabilities;

public final class CombustionBlockEntity extends BlockEntity {
    public int stored,burn,burnTotal;public int output=50;
    private int upgrades,energyRemainder;
    private int disabledFuel,disabledOutputs;
    private final int[] fuelEpoch=new int[6],powerEpoch=new int[6];
    public boolean fuelDisabled(Direction side){return side!=null&&(disabledFuel&(1<<side.ordinal()))!=0;}
    public boolean outputDisabled(Direction side){return side!=null&&(disabledOutputs&(1<<side.ordinal()))!=0;}
    public void setFaceDisabled(Direction side,boolean fuelFace,boolean disabled){
        if(side==null||(fuelFace?fuelDisabled(side):outputDisabled(side))==disabled)return;
        int bit=1<<side.ordinal();
        if(fuelFace){disabledFuel=disabled?disabledFuel|bit:disabledFuel&~bit;fuelEpoch[side.ordinal()]++;}
        else{disabledOutputs=disabled?disabledOutputs|bit:disabledOutputs&~bit;powerEpoch[side.ordinal()]++;}
        setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);
    }
    public net.neoforged.neoforge.items.IItemHandler fuelFor(Direction side){
        if(fuelDisabled(side))return null;int epoch=side==null?0:fuelEpoch[side.ordinal()];
        return new net.neoforged.neoforge.items.IItemHandler(){
            private boolean valid(int slot){return slot==0&&!isRemoved()&&!fuelDisabled(side)&&(side==null||epoch==fuelEpoch[side.ordinal()]);}
            public int getSlots(){return 1;}
            public ItemStack getStackInSlot(int slot){return valid(slot)?fuel.getStackInSlot(slot):ItemStack.EMPTY;}
            public int getSlotLimit(int slot){return valid(slot)?fuel.getSlotLimit(slot):0;}
            public boolean isItemValid(int slot,ItemStack stack){return valid(slot)&&fuel.isItemValid(slot,stack);}
            public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){return isItemValid(slot,stack)?fuel.insertItem(slot,stack,simulate):stack;}
            public ItemStack extractItem(int slot,int count,boolean simulate){return ItemStack.EMPTY;}
        };
    }
    public IEnergyStorage energyFor(Direction side){
        int epoch=side==null?0:powerEpoch[side.ordinal()];
        return new IEnergyStorage(){
            private boolean valid(){return !isRemoved()&&!outputDisabled(side)&&(side==null||epoch==powerEpoch[side.ordinal()]);}
            public int receiveEnergy(int n,boolean simulate){return 0;}
            public int extractEnergy(int n,boolean simulate){return valid()?energy.extractEnergy(n,simulate):0;}
            public int getEnergyStored(){return valid()?stored:0;}
            public int getMaxEnergyStored(){return capacity();}
            public boolean canReceive(){return false;}
            public boolean canExtract(){return valid();}
        };
    }
    public int upgrades(){return upgrades;}
    public int capacity(){return 100000*(1+upgrades);}
    public int outputQuarterFE(){return output*(4+upgrades);}
    public boolean installModule(){if(upgrades>=3)return false;upgrades++;setChanged();return true;}
    public int removeModulesForDrop(){int count=upgrades;upgrades=0;energyRemainder=0;return count;}
    public final ItemStackHandler fuel=new ItemStackHandler(1){@Override public boolean isItemValid(int slot,ItemStack stack){return burnTime(stack)>0;}@Override protected void onContentsChanged(int slot){setChanged();}};
    public final IEnergyStorage energy=new IEnergyStorage(){
        public int receiveEnergy(int n,boolean simulate){return 0;}public int extractEnergy(int amount,boolean simulate){int n=Math.max(0,Math.min(amount,stored));if(!simulate&&n>0){stored-=n;setChanged();}return n;}
        public int getEnergyStored(){return stored;}public int getMaxEnergyStored(){return capacity();}public boolean canExtract(){return true;}public boolean canReceive(){return false;}
    };
    public CombustionBlockEntity(BlockPos pos,BlockState state){super(CombustionRegistry.TYPE.get(),pos,state);}
    public static int burnTime(ItemStack stack){
        if(stack.isEmpty())return 0;
        var id=net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem());
        if(id.getPath().endsWith("dust")||stack.is(net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.ITEM,net.minecraft.resources.ResourceLocation.parse("c:dusts"))))return 0;
        if(stack.is(net.minecraft.tags.ItemTags.COALS))return 1600;
        if(stack.is(net.minecraft.world.level.block.Blocks.COAL_BLOCK.asItem()))return 16000;
        if(stack.is(net.minecraft.tags.ItemTags.LOGS)||stack.is(net.minecraft.tags.ItemTags.PLANKS)
            ||stack.is(net.minecraft.tags.ItemTags.WOODEN_STAIRS)||stack.is(net.minecraft.tags.ItemTags.WOODEN_SLABS)
            ||stack.is(net.minecraft.tags.ItemTags.WOODEN_FENCES)||stack.is(net.minecraft.tags.ItemTags.FENCE_GATES)
            ||stack.is(net.minecraft.tags.ItemTags.WOODEN_DOORS)||stack.is(net.minecraft.tags.ItemTags.WOODEN_TRAPDOORS)
            ||stack.is(net.minecraft.tags.ItemTags.WOODEN_BUTTONS)||stack.is(net.minecraft.tags.ItemTags.WOODEN_PRESSURE_PLATES)
            ||stack.is(Items.STICK)||stack.is(Items.BOWL))return Math.max(0,stack.getBurnTime(net.minecraft.world.item.crafting.RecipeType.SMELTING));
        if(!id.getNamespace().equals("zerog_tweaks"))return 0;
        return switch(id.getPath()){case "nebulite"->2400;case "emberite"->4800;case "cryocite"->7200;case "coronite"->9600;default->0;};
    }
    public static void tick(Level level,BlockPos pos,BlockState state,CombustionBlockEntity be){
        if(level.isClientSide)return;
        if(be.burn==0&&be.stored<be.capacity()){var stack=be.fuel.getStackInSlot(0);int ticks=burnTime(stack);if(ticks>0){be.burn=be.burnTotal=ticks;be.output=switch(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath()){case "emberite"->100;case "cryocite"->150;case "coronite"->200;default->50;};be.fuel.extractItem(0,1,false);be.setChanged();}}
        int numerator=be.outputQuarterFE()+be.energyRemainder,next=numerator/4;
        if(be.burn>0&&be.stored<=be.capacity()-next){be.burn--;be.stored+=next;be.energyRemainder=numerator%4;be.setChanged();}
        boolean lit=be.burn>0;if(state.getValue(BlockStateProperties.LIT)!=lit)level.setBlock(pos,state.setValue(BlockStateProperties.LIT,lit),3);
        int remaining=1000;for(var side:Direction.values()){if(be.outputDisabled(side)||!level.hasChunkAt(pos.relative(side)))continue;var sink=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos.relative(side),side.getOpposite());if(sink==null)continue;int offered=Math.min(remaining,be.stored),accepted=Math.clamp(sink.receiveEnergy(offered,true),0,offered);int n=Math.clamp(sink.receiveEnergy(accepted,false),0,accepted);be.stored-=n;remaining-=n;if(n>0)be.setChanged();if(remaining<=0)break;}
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putInt("fuel_disabled",disabledFuel);tag.putInt("power_disabled",disabledOutputs);tag.putInt("energy",stored);tag.putInt("burn",burn);tag.putInt("burn_total",burnTotal);tag.putInt("output",output);tag.putInt("flux_modules",upgrades);tag.putInt("quarter_remainder",energyRemainder);tag.put("fuel",fuel.serializeNBT(lookup));}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);disabledFuel=tag.getInt("fuel_disabled")&63;disabledOutputs=tag.getInt("power_disabled")&63;for(int i=0;i<6;i++){fuelEpoch[i]++;powerEpoch[i]++;}upgrades=Math.max(0,Math.min(3,tag.getInt("flux_modules")));energyRemainder=Math.max(0,Math.min(3,tag.getInt("quarter_remainder")));stored=Math.max(0,Math.min(capacity(),tag.getInt("energy")));burn=Math.max(0,Math.min(1000000,tag.getInt("burn")));burnTotal=Math.max(burn,Math.min(1000000,tag.getInt("burn_total")));output=Math.max(50,Math.min(200,tag.getInt("output")));fuel.deserializeNBT(lookup,tag.getCompound("fuel"));}
}
