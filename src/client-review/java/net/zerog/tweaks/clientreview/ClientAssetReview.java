package net.zerog.tweaks.clientreview;

import com.mojang.logging.LogUtils;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.renderer.texture.MissingTextureAtlasSprite;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import software.bernie.geckolib.cache.GeckoLibCache;
import software.bernie.geckolib.cache.texture.AutoGlowingTexture;

/** Opt-in isolated client resource/GPU-upload check. Not an in-world visual test. */
@EventBusSubscriber(modid = "zerog_tweaks", value = Dist.CLIENT)
public final class ClientAssetReview {
    private static boolean checked;
    private static int readyTicks;
    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath("zerog_tweaks", path);
    }
    private static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }

    @SubscribeEvent
    public static void tick(ClientTickEvent.Post event) {
        var client = Minecraft.getInstance();
        if (checked || !(client.screen instanceof TitleScreen) || client.getOverlay() != null) return;
        if (++readyTicks < 20) return;
        checked = true;
        try {
            for (String mob : new String[]{"tidewraith", "tidewraith_boss"}) {
                var model = GeckoLibCache.getBakedModels().get(id("geo/" + mob + ".geo.json"));
                require(model != null && !model.topLevelBones().isEmpty(), "Model not baked: " + mob);
                var clips = GeckoLibCache.getBakedAnimations().get(id("animations/" + mob + ".animation.json"));
                require(clips != null, "Animations not baked: " + mob);
                for (String clip : new String[]{"fly", "blink", "mouth_open"}) {
                    require(clips.getAnimation("animation.zerog_tweaks." + mob + "." + clip) != null,
                            "Required clip absent: " + mob + "." + clip);
                }
            }
            var textures = client.getTextureManager();
            for (String palette : new String[]{"tidewraith", "tidewraith_boss", "tidewraith_boss_abyssal",
                    "tidewraith_boss_pearl", "tidewraith_boss_storm"}) {
                var base = id("textures/entity/" + palette + ".png");
                require(textures.getTexture(base) != MissingTextureAtlasSprite.getTexture(), "Base PNG failed: " + palette);
                var glow = AutoGlowingTexture.getEmissiveResource(base);
                require(textures.getTexture(glow) != MissingTextureAtlasSprite.getTexture(), "Glow PNG failed: " + palette);
                textures.bindForSetup(base);
                textures.bindForSetup(glow);
            }
            LogUtils.getLogger().info("ZEROG_CLIENT_ASSET_REVIEW_PASS: 2 baked models, required flight/eye/mouth clips, "
                    + "5 base textures and 5 emissive uploads. No in-world visual approval implied.");
        } catch (Throwable failure) {
            LogUtils.getLogger().error("ZEROG_CLIENT_ASSET_REVIEW_FAIL", failure);
        } finally {
            client.stop();
        }
    }
    private ClientAssetReview() {}
}
