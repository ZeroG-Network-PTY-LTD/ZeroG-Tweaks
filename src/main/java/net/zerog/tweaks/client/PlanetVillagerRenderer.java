package net.zerog.tweaks.client;

import java.util.Set;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.entity.PlanetVillager;
import net.zerog.tweaks.registry.ZGPlanetVillagers;
import software.bernie.geckolib.model.GeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class PlanetVillagerRenderer extends GeoEntityRenderer<PlanetVillager>{
    public PlanetVillagerRenderer(EntityRendererProvider.Context context){
        super(context,new Model());shadowRadius=.5F;withScale(.9375F);addRenderLayer(new AutoGlowingGeoLayer<>(this));
    }
    @Override public void preRender(com.mojang.blaze3d.vertex.PoseStack pose,PlanetVillager mob,
            software.bernie.geckolib.cache.object.BakedGeoModel model,net.minecraft.client.renderer.MultiBufferSource buffers,
            com.mojang.blaze3d.vertex.VertexConsumer buffer,boolean reRender,float partialTick,int light,int overlay,int colour){
        withScale(mob.isBaby()?.46875F:.9375F);shadowRadius=mob.isBaby()?.25F:.5F;
        super.preRender(pose,mob,model,buffers,buffer,reRender,partialTick,light,overlay,colour);
    }
    @SubscribeEvent public static void register(EntityRenderersEvent.RegisterRenderers event){
        ZGPlanetVillagers.TYPES.values().forEach(type->event.registerEntityRenderer(type.get(),PlanetVillagerRenderer::new));
    }
    private static class Model extends GeoModel<PlanetVillager>{
        @Override public void setCustomAnimations(PlanetVillager mob,long instanceId,software.bernie.geckolib.animation.AnimationState<PlanetVillager> state){
            super.setCustomAnimations(mob,instanceId,state);
            var head=getAnimationProcessor().getBone("head");
            var data=state.getData(software.bernie.geckolib.constant.DataTickets.ENTITY_MODEL_DATA);
            if(head!=null && data!=null && mob.getUnhappyCounter()==0){
                head.setRotX(data.headPitch()*net.minecraft.util.Mth.DEG_TO_RAD);
                head.setRotY(data.netHeadYaw()*net.minecraft.util.Mth.DEG_TO_RAD);
            }
        }
        private static final Set<String> JOBS=Set.of("armorer","butcher","cartographer","cleric","farmer","fisherman","fletcher",
                "leatherworker","librarian","mason","shepherd","toolsmith","weaponsmith");
        private ResourceLocation path(String path){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path);}
        @Override public ResourceLocation getModelResource(PlanetVillager mob){return path("geo/villagers/"+mob.species()+".geo.json");}
        @Override public ResourceLocation getAnimationResource(PlanetVillager mob){return path("animations/villagers/"+mob.species()+".animation.json");}
        @Override public ResourceLocation getTextureResource(PlanetVillager mob){
            String job=BuiltInRegistries.VILLAGER_PROFESSION.getKey(mob.getVillagerData().getProfession()).getPath();
            if(!JOBS.contains(job))job="none";
            return path("textures/entity/villager/"+mob.species()+"/style_"+mob.style()+"_"+job+".png");
        }
    }
}
