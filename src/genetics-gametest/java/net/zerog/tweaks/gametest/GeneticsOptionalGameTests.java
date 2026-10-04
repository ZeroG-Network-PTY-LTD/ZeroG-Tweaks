package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.genetics.ProductiveBeeGenes;
import net.zerog.tweaks.genetics.GeneticsRuntime;

@GameTestHolder("zerog_optional")
@PrefixGameTestTemplate(false)
public final class GeneticsOptionalGameTests {
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void ecology_density_preserves_distinct_habitats(GameTestHelper helper) {
        var dry=net.zerog.tweaks.worldgen.PlanetEcologyProfile.habitat("mars","rust_plains");
        var lush=net.zerog.tweaks.worldgen.PlanetEcologyProfile.habitat("mars","gildwood_oasis");
        var ocean=net.zerog.tweaks.worldgen.PlanetEcologyProfile.habitat("cerulon","glimmer_sea");
        helper.assertTrue(lush.treeChance()<dry.treeChance(),"Oasis lost its greater tree density");
        helper.assertTrue(lush.flowerChance()<dry.flowerChance(),"Oasis lost richer flowers");
        helper.assertTrue(ocean.treeChance()<dry.treeChance(),"Ocean planet has arid density");
        for(String dimension:net.zerog.tweaks.registry.ZGDimensionTerrain.dimensions()) {
            var habitat=net.zerog.tweaks.worldgen.PlanetEcologyProfile.habitat(dimension,"");
            helper.assertTrue(habitat.caveColumns()>32&&habitat.caveColumns()<=56,"Unbounded or unchanged cave sampling");
            helper.assertTrue(habitat.treeChance()>0&&habitat.floorChance()>0&&habitat.hangingChance()>0,"Invalid random bound");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void starts_without_productive_bees_or_addon(GameTestHelper helper) {
        helper.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("aeroapiary"),"Optional test accidentally loaded addon");
        helper.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("productivebees"),"Optional test accidentally loaded PB");
        helper.assertTrue(ProductiveBeeGenes.read(new ItemStack(Items.HONEYCOMB)).isEmpty(),"Vanilla item treated as gene specimen");
        helper.assertTrue(!ProductiveBeeGenes.valid("productivity","productivity.high"),"Missing PB API silently accepted trait");
        helper.assertTrue(GeneticsRuntime.id(null).isEmpty(),"Null machine accepted");helper.succeed();
    }
}
