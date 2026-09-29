package net.zerog.tweaks.registry;

import net.minecraft.util.valueproviders.ConstantInt;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ComposterBlock;
import net.minecraft.world.level.block.grower.TreeGrower;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import net.minecraft.world.level.levelgen.feature.configurations.TreeConfiguration;
import net.minecraft.world.level.levelgen.feature.featuresize.TwoLayersFeatureSize;
import net.minecraft.world.level.levelgen.feature.foliageplacers.BlobFoliagePlacer;
import net.minecraft.world.level.levelgen.feature.foliageplacers.SpruceFoliagePlacer;
import net.minecraft.world.level.levelgen.feature.stateproviders.BlockStateProvider;
import net.minecraft.world.level.levelgen.feature.trunkplacers.StraightTrunkPlacer;

import net.zerog.tweaks.ZeroGTweaks;

/**
 * Vanilla-mechanics bootstrap for the ZeroG flora:
 * - composting (leaves + saplings fill the composter like vanilla),
 * - honeycomb waxing off (stone-family blocks stay unwaxed; no-op here),
 * - composter's COMPOSTABLES map is code-side (vanilla fills it in bootstrap).
 */
public final class ModBootstrap {
    private ModBootstrap() {}

    public static void bootstrap() {
        // composter parity: leaves 0.3, saplings 0.3 (vanilla values)
        for (var w : new String[] {"charwood", "gildwood", "hoarwood", "shardwood"}) {
            ComposterBlock.COMPOSTABLES.put(
                    BlockInit.BLOCKS.getEntries().stream()
                            .filter(h -> h.getId().getPath().equals(w + "_leaves"))
                            .findFirst().orElseThrow().value().asItem(),
                    0.3f);
            ComposterBlock.COMPOSTABLES.put(
                    BlockInit.BLOCKS.getEntries().stream()
                            .filter(h -> h.getId().getPath().equals(w + "_sapling"))
                            .findFirst().orElseThrow().value().asItem(),
                    0.3f);
        }
    }
}