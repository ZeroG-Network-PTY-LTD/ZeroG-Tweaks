package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.machine.CombustionBlockEntity;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.transport.TransportBlockEntity;
import net.zerog.tweaks.travel.SurvivalGateBlockEntity;
import net.zerog.tweaks.travel.SurvivalGateLayout;

@GameTestHolder("zerog_gate_power")
@PrefixGameTestTemplate(false)
public final class GatePowerGameTests {
    private static void transfer(GameTestHelper h, boolean port, boolean configured) {
        var level=h.getLevel();
        BlockPos centre=h.absolutePos(new BlockPos(8,4,8));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
        BlockPos controller=centre.offset(0,1,-2);
        level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.NORTH),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);
        h.assertTrue(gate!=null&&gate.formedTier()==1,"Fixture gate failed to form");
        BlockPos target=port?centre.offset(2,1,0):controller;
        Direction outward=port?Direction.EAST:Direction.NORTH;
        BlockPos cablePos=target.relative(outward);
        level.setBlock(cablePos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_energy_conduit")).defaultBlockState(),3);
        var cable=(TransportBlockEntity)level.getBlockEntity(cablePos);
        if(configured){cable.modes[outward.ordinal()]=2;cable.modes[outward.getOpposite().ordinal()]=1;}
        BlockPos sourcePos=cablePos.relative(outward);
        level.setBlock(sourcePos,BlockInit.COMBUSTION_GENERATOR.get().defaultBlockState(),3);
        var source=(CombustionBlockEntity)level.getBlockEntity(sourcePos);
        source.fuel.setStackInSlot(0,new ItemStack(Items.CHARCOAL,2));
        int starting=gate.stored;
        for(int i=0;i<10;i++){
            CombustionBlockEntity.tick(level,sourcePos,source.getBlockState(),source);
            TransportBlockEntity.tick(level,cablePos,cable.getBlockState(),cable);
        }
        h.assertTrue(gate.stored>starting,"No generated FE reached "+(port?"port":"controller")+": gate="+gate.stored+", generator="+source.stored+", cable="+cable.stored+", configured="+configured);
        h.assertTrue(gate.stored+source.stored+cable.stored==500,"Generated FE was lost or duplicated");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void default_conduit_charges_controller(GameTestHelper h){transfer(h,false,false);}
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void default_conduit_charges_gate_port(GameTestHelper h){transfer(h,true,false);}
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void configured_conduit_charges_controller(GameTestHelper h){transfer(h,false,true);}
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void reversed_controller_and_missing_port_are_diagnosed_without_relaxing_formation(GameTestHelper h){
        var level=h.getLevel();BlockPos centre=h.absolutePos(new BlockPos(8,4,8));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
        BlockPos controller=centre.offset(0,1,-2),port=centre.offset(2,1,0);
        level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH),3);
        level.setBlock(port,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);
        h.assertTrue(gate.formedTier()==0&&gate.energy().receiveEnergy(500,false)==0,"Malformed gate incorrectly accepted energy");
        h.assertTrue(SurvivalGateLayout.closestFacing(level,controller,Direction.SOUTH)==Direction.NORTH,"Failed to identify saved-world reversed controller");
        var missing=SurvivalGateLayout.missingParts(level,controller,Direction.NORTH,1);
        h.assertTrue(missing.size()==1&&missing.getFirst().pos().equals(port)&&missing.getFirst().expected()==BlockInit.GATE_ENERGY_PORT.get(),"Missing-port diagnosis gave wrong coordinates");
        var owner=h.makeMockServerPlayerInLevel();gate.claim(owner);
        h.assertTrue(gate.align(owner)&&gate.facing()==Direction.NORTH&&gate.formedTier()==0,"Align bypassed required energy port");
        level.setBlock(port,BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        var capability=level.getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,port,Direction.EAST);
        h.assertTrue(capability!=null&&capability.receiveEnergy(500,false)==500&&gate.stored==500,"Actual port did not charge repaired controller");
        level.setBlock(port,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        h.assertTrue(capability.receiveEnergy(100,false)==0&&gate.stored==500,"Cached port still charged after removal");
        owner.discard();h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void task_journal_marks_actual_milestones_and_hides_unvisited_worlds(GameTestHelper h){
        var player=h.makeMockServerPlayerInLevel();
        var initial=net.zerog.tweaks.item.ConcordCodexItem.checklistPages(player);
        h.assertTrue(initial.size()==1,"Fresh reader saw later planetary tasks");
        var text=(net.minecraft.network.chat.contents.TranslatableContents)initial.getFirst().raw().getContents();
        h.assertTrue(text.getArgs()[0].equals("[ ]"),"Fresh reader had a completed signal task");
        net.zerog.tweaks.lore.ConcordPrologue.grant(player,"root","has_raw_nullifite");
        var refreshed=net.zerog.tweaks.item.ConcordCodexItem.checklistPages(player);
        var updated=(net.minecraft.network.chat.contents.TranslatableContents)refreshed.getFirst().raw().getContents();
        h.assertTrue(updated.getArgs()[0].equals("[x]")&&updated.getArgs()[1].equals("[ ]"),"Task journal failed refresh or completed next task automatically");
        player.getPersistentData().putBoolean("zerog_codex_moon",true);
        h.assertTrue(net.zerog.tweaks.item.ConcordCodexItem.checklistPages(player).size()==2,"Actual Moon memory did not reveal Sol tasks");
        player.discard();h.succeed();
    }
}
