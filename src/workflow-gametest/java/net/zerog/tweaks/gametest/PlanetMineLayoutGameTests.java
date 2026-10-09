package net.zerog.tweaks.gametest;

import java.util.HashSet;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.util.RandomSource;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.worldgen.PlanetMineshaftFeature;
import net.zerog.tweaks.worldgen.PlanetSettlementFeature;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class PlanetMineLayoutGameTests {
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=40)
    public static void mine_plans_are_varied_bounded_and_seed_repeatable(GameTestHelper helper) {
        var variants=new HashSet<String>();
        for(int seed=0;seed<128;seed++) {
            var plan=PlanetMineshaftFeature.plan(RandomSource.create(seed));
            helper.assertTrue(plan.equals(PlanetMineshaftFeature.plan(RandomSource.create(seed))),"Mine plan not seed repeatable");
            helper.assertTrue(plan.size()>=3&&plan.size()<=5,"Unbounded mine branches");
            variants.add(plan.toString());
            for(var corridor:plan) for(int t=0;t<=corridor.length();t++) for(int w=-1;w<=1;w++) {
                BlockPos at=corridor.start().relative(corridor.direction(),t).relative(corridor.direction().getClockWise(),w);
                helper.assertTrue(Math.abs(at.getX())<=16&&Math.abs(at.getZ())<=16,"Mine escaped bounded footprint");
            }
        }
        helper.assertTrue(variants.size()>64,"Mine plans repeat one crossing");helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=40)
    public static void settlement_candidates_keep_rare_spacing_in_negative_regions(GameTestHelper helper) {
        var candidates=new com.google.gson.JsonArray();
        for(String planet:new String[]{"moon","mars","cerulon","skarn","eidolon","solvane"})
            for(int x=-3;x<=3;x++)for(int z=-3;z<=3;z++) {
                var at=PlanetSettlementFeature.candidate(17,planet,x,z);
                helper.assertTrue(at.equals(PlanetSettlementFeature.candidate(17,planet,x,z)),"Village candidate not deterministic");
                helper.assertTrue(Math.floorDiv(at.x,50)==x&&Math.floorDiv(at.z,50)==z,"Village candidate left its region");
                var east=PlanetSettlementFeature.candidate(17,planet,x+1,z);
                var south=PlanetSettlementFeature.candidate(17,planet,x,z+1);
                helper.assertTrue(east.x-at.x>=33&&south.z-at.z>=33,"Rare villages can cluster together");
                if(x>=-1&&x<=1&&z>=-1&&z<=1) {
                    var item=new com.google.gson.JsonObject();item.addProperty("dimension","zerog_tweaks:"+planet);
                    item.addProperty("regionX",x);item.addProperty("regionZ",z);
                    var seedZero=PlanetSettlementFeature.candidate(0,planet,x,z);
                    item.addProperty("chunkX",seedZero.x);item.addProperty("chunkZ",seedZero.z);candidates.add(item);
                }
            }
        try {java.nio.file.Files.writeString(java.nio.file.Path.of("planet-settlement-candidates.json"),candidates.toString());}
        catch(java.io.IOException failure){throw new RuntimeException(failure);}
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void actual_mine_uses_local_wood_and_preserves_obstructions(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
                net.minecraft.core.registries.Registries.DIMENSION,
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing workflowPlanetPreset Mars");
        var centre=new BlockPos(6408,40,6408);
        for(int x=(centre.getX()-20)>>4;x<=(centre.getX()+20)>>4;x++)for(int z=(centre.getZ()-20)>>4;z<=(centre.getZ()+20)>>4;z++)level.getChunk(x,z);
        for(var at:BlockPos.betweenClosed(centre.offset(-17,-1,-17),centre.offset(17,4,17)))level.setBlock(at,BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
        // Any protected block aborts before a single corridor block changes.
        level.setBlock(centre,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),2);
        helper.assertTrue(!PlanetMineshaftFeature.build(level,centre,RandomSource.create(2)),"Mine overwrote controller");
        helper.assertTrue(level.getBlockState(centre.east()).is(BlockInit.MARTIAN_STONE.get()),"Rejected mine partially wrote terrain");
        level.setBlock(centre,BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
        helper.assertTrue(PlanetMineshaftFeature.build(level,centre,RandomSource.create(2)),"Dry underground Mars mine rejected");
        int fences=0,planks=0,chests=0;
        String family=net.zerog.tweaks.worldgen.PlanetEcologyProfile.tree("mars");
        for(var at:BlockPos.betweenClosed(centre.offset(-17,-1,-17),centre.offset(17,4,17))) {
            var state=level.getBlockState(at);String id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath();
            if(id.equals(family+"_fence"))fences++;if(id.equals(family+"_planks"))planks++;
            if(state.is(net.minecraft.world.level.block.Blocks.CHEST)) {
                chests++;
                helper.assertTrue(level.getBlockEntity(at) instanceof net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity,
                        "Mine chest has no loot container");
            }
            if(state.is(net.minecraft.world.level.block.Blocks.RAIL)) {
                var shape=state.getValue(net.minecraft.world.level.block.RailBlock.SHAPE);
                helper.assertTrue(shape==net.minecraft.world.level.block.state.properties.RailShape.NORTH_SOUTH
                        ||shape==net.minecraft.world.level.block.state.properties.RailShape.EAST_WEST,"Mine rail shape invalid");
            }
        }
        helper.assertTrue(fences>12&&planks>80&&chests==1,"Missing local timber supports or chest");helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void settlement_grades_native_terrain_and_rejects_buried_machines(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
                net.minecraft.core.registries.Registries.DIMENSION,
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing workflowPlanetPreset Mars");
        var centre=new BlockPos(6504,200,6408);
        for(int x=(centre.getX()-22)>>4;x<=(centre.getX()+22)>>4;x++)for(int z=(centre.getZ()-22)>>4;z<=(centre.getZ()+22)>>4;z++)level.getChunk(x,z);
        var soil=net.zerog.tweaks.registry.ZGDimensionTerrain.SOILS.get("mars").get();
        for(var at:BlockPos.betweenClosed(centre.offset(-22,-5,-22),new BlockPos(centre.getX()+22,level.getMaxBuildHeight()-1,centre.getZ()+22)))
            level.setBlock(at,at.getY()<=centre.getY()?soil.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        level.setBlock(centre.below(3),BlockInit.GATE_CONTROLLER.get().defaultBlockState(),2);
        helper.assertTrue(!PlanetSettlementFeature.build(level,centre,"mars",1,RandomSource.create(3)),"Colony overwrote buried machine");
        helper.assertTrue(level.getBlockState(centre).is(soil),"Rejected colony wrote anchor");
        level.setBlock(centre.below(3),soil.defaultBlockState(),2);
        for(int y=0;y<=5;y++)level.setBlock(centre.offset(6,-y,7),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        helper.assertTrue(!PlanetSettlementFeature.build(level,centre,"mars",1,RandomSource.create(3)),"Colony accepted hidden ravine");
        helper.assertTrue(level.getBlockState(centre).is(soil),"Ravine rejection partially wrote colony");
        for(int y=0;y<=5;y++)level.setBlock(centre.offset(6,-y,7),soil.defaultBlockState(),2);
        helper.assertTrue(PlanetSettlementFeature.build(level,centre,"mars",1,RandomSource.create(3)),"Supported Mars colony rejected");
        for(var home:PlanetSettlementFeature.homes(1)) {
            var door=level.getBlockState(centre.offset(home).offset(0,1,4));
            helper.assertTrue(door.is(BlockInit.CHARWOOD_DOOR.get()),"Mars colony door mismatches local tree");
        }
        var farm=level.getBlockState(centre.offset(11,0,12));
        helper.assertTrue(farm.is(net.zerog.tweaks.registry.ZGDimensionTerrain.FARMLANDS.get("mars").get())
                &&farm.getValue(net.minecraft.world.level.block.FarmBlock.MOISTURE)==7,"Mars farm palette/moisture mismatch");
        helper.assertTrue(level.getBlockState(centre.offset(19,0,19)).is(soil),"Colony overwrote natural transition edge");
        helper.assertTrue(level.getBlockState(centre.offset(5,2,3)).is(BlockInit.ARESITE_BLOCK.get()),"Rustborn Aresite shrine lost");
        helper.succeed();
    }
}
