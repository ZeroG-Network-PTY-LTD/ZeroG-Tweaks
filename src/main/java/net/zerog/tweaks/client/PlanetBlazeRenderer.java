package net.zerog.tweaks.client;

import net.minecraft.client.renderer.entity.BlazeRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.model.BlazeModel;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.entity.monster.Blaze;
import net.minecraft.resources.ResourceLocation;
import com.mojang.blaze3d.vertex.PoseStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.entity.PlanetBlaze;
import net.zerog.tweaks.registry.ZGPlanetBlazes;

@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class PlanetBlazeRenderer extends BlazeRenderer {
    public PlanetBlazeRenderer(EntityRendererProvider.Context context){
        super(context);
        addLayer(new net.minecraft.client.renderer.entity.layers.RenderLayer<Blaze,BlazeModel<Blaze>>(this){
            @Override public void render(PoseStack stack,MultiBufferSource buffers,int light,Blaze blaze,float limb,float amount,float partial,float age,float yaw,float pitch){
                var mob=(PlanetBlaze)blaze;
                var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/entity/"+mob.style+"_blaze_"+mob.palette()+"_glowmask.png");
                getParentModel().renderToBuffer(stack,buffers.getBuffer(RenderType.eyes(id)),15728640,OverlayTexture.NO_OVERLAY);
            }
        });
    }
    @Override public ResourceLocation getTextureLocation(Blaze blaze){var mob=(PlanetBlaze)blaze;return ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/entity/"+mob.style+"_blaze_"+mob.palette()+".png");}
    @SubscribeEvent public static void register(EntityRenderersEvent.RegisterRenderers event){ZGPlanetBlazes.TYPES.values().forEach(type->event.registerEntityRenderer(type.get(),PlanetBlazeRenderer::new));}
}
