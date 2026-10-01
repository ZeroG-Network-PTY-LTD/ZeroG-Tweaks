package net.zerog.tweaks.client;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.TidewraithContent;

/** Client-only registration, so dedicated servers never load renderer classes. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class TidewraithClientEvents {
    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers event) {
        if (!TidewraithContent.isReady()) return;
        event.registerEntityRenderer(EntityInit.TIDEWRAITH.get(), TidewraithRenderer::new);
        event.registerEntityRenderer(EntityInit.TIDEWRAITH_BOSS.get(), TidewraithRenderer::new);
    }
    private TidewraithClientEvents() {}
}
