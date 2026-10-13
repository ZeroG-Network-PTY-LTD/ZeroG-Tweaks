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
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void natural_vent_fields_place_three_to_six_distinct_vents(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
            net.minecraft.core.registries.Registries.DIMENSION,
            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing fixture planet");
        var centre=new BlockPos(7000,200,7000);
        for(int x=436;x<=438;x++)for(int z=436;z<=438;z++)level.getChunk(x,z);
        for(String theme:new String[]{"moon","skarn"})for(int seed=0;seed<32;seed++) {
            for(var p:BlockPos.betweenClosed(centre.offset(-8,-1,-8),new BlockPos(7008,level.getMaxBuildHeight()-1,7008)))
                level.setBlock(p,p.getY()<=200?net.minecraft.world.level.block.Blocks.STONE.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
            net.zerog.tweaks.worldgen.AmbientPlanetLandforms.place(level,RandomSource.create(seed),centre,theme,net.minecraft.world.level.block.Blocks.STONE);
            int count=0;
            for(var p:BlockPos.betweenClosed(centre.offset(-8,0,-8),centre.offset(8,5,8)))
                if(level.getBlockState(p).is(net.zerog.tweaks.registry.ZGGasVents.AMBIENT_VENTS.get(theme).get()))count++;
            helper.assertTrue(count>=3&&count<=6,"Vent field has "+count+" distinct blocks, theme="+theme+", seed="+seed);
        }
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void undersized_vent_fields_leave_terrain_and_containers_unchanged(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
            net.minecraft.core.registries.Registries.DIMENSION,
            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing fixture planet");
        var centre=new BlockPos(7064,200,7064);
        for(int x=441;x<=442;x++)for(int z=441;z<=442;z++)level.getChunk(x,z);
        for(var p:BlockPos.betweenClosed(centre.offset(-8,-1,-8),new BlockPos(7072,level.getMaxBuildHeight()-1,7072)))
            level.setBlock(p,p.getY()<=200?net.minecraft.world.level.block.Blocks.DIRT.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        level.setBlock(centre,net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),2);
        level.setBlock(centre.east(),net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),2);
        var chest=centre.north();level.setBlock(chest,net.minecraft.world.level.block.Blocks.CHEST.defaultBlockState(),2);
        var identity=level.getBlockEntity(chest);
        for(int seed=0;seed<32;seed++)net.zerog.tweaks.worldgen.AmbientPlanetLandforms.place(level,RandomSource.create(seed),centre,"moon",net.minecraft.world.level.block.Blocks.STONE);
        helper.assertTrue(level.getBlockState(centre).is(net.minecraft.world.level.block.Blocks.STONE)&&level.getBlockState(centre.east()).is(net.minecraft.world.level.block.Blocks.STONE),"Partial undersized field altered surface");
        helper.assertTrue(level.getBlockEntity(chest)==identity,"Vent field replaced protected container");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void village_tries_other_layouts_without_draining_a_blocked_home(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
                net.minecraft.core.registries.Registries.DIMENSION,
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing workflowPlanetPreset Mars");
        var centre=new BlockPos(6824,200,6824);
        for(int x=(centre.getX()-22)>>4;x<=(centre.getX()+22)>>4;x++)for(int z=(centre.getZ()-22)>>4;z<=(centre.getZ()+22)>>4;z++)level.getChunk(x,z);
        var soil=net.zerog.tweaks.registry.ZGDimensionTerrain.SOILS.get("mars").get();
        for(var at:BlockPos.betweenClosed(centre.offset(-22,-8,-22),new BlockPos(centre.getX()+22,level.getMaxBuildHeight()-1,centre.getZ()+22)))
            level.setBlock(at,at.getY()<=centre.getY()?soil.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        var pond=centre.offset(-10,0,-10);
        level.setBlock(pond,net.minecraft.world.level.block.Blocks.WATER.defaultBlockState(),2);
        helper.assertTrue(!PlanetSettlementFeature.build(level,centre,"mars",0,RandomSource.create(3)),"Wet preferred home was accepted");
        helper.assertTrue(PlanetSettlementFeature.tryLayouts(level,centre,"mars",0,RandomSource.create(3)),"Other dry layouts were never attempted");
        helper.assertTrue(level.getFluidState(pond).is(net.minecraft.world.level.material.Fluids.WATER),"Layout retry drained original pond");
        helper.assertTrue(level.getBlockState(centre).is(BlockInit.SETTLEMENT_ANCHOR.get()),"Successful alternative missing anchor");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void settlement_preserves_unused_pond_and_beehive(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
                net.minecraft.core.registries.Registries.DIMENSION,
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing workflowPlanetPreset Mars");
        var centre=new BlockPos(6728,200,6728);
        for(int x=(centre.getX()-22)>>4;x<=(centre.getX()+22)>>4;x++)for(int z=(centre.getZ()-22)>>4;z<=(centre.getZ()+22)>>4;z++)level.getChunk(x,z);
        var soil=net.zerog.tweaks.registry.ZGDimensionTerrain.SOILS.get("mars").get();
        for(var at:BlockPos.betweenClosed(centre.offset(-22,-8,-22),new BlockPos(centre.getX()+22,level.getMaxBuildHeight()-1,centre.getZ()+22)))
            level.setBlock(at,at.getY()<=centre.getY()?soil.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        var pond=centre.offset(-17,0,-11);var hive=centre.offset(-9,1,-18);
        level.setBlock(pond,net.minecraft.world.level.block.Blocks.WATER.defaultBlockState(),2);
        level.setBlock(hive,net.minecraft.world.level.block.Blocks.BEEHIVE.defaultBlockState(),2);
        var oldHive=level.getBlockEntity(hive);
        helper.assertTrue(PlanetSettlementFeature.build(level,centre,"mars",0,RandomSource.create(3)),"Unused edge pond/hive aborted the whole village");
        helper.assertTrue(level.getFluidState(pond).is(net.minecraft.world.level.material.Fluids.WATER),"Village drained unused pond");
        helper.assertTrue(level.getBlockEntity(hive)==oldHive,"Village overwrote unused beehive");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=40)
    public static void village_selects_one_dry_alternative_without_widening_spacing(GameTestHelper helper) {
        for(String planet:new String[]{"moon","cerulon","eidolon","solvane"})for(int rx=-2;rx<=2;rx++)for(int rz=-2;rz<=2;rz++) {
            var sites=PlanetSettlementFeature.searchCandidates(17,planet,rx,rz);
            helper.assertTrue(sites.size()>=3&&sites.size()<=5,"Unbounded or duplicated search");
            var base=sites.getFirst();var viable=sites.get(1);
            var selected=PlanetSettlementFeature.terrainCandidate(17,planet,rx,rz,p->p.equals(viable)?0:1);
            helper.assertTrue(selected.equals(viable),"Village discarded its only attempt instead of selecting dry alternative");
            helper.assertTrue(PlanetSettlementFeature.terrainCandidate(17,planet,rx,rz,p->0).equals(base),"Valid original site moved unnecessarily");
            helper.assertTrue(PlanetSettlementFeature.terrainCandidate(17,planet,rx,rz,p->1).equals(base),"No viable site should retain guarded legacy attempt");
            for(var site:sites)helper.assertTrue(site.x>=rx*50+16&&site.x<=rx*50+33&&site.z>=rz*50+16&&site.z<=rz*50+33,
                    "Search reduced thirty-three-chunk neighbour separation");
        }
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=40)
    public static void expanded_mines_have_long_spines_and_multiple_workings(GameTestHelper helper) {
        for(int seed=0;seed<128;seed++) {
            var plan=PlanetMineshaftFeature.plan(RandomSource.create(seed));
            helper.assertTrue(plan.getFirst().length()>=44,"Main mine spine remains only thirty blocks");
            helper.assertTrue(plan.size()>=5&&plan.size()<=7,"Missing bounded expanded workings");
            helper.assertTrue(plan.stream().mapToInt(PlanetMineshaftFeature.Corridor::length).sum()>=104,"Mine remains a small crossing");
            for(var corridor:plan)for(int t=0;t<=corridor.length();t++)for(int w=-1;w<=1;w++) {
                var at=BlockPos.ZERO.offset(8,0,8).offset(corridor.start()).relative(corridor.direction(),t)
                        .relative(corridor.direction().getClockWise(),w);
                helper.assertTrue(at.getX()>=-16&&at.getX()<=31&&at.getZ()>=-16&&at.getZ()<=31,"Mine escaped worldgen's neighbour write envelope");
                helper.assertTrue(!corridor.rails(),"Expanded mine restored rails");
            }
        }
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=40)
    public static void mine_plans_are_varied_bounded_and_seed_repeatable(GameTestHelper helper) {
        var variants=new HashSet<String>();
        for(int seed=0;seed<128;seed++) {
            var plan=PlanetMineshaftFeature.plan(RandomSource.create(seed));
            helper.assertTrue(plan.equals(PlanetMineshaftFeature.plan(RandomSource.create(seed))),"Mine plan not seed repeatable");
            helper.assertTrue(plan.size()>=5&&plan.size()<=7,"Unbounded mine branches");
            variants.add(plan.toString());
            for(var corridor:plan) for(int t=0;t<=corridor.length();t++) for(int w=-1;w<=1;w++) {
                BlockPos at=corridor.start().relative(corridor.direction(),t).relative(corridor.direction().getClockWise(),w);
                helper.assertTrue(Math.abs(at.getX())<=23&&Math.abs(at.getZ())<=23,"Mine escaped bounded footprint");
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
        for(int x=(centre.getX()-24)>>4;x<=(centre.getX()+24)>>4;x++)for(int z=(centre.getZ()-24)>>4;z<=(centre.getZ()+24)>>4;z++)level.getChunk(x,z);
        for(var at:BlockPos.betweenClosed(centre.offset(-24,-1,-24),centre.offset(24,4,24)))level.setBlock(at,BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
        // Any protected block aborts before a single corridor block changes.
        level.setBlock(centre,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),2);
        helper.assertTrue(!PlanetMineshaftFeature.build(level,centre,RandomSource.create(2)),"Mine overwrote controller");
        helper.assertTrue(level.getBlockState(centre.east()).is(BlockInit.MARTIAN_STONE.get()),"Rejected mine partially wrote terrain");
        level.setBlock(centre,BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
        helper.assertTrue(PlanetMineshaftFeature.build(level,centre,RandomSource.create(2)),"Dry underground Mars mine rejected");
        int fences=0,planks=0,chests=0;
        String family=net.zerog.tweaks.worldgen.PlanetEcologyProfile.tree("mars");
        for(var at:BlockPos.betweenClosed(centre.offset(-24,-1,-24),centre.offset(24,4,24))) {
            var state=level.getBlockState(at);String id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath();
            if(id.equals(family+"_fence"))fences++;if(id.equals(family+"_planks"))planks++;
            if(state.is(net.minecraft.world.level.block.Blocks.CHEST)) {
                chests++;
                helper.assertTrue(level.getBlockEntity(at) instanceof net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity,
                        "Mine chest has no loot container");
            }
            helper.assertTrue(!state.is(net.minecraft.tags.BlockTags.RAILS),"Planet mine generated a retired railway block");
        }
        helper.assertTrue(fences>24&&planks>200&&chests==1,"Missing expanded local timber supports or chest");helper.succeed();
    }
    @GameTest(templateNamespace="zerog_planet_generation",template="equipment_empty",timeoutTicks=1200)
    public static void settlement_accepts_gentle_slope_without_floating_foundations(GameTestHelper helper) {
        var level=helper.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(
                net.minecraft.core.registries.Registries.DIMENSION,
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(level!=null,"Missing workflowPlanetPreset Mars");
        var centre=new BlockPos(6600,200,6600);
        for(int x=(centre.getX()-22)>>4;x<=(centre.getX()+22)>>4;x++)for(int z=(centre.getZ()-22)>>4;z<=(centre.getZ()+22)>>4;z++)level.getChunk(x,z);
        var soil=net.zerog.tweaks.registry.ZGDimensionTerrain.SOILS.get("mars").get();
        for(var at:BlockPos.betweenClosed(centre.offset(-22,-8,-22),new BlockPos(centre.getX()+22,level.getMaxBuildHeight()-1,centre.getZ()+22))) {
            int ground=centre.getY()+Math.floorDiv(at.getX()-centre.getX(),3);
            level.setBlock(at,at.getY()<=ground?soil.defaultBlockState():net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        }
        level.setBlock(centre.below(6),BlockInit.GATE_CONTROLLER.get().defaultBlockState(),2);
        helper.assertTrue(!PlanetSettlementFeature.build(level,centre,"mars",0,RandomSource.create(3)),"Expanded grading overwrote deep controller");
        helper.assertTrue(level.getBlockState(centre).is(soil),"Protected rejection partially wrote colony");
        level.setBlock(centre.below(6),soil.defaultBlockState(),2);
        helper.assertTrue(PlanetSettlementFeature.build(level,centre,"mars",0,RandomSource.create(3)),"Gentle five/six-block slope rejected");
        for(int x=-17;x<=17;x++)for(int z=-17;z<=17;z++) {
            var at=centre.offset(x,-6,z);
            helper.assertTrue(level.getBlockState(at).is(soil),"Graded foundation left a floating column");
        }
        helper.succeed();
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
        for(int y=0;y<=5;y++)level.setBlock(centre.offset(10,-y,11),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        helper.assertTrue(!PlanetSettlementFeature.build(level,centre,"mars",1,RandomSource.create(3)),"Colony accepted hidden ravine");
        helper.assertTrue(level.getBlockState(centre).is(soil),"Ravine rejection partially wrote colony");
        for(int y=0;y<=5;y++)level.setBlock(centre.offset(10,-y,11),soil.defaultBlockState(),2);
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
