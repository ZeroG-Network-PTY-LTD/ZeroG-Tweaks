package net.zerog.tweaks.client;

import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.ItemBlockRenderTypes;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGFluids;
import org.joml.Vector3f;

/** Client side of Liquid Starlight: its animated textures, translucent rendering and a pale cyan underwater fog. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, value = Dist.CLIENT)
public final class ZGFluidClient {
    private static final ResourceLocation STILL = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/liquid_starlight_still");
    private static final ResourceLocation FLOW = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/liquid_starlight_flow");

    @SubscribeEvent
    public static void extensions(RegisterClientExtensionsEvent event) {
        event.registerFluidType(new IClientFluidTypeExtensions() {
            @Override public ResourceLocation getStillTexture() { return STILL; }
            @Override public ResourceLocation getFlowingTexture() { return FLOW; }

            @Override
            public Vector3f modifyFogColor(Camera camera, float partialTick, ClientLevel level, int renderDistance,
                                           float darkenWorldAmount, Vector3f fluidFogColor) {
                return new Vector3f(0.55F, 0.85F, 1.0F);
            }
        }, ZGFluids.LIQUID_STARLIGHT_TYPE.get());
    }

    @SubscribeEvent
    @SuppressWarnings("deprecation")
    public static void setup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemBlockRenderTypes.setRenderLayer(ZGFluids.LIQUID_STARLIGHT.get(), RenderType.translucent());
            ItemBlockRenderTypes.setRenderLayer(ZGFluids.FLOWING_LIQUID_STARLIGHT.get(), RenderType.translucent());
        });
    }

    private ZGFluidClient() {}
}
