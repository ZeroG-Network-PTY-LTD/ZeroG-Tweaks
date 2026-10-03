package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.ZGGeoMob;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

/**
 * GeckoLib renderer for ZeroG mobs whose art is geo/<id>.geo.json, animations/<id>.animation.json and
 * textures/entity/<id>.png (+ _glowmask.png). Babies draw at half size; {@link ZGGeoMob#hiddenBones()} are hidden.
 */
public class ZGGeoMobRenderer<T extends LivingEntity & GeoEntity & ZGGeoMob> extends GeoEntityRenderer<T> {
    public ZGGeoMobRenderer(EntityRendererProvider.Context context, String assetId, float shadowRadius) {
        super(context, new Model<T>(assetId));
        this.shadowRadius = shadowRadius;
        addRenderLayer(new AutoGlowingGeoLayer<>(this));
    }

    @Override
    public void render(T entity, float yaw, float partialTick, PoseStack poseStack, MultiBufferSource buffers, int light) {
        poseStack.pushPose();
        if (entity.isBaby()) poseStack.scale(0.5F, 0.5F, 0.5F);
        super.render(entity, yaw, partialTick, poseStack, buffers, light);
        poseStack.popPose();
    }

    static final class Model<T extends LivingEntity & GeoEntity & ZGGeoMob> extends GeoModel<T> {
        private final ResourceLocation model, animations, texture;

        Model(String id) {
            this.model = rl("geo/" + id + ".geo.json");
            this.animations = rl("animations/" + id + ".animation.json");
            this.texture = rl("textures/entity/" + id + ".png");
        }

        private static ResourceLocation rl(String path) {
            return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path);
        }

        @Override public ResourceLocation getModelResource(T mob) { return model; }
        @Override public ResourceLocation getAnimationResource(T mob) { return animations; }
        @Override public ResourceLocation getTextureResource(T mob) { return texture; }

        @Override
        public void setCustomAnimations(T mob, long instanceId, AnimationState<T> state) {
            super.setCustomAnimations(mob, instanceId, state);
            for (String name : mob.toggleableBones()) {
                var bone = getAnimationProcessor().getBone(name);
                if (bone != null) bone.setHidden(mob.hiddenBones().contains(name));
            }
        }
    }
}
