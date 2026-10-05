package net.zerog.tweaks.storage;

import java.util.Arrays;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.fluids.capability.templates.FluidTank;

public final class StorageTankBlockEntity extends BlockEntity {
    /** 0 both, 1 input, 2 output, 3 disabled. */
    public final int[] modes=new int[6];
    public final FluidTank tank;
    public StorageTankBlockEntity(BlockPos pos,BlockState state){super(StorageTankRegistry.TYPE.get(),pos,state);tank=new FluidTank(StorageTankRegistry.CAPACITIES[((StorageTankBlock)state.getBlock()).tier]){@Override protected void onContentsChanged(){changed();}};}
    public int capacity(){return tank.getCapacity();}
    public void changed(){setChanged();if(level!=null&&!level.isClientSide&&level.hasChunkAt(worldPosition)&&level.getBlockEntity(worldPosition)==this){var state=getBlockState();int gauge=tank.isEmpty()?0:Math.max(1,(int)Math.ceil(8.0*tank.getFluidAmount()/capacity()));if(state.getValue(StorageTankBlock.LEVEL)!=gauge)level.setBlock(worldPosition,state.setValue(StorageTankBlock.LEVEL,gauge),3);}}
    private boolean live(){return !isRemoved()&&level!=null&&!level.isClientSide&&level.hasChunkAt(worldPosition)&&level.getBlockEntity(worldPosition)==this;}
    public IFluidHandler handler(Direction side){return new IFluidHandler(){private int mode(){return side==null?0:modes[side.ordinal()];}private boolean input(){return live()&&(mode()==0||mode()==1);}private boolean output(){return live()&&(mode()==0||mode()==2);}public int getTanks(){return 1;}public FluidStack getFluidInTank(int i){return i==0&&live()?tank.getFluid().copy():FluidStack.EMPTY;}public int getTankCapacity(int i){return i==0?capacity():0;}public boolean isFluidValid(int i,FluidStack fluid){return i==0&&input()&&!fluid.isEmpty()&&tank.isFluidValid(i,fluid);}public int fill(FluidStack fluid,FluidAction action){return input()?tank.fill(fluid,action):0;}public FluidStack drain(FluidStack fluid,FluidAction action){return output()?tank.drain(fluid,action):FluidStack.EMPTY;}public FluidStack drain(int n,FluidAction action){return output()?tank.drain(n,action):FluidStack.EMPTY;}};}
    public void cycle(Direction face){modes[face.ordinal()]=(modes[face.ordinal()]+1)%4;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);}
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.put("fluid",tank.writeToNBT(lookup,new CompoundTag()));tag.putIntArray("modes",modes);}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);tank.readFromNBT(lookup,tag.getCompound("fluid"));if(tank.getFluidAmount()>capacity())tank.setFluid(tank.getFluid().copyWithAmount(capacity()));Arrays.fill(modes,0);var saved=tag.getIntArray("modes");for(int i=0;i<Math.min(saved.length,6);i++)modes[i]=Math.max(0,Math.min(3,saved[i]));}
}
