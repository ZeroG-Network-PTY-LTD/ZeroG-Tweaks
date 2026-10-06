package net.zerog.tweaks.genetics;

import java.util.*;
import java.lang.ref.WeakReference;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.energy.IEnergyStorage;

/** Addon controllers retain their original indices; new frames live in separate persisted storage. */
public final class AlvearyRuntime {
    public static final int[] FRAME_CAPACITY={0,3,4,6,8,12,18,27};
    private static final Map<BlockEntity,ItemStackHandler> FRAME_CACHE=new WeakHashMap<>();
    public static int tier(String id){if(id.equals("apiary_controller")||id.equals("zero_g_hive"))return 1;return id.matches("tier[1-7]_controller")?id.charAt(4)-'0':0;}
    public static int tier(BlockEntity be){return tier(GeneticsRuntime.id(be));}
    public static CompoundTag state(BlockEntity be){var root=be.getPersistentData();if(!root.contains("zerog_tweaks:alveary_v1"))root.put("zerog_tweaks:alveary_v1",new CompoundTag());return root.getCompound("zerog_tweaks:alveary_v1");}
    public static int legacyFrames(BlockEntity be){String id=GeneticsRuntime.id(be);return id.equals("zero_g_hive")?3:id.equals("apiary_controller")?2:tier(be)+1;}
    public static int outputStart(BlockEntity be){return 2+legacyFrames(be);}
    public static boolean isFrame(ItemStack stack){var id=BuiltInRegistries.ITEM.getKey(stack.getItem());return id.getNamespace().equals("aeroapiary")&&id.getPath().endsWith("_frame");}
    public static String species(ItemStack stack){
        if(stack.isEmpty())return "";var id=BuiltInRegistries.ITEM.getKey(stack.getItem());String path=id.getPath();
        var entity=stack.get(DataComponents.ENTITY_DATA);if(entity!=null&&entity.copyTag().contains("type")){var parsed=ResourceLocation.tryParse(entity.copyTag().getString("type"));if(parsed!=null&&parsed.getNamespace().equals("aeroapiary"))path=parsed.getPath();}
        if(!id.getNamespace().equals("aeroapiary"))return "";
        for(String name:new String[]{"comet","meteor","nebula","solar","stardust","void"})if(path.equals(name+"_bee")||path.equals(name+"_bee_spawn_egg")||path.equals(name+"_queen")||path.equals(name+"_princess")||path.equals(name+"_drone"))return name;
        return "";
    }
    public static ItemStackHandler frames(BlockEntity be){
        var existing=FRAME_CACHE.get(be);if(existing!=null)return existing;
        var reference=new WeakReference<>(be);var handler=new ItemStackHandler(27){
            @Override public int getSlotLimit(int slot){return 1;}
            @Override public boolean isItemValid(int slot,ItemStack stack){var owner=reference.get();return owner!=null&&slot<FRAME_CAPACITY[tier(owner)]&&isFrame(stack);}
            @Override protected void onContentsChanged(int slot){var owner=reference.get();if(owner!=null&&owner.getLevel()!=null&&!owner.getLevel().isClientSide){state(owner).put("frames",serializeNBT(owner.getLevel().registryAccess()));owner.setChanged();}}
        };
        if(be.getLevel()!=null&&state(be).contains("frames"))handler.deserializeNBT(be.getLevel().registryAccess(),state(be).getCompound("frames"));FRAME_CACHE.put(be,handler);return handler;
    }
    public static void migrate(BlockEntity be){if(state(be).getBoolean("migrated"))return;var inv=GeneticsRuntime.inventory(be);var frames=frames(be);
        for(int old=2;old<outputStart(be)&&old<inv.getSlots();old++){var stack=inv.getStackInSlot(old);if(!isFrame(stack))continue;for(int slot=0;slot<FRAME_CAPACITY[tier(be)]&&!stack.isEmpty();slot++)stack=frames.insertItem(slot,stack,false);inv.setStackInSlot(old,stack);}
        state(be).putBoolean("migrated",true);be.setChanged();
    }
    public static double productivity(BlockEntity be){var frames=frames(be);double bonus=1;for(int i=0;i<FRAME_CAPACITY[tier(be)];i++){var frame=frames.getStackInSlot(i);if(frame.isEmpty())continue;String name=BuiltInRegistries.ITEM.getKey(frame.getItem()).getPath();bonus+=switch(name){case "honeyed_frame","starlit_frame","starmetal_frame"->.15;case "proven_frame","impregnated_frame"->.10;case "restraint_frame","oblivion_frame"->-.05;default->.05;};}return Math.max(.25,Math.min(4,bonus));}
    public static int cycle(BlockEntity be){return Math.max(80,(int)((900-100*tier(be))/(productivity(be)*(new AlvearyFluids(be).getFluidInTank(1).getAmount()>=25?1.2:1))));}
    public static int feCapacity(BlockEntity be){return tier(be)>=3?50000*tier(be):0;}
    public static boolean formed(BlockEntity be){try{return GeneticsRuntime.id(be).equals("zero_g_hive")||(boolean)be.getClass().getMethod("isFormed").invoke(be);}catch(ReflectiveOperationException ex){return false;}}
    public static ItemStack result(BlockEntity be){String species=species(GeneticsRuntime.inventory(be).getStackInSlot(0));if(species.isEmpty())return ItemStack.EMPTY;var item=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("aeroapiary",species+"_comb"));return item==Items.AIR?ItemStack.EMPTY:new ItemStack(item);}
    public static List<ProductiveBeeProduction.Output> products(BlockEntity be){var nativeResult=result(be);if(!nativeResult.isEmpty())return List.of(new ProductiveBeeProduction.Output(nativeResult,1,1,1));return be.getLevel() instanceof ServerLevel level?ProductiveBeeProduction.outputs(GeneticsRuntime.inventory(be).getStackInSlot(0),level):List.of();}
    /** One bottle measure alongside each completed cycle; existing planet honey IDs only. */
    public static net.neoforged.neoforge.fluids.FluidStack cycleHoney(BlockEntity be){
        if(tier(be)<3||be.getLevel()==null)return net.neoforged.neoforge.fluids.FluidStack.EMPTY;
        var dimension=be.getLevel().dimension().location();
        String planet=dimension.getNamespace().equals("zerog_tweaks")
                &&Set.of("moon","mars","cerulon","skarn","eidolon","solvane").contains(dimension.getPath())
                ?dimension.getPath():"moon";
        var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",planet+"_honey");
        return BuiltInRegistries.FLUID.containsKey(id)?new net.neoforged.neoforge.fluids.FluidStack(BuiltInRegistries.FLUID.get(id),250):net.neoforged.neoforge.fluids.FluidStack.EMPTY;
    }
    public static int status(BlockEntity be){if(!formed(be))return 12;if(tier(be)>=3&&state(be).getInt("energy")<20*tier(be))return 11;var products=products(be);if(products.isEmpty())return 1;
        if(!canDepositAll(be,products.stream().map(ProductiveBeeProduction.Output::maximum).toList())&&!state(be).getBoolean("void"))return 10;var genes=ProductiveBeeGenes.read(GeneticsRuntime.inventory(be).getStackInSlot(0));
        if(be.getLevel() instanceof ServerLevel level){String behavior=genes.getOrDefault("behavior","");if(behavior.endsWith("diurnal")&&!level.isDay()||behavior.endsWith("nocturnal")&&level.isDay())return 8;if(level.isRaining()&&genes.getOrDefault("weather_tolerance","").endsWith("none"))return 9;}
        if(tier(be)>=3){var honey=cycleHoney(be);if(honey.isEmpty()||new AlvearyFluids(be).fill(honey,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE)!=250)return 13;}
        return 0;
    }
    private static boolean canDepositAll(BlockEntity be,List<ItemStack> stacks){var inv=GeneticsRuntime.inventory(be);var copy=new ItemStackHandler(inv.getSlots()-outputStart(be));for(int i=0;i<copy.getSlots();i++)copy.setStackInSlot(i,inv.getStackInSlot(outputStart(be)+i).copy());for(var stack:stacks){var remaining=stack.copy();for(int i=0;i<copy.getSlots()&&!remaining.isEmpty();i++)remaining=copy.insertItem(i,remaining,false);if(!remaining.isEmpty())return false;}return true;}
    private static boolean deposit(BlockEntity be,ItemStack stack){var inv=GeneticsRuntime.inventory(be);var remaining=stack.copy();for(int i=outputStart(be);i<inv.getSlots()&&!remaining.isEmpty();i++)remaining=inv.insertItem(i,remaining,false);return remaining.isEmpty();}
    /** Bottle-to-tank conversion conserves a real honey product and returns its glass. */
    public static void collectHoney(BlockEntity be){if(tier(be)<3)return;var inv=GeneticsRuntime.inventory(be);var tank=new AlvearyFluids(be);for(int i=outputStart(be);i<inv.getSlots();i++){var stack=inv.getStackInSlot(i);if(stack.isEmpty())continue;var id=BuiltInRegistries.ITEM.getKey(stack.getItem());if(!id.getNamespace().equals("zerog_tweaks")||!id.getPath().endsWith("_honey_bottle"))continue;var fluidId=ResourceLocation.fromNamespaceAndPath(id.getNamespace(),id.getPath().replace("_bottle",""));if(!BuiltInRegistries.FLUID.containsKey(fluidId))continue;var fluid=new net.neoforged.neoforge.fluids.FluidStack(BuiltInRegistries.FLUID.get(fluidId),250);if(tank.fill(fluid,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE)!=250)continue;var original=stack.copy();inv.extractItem(i,1,false);if(!canDepositAll(be,List.of(new ItemStack(Items.GLASS_BOTTLE)))){inv.setStackInSlot(i,original);continue;}tank.fill(fluid,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);deposit(be,new ItemStack(Items.GLASS_BOTTLE));}}
    public static void tick(BlockEntity be){if(!(be.getLevel() instanceof ServerLevel level)||tier(be)==0)return;if(!GeneticsRuntime.id(be).equals("zero_g_hive")){try{be.getClass().getMethod("updateFormation").invoke(be);}catch(ReflectiveOperationException ex){return;}}migrate(be);AlvearyServiceModules.tick(be);collectHoney(be);var state=state(be);if(state.getBoolean("eject")&&tier(be)>=3&&level.getGameTime()%20==0)AlvearyPorts.eject(be);if(status(be)!=0)return;
        if(tier(be)>=3)state.putInt("energy",state.getInt("energy")-20*tier(be));int progress=state.getInt("progress")+1;
        if(progress>=cycle(be)){var rolled=products(be).stream().map(p->p.roll(level)).filter(s->!s.isEmpty()).toList();for(var product:rolled)deposit(be,product);var fluids=new AlvearyFluids(be);if(tier(be)>=3)fluids.fill(cycleHoney(be),net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);if(fluids.getFluidInTank(1).getAmount()>=25)fluids.drainTank(1,25,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);progress=0;}
        state.putInt("progress",progress);be.setChanged();
    }
    public static IEnergyStorage energy(BlockEntity be){return new IEnergyStorage(){public int receiveEnergy(int amount,boolean simulate){int n=Math.max(0,Math.min(amount,feCapacity(be)-getEnergyStored()));if(!simulate&&n>0){state(be).putInt("energy",getEnergyStored()+n);be.setChanged();}return n;}public int extractEnergy(int n,boolean s){return 0;}public int getEnergyStored(){return Math.max(0,Math.min(feCapacity(be),state(be).getInt("energy")));}public int getMaxEnergyStored(){return feCapacity(be);}public boolean canReceive(){return feCapacity(be)>0;}public boolean canExtract(){return false;}};}
    public static IItemHandler automation(BlockEntity be){var inv=GeneticsRuntime.inventory(be);var frames=frames(be);return new IItemHandler(){
        public int getSlots(){return inv.getSlots()+27;}public ItemStack getStackInSlot(int slot){return slot<inv.getSlots()?inv.getStackInSlot(slot):frames.getStackInSlot(slot-inv.getSlots());}public int getSlotLimit(int slot){return slot==0||slot>=inv.getSlots()?1:64;}
        public boolean isItemValid(int slot,ItemStack stack){return slot==0&&(!species(stack).isEmpty()||ProductiveBeeGenes.read(stack).size()==5)||slot>=inv.getSlots()&&frames.isItemValid(slot-inv.getSlots(),stack);}
        public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){if(!isItemValid(slot,stack))return stack;if(slot>=inv.getSlots())return frames.insertItem(slot-inv.getSlots(),stack,simulate);if(!inv.getStackInSlot(0).isEmpty())return stack;var remaining=inv.insertItem(0,stack.copyWithCount(1),simulate);return stack.copyWithCount(stack.getCount()-1+remaining.getCount());}
        public ItemStack extractItem(int slot,int amount,boolean simulate){return slot>=outputStart(be)&&slot<inv.getSlots()?inv.extractItem(slot,amount,simulate):ItemStack.EMPTY;}
    };}
    public static void sort(BlockEntity be){var inv=GeneticsRuntime.inventory(be);var contents=new ArrayList<ItemStack>();for(int i=outputStart(be);i<inv.getSlots();i++){if(!inv.getStackInSlot(i).isEmpty())contents.add(inv.getStackInSlot(i).copy());inv.setStackInSlot(i,ItemStack.EMPTY);}contents.sort(Comparator.comparing(s->BuiltInRegistries.ITEM.getKey(s.getItem()).toString()));for(var stack:contents){for(int i=outputStart(be);i<inv.getSlots()&&!stack.isEmpty();i++)stack=inv.insertItem(i,stack,false);if(!stack.isEmpty())throw new IllegalStateException("Output compaction must preserve capacity");}}
    private AlvearyRuntime(){}
}
