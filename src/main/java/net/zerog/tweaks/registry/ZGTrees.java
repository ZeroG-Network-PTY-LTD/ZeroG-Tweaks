package net.zerog.tweaks.registry;

import java.util.Optional;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Tree growers for the four ZeroG saplings. Each points at the matching
 * configured feature in data/zerog_tweaks/worldgen/configured_feature/<wood>_tree.json,
 * the same trees that generate naturally on the planets.
 */
public final class ZGTrees {
    private ZGTrees() {}

    private static ResourceKey<ConfiguredFeature<?, ?>> key(String name) {
        return ResourceKey.create(Registries.CONFIGURED_FEATURE, ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, name));
    }

    private static TreeGrower grower(String wood) {
        return new TreeGrower(ZeroGTweaks.MODID + "_" + wood, Optional.empty(), Optional.of(key(wood + "_tree")), Optional.empty());
    }

    public static final TreeGrower CHARWOOD = grower("charwood");
    public static final TreeGrower GILDWOOD = grower("gildwood");
    public static final TreeGrower HOARWOOD = grower("hoarwood");
    public static final TreeGrower SHARDWOOD = grower("shardwood");
}
