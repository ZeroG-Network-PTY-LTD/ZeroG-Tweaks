package net.zerog.tweaks.client;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.AddPackFindersEvent;
import net.zerog.tweaks.ZeroGTweaks;

/** Explicit priority avoids relying on mod-loading order for aeroapiary repairs.
 * Only client artwork is overridden; the separate bee mod and its data remain intact.
 */
@EventBusSubscriber(modid=ZeroGTweaks.MODID, value=Dist.CLIENT, bus=EventBusSubscriber.Bus.MOD)
public final class InventoryVisualPack {
    private InventoryVisualPack() {}
    @SubscribeEvent
    public static void register(AddPackFindersEvent event) {
        event.addPackFinders(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"resourcepacks/visual_refresh"),
                PackType.CLIENT_RESOURCES,Component.literal("ZeroG: Inventory and Material Refresh"),
                PackSource.BUILT_IN,true,Pack.Position.TOP);
    }
}
