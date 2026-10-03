package net.zerog.tweaks.registry;

import java.util.ArrayList;
import java.util.List;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ColoredFallingBlock;
import net.minecraft.world.level.block.DoublePlantBlock;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.util.ColorRGBA;
import net.neoforged.neoforge.registries.DeferredBlock;

/** Explicit dimension IDs, independent of the future seeded galaxy generator. */
public final class ZGDimensionTerrain {
    public static final Map<String, DeferredBlock<ZGSoilBlock>> SOILS = new LinkedHashMap<>();
    public static final Map<String, DeferredBlock<ZGFarmlandBlock>> FARMLANDS = new LinkedHashMap<>();
    public static final Map<String, DeferredBlock<ZGGrassBlock>> GRASS = new LinkedHashMap<>();
    public static final Map<String, DeferredBlock<ZGShortGrassBlock>> SHORT_GRASS = new LinkedHashMap<>();
    public static final Map<String, DeferredBlock<DoublePlantBlock>> TALL_GRASS = new LinkedHashMap<>();
    public static final Map<String, DeferredBlock<? extends Block>> FLORA = new LinkedHashMap<>();
    private static final Map<String, DeferredBlock<? extends Block>> ITEMS = new LinkedHashMap<>();
    public static List<String> dimensions() {
        var ids = new ArrayList<>(List.of("moon", "mars", "cerulon", "skarn", "eidolon", "solvane"));
        for (int galaxy = 2; galaxy <= 5; galaxy++) {
            for (int planet = 1; planet <= 6; planet++) ids.add("g" + galaxy + "_p" + planet);
            ids.add("g" + galaxy + "_moons");
        }
        return ids;
    }
    public static void init() {
        for (String id : dimensions()) {
            var soil = BlockInit.BLOCKS.register(id + "_soil", () -> new ZGSoilBlock(
                    BlockBehaviour.Properties.ofFullCopy(Blocks.DIRT), () -> FARMLANDS.get(id).get()));
            var farm = BlockInit.BLOCKS.register(id + "_farmland", () -> new ZGFarmlandBlock(
                    BlockBehaviour.Properties.ofFullCopy(Blocks.FARMLAND), soil));
            SOILS.put(id, soil);
            FARMLANDS.put(id, farm);
            ITEMS.put(id + "_soil", soil);
            ITEMS.put(id + "_farmland", farm);
            var tall = BlockInit.BLOCKS.register(id + "_tall_grass", () -> new DoublePlantBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.TALL_GRASS)));
            var shortGrass = BlockInit.BLOCKS.register(id + "_short_grass", () -> new ZGShortGrassBlock(
                    BlockBehaviour.Properties.ofFullCopy(Blocks.SHORT_GRASS), () -> tall.get()));
            var grass = BlockInit.BLOCKS.register(id + "_grass_block", () -> new ZGGrassBlock(
                    BlockBehaviour.Properties.ofFullCopy(Blocks.GRASS_BLOCK), soil, farm, shortGrass));
            GRASS.put(id, grass); SHORT_GRASS.put(id, shortGrass); TALL_GRASS.put(id, tall);
            ITEMS.put(id + "_grass_block", grass); ITEMS.put(id + "_short_grass", shortGrass); ITEMS.put(id + "_tall_grass", tall);
            // Six named-planet sands were already registered by ZGCrystalGrowth.
            if (id.startsWith("g")) ITEMS.put(id + "_star_sand", BlockInit.BLOCKS.register(id + "_star_sand",
                    () -> new ColoredFallingBlock(new ColorRGBA(0xFFB2A4B9), BlockBehaviour.Properties.ofFullCopy(Blocks.SAND))));
        }
        for (String planet : List.of("moon", "mars", "cerulon", "skarn", "eidolon", "solvane")) {
            for (String kind : List.of("glow_shrub", "glow_flower", "glow_mushroom")) {
                String id = planet + "_" + kind;
                var plant = BlockInit.BLOCKS.register(id, () -> new FlowerBlock(MobEffects.NIGHT_VISION, 5F,
                        BlockBehaviour.Properties.ofFullCopy(Blocks.DANDELION).lightLevel(s -> kind.equals("glow_mushroom") ? 6 : 4)));
                FLORA.put(id, plant); ITEMS.put(id, plant);
            }
        }
    }
    public static void registerItems() {
        ITEMS.forEach((id, block) -> ItemInit.ITEMS.register(id, () -> new BlockItem(block.get(), new Item.Properties())));
    }
    private ZGDimensionTerrain() {}
}
