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
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void schematic_packet_round_trips_and_rejects_unbounded_plans(GameTestHelper h){
        var centre=h.absolutePos(new BlockPos(8,4,8));
        var plan=new net.zerog.tweaks.travel.GateSchematicSync.Plan(h.getLevel().dimension().location(),centre.offset(0,1,-2),centre,Direction.NORTH.get2DDataValue(),6);
        var buf=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),h.getLevel().registryAccess());
        try {
            net.zerog.tweaks.travel.GateSchematicSync.Plan.CODEC.encode(buf,plan);
            h.assertTrue(net.zerog.tweaks.travel.GateSchematicSync.Plan.CODEC.decode(buf).equals(plan),"Schematic packet changed authoritative plan");
        } finally {buf.release();}
        boolean rejected=false;
        try {new net.zerog.tweaks.travel.GateSchematicSync.Plan(plan.dimension(),centre.offset(20,1,0),centre,0,6);}catch(IllegalArgumentException expected){rejected=true;}
        h.assertTrue(rejected,"Schematic accepted an unbounded controller footprint");h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void construction_guidance_groups_missing_blocks_by_section(GameTestHelper h){
        var level=h.getLevel();BlockPos centre=h.absolutePos(new BlockPos(8,4,8));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
        BlockPos controller=centre.offset(0,1,-2);
        h.assertTrue(SurvivalGateLayout.missingRequirements(level,controller,Direction.NORTH,1).isEmpty(),"Complete current tier reported repair requirements");
        level.setBlock(centre.offset(2,1,0),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        level.setBlock(centre.offset(-2,-1,0),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        level.setBlock(centre.offset(2,-1,0),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        var groups=SurvivalGateLayout.missingRequirements(level,controller,Direction.NORTH,1);
        h.assertTrue(groups.size()==2,"Missing requirements were not grouped by section and block");
        h.assertTrue(groups.stream().anyMatch(g->g.section().equals("Base frame — tier 1 ring")&&g.count()==2&&g.expected()==BlockInit.NULLIFITE_GATE_FRAME.get()),"Base ring count/name incorrect");
        h.assertTrue(groups.stream().anyMatch(g->g.section().equals("Service row — energy ports")&&g.count()==1&&g.expected()==BlockInit.GATE_ENERGY_PORT.get()),"Energy service diagnosis incorrect");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=1000)
    public static void all_six_tiers_in_four_facings_share_port_energy_and_revoke_removed_handlers(GameTestHelper h){
        var level=h.getLevel();int checked=0;
        for(int tier=1;tier<=6;tier++)for(Direction facing:new Direction[]{Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST}){
            BlockPos centre=h.absolutePos(new BlockPos(128+tier*24,10,128+facing.get2DDataValue()*24));
            SurvivalGateLayout.loadFootprint(level,centre.offset(SurvivalGateLayout.rotate(new BlockPos(0,1,-2),facing)),facing);
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),facing)),part.block().defaultBlockState(),3);
            BlockPos controller=centre.offset(SurvivalGateLayout.rotate(new BlockPos(0,1,-2),facing));
            level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,facing),3);
            var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);
            h.assertTrue(gate!=null&&gate.formedTier()==tier,"Wrong formed tier: "+tier+" "+facing);
            int ports=0;
            for(var part:SurvivalGateLayout.parts(tier))if(part.block()==BlockInit.GATE_ENERGY_PORT.get()){
                BlockPos pos=centre.offset(SurvivalGateLayout.rotate(part.offset(),facing));
                for(Direction side:Direction.values()){
                    var energy=level.getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,pos,side);
                    h.assertTrue(energy!=null&&energy.canReceive()&&!energy.canExtract(),"Missing receive-only port: "+tier+" "+facing+" "+side);
                    int before=gate.stored;
                    h.assertTrue(energy.receiveEnergy(7,true)==7&&gate.stored==before,"Simulation changed shared FE");
                    h.assertTrue(energy.receiveEnergy(7,false)==7&&gate.stored==before+7&&energy.getEnergyStored()==gate.stored,"Port/controller buffer diverged");
                    h.assertTrue(energy.extractEnergy(7,false)==0,"Gate port exported stored launch FE");
                }
                ports++;
            }
            h.assertTrue(ports==(tier<3?1:tier<5?2:4)&&gate.stored==ports*6*7,"Wrong number of ports or non-conserved FE");
            BlockPos removed=centre.offset(SurvivalGateLayout.rotate(new BlockPos(2,1,0),facing));
            var cached=level.getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,removed,Direction.UP);
            int before=gate.stored;level.setBlock(removed,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
            h.assertTrue(gate.formedTier()==0&&cached.receiveEnergy(7,false)==0&&gate.stored==before,"Removed required port retained cached charging");
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),facing)),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
            checked++;
        }
        h.assertTrue(checked==24,"Incomplete gate rotation matrix");h.succeed();
    }
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
