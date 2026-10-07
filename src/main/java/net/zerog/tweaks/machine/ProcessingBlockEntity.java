package net.zerog.tweaks.machine;

import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.items.*;
import net.neoforged.neoforge.energy.IEnergyStorage;
import java.util.*;

/** Atomic recipe completion: worst-case outputs must fit before spending FE or rolling chances. */
public class ProcessingBlockEntity extends BlockEntity {
    public final ProcessingRegistry.Kind kind;
    public int stored, progress, paid;
    private String job="", configuration="";
    public final CompactInventory inventory;
    public static final int VOID_FILTER_SIZE=36;
    private final ItemStack[] voidTemplates=new ItemStack[VOID_FILTER_SIZE];
    private int voidRevision;
    public boolean voidInstalled(){return MachineUpgradeCards.tier(inventory.getStackInSlot(kind.upgrades()+3),MachineUpgradeCards.Family.VOID)>0;}
    public ItemStack voidTemplate(int slot){return slot>=0&&slot<VOID_FILTER_SIZE&&voidTemplates[slot]!=null?voidTemplates[slot].copy():ItemStack.EMPTY;}
    public boolean setVoidTemplate(int slot,ItemStack template){
        if(!voidInstalled()||slot<0||slot>=VOID_FILTER_SIZE)return false;
        // Item types only, not arbitrary nested item components supplied by clients.
        voidTemplates[slot]=template.isEmpty()?ItemStack.EMPTY:new ItemStack(template.getItem());
        voidRevision++;setChanged();return true;
    }
    public boolean voids(ItemStack product){
        if(!voidInstalled()||product.isEmpty())return false;
        for(var template:voidTemplates)if(template!=null&&!template.isEmpty()&&product.is(template.getItem()))return true;
        return false;
    }
    private final boolean[] disabledFaces=new boolean[6];
    // 0 Auto, 1 reagents, 2 catalyst, 3 products, 4 Off. Independent from FE faces.
    private final int[] itemModes=new int[6],itemEpochs=new int[6];
    public int itemMode(Direction side){return side==null?0:itemModes[side.ordinal()];}
    public void setItemMode(Direction side,int mode){if(side==null||mode<0||mode>4)return;int face=side.ordinal();if(itemModes[face]==mode)return;itemModes[face]=mode;itemEpochs[face]++;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);}
    public boolean faceDisabled(Direction side){return side!=null&&disabledFaces[side.ordinal()];}
    public void setFaceDisabled(Direction side,boolean disabled){disabledFaces[side.ordinal()]=disabled;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);}
    public ProcessingBlockEntity(BlockPos pos,BlockState state){
        this(ProcessingRegistry.TYPE.get(),pos,state,null);
    }
    protected ProcessingBlockEntity(net.minecraft.world.level.block.entity.BlockEntityType<?> type,BlockPos pos,BlockState state,ProcessingRegistry.Kind selected){
        super(type,pos,state);
        String id=BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath();
        kind=selected!=null?selected:id.equals("alloy_forge")?ProcessingRegistry.Kind.ALLOYING:id.equals("crystal_growth_chamber")?ProcessingRegistry.Kind.CRYSTAL:ProcessingRegistry.Kind.SALVAGING;
        inventory=new CompactInventory(kind.slots(),kind.inputCount,this::compactTier){
            @Override public int getSlotLimit(int slot){return slot>=kind.upgrades()?1:64;}
            @Override public boolean isItemValid(int slot,ItemStack stack){
                if(slot>=kind.upgrades())return cardValid(slot-kind.upgrades(),stack);
                if(slot>=kind.output())return false;
                if(slot<kind.inputCount&&!acceptsStoredType(slot,stack))return false;
                if(level==null)return false;
                return level.getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(kind).get()).stream().anyMatch(h->slot==kind.catalyst()?h.value().catalyst().map(c->c.ingredient().test(stack)).orElse(false):h.value().inputs().stream().anyMatch(c->c.ingredient().test(stack)));
            }
            @Override protected void onContentsChanged(int slot){setChanged();}
        };
    }
    private static String id(ItemStack s){return BuiltInRegistries.ITEM.getKey(s.getItem()).toString();}
    private static final List<String> CASINGS=List.of("cyrrium_casing","tectium_casing","wraithsteel_casing","astrium_casing");
    private static final List<String> DUSTS=List.of("pulsar_dust","tremor_dust","spectral_dust","fusion_dust");
    public boolean upgradeValid(int slot,ItemStack s){String v=id(s);return switch(slot){case 0->CASINGS.stream().anyMatch(x->v.equals("zerog_tweaks:"+x));case 1->v.equals("zerog_tweaks:cryo_core");case 2->DUSTS.stream().anyMatch(x->v.equals("zerog_tweaks:"+x));default->false;};}
    public int casingTier(){return Math.max(0,CASINGS.indexOf(id(inventory.getStackInSlot(kind.upgrades())).replace("zerog_tweaks:",""))+1);}
    public boolean cardValid(int slot,ItemStack stack){return switch(slot){case 0->MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.ACCELERATION)>0;case 1->MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.ITEM_COMPACT)>0;case 2->MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.ENERGY_COIL)>0;case 3->MachineUpgradeCards.tier(stack,MachineUpgradeCards.Family.VOID)>0;default->false;};}
    public int compactTier(){return MachineUpgradeCards.tier(inventory.getStackInSlot(kind.upgrades()+1),MachineUpgradeCards.Family.ITEM_COMPACT);}
    public void dropContents(){
        if(level==null||level.isClientSide)return;
        for(int slot=0;slot<inventory.getSlots();slot++){
            ItemStack recovered;
            while(!(recovered=inventory.extractItem(slot,64,false)).isEmpty())
                net.minecraft.world.Containers.dropItemStack(level,worldPosition.getX()+.5,worldPosition.getY()+.5,worldPosition.getZ()+.5,recovered);
        }
    }
    public int accelerationTier(){return MachineUpgradeCards.tier(inventory.getStackInSlot(kind.upgrades()),MachineUpgradeCards.Family.ACCELERATION);}
    public int coilTier(){return MachineUpgradeCards.tier(inventory.getStackInSlot(kind.upgrades()+2),MachineUpgradeCards.Family.ENERGY_COIL);}
    public boolean usesCards(){return accelerationTier()>0||coilTier()>0||compactTier()>0||voidInstalled();}
    public int speedPercent(){return usesCards()?100+Math.min(150,accelerationTier()*MachineUpgradeConfig.SPEED_PERCENT_PER_TIER.get()):speedQuarter()*25;}
    public int duration(ProcessingRecipe r){return Math.max(1,(int)(((long)r.time()*100+speedPercent()-1)/speedPercent()));}
    public int speedQuarter(){return usesCards()?(100+Math.min(150,accelerationTier()*MachineUpgradeConfig.SPEED_PERCENT_PER_TIER.get()))/25:4+casingTier()+(upgradeValid(1,inventory.getStackInSlot(kind.upgrades()+1))?2:0);}
    public int energyCost(ProcessingRecipe r){int dust=Math.max(0,DUSTS.indexOf(id(inventory.getStackInSlot(kind.upgrades()+2)).replace("zerog_tweaks:",""))+1);int saving=usesCards()?Math.min(30,coilTier()*MachineUpgradeConfig.ENERGY_SAVING_PER_TIER.get()):5*casingTier()+5*dust;return Math.max(1,(int)(((long)r.energy()*(100-saving)+99)/100));}
    public ProcessingRecipe.Input input(){var in=new ArrayList<ItemStack>();for(int i=0;i<kind.inputCount;i++)in.add(inventory.getStackInSlot(i));return new ProcessingRecipe.Input(in,inventory.getStackInSlot(kind.catalyst()));}
    public ItemStack output(ProcessingRecipe r,int index){var out=r.outputs().get(index).stack().copy();if(!usesCards()&&kind==ProcessingRegistry.Kind.REFINING&&index==0&&casingTier()>0&&r.upgradedCount()>out.getCount())out.setCount(Math.min(out.getMaxStackSize(),r.upgradedCount()));return out;}
    public boolean outputsFit(ProcessingRecipe r){for(int i=0;i<r.outputs().size();i++){var old=inventory.getStackInSlot(kind.output()+i);var add=output(r,i);if(voids(add))continue;if(!old.isEmpty()&&(!ItemStack.isSameItemSameComponents(old,add)||old.getCount()+add.getCount()>old.getMaxStackSize()))return false;}return true;}
    public static void tick(Level level,BlockPos pos,BlockState state,ProcessingBlockEntity be){
        if(level.isClientSide)return;
        var holder=level.getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get(),be.input(),level);
        if(holder.isEmpty()){be.clearJob();return;}
        var h=holder.get();var r=h.value();String config=id(be.inventory.getStackInSlot(be.kind.upgrades()))+":"+id(be.inventory.getStackInSlot(be.kind.upgrades()+1))+":"+id(be.inventory.getStackInSlot(be.kind.upgrades()+2))+":"+be.speedPercent()+":"+be.energyCost(r)+":"+be.voidInstalled()+":"+be.voidRevision;
        if(!be.job.equals(h.id().toString())||!be.configuration.equals(config)){be.clearJob();be.job=h.id().toString();be.configuration=config;}
        if(!be.outputsFit(r))return;
        int ticks=be.duration(r),next=Math.min(ticks,be.progress+1),target=(int)((long)be.energyCost(r)*next/ticks),cost=Math.max(0,target-be.paid);
        if(be.stored<cost)return;
        be.stored-=cost;be.paid=target;be.progress=next;
        if(next==ticks){
            int[] slots=r.assignment(be.input());if(slots==null){be.clearJob();return;}
            for(int i=0;i<r.outputs().size();i++)if(r.outputs().get(i).chance()>=1||level.random.nextDouble()<r.outputs().get(i).chance()){
                var add=be.output(r,i);if(be.voids(add))continue;var old=be.inventory.getStackInSlot(be.kind.output()+i);if(!old.isEmpty())add.setCount(add.getCount()+old.getCount());be.inventory.setStackInSlot(be.kind.output()+i,add);
            }
            for(int i=0;i<slots.length;i++)if(r.inputs().get(i).consumed())be.inventory.extractItem(slots[i],r.inputs().get(i).count(),false);
            r.catalyst().filter(ProcessingRecipe.Counted::consumed).ifPresent(c->be.inventory.extractItem(be.kind.catalyst(),c.count(),false));be.clearJob();
        }
        be.setChanged();
    }
    private void clearJob(){if(progress!=0||paid!=0){progress=0;paid=0;setChanged();}job="";configuration="";}
    public IEnergyStorage energyInput(Direction side){return new IEnergyStorage(){public int receiveEnergy(int n,boolean sim){if(faceDisabled(side)||isRemoved())return 0;int a=Math.min(Math.max(0,n),1_000_000-stored);if(!sim&&a>0){stored+=a;setChanged();}return a;}public int extractEnergy(int n,boolean sim){return 0;}public int getEnergyStored(){return stored;}public int getMaxEnergyStored(){return 1_000_000;}public boolean canExtract(){return false;}public boolean canReceive(){return !faceDisabled(side)&&!isRemoved();}};}
    /** Top = reagents, back = catalyst, bottom/front = output, other sides = reagents. No remote upgrades. */
    public IItemHandler itemsFor(Direction side){
        Direction front=getBlockState().getValue(BlockStateProperties.HORIZONTAL_FACING);
        int mode=itemMode(side),epoch=side==null?0:itemEpochs[side.ordinal()];
        int start=switch(mode){case 1->0;case 2->kind.catalyst();case 3->kind.output();default->side==Direction.DOWN||side==front?kind.output():side==front.getOpposite()?kind.catalyst():0;};
        int count=mode==4?0:start==kind.output()?kind.outputCount:start==kind.catalyst()?1:kind.inputCount;
        return new IItemHandler(){
            private boolean live(){return !isRemoved()&&itemMode(side)==mode&&(side==null||itemEpochs[side.ordinal()]==epoch)&&getBlockState().getValue(BlockStateProperties.HORIZONTAL_FACING)==front;}
            private boolean valid(int n){return live()&&n>=0&&n<count;}
            public int getSlots(){return live()?count:0;}
            public ItemStack getStackInSlot(int n){return valid(n)?inventory.getStackInSlot(start+n):ItemStack.EMPTY;}
            public ItemStack insertItem(int n,ItemStack s,boolean sim){return !valid(n)||start==kind.output()?s:inventory.insertItem(start+n,s,sim);}
            public ItemStack extractItem(int n,int amount,boolean sim){return valid(n)&&start==kind.output()?inventory.extractItem(start+n,amount,sim):ItemStack.EMPTY;}
            public int getSlotLimit(int n){return valid(n)?inventory.getSlotLimit(start+n):0;}
            public boolean isItemValid(int n,ItemStack s){return valid(n)&&start!=kind.output()&&inventory.isItemValid(start+n,s);}
        };
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putIntArray("ItemFaces",itemModes);int mask=0;for(int i=0;i<6;i++)if(disabledFaces[i])mask|=1<<i;tag.putInt("DisabledFaces",mask);tag.put("Inventory",inventory.serializeNBT(lookup));tag.putInt("Energy",stored);tag.putInt("Progress",progress);tag.putInt("Paid",paid);tag.putString("Job",job);tag.putString("Configuration",configuration);
        var entries=new net.minecraft.nbt.ListTag();
        for(int i=0;i<VOID_FILTER_SIZE;i++)if(voidTemplates[i]!=null&&!voidTemplates[i].isEmpty()){
            var entry=new CompoundTag();entry.putInt("Slot",i);entry.putString("Item",id(voidTemplates[i]));entries.add(entry);
        }
        tag.put("VoidFilter",entries);tag.putInt("VoidRevision",voidRevision);
    }
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);int[] modes=tag.getIntArray("ItemFaces");for(int i=0;i<6;i++){itemModes[i]=i<modes.length&&modes[i]>=0&&modes[i]<=4?modes[i]:0;itemEpochs[i]++;disabledFaces[i]=(tag.getInt("DisabledFaces")&(1<<i))!=0;}
        var savedInventory=tag.getCompound("Inventory").copy();savedInventory.putInt("Size",kind.slots());
        inventory.deserializeNBT(lookup,savedInventory);stored=Math.clamp(tag.getInt("Energy"),0,1_000_000);progress=Math.clamp(tag.getInt("Progress"),0,72_000);paid=Math.clamp(tag.getInt("Paid"),0,10_000_000);job=tag.getString("Job");configuration=tag.getString("Configuration");
        Arrays.fill(voidTemplates,null);voidRevision=Math.max(0,tag.getInt("VoidRevision"));
        for(var value:tag.getList("VoidFilter",net.minecraft.nbt.Tag.TAG_COMPOUND)){
            var entry=(CompoundTag)value;int slot=entry.getInt("Slot");
            var key=net.minecraft.resources.ResourceLocation.tryParse(entry.getString("Item"));
            if(slot>=0&&slot<VOID_FILTER_SIZE&&key!=null&&BuiltInRegistries.ITEM.containsKey(key))voidTemplates[slot]=new ItemStack(BuiltInRegistries.ITEM.get(key));
        }
    }
}
