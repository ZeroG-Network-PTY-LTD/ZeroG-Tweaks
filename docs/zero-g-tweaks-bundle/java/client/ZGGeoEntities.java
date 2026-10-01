package net.zerog.tweaks.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Entity;
import net.zerog.tweaks.ZeroGTweaks;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

/**
 * One generic model + renderer for every ZeroG mob (GeckoLib 4.x, NeoForge 1.21.1).
 * Files it expects, all included in resources/:
 *   geo/<id>.geo.json, animations/<id>.animation.json,
 *   textures/entity/<id>.png and (optional) textures/entity/<id>_glowmask.png
 * Explicit resource overrides below avoid relying on a different GeckoLib version's default folders.
 *
 * Register in EntityRenderersEvent.RegisterRenderers, e.g.
 *   event.registerEntityRenderer(ZGEntities.MOON_HOPPER.get(), ctx -> new ZGGeoEntities.Renderer<>(ctx, "moon_hopper", true));
 *
 * In each entity (implements GeoEntity):
 *   private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
 *   private static final RawAnimation IDLE = RawAnimation.begin().thenLoop("animation.zerog_tweaks.moon_hopper.idle");
 *   private static final RawAnimation WALK = RawAnimation.begin().thenLoop("animation.zerog_tweaks.moon_hopper.walk");
 *   @Override public void registerControllers(AnimatableManager.ControllerRegistrar c) {
 *       c.add(new AnimationController<>(this, "main", 5, s -> s.setAndContinue(s.isMoving() ? WALK : IDLE)));
 *   }
 *   @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
 */
public final class ZGGeoEntities {
    private ZGGeoEntities() {}

    public static class Model<T extends GeoAnimatable> extends DefaultedEntityGeoModel<T> {
        private final String id;
        public Model(String id) {
            super(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, id), true);
            this.id = id;
        }
        @Override public ResourceLocation getModelResource(T animatable) {
            return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "geo/" + id + ".geo.json");
        }
        @Override public ResourceLocation getAnimationResource(T animatable) {
            return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "animations/" + id + ".animation.json");
        }
        @Override public ResourceLocation getTextureResource(T animatable) {
            return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "textures/entity/" + id + ".png");
        }
    }

    public static class Renderer<T extends Entity & GeoAnimatable> extends GeoEntityRenderer<T> {
        public Renderer(EntityRendererProvider.Context ctx, String id, boolean glowmask) {
            super(ctx, new Model<>(id));
            if (glowmask) addRenderLayer(new AutoGlowingGeoLayer<>(this));
        }
    }
}
