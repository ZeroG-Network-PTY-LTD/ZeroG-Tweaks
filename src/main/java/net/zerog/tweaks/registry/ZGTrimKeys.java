package net.zerog.tweaks.registry;

import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.armortrim.TrimMaterial;
import net.minecraft.world.item.armortrim.TrimPattern;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Java keys for every ZeroG armor trim, like vanilla's TrimPatterns / TrimMaterials. The trims themselves are data
 * (data/zerog_tweaks/trim_pattern/*.json and trim_material/*.json, loaded by the game like vanilla's); the smithing
 * template items are in ZGTrims. TrimRegistryGameTests checks that every key here exists in the game.
 */
public final class ZGTrimKeys {
    private ZGTrimKeys() {}

    // ---- the 10 ZeroG trim patterns -------------------------------------------------------------
    public static final ResourceKey<TrimPattern> CORONA = pattern("corona");
    public static final ResourceKey<TrimPattern> CRATER = pattern("crater");
    public static final ResourceKey<TrimPattern> FRACTURE = pattern("fracture");
    public static final ResourceKey<TrimPattern> GEODE = pattern("geode");
    public static final ResourceKey<TrimPattern> HULL = pattern("hull");
    public static final ResourceKey<TrimPattern> METEOR = pattern("meteor");
    public static final ResourceKey<TrimPattern> OLYMPUS = pattern("olympus");
    public static final ResourceKey<TrimPattern> PRISM = pattern("prism");
    public static final ResourceKey<TrimPattern> RIFT = pattern("rift");
    public static final ResourceKey<TrimPattern> SURGE = pattern("surge");

    // ---- the 20 ZeroG trim materials (each set's ingot or gem) ----------------------------------
    public static final ResourceKey<TrimMaterial> ASTRIUM = material("astrium");
    public static final ResourceKey<TrimMaterial> AURELION = material("aurelion");
    public static final ResourceKey<TrimMaterial> CERULITE = material("cerulite");
    public static final ResourceKey<TrimMaterial> COBALTIUM = material("cobaltium");
    public static final ResourceKey<TrimMaterial> CYRRIUM = material("cyrrium");
    public static final ResourceKey<TrimMaterial> EIDOLITE = material("eidolite");
    public static final ResourceKey<TrimMaterial> FERROX = material("ferrox");
    public static final ResourceKey<TrimMaterial> MOONSTEEL = material("moonsteel");
    public static final ResourceKey<TrimMaterial> NULLIFITE = material("nullifite");
    public static final ResourceKey<TrimMaterial> OLYMPIUM = material("olympium");
    public static final ResourceKey<TrimMaterial> PALLADINE = material("palladine");
    public static final ResourceKey<TrimMaterial> PHOTIUM = material("photium");
    public static final ResourceKey<TrimMaterial> PYRIUM = material("pyrium");
    public static final ResourceKey<TrimMaterial> RADIANTINE = material("radiantine");
    public static final ResourceKey<TrimMaterial> RUSKITE = material("ruskite");
    public static final ResourceKey<TrimMaterial> SALVIUM = material("salvium");
    public static final ResourceKey<TrimMaterial> SKARNITE = material("skarnite");
    public static final ResourceKey<TrimMaterial> SOLVANITE = material("solvanite");
    public static final ResourceKey<TrimMaterial> TECTIUM = material("tectium");
    public static final ResourceKey<TrimMaterial> WRAITHSTEEL = material("wraithsteel");

    public static final List<ResourceKey<TrimPattern>> ALL_PATTERNS = List.of(CORONA, CRATER, FRACTURE, GEODE, HULL, METEOR, OLYMPUS, PRISM, RIFT, SURGE);
    public static final List<ResourceKey<TrimMaterial>> ALL_MATERIALS = List.of(
            ASTRIUM, AURELION, CERULITE, COBALTIUM, CYRRIUM, EIDOLITE, FERROX, MOONSTEEL, NULLIFITE, OLYMPIUM, PALLADINE, PHOTIUM, PYRIUM, RADIANTINE, RUSKITE, SALVIUM, SKARNITE, SOLVANITE, TECTIUM, WRAITHSTEEL);

    private static ResourceKey<TrimPattern> pattern(String id) {
        return ResourceKey.create(Registries.TRIM_PATTERN, ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, id));
    }

    private static ResourceKey<TrimMaterial> material(String id) {
        return ResourceKey.create(Registries.TRIM_MATERIAL, ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, id));
    }
}
