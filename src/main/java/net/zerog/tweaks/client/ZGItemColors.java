package net.zerog.tweaks.client;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGSpawnEggItem;
import net.zerog.tweaks.registry.ZGSpawnEggs;

/** Colours the spawn eggs (base and spots), like vanilla spawn eggs. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class ZGItemColors {
    private ZGItemColors() {}

    @SubscribeEvent
    public static void onItemColors(RegisterColorHandlersEvent.Item event) {
        for (var egg : ZGSpawnEggs.ALL) {
            event.register((stack, tintIndex) -> 0xFF000000 | ((ZGSpawnEggItem) stack.getItem()).color(tintIndex), egg.get());
        }
    }
}
