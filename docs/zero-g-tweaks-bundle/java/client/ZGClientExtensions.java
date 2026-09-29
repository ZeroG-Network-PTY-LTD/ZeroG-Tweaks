package net.zerog.tweaks.client;

import com.mojang.blaze3d.shaders.FogShape;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.FogRenderer;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.fluid.ZGFluids;
import org.joml.Vector3f;

/** Textures and underwater fog for the six ZeroG liquids. Colour is baked into the textures, so tint stays white. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class ZGClientExtensions {
    private ZGClientExtensions() {}

    @SubscribeEvent
    public static void registerClientExtensions(RegisterClientExtensionsEvent event) {
        register(event, ZGFluids.ACID, 0x73A01F, 5.0f);
        register(event, ZGFluids.LIQUID_STARLIGHT, 0x2E4AC0, 12.0f);
        register(event, ZGFluids.MAGMA_SLAG, 0x8A2A08, 1.5f);
        register(event, ZGFluids.CRYO_FLUID, 0x8FD0E6, 8.0f);
        register(event, ZGFluids.SOLAR_PLASMA, 0xFFB040, 1.0f);
        register(event, ZGFluids.NULL_FLUID, 0x1A1030, 6.0f);
    }

    private static void register(RegisterClientExtensionsEvent event, ZGFluids.Liquid liquid, int fog, float fogEnd) {
        ResourceLocation still = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/" + liquid.id + "_still");
        ResourceLocation flow = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/" + liquid.id + "_flow");
        Vector3f fogColor = new Vector3f(((fog >> 16) & 0xFF) / 255f, ((fog >> 8) & 0xFF) / 255f, (fog & 0xFF) / 255f);
        event.registerFluidType(new IClientFluidTypeExtensions() {
            @Override public ResourceLocation getStillTexture() { return still; }
            @Override public ResourceLocation getFlowingTexture() { return flow; }
            @Override public int getTintColor() { return 0xFFFFFFFF; }
            @Override public Vector3f modifyFogColor(Camera camera, float partialTick, ClientLevel level, int renderDistance, float darkenWorldAmount, Vector3f fluidFogColor) { return fogColor; }
            @Override public void modifyFogRender(Camera camera, FogRenderer.FogMode mode, float renderDistance, float partialTick, float nearDistance, float farDistance, FogShape shape) {
                RenderSystem.setShaderFogStart(0.25f);
                RenderSystem.setShaderFogEnd(fogEnd);
            }
        }, liquid.type.get());
    }
}
