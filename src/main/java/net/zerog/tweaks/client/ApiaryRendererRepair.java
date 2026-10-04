package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.animatable.GeoBlockEntity;
import software.bernie.geckolib.model.GeoModel;
import software.bernie.geckolib.renderer.GeoBlockRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

/** Optional compatibility repair; ordinary baked blocks never require invented geo assets. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
public final class ApiaryRendererRepair {
    private static ResourceLocation asset(String path) {return ResourceLocation.fromNamespaceAndPath("aeroapiary",path);}
    @SubscribeEvent(priority=EventPriority.LOWEST)
    @SuppressWarnings({"rawtypes","unchecked"})
    public static void register(EntityRenderersEvent.RegisterRenderers event) {
        var id=asset("zerog_machine");
        if(!BuiltInRegistries.BLOCK_ENTITY_TYPE.containsKey(id))return;
        BlockEntityType<BlockEntity> type=(BlockEntityType)BuiltInRegistries.BLOCK_ENTITY_TYPE.get(id);
        event.registerBlockEntityRenderer(type,context->new SafeRenderer());
    }
    public static boolean hasAnimatedAssets(String id,java.util.function.Predicate<ResourceLocation> exists) {
        // Only these shipped machines have both a UV atlas and their geo/animation files.
        return id.equals("apiary_controller")
            &&exists.test(asset("geo/machines/"+id+".geo.json"))
            &&exists.test(asset("textures/block/machines/"+id+"_hd.png"))
            &&exists.test(asset("animations/"+id+".animation.json"));
    }
    @SuppressWarnings({"rawtypes","unchecked"})
    private static final class SafeRenderer implements BlockEntityRenderer<BlockEntity> {
        private final GeoBlockRenderer animated;
        SafeRenderer() {
            GeoModel model=new GeoModel<GeoAnimatable>() {
                private String id(GeoAnimatable object) {return BuiltInRegistries.BLOCK.getKey(((BlockEntity)object).getBlockState().getBlock()).getPath();}
                @Override public ResourceLocation getModelResource(GeoAnimatable object) {return asset("geo/machines/"+id(object)+".geo.json");}
                @Override public ResourceLocation getTextureResource(GeoAnimatable object) {return asset("textures/block/machines/"+id(object)+"_hd.png");}
                @Override public ResourceLocation getAnimationResource(GeoAnimatable object) {return asset("animations/"+id(object)+".animation.json");}
            };
            animated=new GeoBlockRenderer(model);
            animated.addRenderLayer(new AutoGlowingGeoLayer(animated));
        }
        @Override public void render(BlockEntity entity,float partialTick,PoseStack pose,MultiBufferSource buffers,int light,int overlay) {
            String id=BuiltInRegistries.BLOCK.getKey(entity.getBlockState().getBlock()).getPath();
            if(entity.getBlockState().getRenderShape()==net.minecraft.world.level.block.RenderShape.ENTITYBLOCK_ANIMATED
                    && entity instanceof GeoBlockEntity && hasAnimatedAssets(id,resource->Minecraft.getInstance().getResourceManager().getResource(resource).isPresent()))
                animated.render(entity,partialTick,pose,buffers,light,overlay);
            // The chunk renderer already renders normal blockstate models,
            // including every tier controller. No duplicate cube or missing geo lookup.
        }
    }
    private ApiaryRendererRepair() {}
}
