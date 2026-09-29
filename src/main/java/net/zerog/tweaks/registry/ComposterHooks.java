package net.zerog.tweaks.registry;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.EventBusSubscriber;

/** Composter + vanilla-registry-side hooks (code-side bootstrap maps). */
public final class ComposterHooks {
    private ComposterHooks() {}

    public static void register(IEventBus modBus) {
        // after registries bootstrap, fill code-side maps (fires on FMLCommonSetupEvent or server about to start)
        modBus.addListener(net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent.class, event -> {
            event.enqueueWork(() -> {
                ModBootstrap.bootstrap();
            });
        });
    }
}