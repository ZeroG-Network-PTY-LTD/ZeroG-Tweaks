package net.zerog.tweaks.transport;

import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.server.level.ServerLevel;

public final class TransportToolItem extends Item {
    private final String kind;
    public TransportToolItem(Properties props,String kind){super(props);this.kind=kind;}
    @Override public net.minecraft.world.InteractionResultHolder<ItemStack> use(net.minecraft.world.level.Level level,net.minecraft.world.entity.player.Player player,net.minecraft.world.InteractionHand hand){if(!kind.endsWith("filter_card"))return super.use(level,player,hand);if(player instanceof net.minecraft.server.level.ServerPlayer server)server.openMenu(new net.minecraft.world.SimpleMenuProvider((id,inv,p)->new TransportFilterMenu(id,inv,hand),Component.literal("Transport Filter")),buf->buf.writeEnum(hand));return net.minecraft.world.InteractionResultHolder.sidedSuccess(player.getItemInHand(hand),level.isClientSide);}
    @Override public InteractionResult useOn(UseOnContext context){
        if(!(context.getLevel().getBlockEntity(context.getClickedPos()) instanceof TransportBlockEntity be))return InteractionResult.PASS;
        if(!(context.getLevel() instanceof ServerLevel level)||context.getPlayer()==null)return InteractionResult.SUCCESS;
        var player=context.getPlayer();int face=context.getClickedFace().ordinal();
        if(kind.equals("flux_wrench")){
            if(player.isShiftKeyDown()){
                if(be.block().family.equals("null_link"))be.unlink();
                var drop=new ItemStack(be.getBlockState().getBlock());drop.set(DataComponents.BLOCK_ENTITY_DATA,CustomData.of(be.saveWithFullMetadata(level.registryAccess())));
                // Clear before replacement: the saved item owns contents, preventing double drops.
                for(int i=0;i<be.items.getSlots();i++)be.items.setStackInSlot(i,ItemStack.EMPTY);be.tank.setFluid(net.neoforged.neoforge.fluids.FluidStack.EMPTY);be.stored=0;
                level.removeBlock(be.getBlockPos(),false);net.minecraft.world.Containers.dropItemStack(level,be.getBlockPos().getX()+.5,be.getBlockPos().getY()+.5,be.getBlockPos().getZ()+.5,drop);
            }else{be.cycleFace(context.getClickedFace());player.displayClientMessage(Component.literal(be.getBlockState().hasProperty(TransportBlock.MODE)?"Port: "+be.getBlockState().getValue(TransportBlock.MODE).getSerializedName():"Face: "+new String[]{"Normal","Push / output","Pull / input","Disabled"}[be.modes[face]]),true);}
        }else if(kind.equals("null_frequency_card")){
            if(!be.block().family.equals("null_link"))return InteractionResult.FAIL;
            var data=context.getItemInHand().getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();
            if(!data.contains("dimension")){data.putString("dimension",level.dimension().location().toString());data.putLong("position",be.getBlockPos().asLong());context.getItemInHand().set(DataComponents.CUSTOM_DATA,CustomData.of(data));}
            else{
                var key=net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,net.minecraft.resources.ResourceLocation.parse(data.getString("dimension")));var sourceLevel=level.getServer().getLevel(key);var pos=net.minecraft.core.BlockPos.of(data.getLong("position"));
                if(sourceLevel==null||!sourceLevel.hasChunkAt(pos)||!(sourceLevel.getBlockEntity(pos) instanceof TransportBlockEntity first)||first==be||!first.block().family.equals("null_link"))return InteractionResult.FAIL;
                // Bind only unused item/fluid endpoints. Energy is merged once, never copied.
                if(first.partner!=null||be.partner!=null||!first.tank.isEmpty()||!be.tank.isEmpty()||(long)first.stored+be.stored>4000000)return InteractionResult.FAIL;
                for(int i=0;i<9;i++)if(!first.items.getStackInSlot(i).isEmpty()||!be.items.getStackInSlot(i).isEmpty())return InteractionResult.FAIL;
                first.partner=be.getBlockPos();first.partnerDimension=level.dimension().location().toString();be.partner=first.getBlockPos();be.partnerDimension=sourceLevel.dimension().location().toString();first.setChanged();be.setChanged();context.getItemInHand().remove(DataComponents.CUSTOM_DATA);
                var owner=first.owner();if(owner==null)return InteractionResult.FAIL;var remote=owner==first?be:first;owner.stored+=remote.stored;remote.stored=0;owner.setChanged();remote.setChanged();
            }
            player.displayClientMessage(Component.literal("Null Link frequency stored / paired (loaded endpoints only)"),true);
        }else{
            var other=player.getOffhandItem();
            var saved=context.getItemInHand().getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();if(saved.contains("templates")){var handler=kind.equals("item_filter_card")?be.ghostItems:be.ghostFluids;if(saved.getCompound("templates").getInt("Size")!=handler.getSlots())return InteractionResult.FAIL;handler.deserializeNBT(level.registryAccess(),saved.getCompound("templates"));be.blacklist=saved.getBoolean("blacklist");be.matchTags=saved.getBoolean("match_tags");be.matchComponents=saved.getBoolean("match_components");be.itemFilter="";be.fluidFilter="";be.setChanged();player.displayClientMessage(Component.literal("Saved filter card applied"),true);return InteractionResult.CONSUME;}
            if(kind.equals("item_filter_card"))for(int i=0;i<9;i++)be.ghostItems.setStackInSlot(i,ItemStack.EMPTY);else for(int i=0;i<3;i++)be.ghostFluids.setStackInSlot(i,ItemStack.EMPTY);
            if(kind.equals("item_filter_card")){if(other.isEmpty())be.itemFilter="";else be.itemFilter=net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(other.getItem()).toString();}
            else{var fluid=net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(other);be.fluidFilter=fluid.map(f->net.minecraft.core.registries.BuiltInRegistries.FLUID.getKey(f.getFluid()).toString()).orElse("");}
            be.blacklist=player.isShiftKeyDown();be.setChanged();player.displayClientMessage(Component.literal("Filter: "+(be.blacklist?"blacklist ":"whitelist ")+(kind.equals("item_filter_card")?be.itemFilter:be.fluidFilter)),true);
        }
        return InteractionResult.CONSUME;
    }
}
