package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.LevelReader;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.block.entity.DispenserBlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.*;
import net.zerog.tweaks.guide.MultiblockGuides;

@GameTestHolder("zerog_hub_exhibits")
@PrefixGameTestTemplate(false)
public final class HubExhibitGameTests {
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=100)
    public static void smoker_calms_nearby_bees_without_affecting_distant_bees(GameTestHelper helper) {
        var level=helper.getLevel();
        helper.assertTrue(BuiltInRegistries.ITEM.containsKey(ResourceLocation.fromNamespaceAndPath("aeroapiary","bee_smoker")),"Existing handheld smoker missing");
        var centre=helper.absoluteVec(new net.minecraft.world.phys.Vec3(2,2,2));
        var near=net.minecraft.world.entity.EntityType.BEE.create(level);
        var far=net.minecraft.world.entity.EntityType.BEE.create(level);
        var player=helper.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        near.moveTo(centre);far.moveTo(centre.add(9,0,0));
        for(var bee:java.util.List.of(near,far)) {
            bee.setRemainingPersistentAngerTime(400);bee.setPersistentAngerTarget(player.getUUID());bee.setTarget(player);
            level.addFreshEntity(bee);
        }
        helper.assertTrue(net.zerog.tweaks.event.HandheldBeeSmoker.calm(level,centre)>=1,"Smoke reached no bees");
        helper.assertTrue(!near.isAngry()&&near.getTarget()==null&&near.getPersistentAngerTarget()==null,"Nearby bee still attacking");
        helper.assertTrue(far.isAngry()&&far.getTarget()==player,"Smoke incorrectly calmed distant bee");
        near.discard();far.discard();helper.succeed();
    }
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=400)
    public static void authored_apiaries_real_formation_and_ten_safe_room_exhibits(GameTestHelper helper) {
        var level=helper.getLevel().getServer().overworld();
        helper.assertTrue(GateLedger.get(level.getServer()).exhibitsBuilt,"Exhibits did not build with installed bee add-on");
        int index=0;
        for(var layout:MultiblockGuides.layouts()) {
            String tier=layout.id().equals("cosmic_alveary")?"tier5":layout.id().substring(0,5);
            var base=HubExhibits.designOrigin(index++);
            for(var cell:layout.cells()) {
                var id=BuiltInRegistries.BLOCK.getKey(level.getBlockState(base.offset(cell.x(),cell.y(),cell.z())).getBlock());
                helper.assertTrue(id.equals(ResourceLocation.fromNamespaceAndPath("aeroapiary",tier+"_"+cell.part())),"Wrong authored block "+layout.id()+" "+cell);
            }
            helper.assertTrue(level.getBlockEntity(base.offset(2,0,layout.maxZ()+3)) instanceof SignBlockEntity,"Missing apiary sign");
        }
        index=0;
        for(String tier:HubExhibits.VALIDATED_TIERS) {
            try {
                var base=HubExhibits.formedOrigin(index++);
                var validator=Class.forName("com.zerog.aeroapiary.AlvearyStructureValidator");
                var result=validator.getMethod("validateAt",LevelReader.class,BlockPos.class,String.class).invoke(null,level,base.offset(4,0,4),tier);
                helper.assertTrue((boolean)result.getClass().getMethod("formed").invoke(result),"Bee add-on rejected "+tier+": "+result);
                // Accepted alternate service positions, without relaxing roof or air requirements.
                var energy=base;var alternative=base.offset(4,0,0);
                var energyState=level.getBlockState(energy);var casingState=level.getBlockState(alternative);
                level.setBlock(energy,casingState,3);level.setBlock(alternative,energyState,3);
                var frame=base.offset(2,1,4);var alternateFrame=base.offset(0,1,2);
                var frameState=level.getBlockState(frame);var westState=level.getBlockState(alternateFrame);
                level.setBlock(frame,westState,3);level.setBlock(alternateFrame,frameState,3);
                var alternateResult=validator.getMethod("validateAt",LevelReader.class,BlockPos.class,String.class).invoke(null,level,base.offset(4,0,4),tier);
                helper.assertTrue((boolean)alternateResult.getClass().getMethod("formed").invoke(alternateResult),"Alternate ports/frame positions rejected "+tier);
                level.setBlock(energy,energyState,3);level.setBlock(alternative,casingState,3);
                level.setBlock(frame,frameState,3);level.setBlock(alternateFrame,westState,3);
                var roof=base.offset(0,4,0);var roofState=level.getBlockState(roof);level.setBlock(roof,casingState,3);
                var invalid=validator.getMethod("validateAt",LevelReader.class,BlockPos.class,String.class).invoke(null,level,base.offset(4,0,4),tier);
                helper.assertTrue(!(boolean)invalid.getClass().getMethod("formed").invoke(invalid),"Wrong roof accepted "+tier);
                level.setBlock(roof,roofState,3);
            } catch(ReflectiveOperationException failure) {throw new IllegalStateException(failure);}
        }
        int spawners=0,launchers=0;index=0;
        for(String room:HubExhibits.ROOMS) {
            var base=HubExhibits.roomOrigin(index++);
            helper.assertTrue(!level.getBlockState(base.offset(8,0,8)).isAir(),"Room floor absent "+room);
            helper.assertTrue(level.getBlockEntity(base.offset(8,0,19)) instanceof SignBlockEntity,"Missing room sign "+room);
            for(var pos:BlockPos.betweenClosed(base,base.offset(16,8,16))) {
                helper.assertTrue(!level.getBlockState(pos).is(Blocks.JIGSAW),"Unreplaced jigsaw in "+room);
                if(level.getBlockEntity(pos) instanceof SpawnerBlockEntity spawner) {
                    var tag=spawner.saveWithoutMetadata(level.registryAccess());
                    helper.assertTrue(tag.getShort("SpawnCount")==0 && tag.getShort("RequiredPlayerRange")==0,"Active exhibit spawner");spawners++;
                }
                if(level.getBlockEntity(pos) instanceof DispenserBlockEntity launcher) {helper.assertTrue(launcher.isEmpty(),"Loaded trap launcher");launchers++;}
            }
        }
        helper.assertTrue(spawners>0 && launchers>0,"Spawner/trap inspection fixtures missing");
        var check=HubExhibits.designOrigin(0).offset(0,10,0);level.setBlock(check,Blocks.DIAMOND_BLOCK.defaultBlockState(),3);
        helper.assertTrue(HubExhibits.build(level).contains("already built"),"Exhibits not idempotent");
        helper.assertTrue(level.getBlockState(check).is(Blocks.DIAMOND_BLOCK),"Player modification overwritten");level.setBlock(check,Blocks.AIR.defaultBlockState(),3);
        helper.succeed();
    }
}
