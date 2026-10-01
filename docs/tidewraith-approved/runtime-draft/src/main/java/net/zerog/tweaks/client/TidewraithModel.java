package net.zerog.tweaks.client;

import net.minecraft.resources.ResourceLocation;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.Tidewraith;
import software.bernie.geckolib.model.GeoModel;

public final class TidewraithModel extends GeoModel<Tidewraith> {
    private ResourceLocation resource(String path) {
        return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path);
    }

    @Override
    public ResourceLocation getModelResource(Tidewraith mob) {
        return resource("geo/" + mob.assetId() + ".geo.json");
    }

    @Override
    public ResourceLocation getAnimationResource(Tidewraith mob) {
        return resource("animations/" + mob.assetId() + ".animation.json");
    }

    @Override
    public ResourceLocation getTextureResource(Tidewraith mob) {
        String style = "";
        if (mob.isBoss()) style = switch (mob.getVariant()) {
            case 1 -> "_abyssal";
            case 2 -> "_pearl";
            case 3 -> "_storm";
            default -> "";
        };
        return resource("textures/entity/" + mob.assetId() + style + ".png");
    }
}
