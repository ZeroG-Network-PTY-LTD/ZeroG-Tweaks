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
    public final ItemStackHandler fuel=new ItemStackHandler(1){@Override public boolean isItemValid(int slot,ItemStack stack){return burnTime(stack)>0;}@Override protected void onContentsChanged(int slot){setChanged();}};
    public final IEnergyStorage energy=new IEnergyStorage(){
        public int receiveEnergy(int n,boolean simulate){return 0;}public int extractEnergy(int amount,boolean simulate){int n=Math.max(0,Math.min(amount,stored));if(!simulate&&n>0){stored-=n;setChanged();}return n;}
        public int getEnergyStored(){return stored;}public int getMaxEnergyStored(){return 100000;}public boolean canExtract(){return true;}public boolean canReceive(){return false;}
    };
    public CombustionBlockEntity(BlockPos pos,BlockState state){super(CombustionRegistry.TYPE.get(),pos,state);}
    public static int burnTime(ItemStack stack){if(stack.is(Items.COAL)||stack.is(Items.CHARCOAL))return 1600;String id=net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath();return switch(id){case "nebulite"->2400;case "emberite"->4800;case "cryocite"->7200;case "coronite"->9600;default->0;};}
    public static void tick(Level level,BlockPos pos,BlockState state,CombustionBlockEntity be){
        if(level.isClientSide)return;
        if(be.burn==0&&be.stored<100000){var stack=be.fuel.getStackInSlot(0);int ticks=burnTime(stack);if(ticks>0){be.burn=be.burnTotal=ticks;be.output=switch(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath()){case "emberite"->100;case "cryocite"->150;case "coronite"->200;default->50;};be.fuel.extractItem(0,1,false);be.setChanged();}}
        if(be.burn>0&&be.stored<=100000-be.output){be.burn--;be.stored+=be.output;be.setChanged();}
        boolean lit=be.burn>0;if(state.getValue(BlockStateProperties.LIT)!=lit)level.setBlock(pos,state.setValue(BlockStateProperties.LIT,lit),3);
        int remaining=1000;for(var side:Direction.values()){if(!level.hasChunkAt(pos.relative(side)))continue;var sink=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos.relative(side),side.getOpposite());if(sink==null)continue;int n=sink.receiveEnergy(Math.min(remaining,be.stored),true);n=sink.receiveEnergy(n,false);be.stored-=n;remaining-=n;if(n>0)be.setChanged();if(remaining<=0)break;}
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putInt("energy",stored);tag.putInt("burn",burn);tag.putInt("burn_total",burnTotal);tag.putInt("output",output);tag.put("fuel",fuel.serializeNBT(lookup));}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);stored=Math.max(0,Math.min(100000,tag.getInt("energy")));burn=Math.max(0,Math.min(9600,tag.getInt("burn")));burnTotal=Math.max(burn,Math.min(9600,tag.getInt("burn_total")));output=Math.max(50,Math.min(200,tag.getInt("output")));fuel.deserializeNBT(lookup,tag.getCompound("fuel"));}
}
