package net.zerog.tweaks.client;

import net.minecraft.resources.ResourceLocation;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.PrismSentinel;
import software.bernie.geckolib.animation.AnimationState;
import software.bernie.geckolib.model.GeoModel;

/** Authored at full size (10.8 tall). The orbit shards hide once they break loose in phase 2. */
public final class PrismSentinelModel extends GeoModel<PrismSentinel> {
    private static final ResourceLocation MODEL = rl("geo/prism_sentinel.geo.json");
    private static final ResourceLocation ANIMATIONS = rl("animations/prism_sentinel.animation.json");
    private static final ResourceLocation TEXTURE = rl("textures/entity/prism_sentinel.png");

    static ResourceLocation rl(String path) {
        return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path);
    }

    @Override
    public ResourceLocation getModelResource(PrismSentinel mob) { return MODEL; }
    @Override
    public ResourceLocation getAnimationResource(PrismSentinel mob) { return ANIMATIONS; }
    @Override
    public ResourceLocation getTextureResource(PrismSentinel mob) { return TEXTURE; }

    @Override
    public void setCustomAnimations(PrismSentinel mob, long instanceId, AnimationState<PrismSentinel> state) {
        super.setCustomAnimations(mob, instanceId, state);
        var orbit = getAnimationProcessor().getBone("orbit");
        if (orbit != null) orbit.setHidden(mob.getPhase() >= 2);
    }
}
