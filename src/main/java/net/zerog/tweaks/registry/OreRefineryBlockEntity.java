package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.zerog.tweaks.machine.*;

/** Registered legacy ID, modern powered processing. Physical input/catalyst/output remain 0/1/2. */
public final class OreRefineryBlockEntity extends ProcessingBlockEntity {
    public static final int PROCESS_TICKS=200;
    public OreRefineryBlockEntity(BlockEntityType<?> type,BlockPos pos,BlockState state){super(type,pos,state,ProcessingRegistry.Kind.REFINING);}
    public ItemStackHandler inventory(){return inventory;}
    public int progress(){return progress;}
    public int progressPercent(){return level==null?0:level.getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(kind).get(),input(),level).map(h->Math.min(100,progress*100/duration(h.value()))).orElse(0);}
    public static void tick(Level level,BlockPos pos,BlockState state,OreRefineryBlockEntity be){ProcessingBlockEntity.tick(level,pos,state,be);}
    public boolean stillValid(Player p){return level!=null&&!isRemoved()&&p.level()==level&&level.getBlockEntity(worldPosition)==this&&p.distanceToSqr(worldPosition.getCenter())<=64;}
    public void clearContent(){for(int i=0;i<inventory.getSlots();i++)inventory.setStackInSlot(i,ItemStack.EMPTY);}
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putInt("RefiningFormat",1);}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){
        CompoundTag upgraded=tag.copy();CompoundTag items=upgraded.getCompound("Inventory");
        // ItemStackHandler's old Size=3 must not shrink away the upgrade slots.
        items.putInt("Size",kind.slots());upgraded.put("Inventory",items);
        if(!tag.contains("RefiningFormat")){
            // Legacy progress was free; never inherit it as a paid modern job.
            upgraded.putInt("Progress",0);upgraded.putInt("Paid",0);upgraded.putString("Job","");upgraded.putString("Configuration","");
        }
        super.loadAdditional(upgraded,lookup);
    }
}
