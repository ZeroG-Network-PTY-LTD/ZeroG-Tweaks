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

/**
 * GeckoLib renderer for ZeroG mobs whose art is geo/<id>.geo.json, animations/<id>.animation.json and
 * textures/entity/<id>.png (+ _glowmask.png). Babies draw at half size; {@link ZGGeoMob#hiddenBones()} are hidden.
 * A mob can switch art sets per instance with {@link ZGGeoMob#assetId(String)} (styles).
 */
public class ZGGeoMobRenderer<T extends LivingEntity & GeoEntity & ZGGeoMob> extends GeoEntityRenderer<T> {
    public ZGGeoMobRenderer(EntityRendererProvider.Context context, String assetId, float shadowRadius) {
        super(context, new Model<T>(assetId));
        this.shadowRadius = shadowRadius;
        addRenderLayer(new OptionalGlowingGeoLayer<>(this));
    }

    @Override
    public void render(T entity, float yaw, float partialTick, PoseStack poseStack, MultiBufferSource buffers, int light) {
        poseStack.pushPose();
        if (entity.isBaby()) poseStack.scale(0.5F, 0.5F, 0.5F);
        super.render(entity, yaw, partialTick, poseStack, buffers, light);
        poseStack.popPose();
    }

    static final class Model<T extends LivingEntity & GeoEntity & ZGGeoMob> extends GeoModel<T> {
        private final String base;
        private final java.util.Map<String, ResourceLocation[]> sets = new java.util.HashMap<>();

        Model(String id) {
            this.base = id;
        }

        /** [model, animations, texture] for the mob's current art set; "namespace:id" draws from another namespace. */
        private ResourceLocation[] set(T mob) {
            return sets.computeIfAbsent(mob.assetId(base), key -> {
                int colon = key.indexOf(':');
                String ns = colon < 0 ? ZeroGTweaks.MODID : key.substring(0, colon), id = key.substring(colon + 1);
                return new ResourceLocation[] {rl(ns, "geo/" + id + ".geo.json"),
                        rl(ns, "animations/" + id + ".animation.json"), rl(ns, "textures/entity/" + id + ".png")};
            });
        }

        private static ResourceLocation rl(String namespace, String path) {
            return ResourceLocation.fromNamespaceAndPath(namespace, path);
        }

        @Override public ResourceLocation getModelResource(T mob) { return set(mob)[0]; }
        @Override public ResourceLocation getAnimationResource(T mob) { return set(mob)[1]; }
        @Override public ResourceLocation getTextureResource(T mob) { return set(mob)[2]; }

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
