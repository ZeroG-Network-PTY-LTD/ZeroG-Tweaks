package net.zerog.tweaks.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.zerog.tweaks.entity.Tidewraith;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

public final class TidewraithRenderer extends GeoEntityRenderer<Tidewraith> {
    public TidewraithRenderer(EntityRendererProvider.Context context) {
        super(context, new TidewraithModel());
        this.shadowRadius = 1;
        addRenderLayer(new AutoGlowingGeoLayer<>(this));
        // Geometry already has its authored dimensions; do not apply another scale.
    }
}
