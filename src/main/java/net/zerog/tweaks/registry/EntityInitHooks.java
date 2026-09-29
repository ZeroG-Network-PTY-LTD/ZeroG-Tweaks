package net.zerog.tweaks.registry;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HorseRenderer;
import net.minecraft.client.renderer.entity.NoopRenderer;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

import net.zerog.tweaks.ZeroGTweaks;

/**
 * Client renderers for the five live mobs. Renderers reuse vanilla geometry;
 * dedicated ZeroG mob models + palette skins are a known open item (the mobs
 * already have design sheets in docs/zero-g-tweaks-bundle/sheets/mobs/).
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, value = Dist.CLIENT)
public final class EntityInitHooks {

    @SuppressWarnings({"unchecked", "rawtypes"})
    @SubscribeEvent
    public static void onRegisterRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(EntityInit.CRYSTAL_STAG.get(),
                (EntityRendererProvider) HorseRenderer::new);
        event.registerEntityRenderer(EntityInit.FROST_YAK.get(),
                (EntityRendererProvider) NoopRenderer::new);
        event.registerEntityRenderer(EntityInit.PRISMLING_HOLDER.get(),
                (EntityRendererProvider) NoopRenderer::new);
        event.registerEntityRenderer(EntityInit.RUST_BEETLE.get(),
                (EntityRendererProvider) NoopRenderer::new);
        event.registerEntityRenderer(EntityInit.DUNE_BURROWER.get(),
                (EntityRendererProvider) NoopRenderer::new);
    }
}