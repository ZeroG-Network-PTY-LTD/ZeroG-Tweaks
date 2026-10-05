package net.zerog.tweaks.transport;

import net.minecraft.core.component.DataComponents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.core.registries.BuiltInRegistries;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.items.SlotItemHandler;

/** Held-card editor: templates are metadata, never a second physical inventory. */
public final class TransportFilterMenu extends AbstractContainerMenu {
    public final InteractionHand hand;public final ItemStack card;public final boolean fluid;public final ItemStackHandler templates;private final ContainerData data;
    public TransportFilterMenu(int id,Inventory inv,InteractionHand hand){super(TransportMenus.FILTER.get(),id);this.hand=hand;card=inv.player.getItemInHand(hand);String name=BuiltInRegistries.ITEM.getKey(card.getItem()).toString();fluid=name.equals("zerog_tweaks:fluid_filter_card");if(!fluid&&!name.equals("zerog_tweaks:item_filter_card"))throw new IllegalArgumentException("Not a filter card");templates=new ItemStackHandler(fluid?3:9);var tag=card.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();if(tag.contains("templates")&&tag.getCompound("templates").getInt("Size")==templates.getSlots())templates.deserializeNBT(inv.player.level().registryAccess(),tag.getCompound("templates"));
        data=inv.player.level().isClientSide?new SimpleContainerData(3):new ContainerData(){public int get(int i){var t=card.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();return t.getBoolean(new String[]{"blacklist","match_tags","match_components"}[i])?1:0;}public void set(int i,int v){}public int getCount(){return 3;}};addDataSlots(data);
        for(int i=0;i<templates.getSlots();i++)addSlot(new SlotItemHandler(templates,i,8+i*18,30){@Override public boolean mayPickup(Player p){return false;}@Override public boolean mayPlace(ItemStack stack){return false;}});
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(inv,9+row*9+col,8+col*18,100+row*18));for(int col=0;col<9;col++)addSlot(new Slot(inv,col,8+col*18,158));
    }
    public int value(int i){return data.get(i);}
    private void save(Player player){var tag=card.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();tag.put("templates",templates.serializeNBT(player.level().registryAccess()));card.set(DataComponents.CUSTOM_DATA,CustomData.of(tag));player.getInventory().setChanged();broadcastChanges();}
    @Override public boolean stillValid(Player player){return player.getItemInHand(hand)==card&&!card.isEmpty();}
    @Override public void clicked(int slot,int button,ClickType type,Player player){if(!player.level().isClientSide&&!stillValid(player))return;if(slot>=0&&slot<templates.getSlots()){if(player.level().isClientSide||type!=ClickType.PICKUP)return;var template=button==1?ItemStack.EMPTY:getCarried().copyWithCount(1);if(!fluid||template.isEmpty()||net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(template).isPresent()){templates.setStackInSlot(slot,template);save(player);}return;}super.clicked(slot,button,type,player);}
    @Override public boolean clickMenuButton(Player player,int id){if(player.level().isClientSide||!stillValid(player)||id<0||id>3)return false;var tag=card.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();if(id==3){for(int i=0;i<templates.getSlots();i++)templates.setStackInSlot(i,ItemStack.EMPTY);}else{String key=new String[]{"blacklist","match_tags","match_components"}[id];tag.putBoolean(key,!tag.getBoolean(key));card.set(DataComponents.CUSTOM_DATA,CustomData.of(tag));}save(player);return true;}
    @Override public ItemStack quickMoveStack(Player player,int index){return ItemStack.EMPTY;}
}
