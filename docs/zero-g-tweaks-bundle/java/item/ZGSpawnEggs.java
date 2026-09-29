package net.zerog.tweaks.item;

import java.util.function.Supplier;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredItem;
import net.zerog.tweaks.registry.ZGEntities;
import net.zerog.tweaks.registry.ZGItems;

/**
 * Spawn eggs for all 28 ZeroG mobs. Colours come from each mob's palette (base, spots).
 * DeferredSpawnEggItem registers its own colour handler, and the item models use
 * minecraft:item/template_spawn_egg, so no textures are needed.
 * Add them to a creative tab (e.g. the vanilla Spawn Eggs tab via BuildCreativeModeTabContentsEvent).
 */
public final class ZGSpawnEggs {
    private ZGSpawnEggs() {}

    private static DeferredItem<DeferredSpawnEggItem> egg(String id, Supplier<? extends EntityType<? extends Mob>> type, int base, int spots) {
        return ZGItems.ITEMS.register(id + "_spawn_egg", () -> new DeferredSpawnEggItem(type, base, spots, new Item.Properties()));
    }

    public static final DeferredItem<DeferredSpawnEggItem> REGOLITH_CRAWLER_SPAWN_EGG = egg("regolith_crawler", ZGEntities.REGOLITH_CRAWLER, 0x9A9AA0, 0x6FE0FF);
    public static final DeferredItem<DeferredSpawnEggItem> RUST_BEETLE_SPAWN_EGG = egg("rust_beetle", ZGEntities.RUST_BEETLE, 0x9C4424, 0xE89A62);
    public static final DeferredItem<DeferredSpawnEggItem> CRYSTAL_STAG_SPAWN_EGG = egg("crystal_stag", ZGEntities.CRYSTAL_STAG, 0x2C3D57, 0x3FC9E8);
    public static final DeferredItem<DeferredSpawnEggItem> PRISMLING_SPAWN_EGG = egg("prismling", ZGEntities.PRISMLING, 0x1592B8, 0xE8FFFF);
    public static final DeferredItem<DeferredSpawnEggItem> CINDER_HOUND_SPAWN_EGG = egg("cinder_hound", ZGEntities.CINDER_HOUND, 0x221C1A, 0xFFD070);
    public static final DeferredItem<DeferredSpawnEggItem> FROST_WARDEN_SPAWN_EGG = egg("frost_warden", ZGEntities.FROST_WARDEN, 0x5E6E74, 0x9FF0F0);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> FLARE_SPRITE_SPAWN_EGG = egg("flare_sprite", ZGEntities.FLARE_SPRITE, 0xFFA030, 0xFFF0A0);
    public static final DeferredItem<DeferredSpawnEggItem> SUN_COLOSSUS_SPAWN_EGG = egg("sun_colossus", ZGEntities.SUN_COLOSSUS, 0x7A3C1A, 0xFFF0A0);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> DUNE_BURROWER_SPAWN_EGG = egg("dune_burrower", ZGEntities.DUNE_BURROWER, 0xD8C090, 0xF0E6D0);
    public static final DeferredItem<DeferredSpawnEggItem> ASH_STRIDER_SPAWN_EGG = egg("ash_strider", ZGEntities.ASH_STRIDER, 0x1A1A1A, 0xFF8A2A);
    public static final DeferredItem<DeferredSpawnEggItem> RIME_STALKER_SPAWN_EGG = egg("rime_stalker", ZGEntities.RIME_STALKER, 0xDCE6EC, 0x7AE8FF);
    public static final DeferredItem<DeferredSpawnEggItem> BOG_LURKER_SPAWN_EGG = egg("bog_lurker", ZGEntities.BOG_LURKER, 0x4A5A3A, 0xE8FF80);
    public static final DeferredItem<DeferredSpawnEggItem> CRATER_DRIFTER_SPAWN_EGG = egg("crater_drifter", ZGEntities.CRATER_DRIFTER, 0x3A3A3A, 0xCFCFCF);
    public static final DeferredItem<DeferredSpawnEggItem> PRISM_SENTINEL_SPAWN_EGG = egg("prism_sentinel", ZGEntities.PRISM_SENTINEL, 0x3FC9E8, 0xE0DCB8);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> RIFT_TYRANT_SPAWN_EGG = egg("rift_tyrant", ZGEntities.RIFT_TYRANT, 0x2E2624, 0xB48CFF);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> EIDOLON_CAPTAIN_SPAWN_EGG = egg("eidolon_captain", ZGEntities.EIDOLON_CAPTAIN, 0x2A4050, 0xC4E0EC);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> DYING_STAR_SPAWN_EGG = egg("dying_star", ZGEntities.DYING_STAR, 0xF08A14, 0xFFF0A0);  // boss
    public static final DeferredItem<DeferredSpawnEggItem> MOON_HOPPER_SPAWN_EGG = egg("moon_hopper", ZGEntities.MOON_HOPPER, 0xECEEF2, 0xE8A0B0);
    public static final DeferredItem<DeferredSpawnEggItem> DUST_GRAZER_SPAWN_EGG = egg("dust_grazer", ZGEntities.DUST_GRAZER, 0xC4683A, 0xE8D0B0);
    public static final DeferredItem<DeferredSpawnEggItem> AZURE_FOWL_SPAWN_EGG = egg("azure_fowl", ZGEntities.AZURE_FOWL, 0x4A8AD0, 0x3FC9E8);
    public static final DeferredItem<DeferredSpawnEggItem> GLIMMERFISH_SPAWN_EGG = egg("glimmerfish", ZGEntities.GLIMMERFISH, 0x3FC9E8, 0xB0F2FF);
    public static final DeferredItem<DeferredSpawnEggItem> SLAG_BOAR_SPAWN_EGG = egg("slag_boar", ZGEntities.SLAG_BOAR, 0x3E2A20, 0x8A8A8A);
    public static final DeferredItem<DeferredSpawnEggItem> SCORCH_WYRMLING_SPAWN_EGG = egg("scorch_wyrmling", ZGEntities.SCORCH_WYRMLING, 0xE8661E, 0xFFB040);
    public static final DeferredItem<DeferredSpawnEggItem> FROST_YAK_SPAWN_EGG = egg("frost_yak", ZGEntities.FROST_YAK, 0xA6B6C0, 0x3A464C);
    public static final DeferredItem<DeferredSpawnEggItem> ICE_LEECH_SPAWN_EGG = egg("ice_leech", ZGEntities.ICE_LEECH, 0x6AD0C0, 0xD0FBFB);
    public static final DeferredItem<DeferredSpawnEggItem> GILDCRAB_SPAWN_EGG = egg("gildcrab", ZGEntities.GILDCRAB, 0xE0A010, 0xFFFFFF);
    public static final DeferredItem<DeferredSpawnEggItem> DEEP_EEL_SPAWN_EGG = egg("deep_eel", ZGEntities.DEEP_EEL, 0x5A6A7A, 0x9FF0F0);
    public static final DeferredItem<DeferredSpawnEggItem> SAND_SKITTER_SPAWN_EGG = egg("sand_skitter", ZGEntities.SAND_SKITTER, 0xC8A868, 0x8AC040);

    /** Call from your mod constructor so the class loads before registration. */
    public static void init() {}
}
