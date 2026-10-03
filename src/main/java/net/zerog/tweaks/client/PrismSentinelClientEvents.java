package net.zerog.tweaks.client;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.EntityInit;

/** Client-only registration, so dedicated servers never load renderer classes. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, value = Dist.CLIENT)
public final class PrismSentinelClientEvents {
    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(EntityInit.PRISM_SENTINEL.get(), PrismSentinelRenderer::new);
    }
    private PrismSentinelClientEvents() {}
}
