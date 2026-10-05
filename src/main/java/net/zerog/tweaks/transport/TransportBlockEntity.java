package net.zerog.tweaks.transport;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.fluids.capability.templates.FluidTank;

/** Per-node persisted buffers; simulation precedes extraction. Never loads another chunk. */
public final class TransportBlockEntity extends BlockEntity {
    public ItemStack motionItem=ItemStack.EMPTY;
    public FluidStack motionFluid=FluidStack.EMPTY;
    public long motionTick=-1000;
    public int motionFrom,motionTo;
    @Override public CompoundTag getUpdateTag(HolderLookup.Provider lookup){
        var tag=new CompoundTag();tag.putLong("motion_tick",motionTick);tag.putInt("from",motionFrom);tag.putInt("to",motionTo);
        if(!motionItem.isEmpty())tag.put("motion_item",motionItem.save(lookup));
        if(!motionFluid.isEmpty())tag.put("motion_fluid",motionFluid.save(lookup));return tag;
    }
    @Override public net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket getUpdatePacket(){return net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket.create(this);}
    @Override public void handleUpdateTag(CompoundTag tag,HolderLookup.Provider lookup){
        motionTick=tag.getLong("motion_tick");motionFrom=Math.floorMod(tag.getInt("from"),6);motionTo=Math.floorMod(tag.getInt("to"),6);
        motionItem=tag.contains("motion_item")?ItemStack.parseOptional(lookup,tag.getCompound("motion_item")):ItemStack.EMPTY;
        motionFluid=tag.contains("motion_fluid")?FluidStack.parseOptional(lookup,tag.getCompound("motion_fluid")):FluidStack.EMPTY;
    }
    @Override public void onDataPacket(net.minecraft.network.Connection connection,net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket packet,HolderLookup.Provider lookup){if(packet.getTag()!=null)handleUpdateTag(packet.getTag(),lookup);}
    public int stored;public int colour=-1;public int redstone;public int routing;public int cursor;
    // 0 normal, 1 push, 2 pull, 3 disabled. Input/output is always relative to the network.
    public final int[] modes=new int[6];public final int[] priorities=new int[6];
    public final ItemStackHandler items=new ItemStackHandler(9){@Override public boolean isItemValid(int slot,ItemStack stack){return supports("item");}@Override protected void onContentsChanged(int slot){setChanged();}};
    // These are filter templates only: never extracted, dropped, or transferred as real inventory.
    public final ItemStackHandler ghostItems=new ItemStackHandler(9){@Override protected void onContentsChanged(int slot){setChanged();}};
    public final ItemStackHandler ghostFluids=new ItemStackHandler(3){@Override protected void onContentsChanged(int slot){setChanged();}};
    public boolean matchTags,matchComponents;
    public final FluidTank tank=new FluidTank(16000){@Override protected void onContentsChanged(){setChanged();}};
    public String itemFilter="",fluidFilter="";public boolean blacklist;
    public String partnerDimension="";public BlockPos partner;
    private long topologyTick=Long.MIN_VALUE;private List<TransportBlockEntity> topology=List.of();
    public TransportBlockEntity(BlockPos pos,BlockState state){super(TransportRegistry.TYPE.get(),pos,state);if(block().family.equals("energy_cell")){Arrays.fill(modes,2);modes[state.hasProperty(net.minecraft.world.level.block.state.properties.BlockStateProperties.FACING)?state.getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.FACING).ordinal():Direction.NORTH.ordinal()]=1;}}
    public TransportBlock block(){return (TransportBlock)getBlockState().getBlock();}
    public TransportTier tier(){return TransportTier.ALL[block().tier];}
    public int synchronizedLimit(){
        int minimum=block().tier;
        if(level instanceof ServerLevel server&&!supports("item")&&(block().family.endsWith("pipe")||block().family.endsWith("conduit"))){
            var nodes=network(server);if(nodes.isEmpty())return 0;minimum=nodes.stream().mapToInt(n->n.block().tier).min().orElse(minimum);
        }
        var common=TransportTier.ALL[minimum];return supports("fluid")?common.fluid():supports("energy")?common.energy():common.items();
    }
    public boolean supports(String family){return block().family.startsWith(family)||block().family.equals("null_link");}
    public int capacity(){return block().family.equals("energy_cell")?tier().capacity():block().family.equals("null_link")?4000000:block().family.equals("energy_port")?1000000:tier().energy();}
    public boolean input(Direction side){return net.zerog.tweaks.genetics.AlvearyServiceModules.sideAllowed(this,side)&&( !getBlockState().hasProperty(TransportBlock.MODE)||getBlockState().getValue(TransportBlock.MODE)!=TransportBlock.PortMode.OUTPUT)&&(side==null||modes[side.ordinal()]==0||modes[side.ordinal()]==2);}
    public boolean output(Direction side){return net.zerog.tweaks.genetics.AlvearyServiceModules.sideAllowed(this,side)&&( !getBlockState().hasProperty(TransportBlock.MODE)||getBlockState().getValue(TransportBlock.MODE)!=TransportBlock.PortMode.INPUT)&&(side==null||modes[side.ordinal()]==0||modes[side.ordinal()]==1);}
    public boolean permitted(String filter,String id){return filter.isEmpty()||blacklist!=Arrays.asList(filter.split(",")).contains(id);}
    public boolean permittedItem(ItemStack stack){boolean configured=false,match=false;for(int i=0;i<9;i++){var template=ghostItems.getStackInSlot(i);if(template.isEmpty())continue;configured=true;boolean type=template.is(stack.getItem())||matchTags&&template.getTags().anyMatch(stack::is);if(type&&(!matchComponents||template.getComponents().equals(stack.getComponents())))match=true;}return configured?blacklist!=match:permitted(itemFilter,BuiltInRegistries.ITEM.getKey(stack.getItem()).toString());}
    public boolean permittedFluid(FluidStack stack){boolean configured=false,match=false;for(int i=0;i<3;i++){var template=net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(ghostFluids.getStackInSlot(i)).orElse(FluidStack.EMPTY);if(template.isEmpty())continue;configured=true;boolean type=template.getFluid()==stack.getFluid()||matchTags&&template.getFluid().builtInRegistryHolder().tags().anyMatch(tag->stack.getFluid().builtInRegistryHolder().is(tag));if(type&&(!matchComponents||template.getComponents().equals(stack.getComponents())))match=true;}return configured?blacklist!=match:permitted(fluidFilter,BuiltInRegistries.FLUID.getKey(stack.getFluid()).toString());}
    public void cycleFace(Direction side){int index=side.ordinal();if(getBlockState().hasProperty(TransportBlock.MODE)&&level!=null)level.setBlock(worldPosition,getBlockState().setValue(TransportBlock.MODE,TransportBlock.PortMode.values()[(getBlockState().getValue(TransportBlock.MODE).ordinal()+1)%3]),2);else modes[index]=block().family.equals("energy_cell")?(modes[index]==1?2:1):(modes[index]+1)%4;topologyTick=Long.MIN_VALUE;setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);}
    public TransportBlockEntity owner(){if(!block().family.equals("null_link")||partner==null)return this;if(!(level instanceof ServerLevel server))return this;var id=net.minecraft.resources.ResourceLocation.tryParse(partnerDimension);if(id==null)return null;var key=net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,id);var targetLevel=server.getServer().getLevel(key);if(targetLevel==null||!targetLevel.hasChunkAt(partner)||!(targetLevel.getBlockEntity(partner) instanceof TransportBlockEntity other)||other.partner==null||!other.partner.equals(worldPosition)||!other.partnerDimension.equals(server.dimension().location().toString()))return null;return (server.dimension().location().toString()+worldPosition.asLong()).compareTo(partnerDimension+partner.asLong())<0?this:other;}
    public void unlink(){if(partner!=null&&level instanceof ServerLevel server){var id=net.minecraft.resources.ResourceLocation.tryParse(partnerDimension);if(id!=null){var target=server.getServer().getLevel(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,id));if(target!=null&&target.hasChunkAt(partner)&&target.getBlockEntity(partner) instanceof TransportBlockEntity other&&worldPosition.equals(other.partner)&&server.dimension().location().toString().equals(other.partnerDimension)){other.partner=null;other.partnerDimension="";other.setChanged();target.invalidateCapabilities(other.worldPosition);}}}partner=null;partnerDimension="";setChanged();if(level!=null)level.invalidateCapabilities(worldPosition);}
    private boolean validOwner(TransportBlockEntity owner){return !isRemoved()&&!owner.isRemoved()&&owner()==owner;}
    private int remoteFactor(TransportBlockEntity owner){return owner==this?0:owner.getLevel()==getLevel()?1:2;}
    public IEnergyStorage energy(Direction side){var owner=owner();if(owner==null)return null;int factor=remoteFactor(owner);return new IEnergyStorage(){
        public int receiveEnergy(int amount,boolean simulate){int n=validOwner(owner)&&input(side)?Math.max(0,Math.min(amount,owner.capacity()-owner.stored)):0;int fee=(int)(((long)n*factor+99)/100);if(!simulate&&n>0){owner.stored+=n-fee;owner.setChanged();}return n;}
        public int extractEnergy(int amount,boolean simulate){int n=validOwner(owner)&&output(side)?Math.max(0,Math.min(amount,(int)((long)owner.stored*100/(100+factor)))):0;int fee=(int)(((long)n*factor+99)/100);if(!simulate&&n>0){owner.stored-=n+fee;owner.setChanged();}return n;}
        public int getEnergyStored(){return owner.stored;}public int getMaxEnergyStored(){return owner.capacity();}public boolean canExtract(){return output(side);}public boolean canReceive(){return input(side);}
    };}
    public IItemHandler itemHandler(Direction side){var owner=owner();if(owner==null)return null;int factor=remoteFactor(owner);return new IItemHandler(){
        public int getSlots(){return owner.items.getSlots();}public ItemStack getStackInSlot(int slot){return owner.items.getStackInSlot(slot);}public int getSlotLimit(int slot){return 64;}
        public boolean isItemValid(int slot,ItemStack stack){return supports("item")&&validOwner(owner)&&input(side)&&permittedItem(stack);}
        public ItemStack insertItem(int slot,ItemStack stack,boolean simulate){if(!isItemValid(slot,stack))return stack;int count=Math.min(stack.getCount(),factor==0?stack.getCount():owner.stored/(2*factor));var rest=owner.items.insertItem(slot,stack.copyWithCount(count),simulate);int accepted=count-rest.getCount();if(!simulate&&accepted>0){owner.stored-=accepted*2*factor;owner.setChanged();}return stack.copyWithCount(stack.getCount()-accepted);}
        public ItemStack extractItem(int slot,int amount,boolean simulate){if(!validOwner(owner)||!output(side))return ItemStack.EMPTY;int count=Math.max(0,Math.min(amount,factor==0?amount:owner.stored/(2*factor)));var result=owner.items.extractItem(slot,count,simulate);if(!simulate&&!result.isEmpty()){owner.stored-=result.getCount()*2*factor;owner.setChanged();}return result;}
    };}
    public IFluidHandler fluidHandler(Direction side){var owner=owner();if(owner==null)return null;int factor=remoteFactor(owner);return new IFluidHandler(){
        public int getTanks(){return 1;}public FluidStack getFluidInTank(int index){return owner.tank.getFluid();}public int getTankCapacity(int index){return owner.tank.getCapacity();}
        public boolean isFluidValid(int index,FluidStack stack){var id=BuiltInRegistries.FLUID.getKey(stack.getFluid()).toString();return TransportTier.minimumFluidTier(id)<=block().tier&&permittedFluid(stack);}
        public int fill(FluidStack stack,FluidAction action){if(!validOwner(owner)||!input(side)||!isFluidValid(0,stack))return 0;if(block().family.equals("fluid_pipe")&&level instanceof ServerLevel server){var nodes=network(server);if(nodes.isEmpty())return 0;for(var node:nodes)if(!node.tank.isEmpty()&&!FluidStack.isSameFluidSameComponents(node.tank.getFluid(),stack))return 0;}int count=Math.min(stack.getAmount(),factor==0?stack.getAmount():owner.stored/factor);int n=owner.tank.fill(stack.copyWithAmount(count),action);if(action.execute()&&n>0){owner.stored-=n*factor;owner.setChanged();}return n;}
        public FluidStack drain(FluidStack stack,FluidAction action){return FluidStack.isSameFluidSameComponents(stack,owner.tank.getFluid())?drain(stack.getAmount(),action):FluidStack.EMPTY;}
        public FluidStack drain(int amount,FluidAction action){if(!validOwner(owner)||!output(side))return FluidStack.EMPTY;int count=Math.max(0,Math.min(amount,factor==0?amount:owner.stored/factor));var result=owner.tank.drain(count,action);if(action.execute()&&!result.isEmpty()){owner.stored-=result.getAmount()*factor;owner.setChanged();}return result;}
    };}
    public boolean enabled(){if(level==null)return false;boolean signal=level.hasNeighborSignal(worldPosition);return redstone==0||redstone==1&&signal||redstone==2&&!signal;}
    public static void tick(Level level,BlockPos pos,BlockState state,TransportBlockEntity be){
        if(!(level instanceof ServerLevel server)||!be.enabled())return;
        if(server.getGameTime()%10==0)be.updateVisualState(server);
        if(be.block().family.equals("null_link"))return;
        boolean line=be.block().family.endsWith("conduit")||be.block().family.endsWith("pipe")||be.block().family.endsWith("tube");
        if(line){
            // Only the lexicographically first loaded node performs the bounded graph pass.
            var nodes=be.network(server);if(nodes.isEmpty()||nodes.get(0)!=be)return;
            String family=be.supports("energy")?"energy":be.supports("fluid")?"fluid":"item";
            int minTier=nodes.stream().mapToInt(n->n.block().tier).min().orElse(0);var tier=TransportTier.ALL[minTier];
            int budget=family.equals("energy")?tier.energy():family.equals("fluid")?tier.fluid():tier.items();
            if(family.equals("item")&&server.getGameTime()%tier.interval()!=0)return;
            for(var node:nodes)for(var side:Direction.values()){
                // Exhausting intake must not skip the delivery phase (a full buffer would stall forever).
                if(budget<=0)continue;if(node.modes[side.ordinal()]==3)continue;
                var other=node.worldPosition.relative(side);if(!server.hasChunkAt(other)||server.getBlockEntity(other) instanceof TransportBlockEntity next&&nodes.contains(next))continue;
                if(node.modes[side.ordinal()]==2)budget-=node.pull(server,other,side,family,budget);
            }
            // Stored content is moved directly to reachable endpoints; no extract without capacity.
            var endpoints=new ArrayList<Map.Entry<TransportBlockEntity,Direction>>();
            for(var node:nodes)for(var side:Direction.values())if(node.output(side)){
                var other=node.worldPosition.relative(side);if(server.hasChunkAt(other)&&!(server.getBlockEntity(other) instanceof TransportBlockEntity next&&nodes.contains(next)))endpoints.add(Map.entry(node,side));
            }
            endpoints.sort(Comparator.comparingInt((Map.Entry<TransportBlockEntity,Direction> e)->-e.getKey().priorities[e.getValue().ordinal()]));
            if(be.routing==1&&!endpoints.isEmpty())Collections.rotate(endpoints,-Math.floorMod(be.cursor++,endpoints.size()));
            if(be.routing==2)Collections.shuffle(endpoints,new Random(server.getGameTime()^pos.asLong()));
            int moved=0;
            for(var source:nodes)for(var endpoint:endpoints){if(moved>= (family.equals("energy")?tier.energy():family.equals("fluid")?tier.fluid():tier.items()))return;var dest=endpoint.getKey();moved+=source.push(server,dest.worldPosition.relative(endpoint.getValue()),endpoint.getValue(),family,(family.equals("energy")?tier.energy():family.equals("fluid")?tier.fluid():tier.items())-moved);}
        }else{String family=be.supports("energy")?"energy":be.supports("fluid")?"fluid":"item";int budget=be.supports("energy")?be.tier().energy():be.supports("fluid")?be.tier().fluid():be.tier().items();for(var side:Direction.values())if(budget>0&&be.output(side)&&server.hasChunkAt(pos.relative(side)))budget-=be.push(server,pos.relative(side),side,family,budget);}
    }
    private List<TransportBlockEntity> network(ServerLevel level){
        if(topologyTick==level.getGameTime())return topology;
        var found=new ArrayList<TransportBlockEntity>();var seen=new HashSet<BlockPos>();var queue=new ArrayDeque<TransportBlockEntity>();queue.add(this);seen.add(worldPosition);
        while(!queue.isEmpty()&&found.size()<256){var node=queue.remove();found.add(node);for(var side:Direction.values()){
            if(node.modes[side.ordinal()]==3)continue;var p=node.worldPosition.relative(side);if(!seen.add(p)||!level.hasChunkAt(p))continue;
            if(level.getBlockEntity(p) instanceof TransportBlockEntity next&&next.block().family.equals(block().family)&&next.modes[side.getOpposite().ordinal()]!=3&&(next.colour<0||node.colour<0||next.colour==node.colour)&&next.enabled())queue.add(next);
        }}if(!queue.isEmpty()){for(var node:found){node.topologyTick=level.getGameTime();node.topology=List.of();}return List.of();}found.sort(Comparator.comparingLong(n->n.worldPosition.asLong()));var snapshot=List.copyOf(found);for(var node:found){node.topologyTick=level.getGameTime();node.topology=snapshot;}return snapshot;
    }
    private void updateVisualState(ServerLevel level){var original=getBlockState();var next=original;
        if(next.hasProperty(TransportBlock.GAUGE))next=next.setValue(TransportBlock.GAUGE,(int)Math.min(8,(long)stored*8/Math.max(1,capacity())));
        for(var side:Direction.values()){var property=TransportBlock.SIDES.get(side);if(!next.hasProperty(property))continue;var neighbor=worldPosition.relative(side);var connection=TransportBlock.Connection.NONE;
            if(modes[side.ordinal()]!=3&&level.hasChunkAt(neighbor)){
                if(level.getBlockEntity(neighbor) instanceof TransportBlockEntity other&&other.block().family.equals(block().family)&&other.modes[side.getOpposite().ordinal()]!=3&&(colour<0||other.colour<0||colour==other.colour))connection=TransportBlock.Connection.PIPE;
                else if(supports("energy")&&level.getCapability(Capabilities.EnergyStorage.BLOCK,neighbor,side.getOpposite())!=null||supports("fluid")&&level.getCapability(Capabilities.FluidHandler.BLOCK,neighbor,side.getOpposite())!=null||supports("item")&&level.getCapability(Capabilities.ItemHandler.BLOCK,neighbor,side.getOpposite())!=null)connection=modes[side.ordinal()]==1?TransportBlock.Connection.PUSH:modes[side.ordinal()]==2?TransportBlock.Connection.PULL:TransportBlock.Connection.NORMAL;
            }next=next.setValue(property,connection);
        }
        if(!next.equals(original))level.setBlock(worldPosition,next,2);
    }
    private int pull(ServerLevel level,BlockPos pos,Direction side,String family,int limit){
        if(family.equals("energy")){var from=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos,side.getOpposite());if(from==null)return 0;int n=Math.min(Math.max(0,capacity()-stored),from.extractEnergy(limit,true));n=from.extractEnergy(n,false);stored+=n;if(n>0)setChanged();return n;}
        if(family.equals("fluid")){var from=level.getCapability(Capabilities.FluidHandler.BLOCK,pos,side.getOpposite());if(from==null)return 0;var sample=from.drain(limit,IFluidHandler.FluidAction.SIMULATE);int n=fluidHandler(null).fill(sample,IFluidHandler.FluidAction.SIMULATE);if(n<=0)return 0;sample=from.drain(sample.copyWithAmount(n),IFluidHandler.FluidAction.EXECUTE);return fluidHandler(null).fill(sample,IFluidHandler.FluidAction.EXECUTE);}
        var from=level.getCapability(Capabilities.ItemHandler.BLOCK,pos,side.getOpposite());if(from==null)return 0;for(int i=0;i<from.getSlots();i++){var sample=from.extractItem(i,limit,true);int n=sample.getCount()-insert(items,sample,true).getCount();if(n<=0||!permittedItem(sample))continue;var actual=from.extractItem(i,n,false);var rest=insert(items,actual,false);if(!rest.isEmpty())from.insertItem(i,rest,false);return actual.getCount()-rest.getCount();}return 0;
    }
    public int push(ServerLevel level,BlockPos pos,Direction side,String family,int limit){
        if(family.equals("energy")){var to=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos,side.getOpposite());if(to==null)return 0;int n=to.receiveEnergy(Math.min(stored,limit),true);n=to.receiveEnergy(n,false);stored-=n;if(n>0)setChanged();return n;}
        if(family.equals("fluid")){var to=level.getCapability(Capabilities.FluidHandler.BLOCK,pos,side.getOpposite());if(to==null)return 0;var sample=tank.drain(limit,IFluidHandler.FluidAction.SIMULATE);int n=to.fill(sample,IFluidHandler.FluidAction.SIMULATE);if(n<=0)return 0;n=to.fill(sample.copyWithAmount(n),IFluidHandler.FluidAction.EXECUTE);tank.drain(n,IFluidHandler.FluidAction.EXECUTE);if(n>0)TransportMotion.committed(this,level,pos,side,ItemStack.EMPTY,sample);return n;}
        var to=level.getCapability(Capabilities.ItemHandler.BLOCK,pos,side.getOpposite());if(to==null)return 0;for(int i=0;i<items.getSlots();i++){var sample=items.extractItem(i,limit,true);int n=sample.getCount()-insert(to,sample,true).getCount();if(n<=0)continue;var rest=insert(to,sample.copyWithCount(n),false);n-=rest.getCount();items.extractItem(i,n,false);if(n>0)TransportMotion.committed(this,level,pos,side,sample,FluidStack.EMPTY);return n;}return 0;
    }
    public static ItemStack insert(IItemHandler handler,ItemStack stack,boolean simulate){var remaining=stack.copy();for(int i=0;i<handler.getSlots()&&!remaining.isEmpty();i++)remaining=handler.insertItem(i,remaining,simulate);return remaining;}
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.saveAdditional(tag,lookup);tag.putInt("energy",stored);tag.putIntArray("modes",modes);tag.putIntArray("priority",priorities);tag.putInt("colour",colour);tag.putInt("redstone",redstone);tag.putInt("routing",routing);tag.putString("item_filter",itemFilter);tag.putString("fluid_filter",fluidFilter);tag.putBoolean("blacklist",blacklist);tag.putBoolean("match_tags",matchTags);tag.putBoolean("match_components",matchComponents);tag.put("ghost_items",ghostItems.serializeNBT(lookup));tag.put("ghost_fluids",ghostFluids.serializeNBT(lookup));tag.put("items",items.serializeNBT(lookup));tank.writeToNBT(lookup,tag);tag.putString("partner_dimension",partnerDimension);if(partner!=null)tag.putLong("partner",partner.asLong());}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider lookup){super.loadAdditional(tag,lookup);stored=Math.max(0,Math.min(capacity(),tag.getInt("energy")));var m=tag.getIntArray("modes");var p=tag.getIntArray("priority");for(int i=0;i<6;i++){if(i<m.length)modes[i]=Math.floorMod(m[i],4);priorities[i]=i<p.length?Math.max(-10,Math.min(10,p[i])):0;}colour=tag.contains("colour")?tag.getInt("colour"):-1;redstone=Math.floorMod(tag.getInt("redstone"),4);routing=Math.floorMod(tag.getInt("routing"),3);itemFilter=tag.getString("item_filter");fluidFilter=tag.getString("fluid_filter");blacklist=tag.getBoolean("blacklist");matchTags=tag.getBoolean("match_tags");matchComponents=tag.getBoolean("match_components");if(tag.contains("ghost_items")&&tag.getCompound("ghost_items").getInt("Size")==9)ghostItems.deserializeNBT(lookup,tag.getCompound("ghost_items"));if(tag.contains("ghost_fluids")&&tag.getCompound("ghost_fluids").getInt("Size")==3)ghostFluids.deserializeNBT(lookup,tag.getCompound("ghost_fluids"));items.deserializeNBT(lookup,tag.getCompound("items"));tank.readFromNBT(lookup,tag);partnerDimension=tag.getString("partner_dimension");partner=tag.contains("partner")?BlockPos.of(tag.getLong("partner")):null;}
}
