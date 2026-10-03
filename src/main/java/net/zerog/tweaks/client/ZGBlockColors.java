package net.zerog.tweaks.client;

import java.util.HashMap;
import java.util.Map;
import net.minecraft.client.Minecraft;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Block;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Tints the grayscale wasteland blocks: colour = wasteland type colour x galaxy colour.
 * The galaxy comes from the current dimension id (slot dimensions named like "g3_p2" mean Galaxy 3).
 * Models already carry tintindex 0 (see models/block/parent/tinted_*.json).
 * Outside the gN_pM slot dimensions (Overworld, Moon, planets) it falls back to the Galaxy 2 colour,
 * so these blocks are never left raw grey. Glowkelp is not tinted: its texture is coloured (kelp-style).
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class ZGBlockColors {
    private ZGBlockColors() {}

    public enum WastelandType {
        OCEAN(0x7C9CB8),
        DESERT(0xE3CB94),
        VOLCANIC(0x9A7A6A),
        FROZEN(0xDDEAF2),
        TOXIC(0x98AE6A),
        CRYSTAL(0xC6AEE6),
        BARREN(0xB0ACA6);
        public final int color;
        WastelandType(int color) { this.color = color; }
    }

    /** Galaxy colours; index = galaxy number. Galaxy 1 (Sol) has no wastelands, so it falls back to Galaxy 2. */
    private static final int[] GALAXY = {0xFFFFFF, 0x9CB8F0, 0x9CB8F0, 0xF0A878, 0xC8E6F0, 0xF4D68C};

    private static final Map<String, WastelandType> BLOCKS = new HashMap<>();
    static {
        var crystals = Map.of("brine", WastelandType.OCEAN, "frost", WastelandType.FROZEN, "prism", WastelandType.CRYSTAL);
        crystals.forEach((family, tint) -> {
            BLOCKS.put("budding_" + family + "_crystal", tint);
            for (String size : new String[]{"small", "medium", "large"}) BLOCKS.put(size + "_" + family + "_bud", tint);
        });
    }
    private static void put(String id, WastelandType t) { BLOCKS.put(id, t); }
    static {
        // barren
        put("chiseled_craterstone", WastelandType.BARREN);
        put("chiseled_craterstone_slab", WastelandType.BARREN);
        put("chiseled_craterstone_stairs", WastelandType.BARREN);
        put("chiseled_craterstone_wall", WastelandType.BARREN);
        put("chiseled_polished_black_craterstone", WastelandType.BARREN);
        put("chiseled_polished_black_craterstone_slab", WastelandType.BARREN);
        put("chiseled_polished_black_craterstone_stairs", WastelandType.BARREN);
        put("chiseled_polished_black_craterstone_wall", WastelandType.BARREN);
        put("cobbled_craterstone", WastelandType.BARREN);
        put("cobbled_craterstone_slab", WastelandType.BARREN);
        put("cobbled_craterstone_stairs", WastelandType.BARREN);
        put("cobbled_craterstone_wall", WastelandType.BARREN);
        put("cracked_craterstone_brick_slab", WastelandType.BARREN);
        put("cracked_craterstone_brick_stairs", WastelandType.BARREN);
        put("cracked_craterstone_brick_wall", WastelandType.BARREN);
        put("cracked_craterstone_bricks", WastelandType.BARREN);
        put("crater_dust", WastelandType.BARREN);
        put("craterstone", WastelandType.BARREN);
        put("craterstone_brick_slab", WastelandType.BARREN);
        put("craterstone_brick_stairs", WastelandType.BARREN);
        put("craterstone_brick_wall", WastelandType.BARREN);
        put("craterstone_bricks", WastelandType.BARREN);
        put("craterstone_slab", WastelandType.BARREN);
        put("craterstone_stairs", WastelandType.BARREN);
        put("craterstone_wall", WastelandType.BARREN);
        put("meteorite_fragment", WastelandType.BARREN);
        put("polished_black_craterstone", WastelandType.BARREN);
        put("polished_black_craterstone_brick_slab", WastelandType.BARREN);
        put("polished_black_craterstone_brick_stairs", WastelandType.BARREN);
        put("polished_black_craterstone_brick_wall", WastelandType.BARREN);
        put("polished_black_craterstone_bricks", WastelandType.BARREN);
        put("polished_black_craterstone_slab", WastelandType.BARREN);
        put("polished_black_craterstone_stairs", WastelandType.BARREN);
        put("polished_black_craterstone_wall", WastelandType.BARREN);
        put("polished_craterstone", WastelandType.BARREN);
        put("polished_craterstone_slab", WastelandType.BARREN);
        put("polished_craterstone_stairs", WastelandType.BARREN);
        put("polished_craterstone_wall", WastelandType.BARREN);
        put("smooth_craterstone", WastelandType.BARREN);
        put("smooth_craterstone_slab", WastelandType.BARREN);
        put("smooth_craterstone_stairs", WastelandType.BARREN);
        put("smooth_craterstone_wall", WastelandType.BARREN);
        // crystal
        put("chiseled_polished_black_prismstone", WastelandType.CRYSTAL);
        put("chiseled_polished_black_prismstone_slab", WastelandType.CRYSTAL);
        put("chiseled_polished_black_prismstone_stairs", WastelandType.CRYSTAL);
        put("chiseled_polished_black_prismstone_wall", WastelandType.CRYSTAL);
        put("chiseled_prismstone", WastelandType.CRYSTAL);
        put("chiseled_prismstone_slab", WastelandType.CRYSTAL);
        put("chiseled_prismstone_stairs", WastelandType.CRYSTAL);
        put("chiseled_prismstone_wall", WastelandType.CRYSTAL);
        put("cobbled_prismstone", WastelandType.CRYSTAL);
        put("cobbled_prismstone_slab", WastelandType.CRYSTAL);
        put("cobbled_prismstone_stairs", WastelandType.CRYSTAL);
        put("cobbled_prismstone_wall", WastelandType.CRYSTAL);
        put("cracked_prismstone_brick_slab", WastelandType.CRYSTAL);
        put("cracked_prismstone_brick_stairs", WastelandType.CRYSTAL);
        put("cracked_prismstone_brick_wall", WastelandType.CRYSTAL);
        put("cracked_prismstone_bricks", WastelandType.CRYSTAL);
        put("polished_black_prismstone", WastelandType.CRYSTAL);
        put("polished_black_prismstone_brick_slab", WastelandType.CRYSTAL);
        put("polished_black_prismstone_brick_stairs", WastelandType.CRYSTAL);
        put("polished_black_prismstone_brick_wall", WastelandType.CRYSTAL);
        put("polished_black_prismstone_bricks", WastelandType.CRYSTAL);
        put("polished_black_prismstone_slab", WastelandType.CRYSTAL);
        put("polished_black_prismstone_stairs", WastelandType.CRYSTAL);
        put("polished_black_prismstone_wall", WastelandType.CRYSTAL);
        put("polished_prismstone", WastelandType.CRYSTAL);
        put("polished_prismstone_slab", WastelandType.CRYSTAL);
        put("polished_prismstone_stairs", WastelandType.CRYSTAL);
        put("polished_prismstone_wall", WastelandType.CRYSTAL);
        put("prism_cluster", WastelandType.CRYSTAL);
        put("prismstone", WastelandType.CRYSTAL);
        put("prismstone_brick_slab", WastelandType.CRYSTAL);
        put("prismstone_brick_stairs", WastelandType.CRYSTAL);
        put("prismstone_brick_wall", WastelandType.CRYSTAL);
        put("prismstone_bricks", WastelandType.CRYSTAL);
        put("prismstone_slab", WastelandType.CRYSTAL);
        put("prismstone_stairs", WastelandType.CRYSTAL);
        put("prismstone_wall", WastelandType.CRYSTAL);
        put("refracting_glass", WastelandType.CRYSTAL);
        put("shimmer_glass", WastelandType.CRYSTAL);
        put("shimmer_sand", WastelandType.CRYSTAL);
        put("smooth_prismstone", WastelandType.CRYSTAL);
        put("smooth_prismstone_slab", WastelandType.CRYSTAL);
        put("smooth_prismstone_stairs", WastelandType.CRYSTAL);
        put("smooth_prismstone_wall", WastelandType.CRYSTAL);
        // desert
        put("chiseled_polished_black_sunbaked_stone", WastelandType.DESERT);
        put("chiseled_polished_black_sunbaked_stone_slab", WastelandType.DESERT);
        put("chiseled_polished_black_sunbaked_stone_stairs", WastelandType.DESERT);
        put("chiseled_polished_black_sunbaked_stone_wall", WastelandType.DESERT);
        put("chiseled_sunbaked_stone", WastelandType.DESERT);
        put("chiseled_sunbaked_stone_slab", WastelandType.DESERT);
        put("chiseled_sunbaked_stone_stairs", WastelandType.DESERT);
        put("chiseled_sunbaked_stone_wall", WastelandType.DESERT);
        put("cobbled_sunbaked_stone", WastelandType.DESERT);
        put("cobbled_sunbaked_stone_slab", WastelandType.DESERT);
        put("cobbled_sunbaked_stone_stairs", WastelandType.DESERT);
        put("cobbled_sunbaked_stone_wall", WastelandType.DESERT);
        put("cracked_sunbaked_stone_brick_slab", WastelandType.DESERT);
        put("cracked_sunbaked_stone_brick_stairs", WastelandType.DESERT);
        put("cracked_sunbaked_stone_brick_wall", WastelandType.DESERT);
        put("cracked_sunbaked_stone_bricks", WastelandType.DESERT);
        put("dune_glass", WastelandType.DESERT);
        put("dunesand", WastelandType.DESERT);
        put("polished_black_sunbaked_stone", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_brick_slab", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_brick_stairs", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_brick_wall", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_bricks", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_slab", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_stairs", WastelandType.DESERT);
        put("polished_black_sunbaked_stone_wall", WastelandType.DESERT);
        put("polished_sunbaked_stone", WastelandType.DESERT);
        put("polished_sunbaked_stone_slab", WastelandType.DESERT);
        put("polished_sunbaked_stone_stairs", WastelandType.DESERT);
        put("polished_sunbaked_stone_wall", WastelandType.DESERT);
        put("ruinstone", WastelandType.DESERT);
        put("ruinstone_slab", WastelandType.DESERT);
        put("ruinstone_stairs", WastelandType.DESERT);
        put("ruinstone_wall", WastelandType.DESERT);
        put("salt_crust", WastelandType.DESERT);
        put("salt_crust_slab", WastelandType.DESERT);
        put("salt_crust_stairs", WastelandType.DESERT);
        put("salt_crust_wall", WastelandType.DESERT);
        put("smooth_sunbaked_stone", WastelandType.DESERT);
        put("smooth_sunbaked_stone_slab", WastelandType.DESERT);
        put("smooth_sunbaked_stone_stairs", WastelandType.DESERT);
        put("smooth_sunbaked_stone_wall", WastelandType.DESERT);
        put("sunbaked_stone", WastelandType.DESERT);
        put("sunbaked_stone_brick_slab", WastelandType.DESERT);
        put("sunbaked_stone_brick_stairs", WastelandType.DESERT);
        put("sunbaked_stone_brick_wall", WastelandType.DESERT);
        put("sunbaked_stone_bricks", WastelandType.DESERT);
        put("sunbaked_stone_slab", WastelandType.DESERT);
        put("sunbaked_stone_stairs", WastelandType.DESERT);
        put("sunbaked_stone_wall", WastelandType.DESERT);
        // frozen
        put("chiseled_frostrock", WastelandType.FROZEN);
        put("chiseled_frostrock_slab", WastelandType.FROZEN);
        put("chiseled_frostrock_stairs", WastelandType.FROZEN);
        put("chiseled_frostrock_wall", WastelandType.FROZEN);
        put("chiseled_polished_black_frostrock", WastelandType.FROZEN);
        put("chiseled_polished_black_frostrock_slab", WastelandType.FROZEN);
        put("chiseled_polished_black_frostrock_stairs", WastelandType.FROZEN);
        put("chiseled_polished_black_frostrock_wall", WastelandType.FROZEN);
        put("cobbled_frostrock", WastelandType.FROZEN);
        put("cobbled_frostrock_slab", WastelandType.FROZEN);
        put("cobbled_frostrock_stairs", WastelandType.FROZEN);
        put("cobbled_frostrock_wall", WastelandType.FROZEN);
        put("cracked_frostrock_brick_slab", WastelandType.FROZEN);
        put("cracked_frostrock_brick_stairs", WastelandType.FROZEN);
        put("cracked_frostrock_brick_wall", WastelandType.FROZEN);
        put("cracked_frostrock_bricks", WastelandType.FROZEN);
        put("frost_crystal", WastelandType.FROZEN);
        put("frostrock", WastelandType.FROZEN);
        put("frostrock_brick_slab", WastelandType.FROZEN);
        put("frostrock_brick_stairs", WastelandType.FROZEN);
        put("frostrock_brick_wall", WastelandType.FROZEN);
        put("frostrock_bricks", WastelandType.FROZEN);
        put("frostrock_slab", WastelandType.FROZEN);
        put("frostrock_stairs", WastelandType.FROZEN);
        put("frostrock_wall", WastelandType.FROZEN);
        put("glacial_ice", WastelandType.FROZEN);
        put("polished_black_frostrock", WastelandType.FROZEN);
        put("polished_black_frostrock_brick_slab", WastelandType.FROZEN);
        put("polished_black_frostrock_brick_stairs", WastelandType.FROZEN);
        put("polished_black_frostrock_brick_wall", WastelandType.FROZEN);
        put("polished_black_frostrock_bricks", WastelandType.FROZEN);
        put("polished_black_frostrock_slab", WastelandType.FROZEN);
        put("polished_black_frostrock_stairs", WastelandType.FROZEN);
        put("polished_black_frostrock_wall", WastelandType.FROZEN);
        put("polished_frostrock", WastelandType.FROZEN);
        put("polished_frostrock_slab", WastelandType.FROZEN);
        put("polished_frostrock_stairs", WastelandType.FROZEN);
        put("polished_frostrock_wall", WastelandType.FROZEN);
        put("smooth_frostrock", WastelandType.FROZEN);
        put("smooth_frostrock_slab", WastelandType.FROZEN);
        put("smooth_frostrock_stairs", WastelandType.FROZEN);
        put("smooth_frostrock_wall", WastelandType.FROZEN);
        put("snowpack", WastelandType.FROZEN);
        // ocean
        put("abyssal_stone", WastelandType.OCEAN);
        put("abyssal_stone_brick_slab", WastelandType.OCEAN);
        put("abyssal_stone_brick_stairs", WastelandType.OCEAN);
        put("abyssal_stone_brick_wall", WastelandType.OCEAN);
        put("abyssal_stone_bricks", WastelandType.OCEAN);
        put("abyssal_stone_slab", WastelandType.OCEAN);
        put("abyssal_stone_stairs", WastelandType.OCEAN);
        put("abyssal_stone_wall", WastelandType.OCEAN);
        put("brine_crystal", WastelandType.OCEAN);
        put("chiseled_abyssal_stone", WastelandType.OCEAN);
        put("chiseled_abyssal_stone_slab", WastelandType.OCEAN);
        put("chiseled_abyssal_stone_stairs", WastelandType.OCEAN);
        put("chiseled_abyssal_stone_wall", WastelandType.OCEAN);
        put("chiseled_polished_black_abyssal_stone", WastelandType.OCEAN);
        put("chiseled_polished_black_abyssal_stone_slab", WastelandType.OCEAN);
        put("chiseled_polished_black_abyssal_stone_stairs", WastelandType.OCEAN);
        put("chiseled_polished_black_abyssal_stone_wall", WastelandType.OCEAN);
        put("cobbled_abyssal_stone", WastelandType.OCEAN);
        put("cobbled_abyssal_stone_slab", WastelandType.OCEAN);
        put("cobbled_abyssal_stone_stairs", WastelandType.OCEAN);
        put("cobbled_abyssal_stone_wall", WastelandType.OCEAN);
        put("cracked_abyssal_stone_brick_slab", WastelandType.OCEAN);
        put("cracked_abyssal_stone_brick_stairs", WastelandType.OCEAN);
        put("cracked_abyssal_stone_brick_wall", WastelandType.OCEAN);
        put("cracked_abyssal_stone_bricks", WastelandType.OCEAN);
        put("polished_abyssal_stone", WastelandType.OCEAN);
        put("polished_abyssal_stone_slab", WastelandType.OCEAN);
        put("polished_abyssal_stone_stairs", WastelandType.OCEAN);
        put("polished_abyssal_stone_wall", WastelandType.OCEAN);
        put("polished_black_abyssal_stone", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_brick_slab", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_brick_stairs", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_brick_wall", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_bricks", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_slab", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_stairs", WastelandType.OCEAN);
        put("polished_black_abyssal_stone_wall", WastelandType.OCEAN);
        put("smooth_abyssal_stone", WastelandType.OCEAN);
        put("smooth_abyssal_stone_slab", WastelandType.OCEAN);
        put("smooth_abyssal_stone_stairs", WastelandType.OCEAN);
        put("smooth_abyssal_stone_wall", WastelandType.OCEAN);
        put("tide_glass", WastelandType.OCEAN);
        put("tidesand", WastelandType.OCEAN);
        // toxic
        put("blightmoss", WastelandType.TOXIC);
        put("chiseled_polished_black_sludgestone", WastelandType.TOXIC);
        put("chiseled_polished_black_sludgestone_slab", WastelandType.TOXIC);
        put("chiseled_polished_black_sludgestone_stairs", WastelandType.TOXIC);
        put("chiseled_polished_black_sludgestone_wall", WastelandType.TOXIC);
        put("chiseled_sludgestone", WastelandType.TOXIC);
        put("chiseled_sludgestone_slab", WastelandType.TOXIC);
        put("chiseled_sludgestone_stairs", WastelandType.TOXIC);
        put("chiseled_sludgestone_wall", WastelandType.TOXIC);
        put("cobbled_sludgestone", WastelandType.TOXIC);
        put("cobbled_sludgestone_slab", WastelandType.TOXIC);
        put("cobbled_sludgestone_stairs", WastelandType.TOXIC);
        put("cobbled_sludgestone_wall", WastelandType.TOXIC);
        put("cracked_sludgestone_brick_slab", WastelandType.TOXIC);
        put("cracked_sludgestone_brick_stairs", WastelandType.TOXIC);
        put("cracked_sludgestone_brick_wall", WastelandType.TOXIC);
        put("cracked_sludgestone_bricks", WastelandType.TOXIC);
        put("polished_black_sludgestone", WastelandType.TOXIC);
        put("polished_black_sludgestone_brick_slab", WastelandType.TOXIC);
        put("polished_black_sludgestone_brick_stairs", WastelandType.TOXIC);
        put("polished_black_sludgestone_brick_wall", WastelandType.TOXIC);
        put("polished_black_sludgestone_bricks", WastelandType.TOXIC);
        put("polished_black_sludgestone_slab", WastelandType.TOXIC);
        put("polished_black_sludgestone_stairs", WastelandType.TOXIC);
        put("polished_black_sludgestone_wall", WastelandType.TOXIC);
        put("polished_sludgestone", WastelandType.TOXIC);
        put("polished_sludgestone_slab", WastelandType.TOXIC);
        put("polished_sludgestone_stairs", WastelandType.TOXIC);
        put("polished_sludgestone_wall", WastelandType.TOXIC);
        put("sludgestone", WastelandType.TOXIC);
        put("sludgestone_brick_slab", WastelandType.TOXIC);
        put("sludgestone_brick_stairs", WastelandType.TOXIC);
        put("sludgestone_brick_wall", WastelandType.TOXIC);
        put("sludgestone_bricks", WastelandType.TOXIC);
        put("sludgestone_slab", WastelandType.TOXIC);
        put("sludgestone_stairs", WastelandType.TOXIC);
        put("sludgestone_wall", WastelandType.TOXIC);
        put("smooth_sludgestone", WastelandType.TOXIC);
        put("smooth_sludgestone_slab", WastelandType.TOXIC);
        put("smooth_sludgestone_stairs", WastelandType.TOXIC);
        put("smooth_sludgestone_wall", WastelandType.TOXIC);
        put("toxic_mud", WastelandType.TOXIC);
        // volcanic
        put("ashfall", WastelandType.VOLCANIC);
        put("chiseled_polished_black_scoria", WastelandType.VOLCANIC);
        put("chiseled_polished_black_scoria_slab", WastelandType.VOLCANIC);
        put("chiseled_polished_black_scoria_stairs", WastelandType.VOLCANIC);
        put("chiseled_polished_black_scoria_wall", WastelandType.VOLCANIC);
        put("chiseled_scoria", WastelandType.VOLCANIC);
        put("chiseled_scoria_slab", WastelandType.VOLCANIC);
        put("chiseled_scoria_stairs", WastelandType.VOLCANIC);
        put("chiseled_scoria_wall", WastelandType.VOLCANIC);
        put("cobbled_scoria", WastelandType.VOLCANIC);
        put("cobbled_scoria_slab", WastelandType.VOLCANIC);
        put("cobbled_scoria_stairs", WastelandType.VOLCANIC);
        put("cobbled_scoria_wall", WastelandType.VOLCANIC);
        put("cracked_scoria_brick_slab", WastelandType.VOLCANIC);
        put("cracked_scoria_brick_stairs", WastelandType.VOLCANIC);
        put("cracked_scoria_brick_wall", WastelandType.VOLCANIC);
        put("cracked_scoria_bricks", WastelandType.VOLCANIC);
        put("glassy_obsidian", WastelandType.VOLCANIC);
        put("polished_black_scoria", WastelandType.VOLCANIC);
        put("polished_black_scoria_brick_slab", WastelandType.VOLCANIC);
        put("polished_black_scoria_brick_stairs", WastelandType.VOLCANIC);
        put("polished_black_scoria_brick_wall", WastelandType.VOLCANIC);
        put("polished_black_scoria_bricks", WastelandType.VOLCANIC);
        put("polished_black_scoria_slab", WastelandType.VOLCANIC);
        put("polished_black_scoria_stairs", WastelandType.VOLCANIC);
        put("polished_black_scoria_wall", WastelandType.VOLCANIC);
        put("polished_scoria", WastelandType.VOLCANIC);
        put("polished_scoria_slab", WastelandType.VOLCANIC);
        put("polished_scoria_stairs", WastelandType.VOLCANIC);
        put("polished_scoria_wall", WastelandType.VOLCANIC);
        put("scoria", WastelandType.VOLCANIC);
        put("scoria_brick_slab", WastelandType.VOLCANIC);
        put("scoria_brick_stairs", WastelandType.VOLCANIC);
        put("scoria_brick_wall", WastelandType.VOLCANIC);
        put("scoria_bricks", WastelandType.VOLCANIC);
        put("scoria_slab", WastelandType.VOLCANIC);
        put("scoria_stairs", WastelandType.VOLCANIC);
        put("scoria_wall", WastelandType.VOLCANIC);
        put("smooth_scoria", WastelandType.VOLCANIC);
        put("smooth_scoria_slab", WastelandType.VOLCANIC);
        put("smooth_scoria_stairs", WastelandType.VOLCANIC);
        put("smooth_scoria_wall", WastelandType.VOLCANIC);
        put("vent_rock", WastelandType.VOLCANIC);
    }

    static int galaxyOfCurrentDimension() {
        var level = Minecraft.getInstance().level;
        if (level == null) return 2;
        String path = level.dimension().location().getPath();          // e.g. "g3_p2"
        if (path.length() > 1 && path.charAt(0) == 'g' && Character.isDigit(path.charAt(1))) return path.charAt(1) - '0';
        return 2;
    }

    static int multiply(int a, int b) {
        int r = ((a >> 16) & 0xFF) * ((b >> 16) & 0xFF) / 255;
        int g = ((a >> 8) & 0xFF) * ((b >> 8) & 0xFF) / 255;
        int bl = (a & 0xFF) * (b & 0xFF) / 255;
        return (r << 16) | (g << 8) | bl;
    }

    static int tint(WastelandType type, int galaxy) {
        int gal = GALAXY[Math.max(1, Math.min(galaxy, GALAXY.length - 1))];
        return multiply(type.color, (gal & 0xFEFEFE) / 2 + 0x808080);   // soften the galaxy colour so the type still reads
    }

    @SubscribeEvent
    public static void onBlockColors(RegisterColorHandlersEvent.Block event) {
        for (var e : BLOCKS.entrySet()) {
            Block block = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, e.getKey()));
            WastelandType type = e.getValue();
            event.register((state, level, pos, tintIndex) -> tint(type, galaxyOfCurrentDimension()), block);
        }
    }

    @SubscribeEvent
    public static void onItemColors(RegisterColorHandlersEvent.Item event) {
        for (var e : BLOCKS.entrySet()) {
            Block block = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, e.getKey()));
            WastelandType type = e.getValue();
            event.register((stack, tintIndex) -> tintIndex == 0 ? (0xFF000000 | tint(type, galaxyOfCurrentDimension())) : -1, block.asItem());
        }
    }
}
