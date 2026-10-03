package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ColoredFallingBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGCrystalGrowth;
import net.zerog.tweaks.registry.ZGStarGlassBlock;

/** Real random-tick and registry checks. Running requires separate game-launch approval. */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class CrystalMaterialsGameTests {
    private static Block block(String name) {
        return BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, name));
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void all_families_grow_four_waterlogged_stages(GameTestHelper helper) {
        var level = helper.getLevel();
        BlockPos root = helper.absolutePos(new BlockPos(8, 3, 8));
        for (String family : new String[]{"cerulite", "brine", "frost", "prism"}) {
            String parent = family.equals("cerulite") ? "budding_cerulite" : "budding_" + family + "_crystal";
            BlockState budding = block(parent).defaultBlockState();
            for (Direction facing : Direction.values()) {
                level.setBlockAndUpdate(root, budding);
                for (Direction d : Direction.values()) level.setBlockAndUpdate(root.relative(d), Blocks.STONE.defaultBlockState());
                BlockPos target = root.relative(facing);
                level.setBlockAndUpdate(target, Blocks.WATER.defaultBlockState());
                var random = RandomSource.create(9137);
                for (Block expected : ZGCrystalGrowth.stages(family)) {
                    Block previous = level.getBlockState(target).getBlock();
                    for (int i = 0; i < 2000 && level.getBlockState(target).is(previous); i++)
                        budding.randomTick(level, root, random);
                    BlockState grown = level.getBlockState(target);
                    helper.assertTrue(grown.is(expected), family + " growth skipped or stalled at " + facing);
                    helper.assertTrue(grown.getValue(AmethystClusterBlock.FACING) == facing, "Incorrect facing");
                    helper.assertTrue(grown.getValue(AmethystClusterBlock.WATERLOGGED), "Lost waterlogging");
                }
                // A mature crystal remains mature; it doesn't restart the sequence.
                for (int i = 0; i < 100; i++) budding.randomTick(level, root, random);
                helper.assertTrue(level.getBlockState(target).is(ZGCrystalGrowth.stages(family)[3]), "Mature cluster regressed");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void crystal_and_star_glass_light_levels(GameTestHelper helper) {
        int[] expected = {1, 2, 4, 5};
        for (String family : new String[]{"cerulite", "brine", "frost", "prism"}) {
            Block[] stages = ZGCrystalGrowth.stages(family);
            for (int i = 0; i < stages.length; i++)
                helper.assertTrue(stages[i].defaultBlockState().getLightEmission() == expected[i], "Wrong crystal light");
        }
        for (ZGStarGlassBlock.Nebula colour : ZGStarGlassBlock.Nebula.values())
            helper.assertTrue(ZGCrystalGrowth.STAR_GLASS.get().defaultBlockState()
                    .setValue(ZGStarGlassBlock.NEBULA, colour).getLightEmission() == 12, "Star Glass light must remain 12");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void six_planet_sands_are_registered_falling_blocks(GameTestHelper helper) {
        for (String planet : new String[]{"moon", "mars", "cerulon", "skarn", "eidolon", "solvane"}) {
            Block sand = block(planet + "_star_sand");
            helper.assertTrue(sand instanceof ColoredFallingBlock, planet + " sand doesn't fall");
            helper.assertTrue(sand.asItem() != net.minecraft.world.item.Items.AIR, planet + " sand has no inventory item");
        }
        helper.succeed();
    }
}
