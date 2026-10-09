package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_planet_generation")
@PrefixGameTestTemplate(false)
public final class PlanetCaveEcologyGameTests {
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=100)
    public static void prismlings_accept_covered_highland_caves_not_exposed_caves(GameTestHelper helper) {
        var level=helper.getLevel();var at=helper.absolutePos(new BlockPos(7,130,7));
        var server=level.getServer();server.setDifficulty(net.minecraft.world.Difficulty.HARD,true);
        String corners=(at.getX()-4)+" "+(at.getY()-4)+" "+(at.getZ()-4)+" "+(at.getX()+4)+" "+(at.getY()+4)+" "+(at.getZ()+4);
        server.getCommands().performPrefixedCommand(server.createCommandSourceStack().withLevel(level).withPermission(4),
                "fillbiome "+corners+" zerog_tweaks:starlight_caverns");
        helper.assertTrue(level.getBiome(at).is(ZGSpawnRules.PRISMLING_CAVES),"Authored cave biome not loaded");
        for(int x=-2;x<=2;x++)for(int z=-2;z<=2;z++)for(int y=-1;y<=3;y++)
            level.setBlock(at.offset(x,y,z),(Math.abs(x)==2||Math.abs(z)==2||y==-1||y==3?Blocks.STONE:Blocks.AIR).defaultBlockState(),2);
        // Sky light updates asynchronously after placing/removing the roof.
        helper.runAfterDelay(20,()-> {
            helper.assertTrue(ZGSpawnRules.prismlingHabitat(level,at),"Covered highland cave incorrectly excluded by sea level");
            boolean accepted=false;
            for(int n=0;n<100;n++)accepted|=ZGSpawnRules.prismling(EntityInit.PRISMLING_HOLDER.get(),level,
                    net.minecraft.world.entity.MobSpawnType.NATURAL,at,net.minecraft.util.RandomSource.create(n));
            helper.assertTrue(accepted,"Natural Prismling predicate never accepts a dark covered authored cave");
            for(int y=1;y<=5;y++)level.setBlock(at.above(y),Blocks.AIR.defaultBlockState(),2);
            helper.runAfterDelay(20,()-> {
                helper.assertTrue(!ZGSpawnRules.prismlingHabitat(level,at),"Exposed high-altitude cave bypasses surface restriction");
                helper.succeed();
            });
        });
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=100)
    public static void cave_kelp_uses_sources_and_keeps_a_terminal_head(GameTestHelper helper) {
        var level=helper.getLevel();var at=helper.absolutePos(new BlockPos(2,130,2));
        for(String theme:java.util.List.of("moon","mars","cerulon","skarn","eidolon","solvane")) {
            var family=ZGPlanetAquatic.FAMILIES.get(theme);
            level.setBlock(at.below(),Blocks.STONE.defaultBlockState(),2);
            for(int n=0;n<5;n++)level.setBlock(at.above(n),Blocks.WATER.defaultBlockState(),2);
            level.setBlock(at.above(2),Blocks.WATER.defaultBlockState().setValue(LiquidBlock.LEVEL,1),2);
            helper.assertTrue(net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature.kelp(level,at,theme,5),"Source column not planted "+theme);
            helper.assertTrue(level.getBlockState(at).is(family.body().get()),"Kelp body missing "+theme);
            helper.assertTrue(level.getBlockState(at.above()).is(family.head().get()),"Shortened kelp has no head "+theme);
            helper.assertTrue(level.getBlockState(at.above(2)).is(Blocks.WATER),"Flowing water overwritten "+theme);
            level.setBlock(at,Blocks.WATER.defaultBlockState().setValue(LiquidBlock.LEVEL,1),2);
            helper.assertTrue(!net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature.kelp(level,at,theme,5),"Kelp rooted in flowing water "+theme);
            level.setBlock(at,Blocks.AIR.defaultBlockState(),2);
            helper.assertTrue(!net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature.kelp(level,at,theme,5),"Kelp planted on dry ground "+theme);
        }
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=100)
    public static void cave_wall_vines_hang_without_overwriting_obstacles(GameTestHelper helper) {
        var level=helper.getLevel();var at=helper.absolutePos(new BlockPos(5,135,5));
        for(int n=0;n<6;n++) {
            level.setBlock(at.below(n),Blocks.AIR.defaultBlockState(),2);
            level.setBlock(at.below(n).north(),Blocks.STONE.defaultBlockState(),2);
        }
        level.setBlock(at.below(3),Blocks.CHEST.defaultBlockState(),2);
        var random=net.minecraft.util.RandomSource.create(41);
        helper.assertTrue(net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature.wallVine(level,random,at,"cerulon","fruit_ivy",Direction.NORTH,5),"Supported wall strand missing");
        for(int n=0;n<3;n++)helper.assertTrue(level.getBlockState(at.below(n)).is(ZGAlienVines.VINES.get("cerulon_fruit_ivy").get()),"Wall strand interrupted");
        helper.assertTrue(level.getBlockState(at.below(3)).is(Blocks.CHEST),"Wall vine replaced a chest");
        helper.assertTrue(level.isEmptyBlock(at.below(4)),"Wall strand crossed obstacle");
        helper.assertTrue(!net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature.wallVine(level,random,at.offset(4,0,0),"cerulon","ivy",Direction.NORTH,5),"Unsupported wall strand accepted");
        helper.succeed();
    }

}
