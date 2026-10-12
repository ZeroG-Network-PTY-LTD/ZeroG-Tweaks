package net.zerog.tweaks.registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.BlockItem;
import net.neoforged.bus.api.*;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.zerog.tweaks.travel.HubExhibits;
/** Owner-selected hub shells are the usable catalogue; IDs survive for old saves. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class ApiaryCatalogue {
 @SubscribeEvent(priority=EventPriority.LOWEST)
 public static void filter(BuildCreativeModeTabContentsEvent e){
  if(!BuiltInRegistries.BLOCK.containsKey(net.minecraft.resources.ResourceLocation.parse("aeroapiary:tier1_casing")))return;
  var supported=HubExhibits.serviceShellItemIds();
  java.util.function.Predicate<net.minecraft.world.item.ItemStack> retired=stack->{
   if(!(stack.getItem() instanceof BlockItem))return false;
   var key=BuiltInRegistries.ITEM.getKey(stack.getItem());return key.getNamespace().equals("aeroapiary")
    &&(key.getPath().matches("tier[0-9]+_.*")||key.getPath().equals("apiary_controller"))&&!supported.contains(key);
  };
  java.util.stream.Stream.concat(e.getParentEntries().stream(),e.getSearchEntries().stream()).filter(retired).toList()
   .forEach(stack->e.remove(stack,net.minecraft.world.item.CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS));
 }
 private ApiaryCatalogue(){}
}
