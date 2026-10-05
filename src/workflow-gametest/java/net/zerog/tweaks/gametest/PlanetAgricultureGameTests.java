package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.StemBlock;
import net.minecraft.world.level.block.DoorBlock;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class PlanetAgricultureGameTests {
    private record Room(ServerLevel level,BlockPos pos) {}
    private static Room room(GameTestHelper helper,int slot){
        var level=helper.getLevel().getServer().getLevel(Level.NETHER);helper.assertTrue(level!=null,"Missing isolated Nether");
        var pos=new BlockPos(8200+slot*32,90,8200);level.getChunkAt(pos);level.setChunkForced(pos.getX()>>4,pos.getZ()>>4,true);
        for(var at:BlockPos.betweenClosed(pos.offset(-4,-2,-4),pos.offset(4,5,4))){
            boolean shell=Math.abs(at.getX()-pos.getX())==4||Math.abs(at.getZ()-pos.getZ())==4||at.getY()==pos.getY()+5||at.getY()==pos.getY()-2;
            level.setBlock(at,shell?Blocks.OBSIDIAN.defaultBlockState():Blocks.AIR.defaultBlockState(),2);
        }
        for(var at:BlockPos.betweenClosed(pos.offset(-2,-1,-2),pos.offset(2,-1,2)))level.setBlock(at,ZGDimensionTerrain.FARMLANDS.get("moon").get().defaultBlockState().setValue(FarmBlock.MOISTURE,7),2);
        return new Room(level,pos);
    }
    private static void finish(GameTestHelper helper,Room room){room.level.setChunkForced(room.pos.getX()>>4,room.pos.getZ()>>4,false);helper.succeed();}
    private static final class Roll extends net.minecraft.world.level.levelgen.LegacyRandomSource {
        final int result;int bound;
        Roll(int result){super(17);this.result=result;}
        @Override public int nextInt(int bound){this.bound=bound;return Math.floorMod(result,bound);}
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void every_custom_crop_survives_darkness_and_keeps_dry_farmland(GameTestHelper helper){
        var room=room(helper,0);var level=room.level;var pos=room.pos;
        helper.runAfterDelay(10,()->{
            helper.assertTrue(level.getRawBrightness(pos,0)==0,"Dark crop fixture is not zero-light");int count=0;
            for(var block:BuiltInRegistries.BLOCK){
                if(!(block instanceof ZGCropBlock crop))continue;count++;
                var state=crop.getStateForAge(0);level.setBlock(pos,state,2);
                helper.assertTrue(state.canSurvive(level,pos),"Custom crop dies in zero-light: "+BuiltInRegistries.BLOCK.getKey(block));
                helper.assertTrue(state.is(BlockTags.MAINTAINS_FARMLAND),"Missing dry-farmland protection: "+BuiltInRegistries.BLOCK.getKey(block));
                var miss=new Roll(1);state.randomTick(level,pos,miss);helper.assertTrue(crop.getAge(level.getBlockState(pos))==0,"Dark crop grew on missed slow roll");
                helper.assertTrue(miss.bound==ZGCropBlock.darkGrowthChance(state,level,pos)&&miss.bound%16==0,"Dark crop roll is not 16x slower");
                state.randomTick(level,pos,new Roll(0));helper.assertTrue(crop.getAge(level.getBlockState(pos))==1,"Dark crop cannot grow on accepted roll");
                level.setBlock(pos.below(),ZGDimensionTerrain.FARMLANDS.get("moon").get().defaultBlockState().setValue(FarmBlock.MOISTURE,0),2);
                for(int tick=0;tick<12;tick++)level.getBlockState(pos.below()).randomTick(level,pos.below(),RandomSource.create(tick));
                helper.assertTrue(level.getBlockState(pos.below()).getBlock() instanceof FarmBlock,"Dry soil reverted beneath custom crop");
                level.setBlock(pos.below(),Blocks.STONE.defaultBlockState(),2);helper.assertTrue(!state.canSurvive(level,pos),"Crop survives unsupported stone");
                level.setBlock(pos.below(),ZGDimensionTerrain.FARMLANDS.get("moon").get().defaultBlockState().setValue(FarmBlock.MOISTURE,7),2);
            }
            helper.assertTrue(count>=33,"Custom crop audit missed registered families");
            var wheat=Blocks.WHEAT.defaultBlockState();level.setBlock(pos,wheat,2);helper.assertTrue(!wheat.canSurvive(level,pos),"Vanilla crop dark-survival changed");
            finish(helper,room);
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void dark_gourds_grow_fruit_and_restore_stems_after_harvest(GameTestHelper helper){
        var room=room(helper,1);var level=room.level;var pos=room.pos;
        helper.runAfterDelay(10,()->{
            helper.assertTrue(level.getRawBrightness(pos,0)==0,"Dark stem fixture is not zero-light");
            for(String id:ZGAlienAgriculture.GOURD_IDS){
                for(var direction:Direction.Plane.HORIZONTAL)level.setBlock(pos.relative(direction),Blocks.AIR.defaultBlockState(),3);
                var stem=ZGAlienAgriculture.STEMS.get(id).get();helper.assertTrue(stem instanceof ZGSpaceStemBlock,"Gourd retained vanilla light-only stem "+id);
                var state=stem.defaultBlockState();level.setBlock(pos,state,3);helper.assertTrue(state.canSurvive(level,pos)&&state.is(BlockTags.MAINTAINS_FARMLAND),"Dark stem soil/survival wrong "+id);
                var miss=new Roll(1);state.randomTick(level,pos,miss);helper.assertTrue(level.getBlockState(pos).getValue(StemBlock.AGE)==0&&miss.bound%16==0,"Stem slow-growth roll wrong");
                state.randomTick(level,pos,new Roll(0));helper.assertTrue(level.getBlockState(pos).getValue(StemBlock.AGE)==1,"Dark stem cannot age");
                state=state.setValue(StemBlock.AGE,7);level.setBlock(pos,state,3);state.randomTick(level,pos,new Roll(0));
                var attached=level.getBlockState(pos);helper.assertTrue(BuiltInRegistries.BLOCK.getKey(attached.getBlock()).getPath().equals(id+"_attached_stem"),"Dark gourd cannot set fruit "+id);
                helper.assertTrue(attached.canSurvive(level,pos)&&attached.is(BlockTags.MAINTAINS_FARMLAND),"Attached dark stem dies/reverts soil");
                var facing=attached.getValue(net.minecraft.world.level.block.HorizontalDirectionalBlock.FACING);var fruit=pos.relative(facing);
                helper.assertTrue(level.getBlockState(fruit).is(ZGAlienAgriculture.GOURDS.get(id).get()),"Wrong gourd fruit");level.setBlock(fruit,Blocks.AIR.defaultBlockState(),3);
                helper.assertTrue(level.getBlockState(pos).is(stem)&&level.getBlockState(pos).getValue(StemBlock.AGE)==7,"Harvest did not restore mature stem");
            }finish(helper,room);
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void lit_custom_crops_preserve_vanilla_growth_rate(GameTestHelper helper){
        var room=room(helper,2);var level=room.level;var pos=room.pos;level.setBlock(pos.east(2),Blocks.SEA_LANTERN.defaultBlockState(),3);
        helper.runAfterDelay(15,()->{
            helper.assertTrue(level.getRawBrightness(pos,0)>=9,"Lit comparison fixture too dim");
            var crop=ZGPlanetCrops.CROPS.get("moon_millet").get();var state=crop.getStateForAge(0);level.setBlock(pos,state,2);var custom=new Roll(1);state.randomTick(level,pos,custom);
            var wheat=Blocks.WHEAT.defaultBlockState();level.setBlock(pos,wheat,2);var vanilla=new Roll(1);wheat.randomTick(level,pos,vanilla);
            helper.assertTrue(custom.bound==vanilla.bound&&custom.bound>0,"Lit custom crop changed vanilla growth probability");
            helper.assertTrue(ZGCropBlock.darkGrowthChance(state,level,pos)==custom.bound*16,"Dark multiplier does not match equivalent lit crop");finish(helper,room);
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void settlement_doors_match_all_four_surrounding_wood_families(GameTestHelper helper){
        var level=helper.getLevel();BlockPos centre=helper.absolutePos(new BlockPos(96,24,96));
        for(int x=(centre.getX()-24)>>4;x<=(centre.getX()+24)>>4;x++)for(int z=(centre.getZ()-24)>>4;z<=(centre.getZ()+24)>>4;z++)level.getChunk(x,z);
        for(String planet:new String[]{"moon","mars","cerulon","solvane"}){
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,10,22)))level.setBlock(at,Blocks.AIR.defaultBlockState(),2);
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,0,22)))level.setBlock(at,ZGDimensionTerrain.SOILS.get(planet).get().defaultBlockState(),2);
            helper.assertTrue(net.zerog.tweaks.worldgen.PlanetSettlementFeature.build(level,centre,planet,0,RandomSource.create(23)),"Settlement fixture rejected "+planet);
            String family=net.zerog.tweaks.worldgen.PlanetEcologyProfile.tree(planet);
            for(var home:net.zerog.tweaks.worldgen.PlanetSettlementFeature.homes(0)){
                var at=centre.offset(home);var lower=level.getBlockState(at.offset(0,1,4));var upper=level.getBlockState(at.offset(0,2,4));
                helper.assertTrue(BuiltInRegistries.BLOCK.getKey(lower.getBlock()).getPath().equals(family+"_door")&&upper.is(lower.getBlock()),"Door family mismatch "+planet);
                helper.assertTrue(lower.getValue(DoorBlock.HALF)==DoubleBlockHalf.LOWER&&upper.getValue(DoorBlock.HALF)==DoubleBlockHalf.UPPER,"Door halves wrong");
                helper.assertTrue(lower.canSurvive(level,at.offset(0,1,4))&&upper.canSurvive(level,at.offset(0,2,4)),"Themed door cannot survive");
                helper.assertTrue(BuiltInRegistries.BLOCK.getKey(level.getBlockState(at.offset(1,0,1)).getBlock()).getPath().equals(family+"_planks"),"Surrounding wood differs from door");
            }
        }helper.succeed();
    }
}
