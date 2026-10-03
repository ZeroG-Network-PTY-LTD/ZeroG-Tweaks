package net.zerog.tweaks.client;

import net.minecraft.client.model.BeeModel;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.BeeRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Bee;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.entity.AlienGlowbug;
import net.zerog.tweaks.registry.ZGGlowbugs;

@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class AlienGlowbugRenderer extends BeeRenderer {
    public AlienGlowbugRenderer(EntityRendererProvider.Context context){
        super(context);shadowRadius=.18F;
        addLayer(new net.minecraft.client.renderer.entity.layers.RenderLayer<Bee,BeeModel<Bee>>(this){
            @Override public void render(PoseStack stack,MultiBufferSource buffers,int light,Bee bee,float limbSwing,float limbAmount,float partialTick,float age,float yaw,float pitch){
                if(Math.floorMod(bee.tickCount+bee.getId()*7,100)<4) return;
                var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/entity/"+((AlienGlowbug)bee).planet+"_glowbug_glowmask.png");
                getParentModel().renderToBuffer(stack,buffers.getBuffer(RenderType.eyes(id)),15728640,OverlayTexture.NO_OVERLAY);
            }
        });
    }
    @Override public ResourceLocation getTextureLocation(Bee entity){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/entity/"+((AlienGlowbug)entity).planet+"_glowbug"+(Math.floorMod(entity.tickCount+entity.getId()*7,100)<4?"_blink":"_frame_"+Math.floorMod(entity.tickCount/3,8))+".png");}
    @Override protected void scale(Bee entity,PoseStack stack,float partialTick){super.scale(entity,stack,partialTick);stack.scale(.5F,.5F,.5F);}
    @SubscribeEvent public static void register(EntityRenderersEvent.RegisterRenderers event){ZGGlowbugs.TYPES.values().forEach(type->event.registerEntityRenderer(type.get(),AlienGlowbugRenderer::new));}
}
