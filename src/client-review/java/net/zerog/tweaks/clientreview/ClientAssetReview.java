package net.zerog.tweaks.clientreview;

import com.mojang.logging.LogUtils;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.renderer.texture.MissingTextureAtlasSprite;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import software.bernie.geckolib.cache.GeckoLibCache;
import software.bernie.geckolib.cache.texture.AutoGlowingTexture;
import net.zerog.tweaks.client.MultiblockGuideScreen;
import net.zerog.tweaks.guide.MultiblockGuides;

/** Opt-in isolated client resource/GPU-upload check. Not an in-world visual test. */
@EventBusSubscriber(modid = "zerog_tweaks", value = Dist.CLIENT)
public final class ClientAssetReview {
    private static boolean checked;
    private static int readyTicks;
    private static boolean reviewingGuide;
    private static int guidePose;
    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath("zerog_tweaks", path);
    }
    private static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }

    @SubscribeEvent
    public static void tick(ClientTickEvent.Post event) {
        var client = Minecraft.getInstance();
        if (reviewingGuide) {
            if (++readyTicks < 5) return;
            readyTicks=0;
            try {
                require(client.screen instanceof MultiblockGuideScreen, "Guide screen closed during review");
                var guide=(MultiblockGuideScreen)client.screen;
                require(guide.renderedFaces()>0, "No multiblock reference geometry rendered");
                if (++guidePose==32) {
                    LogUtils.getLogger().info("ZEROG_MULTIBLOCK_GUIDE_REVIEW_PASS: 32 quarter-turn/layer poses across all eight layouts rendered; "
                            + "authored guide only, no formation or pixel-approval claim.");
                    reviewingGuide=false;client.stop();return;
                }
                int layoutIndex=guidePose/4;
                guide.reviewLayout(layoutIndex);
                boolean through=guidePose%4!=3;
                guide.reviewPose((guidePose%4)*90,through ? MultiblockGuides.layouts().get(layoutIndex).maxY() : 0,through);
            } catch(Throwable failure) {
                LogUtils.getLogger().error("ZEROG_MULTIBLOCK_GUIDE_REVIEW_FAIL",failure);
                reviewingGuide=false;client.stop();
            }
            return;
        }
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
            reviewMoonsteel(client);
            var guide=new MultiblockGuideScreen();
            client.setScreen(guide);
            guide.reviewPose(0,MultiblockGuides.layouts().getFirst().maxY(),true);
            reviewingGuide=true;readyTicks=0;
        } catch (Throwable failure) {
            LogUtils.getLogger().error("ZEROG_CLIENT_ASSET_REVIEW_FAIL", failure);
            client.stop();
        }
    }
    /**
     * Moonsteel: every 3D tool must bake to real geometry with real sprites (a cube model whose parent chain
     * reaches builtin/generated is rebuilt from layer0..4 and silently bakes to nothing), and the GeckoLib
     * armor model and its glowmask must load.
     */
    private static void reviewMoonsteel(Minecraft client) {
        var random = RandomSource.create(42);
        var missing = MissingTextureAtlasSprite.getLocation();
        int quads = 0;
        for (String tool : new String[]{"sword", "pickaxe", "axe", "shovel", "hoe"}) {
            var item = BuiltInRegistries.ITEM.get(id("moonsteel_" + tool));
            var model = client.getItemRenderer().getModel(new ItemStack(item), null, null, 0);
            var toolQuads = model.getQuads(null, null, random);
            require(!toolQuads.isEmpty(), "Moonsteel " + tool + " baked to no geometry (invisible item)");
            for (var quad : toolQuads) {
                require(!quad.getSprite().contents().name().equals(missing), "Moonsteel " + tool + " uses the missing texture");
            }
            quads += toolQuads.size();
        }
        var armor = GeckoLibCache.getBakedModels().get(id("geo/item/armor/moonsteel.geo.json"));
        require(armor != null && !armor.topLevelBones().isEmpty(), "Moonsteel armor GeckoLib model not baked");
        var textures = client.getTextureManager();
        var armorTexture = id("textures/item/armor/moonsteel.png");
        require(textures.getTexture(armorTexture) != MissingTextureAtlasSprite.getTexture(), "Moonsteel armor texture failed");
        require(textures.getTexture(AutoGlowingTexture.getEmissiveResource(armorTexture)) != MissingTextureAtlasSprite.getTexture(),
                "Moonsteel armor glowmask failed");
        LogUtils.getLogger().info("ZEROG_MOONSTEEL_REVIEW_PASS: 5 tool models baked ({} quads, no missing sprites), "
                + "GeckoLib armor model, texture and glowmask loaded.", quads);
    }

    private ClientAssetReview() {}
}
