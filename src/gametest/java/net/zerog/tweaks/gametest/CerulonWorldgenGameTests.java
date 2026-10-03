package net.zerog.tweaks.gametest;

import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.feature.configurations.GeodeConfiguration;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;

/** Cerulon worldgen rules that were broken once (owner review 2026-10-03). */
@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class CerulonWorldgenGameTests {
    private static ResourceLocation rl(String path) {
        return ResourceLocation.fromNamespaceAndPath("zerog_tweaks", path);
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void geodes_hold_no_storage_blocks(GameTestHelper helper) {
        var registry = helper.getLevel().registryAccess().registryOrThrow(Registries.CONFIGURED_FEATURE);
        var geode = registry.getOrThrow(ResourceKey.create(Registries.CONFIGURED_FEATURE, rl("cerulite_geode")));
        var blocks = ((GeodeConfiguration) geode.config()).geodeBlockSettings;
        var pos = helper.absolutePos(net.minecraft.core.BlockPos.ZERO);
        var random = helper.getLevel().random;
        for (var provider : java.util.List.of(blocks.fillingProvider, blocks.innerLayerProvider, blocks.middleLayerProvider,
                blocks.outerLayerProvider)) {
            helper.assertFalse(provider.getState(random, pos).is(BlockInit.CERULITE_BLOCK.get()),
                    "A geode layer is the Cerulite storage block (free gems)");
        }
        helper.assertTrue(blocks.alternateInnerLayerProvider.getState(random, pos).is(BlockInit.BUDDING_CERULITE.get()),
                "Budding Cerulite should line the geode so clusters grow");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void cerulon_biomes_have_their_own_vegetation(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        var shores = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("crystal_shores")));
        var grove = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("shardwood_grove")));
        var plains = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("azure_plains")));
        helper.assertFalse(has(shores, "shardwood_trees") || has(shores, "shardwood_trees_dense"), "Crystal Shores grows trees");
        helper.assertFalse(has(shores, "patch_starbloom") || has(shores, "patch_starbloom_plains"), "Crystal Shores grows Starbloom");
        helper.assertTrue(has(grove, "shardwood_trees_dense") && !has(grove, "shardwood_trees"), "The grove should be dense Shardwood");
        helper.assertTrue(has(plains, "shardwood_trees") && has(plains, "patch_starbloom_plains"),
                "The plains should have the odd tree and plenty of Starbloom");
        helper.assertTrue(has(shores, "cerulite_geode") && has(plains, "ore_cobaltium"), "Underground features should stay everywhere");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void cerulon_has_all_nine_biomes_and_no_cerulite_vein(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        for (String id : java.util.List.of("azure_plains", "shardwood_grove", "crystal_shores", "glimmer_sea", "starbloom_meadow",
                "cerulean_peaks", "concord_quarries", "starlight_caverns", "geode_depths")) {
            var biome = biomes.get(ResourceKey.create(Registries.BIOME, rl(id)));
            helper.assertTrue(biome != null, "Missing biome " + id);
            helper.assertFalse(has(biome, "ore_cerulite"), id + " still has the Cerulite ore vein (Cerulite comes from geodes)");
        }
        var caverns = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("starlight_caverns")));
        var depths = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("geode_depths")));
        helper.assertTrue(has(caverns, "lake_liquid_starlight_underground"), "Starlight Caverns need Liquid Starlight pools");
        helper.assertTrue(has(depths, "cerulite_geode_depths"), "Geode Depths need their dense geodes");
        helper.assertTrue(BlockInit.CERULITE_CLUSTER.get().defaultBlockState().is(net.minecraft.tags.TagKey.create(Registries.BLOCK,
                rl("needs_cyrrium_tool"))), "Cerulite clusters should need a Cyrrium pick (the ore used to)");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void liquid_starlight_lights_and_lifts(GameTestHelper helper) {
        var pos = new net.minecraft.core.BlockPos(8, 2, 8);
        helper.setBlock(pos, BlockInit.LIQUID_STARLIGHT.get());
        var state = helper.getBlockState(pos);
        helper.assertTrue(state.getFluidState().is(net.zerog.tweaks.registry.ZGFluids.LIQUID_STARLIGHT.get()), "Not Liquid Starlight");
        helper.assertTrue(state.getLightEmission(helper.getLevel(), helper.absolutePos(pos)) == 12, "Liquid Starlight should glow at 12");
        var pig = helper.spawn(net.minecraft.world.entity.EntityType.PIG, 8, 2, 8);
        helper.runAfterDelay(10, () -> {
            helper.assertTrue(pig.hasEffect(net.minecraft.world.effect.MobEffects.SLOW_FALLING)
                    && pig.hasEffect(net.minecraft.world.effect.MobEffects.NIGHT_VISION), "Swimming in it should give Slow Falling + Night Vision");
            helper.assertTrue(new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.LIQUID_STARLIGHT_BUCKET.get())
                    .getItem() instanceof net.minecraft.world.item.BucketItem, "Liquid Starlight bucket");
            pig.discard();
            helper.succeed();
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void cerulean_soil_grows_plants(GameTestHelper helper) {
        var soil = BlockInit.CERULEAN_SOIL.get().defaultBlockState();
        helper.assertTrue(soil.is(net.minecraft.tags.BlockTags.DIRT) && soil.is(net.minecraft.tags.BlockTags.MINEABLE_WITH_SHOVEL),
                "Cerulean Soil should be dirt (plants grow on it) and shovel-mineable");
        helper.setBlock(new net.minecraft.core.BlockPos(4, 1, 4), soil);
        helper.assertTrue(BlockInit.STARBLOOM.get().defaultBlockState().canSurvive(helper.getLevel(),
                helper.absolutePos(new net.minecraft.core.BlockPos(4, 2, 4))), "Starbloom should grow on Cerulean Soil");
        helper.succeed();
    }

    private static boolean has(net.minecraft.world.level.biome.Biome biome, String placed) {
        return biome.getGenerationSettings().features().stream().flatMap(set -> set.stream())
                .anyMatch(f -> f.unwrapKey().map(k -> k.location().equals(rl(placed))).orElse(false));
    }
}
