package net.zerog.tweaks.genetics;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.items.ItemStackHandler;

/** Server-owned jobs stored in the existing BE's persistent data. No background world access. */
public final class GeneticsRuntime {
    public static final String KEY="zerog_tweaks:genetics_v1";
    public static String id(Object object) {
        if(object==null||!object.getClass().getName().equals("com.zerog.aeroapiary.ZeroGMachineBlockEntity"))return "";
        try{return (String)object.getClass().getMethod("getMachineId").invoke(object);}catch(ReflectiveOperationException ex){return "";}
    }
    public static boolean handles(String id){return id.equals("genetic_splicer")||id.equals("geno_station");}
    public static boolean legacyFiltered(String id){return id.equals("starmetal_smelter")||id.equals("silk_weaver")||id.equals("frame_infusion_altar");}
    /** The verified addon's inventory lacks filters; apply its menu contract to pipes too. */
    public static net.neoforged.neoforge.items.IItemHandler legacyAutomation(Object machine) {
        var inv=inventory(machine);String id=id(machine);
        return new net.neoforged.neoforge.items.IItemHandler(){
            public int getSlots(){return inv.getSlots();}
            public ItemStack getStackInSlot(int slot){return inv.getStackInSlot(slot);}
            public int getSlotLimit(int slot){return inv.getSlotLimit(slot);}
            public boolean isItemValid(int slot,ItemStack stack){
                if(slot<0||slot>=inv.getSlots())return false;
                try{return (Boolean)Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("mayPlaceIn",String.class,int.class,ItemStack.class).invoke(null,id,slot,stack);}
                catch(ReflectiveOperationException ex){return false;}
            }
            public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){return isItemValid(slot,stack)?inv.insertItem(slot,stack,simulate):stack;}
            public ItemStack extractItem(int slot,int count,boolean simulate){return inv.extractItem(slot,count,simulate);}
        };
    }
    public static ItemStackHandler inventory(Object machine) {
        try{return (ItemStackHandler)machine.getClass().getMethod("getInventory").invoke(machine);}
        catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified addon inventory API changed",ex);}
    }
    public static net.neoforged.neoforge.items.IItemHandler automation(Object machine) {
        var inv=inventory(machine);String id=id(machine);
        return new net.neoforged.neoforge.items.IItemHandler() {
            public int getSlots(){return inv.getSlots();}
            public ItemStack getStackInSlot(int slot){return inv.getStackInSlot(slot);}
            public int getSlotLimit(int slot){return slot==0?1:inv.getSlotLimit(slot);}
            public boolean isItemValid(int slot,ItemStack stack){return slot>=0&&slot<3&&mayPlace(id,slot,stack);}
            public ItemStack insertItem(int slot,ItemStack stack,boolean simulate) {
                if(!isItemValid(slot,stack))return stack;
                if(slot!=0)return inv.insertItem(slot,stack,simulate);
                if(!inv.getStackInSlot(0).isEmpty())return stack;
                var rest=inv.insertItem(0,stack.copyWithCount(1),simulate);
                return stack.copyWithCount(stack.getCount()-1+rest.getCount());
            }
            public ItemStack extractItem(int slot,int amount,boolean simulate){return slot>=3?inv.extractItem(slot,amount,simulate):ItemStack.EMPTY;}
        };
    }
    public static CompoundTag state(BlockEntity be) {
        var data=be.getPersistentData();
        if(!data.contains(KEY))data.put(KEY,new CompoundTag());
        return data.getCompound(KEY);
    }
    public static boolean item(ItemStack stack,String name){return !stack.isEmpty()&&BuiltInRegistries.ITEM.getKey(stack.getItem()).equals(ResourceLocation.fromNamespaceAndPath("aeroapiary",name));}
    public static ItemStack product(String name){var item=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("aeroapiary",name));return item==Items.AIR?ItemStack.EMPTY:new ItemStack(item);}
    public static CompoundTag serum(ItemStack stack) {
        if(!item(stack,"trait_serum"))return new CompoundTag();
        var data=stack.get(DataComponents.CUSTOM_DATA);if(data==null)return new CompoundTag();
        var tag=data.copyTag().getCompound("zerog_tweaks:trait");
        return ProductiveBeeGenes.valid(tag.getString("gene"),tag.getString("value"))?tag:new CompoundTag();
    }
    public static boolean mayPlace(String machine,int slot,ItemStack stack) {
        if(slot==0)return ProductiveBeeGenes.read(stack).size()==5;
        if(slot==1)return machine.equals("geno_station")?item(stack,"serum_vial"):!serum(stack).isEmpty();
        if(slot==2)return machine.equals("geno_station")?(item(stack,"honey_drop")||stack.is(Items.HONEY_BOTTLE)):(item(stack,"royal_jelly")||item(stack,"cosmic_jelly"));
        return false;
    }
    public static int capacity(String id){return id.equals("geno_station")?10000:40000;}
    public static int duration(String id,int mode){return id.equals("genetic_splicer")?400:mode==1?300:100;}
    public static int cost(String id){return id.equals("genetic_splicer")?60:20;}
    public static int chance(ItemStack catalyst){return item(catalyst,"cosmic_jelly")?100:item(catalyst,"royal_jelly")?75:0;}
    public static int chance(BlockEntity be){int itemChance=chance(inventory(be).getStackInSlot(2));if(itemChance>0)return itemChance;var tank=new GeneticsTank(be);return tank.ready()?(tank.kind().equals("cosmic_jelly")?100:75):0;}
    private static boolean fits(ItemStackHandler inv,int slot,ItemStack result) {
        var target=inv.getStackInSlot(slot);
        return !result.isEmpty()&&(target.isEmpty()?result.getCount()<=Math.min(inv.getSlotLimit(slot),result.getMaxStackSize()):
            ItemStack.isSameItemSameComponents(target,result)&&target.getCount()+result.getCount()<=Math.min(inv.getSlotLimit(slot),target.getMaxStackSize()));
    }
    private static void put(ItemStackHandler inv,int slot,ItemStack result) {
        var target=inv.getStackInSlot(slot);if(target.isEmpty())inv.setStackInSlot(slot,result.copy());
        else{var copy=target.copy();copy.grow(result.getCount());inv.setStackInSlot(slot,copy);}
    }
    public static int status(BlockEntity be) {
        String id=id(be);var inv=inventory(be);var state=state(be);
        if(inv.getSlots()<5||!mayPlace(id,0,inv.getStackInSlot(0)))return 1;
        if(id.equals("genetic_splicer")||state.getInt("mode")==1){var specimen=inv.getStackInSlot(0).get(DataComponents.CUSTOM_DATA);if(specimen==null||!specimen.copyTag().getBoolean("zerog_tweaks:analysed"))return 6;}
        if(!mayPlace(id,2,inv.getStackInSlot(2))&&!new GeneticsTank(be).ready())return 2;
        if(id.equals("genetic_splicer")&&!mayPlace(id,1,inv.getStackInSlot(1)))return 3;
        if(id.equals("geno_station")&&state.getInt("mode")==1&&(!mayPlace(id,1,inv.getStackInSlot(1))||state.getInt("gene")<0||state.getInt("gene")>=5))return 3;
        var bee=ProductiveBeeGenes.analyse(inv.getStackInSlot(0));
        if(id.equals("genetic_splicer")) {
            var trait=serum(inv.getStackInSlot(1));
            var changed=ProductiveBeeGenes.splice(inv.getStackInSlot(0),trait.getString("gene"),trait.getString("value"));
            // Both outcomes must fit before any FE is charged or chance is rolled.
            if(!fits(inv,3,changed)||!fits(inv,3,inv.getStackInSlot(0).copyWithCount(1)))return 4;
            bee=changed;
        }
        var secondary=secondary(be);
        if(!fits(inv,3,bee)||(secondary!=null&&!fits(inv,4,secondary)))return 4;
        if(id.equals("geno_station")&&state.getInt("mode")==1&&inv.getStackInSlot(2).is(Items.HONEY_BOTTLE)&&remainderSlot(inv)<0)return 4;
        if(id.equals("genetic_splicer")&&state.getInt("energy")<cost(id))return 5;
        return 0;
    }
    private static ItemStack secondary(BlockEntity be) {
        var state=state(be);var inv=inventory(be);
        if(id(be).equals("genetic_splicer"))return product("serum_vial");
        if(state.getInt("mode")!=1)return inv.getStackInSlot(2).is(Items.HONEY_BOTTLE)?new ItemStack(Items.GLASS_BOTTLE):null;
        int gene=state.getInt("gene");if(gene<0||gene>=5)return ItemStack.EMPTY;
        var genes=ProductiveBeeGenes.read(inv.getStackInSlot(0));String key=ProductiveBeeGenes.GENES[gene];
        if(!genes.containsKey(key))return ItemStack.EMPTY;
        var result=product("trait_serum");if(result.isEmpty())return result;
        var tag=new CompoundTag();var trait=new CompoundTag();trait.putString("gene",key);trait.putString("value",genes.get(key));
        tag.put("zerog_tweaks:trait",trait);result.set(DataComponents.CUSTOM_DATA,CustomData.of(tag));return result;
    }
    public static void tick(Object object) {
        if(!(object instanceof BlockEntity be)||!(be.getLevel() instanceof ServerLevel level)||!handles(id(be)))return;
        var state=state(be);var inv=inventory(be);if(!state.getBoolean("requested"))return;
        // Fingerprint includes all input components. Removal/replacement invalidates the job.
        var input=new CompoundTag();for(int i=0;i<3;i++)if(!inv.getStackInSlot(i).isEmpty())input.put("s"+i,inv.getStackInSlot(i).save(level.registryAccess()));
        if(!mayPlace(id(be),2,inv.getStackInSlot(2)))input.putString("fluid",state.getString("fluid"));
        if(state.contains("input")&&!state.getCompound("input").equals(input)){cancel(be);return;}
        if(!state.contains("input"))state.put("input",input);
        if(status(be)!=0)return;
        String id=id(be);int energy=state.getInt("energy");
        int step=4;if(energy>=cost(id)){state.putInt("energy",energy-cost(id));step=1;}
        int progress=state.getInt("progress");
        // Store fixed quarter-tick units so power changes never shorten already-earned progress.
        progress+=step==1?4:1;state.putInt("progress",progress);be.setChanged();
        if(progress<duration(id,state.getInt("mode"))*4)return;
        var original=inv.getStackInSlot(0);ItemStack bee=ProductiveBeeGenes.analyse(original);
        if(id.equals("genetic_splicer")) {
            var serum=serum(inv.getStackInSlot(1));
            var spliced=ProductiveBeeGenes.splice(original,serum.getString("gene"),serum.getString("value"));
            // Reserve for the changed output too, before rolling/consuming anything.
            if(!fits(inv,3,spliced)){state.putInt("progress",progress-4);return;}
            boolean success=level.random.nextInt(100)<chance(be);
            bee=success?spliced:original.copyWithCount(1);state.putBoolean("last_success",success);
        }
        ItemStack secondary=secondary(be);if(!fits(inv,3,bee)||(secondary!=null&&!fits(inv,4,secondary)))return;
        put(inv,3,bee);if(secondary!=null)put(inv,4,secondary);
        if(id.equals("geno_station")&&state.getInt("mode")==1&&inv.getStackInSlot(2).is(Items.HONEY_BOTTLE))put(inv,remainderSlot(inv),new ItemStack(Items.GLASS_BOTTLE));
        inv.extractItem(0,1,false);if(mayPlace(id,2,inv.getStackInSlot(2)))inv.extractItem(2,1,false);else new GeneticsTank(be).consume();
        if(id.equals("genetic_splicer")||state.getInt("mode")==1)inv.extractItem(1,1,false);
        cancel(be);
    }
    public static void cancel(BlockEntity be){var data=state(be);data.putBoolean("requested",false);data.putInt("progress",0);data.remove("input");be.setChanged();}
    private static int remainderSlot(ItemStackHandler inv){for(int i=5;i<inv.getSlots();i++)if(fits(inv,i,new ItemStack(Items.GLASS_BOTTLE)))return i;return -1;}
    public static IEnergyStorage energy(BlockEntity be) {
        return new IEnergyStorage() {
            public int receiveEnergy(int amount,boolean simulate){int accepted=Math.max(0,Math.min(amount,capacity(id(be))-getEnergyStored()));if(!simulate&&accepted>0){state(be).putInt("energy",getEnergyStored()+accepted);be.setChanged();}return accepted;}
            public int extractEnergy(int amount,boolean simulate){return 0;}
            public int getEnergyStored(){return Math.max(0,Math.min(capacity(id(be)),state(be).getInt("energy")));}
            public int getMaxEnergyStored(){return capacity(id(be));}
            public boolean canExtract(){return false;}
            public boolean canReceive(){return true;}
        };
    }
    private GeneticsRuntime(){}
}
