package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.*;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_workflow")
@PrefixGameTestTemplate(false)
public final class GateProgressionGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void mars_structures_templates_and_loot_are_live(GameTestHelper helper){
        var level=helper.getLevel();var structures=level.registryAccess().registryOrThrow(net.minecraft.core.registries.Registries.STRUCTURE);
        for(String id:new String[]{"mars_crash_site","mars_aresite_shrine"})helper.assertTrue(structures.containsKey(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id)),"Missing Mars structure "+id);
        var settings=new net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings();
        for(String id:new String[]{"mars_crash_site/wreck_a","mars_crash_site/wreck_b","mars_aresite_shrine/shrine"}){
            var template=level.getStructureManager().get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id)).orElseThrow();
            var chests=template.filterBlocks(BlockPos.ZERO,settings,Blocks.CHEST);
            helper.assertTrue(chests.size()==1,"Wrong template chest count "+id);
            helper.assertTrue(chests.get(0).nbt()!=null&&chests.get(0).nbt().getString("LootTable").equals("zerog_tweaks:chests/"+(id.startsWith("mars_crash")?"mars_crash_site":"mars_aresite_shrine")),"Wrong lore/progression loot binding "+id);
        }
        for(String id:new String[]{"mars_crash_site","mars_aresite_shrine"}){
            var table=level.getServer().reloadableRegistries().getLootTable(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.LOOT_TABLE,net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","chests/"+id)));
            helper.assertTrue(table!=net.minecraft.world.level.storage.loot.LootTable.EMPTY,"Missing Mars loot "+id);
        }helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void gate_tiers_rotate_upgrade_and_downgrade(GameTestHelper helper){
        var level=helper.getLevel();BlockPos centre=helper.absolutePos(new BlockPos(8,4,8));
        for(Direction facing:new Direction[]{Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST}){
            for(int tier=1;tier<=6;tier++){
                for(var part:SurvivalGateLayout.parts(tier))level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),facing)),part.block().defaultBlockState(),3);
                BlockPos controller=centre.offset(SurvivalGateLayout.rotate(new BlockPos(0,1,-2),facing));
                level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,facing),3);
                helper.assertTrue(SurvivalGateLayout.formedTier(level,controller,facing)==tier,"Wrong formed tier at "+tier+" "+facing);
                if(tier>1){int radius=tier+1;var part=SurvivalGateLayout.parts(tier).stream().filter(p->p.offset().equals(new BlockPos(radius,-1,0))).findFirst().orElseThrow();BlockPos at=centre.offset(SurvivalGateLayout.rotate(part.offset(),facing));level.setBlock(at,Blocks.AIR.defaultBlockState(),3);helper.assertTrue(SurvivalGateLayout.formedTier(level,controller,facing)==tier-1,"Broken outer frame did not downgrade");level.setBlock(at,part.block().defaultBlockState(),3);}
            }
            for(var part:SurvivalGateLayout.parts(6))level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),facing)),Blocks.AIR.defaultBlockState(),3);
        }helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void gate_costs_storage_filters_and_persistence(GameTestHelper helper){
        helper.assertTrue(SurvivalGateLayout.cost(500000,"minecraft:overworld","zerog_tweaks:moon",1,false)==125000,"Wrong same-galaxy cost");
        helper.assertTrue(SurvivalGateLayout.cost(1000000,"minecraft:overworld","zerog_tweaks:cerulon",2,false)==1100000,"Wrong intergalaxy passenger cost");
        helper.assertTrue(SurvivalGateLayout.cost(1000000,"minecraft:overworld","zerog_tweaks:cerulon",1,true)==800000,"Lens discount missing");
        var level=helper.getLevel();BlockPos centre=helper.absolutePos(new BlockPos(6,4,6));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
        BlockPos at=centre.offset(0,1,-2);var gate=(SurvivalGateBlockEntity)level.getBlockEntity(at);
        helper.assertTrue(gate.canReach("zerog_tweaks:moon")&&!gate.canReach("zerog_tweaks:cerulon"),"T1 routing bypassed progression");
        var energy=gate.energy();helper.assertTrue(energy.receiveEnergy(123456,true)==1000&&gate.stored==0,"Simulated FE mutated or rate missing");energy.receiveEnergy(123456,false);
        helper.assertTrue(energy.receiveEnergy(1000,false)==0,"Multiple calls bypassed per-tick charging limit");
        helper.assertTrue(energy.extractEnergy(1000,false)==0&&gate.stored==1000,"Controller leaked FE");
        var loaded=new SurvivalGateBlockEntity(at,gate.getBlockState());loaded.loadWithComponents(gate.saveWithFullMetadata(level.registryAccess()),level.registryAccess());
        helper.assertTrue(loaded.stored==1000&&loaded.countdown==0,"Saved FE or launch reset incorrect");
        var port=SurvivalGates.portEnergy(level,centre.offset(2,1,0));helper.assertTrue(port!=null,"Formed gate energy port unavailable");
        helper.succeed();
    }
}
