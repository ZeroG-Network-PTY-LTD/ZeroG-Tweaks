package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredBlock;

/** New IDs only; mature clusters and budding_cerulite keep their existing IDs. */
public final class ZGCrystalGrowth {
    private static final Map<String, DeferredBlock<? extends Block>[]> STAGES = new LinkedHashMap<>();
    private static final Map<String, DeferredBlock<? extends Block>> ITEMS = new LinkedHashMap<>();
    private static boolean initialized;
    public static DeferredBlock<ZGStarGlassBlock> STAR_GLASS;

    @SuppressWarnings("unchecked")
    public static void init() {
        if (initialized) return;
        initialized = true;
        var clusters = Map.of("cerulite", BlockInit.CERULITE_CLUSTER, "brine", BlockInit.BRINE_CRYSTAL,
                "frost", BlockInit.FROST_CRYSTAL, "prism", BlockInit.PRISM_CLUSTER);
        String[] sizes = {"small", "medium", "large"};
        int[] heights = {3, 4, 5}, offsets = {4, 3, 3}, light = {1, 2, 4};
        for (String family : new String[]{"cerulite", "brine", "frost", "prism"}) {
            DeferredBlock<? extends Block>[] stages = new DeferredBlock[4];
            for (int i = 0; i < 3; i++) {
                String id = sizes[i] + "_" + family + "_bud";
                int index = i;
                stages[i] = BlockInit.BLOCKS.register(id, () -> new AmethystClusterBlock(heights[index], offsets[index],
                        BlockBehaviour.Properties.ofFullCopy(Blocks.SMALL_AMETHYST_BUD)
                                .lightLevel(s -> light[index])));
                ITEMS.put(id, stages[i]);
            }
            stages[3] = clusters.get(family);
            STAGES.put(family, stages);
            if (!family.equals("cerulite")) {
                String id = "budding_" + family + "_crystal";
                var budding = BlockInit.BLOCKS.register(id, () -> new ZGBuddingCrystalBlock(
                        BlockBehaviour.Properties.ofFullCopy(Blocks.BUDDING_AMETHYST)
                                .pushReaction(PushReaction.DESTROY), () -> stages(family)));
                ITEMS.put(id, budding);
            }
        }
        STAR_GLASS = BlockInit.BLOCKS.register("star_glass", () -> new ZGStarGlassBlock(
                BlockBehaviour.Properties.ofFullCopy(Blocks.GLASS).strength(2.0F, 8.0F)
                        .lightLevel(s -> 12)));
        ITEMS.put("star_glass", STAR_GLASS);
        for (String planet : new String[]{"moon", "mars", "cerulon", "skarn", "eidolon", "solvane"}) {
            var sand = BlockInit.BLOCKS.register(planet + "_star_sand", () -> new net.minecraft.world.level.block.ColoredFallingBlock(
                    new net.minecraft.util.ColorRGBA(sandColour(planet)), BlockBehaviour.Properties.ofFullCopy(Blocks.SAND)));
            ITEMS.put(planet + "_star_sand", sand);
        }
    }

    public static Block[] stages(String family) {
        var entries = STAGES.get(family);
        if (entries == null) throw new IllegalArgumentException("Unknown crystal family: " + family);
        return java.util.Arrays.stream(entries).map(DeferredBlock::get).toArray(Block[]::new);
    }

    public static void registerItems() {
        ITEMS.forEach((id, block) -> ItemInit.ITEMS.register(id, () -> new BlockItem(block.get(), new net.minecraft.world.item.Item.Properties())));
        for(var colour:new ZGStarGlassBlock.Nebula[]{ZGStarGlassBlock.Nebula.BLUE,ZGStarGlassBlock.Nebula.TEAL})
            ItemInit.ITEMS.register("star_glass_"+colour.getSerializedName(),() -> new net.zerog.tweaks.item.StarGlassVariantItem(STAR_GLASS.get(),colour));
    }

    private static int sandColour(String planet) {
        return switch (planet) {
            case "moon" -> 0xFFD4D5DF;
            case "mars" -> 0xFFC77655;
            case "cerulon" -> 0xFF8EC9E0;
            case "skarn" -> 0xFF704F46;
            case "eidolon" -> 0xFFD2E6F0;
            case "solvane" -> 0xFFF5BC70;
            default -> throw new IllegalArgumentException(planet);
        };
    }

    private ZGCrystalGrowth() {}
}
