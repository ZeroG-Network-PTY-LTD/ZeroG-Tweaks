package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FastColor;
import net.minecraft.util.Mth;
import net.zerog.tweaks.entity.PrismSentinel;
import software.bernie.geckolib.cache.GeckoLibCache;
import software.bernie.geckolib.cache.object.BakedGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.GeoRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;
import software.bernie.geckolib.renderer.layer.GeoRenderLayer;

public final class PrismSentinelRenderer extends GeoEntityRenderer<PrismSentinel> {
    public PrismSentinelRenderer(EntityRendererProvider.Context context) {
        super(context, new PrismSentinelModel());
        this.shadowRadius = 1.8F;
        addRenderLayer(new AutoGlowingGeoLayer<>(this));
        addRenderLayer(new AuraLayer(this));
        // Geometry already has its authored dimensions; do not apply another scale.
    }

    /**
     * The crossed-plane aura (geo/prism_sentinel.aura.geo.json), drawn full-bright and translucent around the core.
     * It pulses, and flares while the core is open in phase 3. Read from the cache directly: GeoModel#getBakedModel
     * would swap the Sentinel's active model.
     */
    private static final class AuraLayer extends GeoRenderLayer<PrismSentinel> {
        private static final ResourceLocation MODEL = PrismSentinelModel.rl("geo/prism_sentinel.aura.geo.json");
        private static final ResourceLocation TEXTURE = PrismSentinelModel.rl("textures/entity/prism_sentinel_aura.png");
        private static final float CENTRE_Y = 5.4F;

        AuraLayer(GeoRenderer<PrismSentinel> renderer) { super(renderer); }

        @Override
        public void render(PoseStack poseStack, PrismSentinel mob, BakedGeoModel model, RenderType renderType,
                           MultiBufferSource buffers, VertexConsumer buffer, float partialTick, int light, int overlay) {
            BakedGeoModel aura = GeckoLibCache.getBakedModels().get(MODEL);
            if (aura == null) return;
            float t = mob.tickCount + partialTick;
            boolean flare = mob.getPhase() == 3 && mob.isCoreOpen();
            float scale = (flare ? 1.12F : 1F) + 0.05F * Mth.sin(t * 0.16F);   // the 4 s aura pulse
            int alpha = flare ? 230 : 150 + (int) (40 * Mth.sin(t * 0.16F));
            RenderType type = RenderType.entityTranslucentEmissive(TEXTURE);
            poseStack.pushPose();
            poseStack.translate(0, CENTRE_Y, 0);
            poseStack.scale(scale, scale, scale);
            poseStack.translate(0, -CENTRE_Y, 0);
            getRenderer().reRender(aura, poseStack, buffers, mob, type, buffers.getBuffer(type), partialTick,
                    LightTexture.FULL_BRIGHT, overlay, FastColor.ARGB32.color(alpha, 255, 255, 255));
            poseStack.popPose();
        }
    }
}
