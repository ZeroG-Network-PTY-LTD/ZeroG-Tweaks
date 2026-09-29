package net.zerog.tweaks.registry;

import java.util.Optional;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;

import net.zerog.tweaks.ZeroGTweaks;

/**
 * The four ZeroG species TreeGrowers. ConfiguredFeatures are DATAPACK-side
 * (vanilla convention: data/<ns>/worldgen/configured_feature/*.json);
 * TreeGrower looks the key up at grow time. Saplings keep the vanilla
 * STAGE/randomTick/bonemeal cycle and support rules.
 */
public final class ZGTreeGrowers {

    private static TreeGrower grower(String name) {
        ResourceKey<ConfiguredFeature<?, ?>> key = ResourceKey.create(
                Registries.CONFIGURED_FEATURE,
                ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, name));
        return new TreeGrower(name,
                Optional.empty(),        // mega tree
                Optional.of(key),        // tree
                Optional.empty());       // flowers (beehive)
    }

    public static final TreeGrower CHARWOOD = grower("charwood_tree");
    public static final TreeGrower GILDWOOD = grower("gildwood_tree");
    public static final TreeGrower HOARWOOD = grower("hoarwood_tree");
    public static final TreeGrower SHARDWOOD = grower("shardwood_tree");

    private ZGTreeGrowers() {}
}