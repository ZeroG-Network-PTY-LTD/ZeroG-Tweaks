package net.zerog.tweaks.client;

import java.io.IOException;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.renderer.GeoRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;
import software.bernie.geckolib.resource.GeoGlowingTextureMeta;

/** Only draw GeckoLib's emissive pass when the active resource pack supplies its pixels. */
public final class OptionalGlowingGeoLayer<T extends GeoAnimatable> extends AutoGlowingGeoLayer<T> {
    public OptionalGlowingGeoLayer(GeoRenderer<T> renderer) {
        super(renderer);
    }

    @Override
    protected RenderType getRenderType(T animatable) {
        ResourceLocation base = getTextureResource(animatable);
        String path = base.getPath();
        if (!path.endsWith(".png")) return null;
        ResourceLocation mask = base.withPath(path.substring(0, path.length() - 4) + "_glowmask.png");
        var resources = Minecraft.getInstance().getResourceManager();
        if (resources.getResource(mask).isPresent()) return super.getRenderType(animatable);
        var texture = resources.getResource(base);
        if (texture.isEmpty()) return null;
        try {
            if (texture.get().metadata().getSection(GeoGlowingTextureMeta.DESERIALIZER).isPresent()) {
                return super.getRenderType(animatable);
            }
        } catch (IOException ignored) {
            // Malformed optional metadata must not hide the ordinary textured mob.
        }
        // GeckoLib 4.9.3 does not upload a glow texture without a mask or metadata,
        // but its unguarded layer still renders it. Never submit that empty pass.
        return null;
    }
}
