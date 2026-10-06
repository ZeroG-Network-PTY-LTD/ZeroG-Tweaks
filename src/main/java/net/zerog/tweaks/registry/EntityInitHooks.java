package net.zerog.tweaks.registry;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
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
        event.registerEntityRenderer(EntityInit.METEOR_MAW.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c,"meteor_maw_ironfall",1.25F));
        event.registerEntityRenderer(EntityInit.CINDER_MITE.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "shatteredskies:splinter_mite_cinder", .35F));
        event.registerEntityRenderer(EntityInit.REGOLITH_CRAWLER.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "regolith_crawler", .45F));
        event.registerEntityRenderer(EntityInit.CRYSTAL_STAG.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "crystal_stag", 0.7F));
        event.registerEntityRenderer(EntityInit.FROST_YAK.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "frost_yak", .7F));
        event.registerEntityRenderer(EntityInit.MOON_HOPPER.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "moon_hopper", .25F));
        event.registerEntityRenderer(EntityInit.DUST_GRAZER.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "dust_grazer", .7F));
        event.registerEntityRenderer(EntityInit.PRISMLING_HOLDER.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "prismling", 0.35F));
        event.registerEntityRenderer(EntityInit.AZURE_FOWL.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "azure_fowl", 0.3F));
        event.registerEntityRenderer(EntityInit.MOSSBACK.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "mossback", 1.3F));
        event.registerEntityRenderer(EntityInit.GLIMMERFISH.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "glimmerfish", 0.2F));
        event.registerEntityRenderer(EntityInit.RUST_BEETLE.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "rust_beetle", .4F));
        event.registerEntityRenderer(EntityInit.DUNE_BURROWER.get(),
                c -> new net.zerog.tweaks.client.ZGGeoMobRenderer<>(c, "dune_burrower", .4F));
    }
}
