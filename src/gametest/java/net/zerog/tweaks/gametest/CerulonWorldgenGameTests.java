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

    private static boolean has(net.minecraft.world.level.biome.Biome biome, String placed) {
        return biome.getGenerationSettings().features().stream().flatMap(set -> set.stream())
                .anyMatch(f -> f.unwrapKey().map(k -> k.location().equals(rl(placed))).orElse(false));
    }
}
