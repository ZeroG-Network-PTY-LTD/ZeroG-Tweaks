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
        for(var gas:net.zerog.tweaks.registry.ZGGases.ALL) {
            event.registerFluidType(new IClientFluidTypeExtensions(){
                @Override public ResourceLocation getStillTexture(){return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"block/transport/"+gas.id()+"_wisp");}
                @Override public ResourceLocation getFlowingTexture(){return getStillTexture();}
            },gas.type().get());
        }
        for(var jelly:net.zerog.tweaks.registry.ZGGeneticsFluids.ALL) {
            event.registerFluidType(new IClientFluidTypeExtensions(){
                @Override public ResourceLocation getStillTexture(){return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"block/"+jelly.textureFamily+"_honey_still");}
                @Override public ResourceLocation getFlowingTexture(){return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"block/"+jelly.textureFamily+"_honey_flow");}
                @Override public Vector3f modifyFogColor(Camera camera,float partialTick,ClientLevel level,int renderDistance,float darkenWorldAmount,Vector3f colour){
                    return new Vector3f(((jelly.fog>>16)&255)/255F,((jelly.fog>>8)&255)/255F,(jelly.fog&255)/255F);
                }
            },jelly.type.get());
        }
        for(var honey:net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.values()) {
            event.registerFluidType(new IClientFluidTypeExtensions(){
                @Override public ResourceLocation getStillTexture(){return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"block/"+honey.id+"_honey_still");}
                @Override public ResourceLocation getFlowingTexture(){return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"block/"+honey.id+"_honey_flow");}
            },honey.type.get());
        }
        for (var liquid : net.zerog.tweaks.registry.ZGDimensionFluids.ALL) {
            event.registerFluidType(new IClientFluidTypeExtensions() {
                @Override public ResourceLocation getStillTexture() {
                    return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/" + liquid.id + "_still");
                }
                @Override public ResourceLocation getFlowingTexture() {
                    return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "block/" + liquid.id + "_flow");
                }
                @Override public Vector3f modifyFogColor(Camera camera, float partialTick, ClientLevel level,
                        int renderDistance, float darkenWorldAmount, Vector3f colour) {
                    return new Vector3f(((liquid.fog >> 16) & 255) / 255F, ((liquid.fog >> 8) & 255) / 255F, (liquid.fog & 255) / 255F);
                }
            }, liquid.type.get());
        }
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
            net.minecraft.client.renderer.item.ItemProperties.register(net.zerog.tweaks.registry.ZGGases.CANISTER.get(),
                ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"gas"),(stack,level,entity,seed)->{
                    var contents=stack.getOrDefault(net.zerog.tweaks.registry.ZGGases.CONTENT.get(),net.neoforged.neoforge.fluids.SimpleFluidContent.EMPTY);
                    return contents.is(net.zerog.tweaks.registry.ZGGases.HYDROGEN.fluid().get())?2:
                        contents.is(net.zerog.tweaks.registry.ZGGases.OXYGEN.fluid().get())?1:0;
                });
            for(var jelly:net.zerog.tweaks.registry.ZGGeneticsFluids.ALL) {
                ItemBlockRenderTypes.setRenderLayer(jelly.source.get(),RenderType.translucent());
                ItemBlockRenderTypes.setRenderLayer(jelly.flowing.get(),RenderType.translucent());
            }
            for(var honey:net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.values()) {
                ItemBlockRenderTypes.setRenderLayer(honey.source.get(),RenderType.translucent());
                ItemBlockRenderTypes.setRenderLayer(honey.flowing.get(),RenderType.translucent());
            }
            for (var liquid : net.zerog.tweaks.registry.ZGDimensionFluids.ALL) {
                ItemBlockRenderTypes.setRenderLayer(liquid.source.get(), RenderType.translucent());
                ItemBlockRenderTypes.setRenderLayer(liquid.flowing.get(), RenderType.translucent());
            }
            ItemBlockRenderTypes.setRenderLayer(ZGFluids.LIQUID_STARLIGHT.get(), RenderType.translucent());
            ItemBlockRenderTypes.setRenderLayer(ZGFluids.FLOWING_LIQUID_STARLIGHT.get(), RenderType.translucent());
        });
    }

    private ZGFluidClient() {}
}
