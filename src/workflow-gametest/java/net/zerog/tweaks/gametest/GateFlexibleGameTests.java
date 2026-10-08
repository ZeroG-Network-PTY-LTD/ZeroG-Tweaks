package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.travel.SurvivalGateBlockEntity;
import net.zerog.tweaks.travel.SurvivalGateLayout;

@GameTestHolder("zerog_gate_flexible")
@PrefixGameTestTemplate(false)
public final class GateFlexibleGameTests {
    private static final Direction[] SIDES={Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST};
    private static void place(GameTestHelper h,BlockPos centre,int tier,Direction structure){
        var level=h.getLevel();SurvivalGateLayout.loadFootprint(level,centre.offset(0,1,-2),Direction.NORTH);
        for(var part:SurvivalGateLayout.parts(tier)){
            if(part.block()==BlockInit.GATE_CONTROLLER.get()||part.block()==BlockInit.GATE_ENERGY_PORT.get())continue;
            level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),structure)),part.block().defaultBlockState(),3);
        }
    }
    @GameTest(templateNamespace="zerog_gate_flexible",template="equipment_empty",timeoutTicks=2000)
    public static void controllers_and_ports_move_independently_on_all_sides_and_tiers(GameTestHelper h){
        matrixFixture(h,0,new int[]{0});
    }
    private static void matrixFixture(GameTestHelper h,int index,int[] checked){
        if(index==24){h.assertTrue(checked[0]==384,"Incomplete independent service-placement matrix");h.succeed();return;}
        var level=h.getLevel();int tier=index/4+1;Direction structure=SIDES[index%4];
            BlockPos centre=h.absolutePos(new BlockPos(128+tier*24,10,128+structure.get2DDataValue()*24));
            place(h,centre,tier,structure);int radius=tier+1,portCount=tier<3?1:tier<5?2:4;
            for(Direction controllerSide:SIDES){
                BlockPos controller=centre.offset(SurvivalGateLayout.rotate(new BlockPos(0,1,-radius),controllerSide));
                level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,controllerSide.getClockWise()),3);
                var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);
                for(Direction portSide:SIDES){
                    var ports=new java.util.ArrayList<BlockPos>();int[] offsets={-1,1,-2,2};
                    for(int i=0;i<portCount;i++){
                        BlockPos port=centre.offset(SurvivalGateLayout.rotate(new BlockPos(offsets[i],1,-radius),portSide));
                        ports.add(port);level.setBlock(port,BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
                    }
                    h.assertTrue(gate.formedTier()==tier,"Relocated service blocks failed: tier="+tier+", structure="+structure+", controller="+controllerSide+", ports="+portSide);
                    h.assertTrue(gate.centre().equals(centre),"Controller visual front changed the passenger centre");
                    h.assertTrue(!gate.adminTest(),"Relocated ordinary controller gained admin privileges");
                    for(BlockPos port:ports)for(Direction face:Direction.values()){
                        var energy=level.getCapability(Capabilities.EnergyStorage.BLOCK,port,face);int before=gate.stored;
                        h.assertTrue(energy!=null&&energy.receiveEnergy(7,true)==7&&gate.stored==before,"Relocated port simulation mutated or rejected FE");
                        h.assertTrue(energy.receiveEnergy(7,false)==7&&gate.stored==before+7&&energy.getEnergyStored()==gate.stored,"Relocated port did not share the controller buffer");
                    }
                    var cached=level.getCapability(Capabilities.EnergyStorage.BLOCK,ports.getFirst(),Direction.UP);
                    int before=gate.stored;level.setBlock(ports.getFirst(),Blocks.AIR.defaultBlockState(),3);
                    h.assertTrue(cached.receiveEnergy(7,false)==0&&gate.stored==before,"Removed relocated port retained charging");
                    for(var port:ports)level.setBlock(port,Blocks.AIR.defaultBlockState(),3);
                    checked[0]++;
                }
                level.setBlock(controller,Blocks.AIR.defaultBlockState(),3);
            }
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(centre.offset(SurvivalGateLayout.rotate(part.offset(),structure)),Blocks.AIR.defaultBlockState(),3);
        h.runAfterDelay(1,()->matrixFixture(h,index+1,checked));
    }
    @GameTest(templateNamespace="zerog_gate_flexible",template="equipment_empty",timeoutTicks=100)
    public static void duplicate_controllers_and_replaced_direct_handlers_cannot_charge(GameTestHelper h){
        var level=h.getLevel();BlockPos centre=h.absolutePos(new BlockPos(8,4,8));place(h,centre,1,Direction.NORTH);
        BlockPos controller=centre.offset(0,1,-2),port=centre.offset(2,1,0),duplicate=centre.offset(0,1,2);
        level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);level.setBlock(port,BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);gate.owner=java.util.UUID.randomUUID();gate.stored=240;
        var direct=gate.energy();var cached=level.getCapability(Capabilities.EnergyStorage.BLOCK,port,Direction.UP);
        h.assertTrue(gate.formedTier()==1,"Baseline duplicate-controller fixture invalid");
        level.setBlock(duplicate,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
        h.assertTrue(gate.formedTier()==0&&direct.receiveEnergy(7,false)==0&&cached.receiveEnergy(7,false)==0,"Duplicate controller retained live charging");
        level.setBlock(duplicate,Blocks.AIR.defaultBlockState(),3);
        var saved=gate.saveWithFullMetadata(level.registryAccess());
        level.setBlock(controller,Blocks.AIR.defaultBlockState(),3);
        level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
        var restored=(SurvivalGateBlockEntity)level.getBlockEntity(controller);restored.loadWithComponents(saved,level.registryAccess());
        h.assertTrue(restored.formedTier()==1&&restored.owner.equals(gate.owner)&&restored.stored==240,"Save/reload changed owner, stored FE or formation");
        h.assertTrue(direct.receiveEnergy(7,false)==0&&gate.stored==240&&!direct.canReceive(),"Removed direct controller handler charged an orphan buffer");
        h.assertTrue(cached.receiveEnergy(7,false)==7&&restored.stored==247,"Cached port did not reconnect to the actual replacement controller");
        level.setBlock(centre.offset(0,0,0),Blocks.AIR.defaultBlockState(),3);
        h.assertTrue(restored.formedTier()==0&&cached.receiveEnergy(7,false)==0&&restored.stored==247,"Broken landing pad did not immediately revoke charging");h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_flexible",template="equipment_empty",timeoutTicks=100)
    public static void shared_ports_and_ambiguous_centres_are_rejected(GameTestHelper h){
        var level=h.getLevel();BlockPos first=h.absolutePos(new BlockPos(8,4,8)),second=first.offset(4,0,0);
        place(h,first,1,Direction.NORTH);place(h,second,1,Direction.NORTH);
        BlockPos left=first.offset(-2,1,0),right=second.offset(2,1,0),shared=first.offset(2,1,0);
        level.setBlock(left,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);level.setBlock(right,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
        level.setBlock(shared,BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        var a=(SurvivalGateBlockEntity)level.getBlockEntity(left);var b=(SurvivalGateBlockEntity)level.getBlockEntity(right);
        var port=level.getCapability(Capabilities.EnergyStorage.BLOCK,shared,Direction.NORTH);
        h.assertTrue(a.formedTier()==0&&b.formedTier()==0&&port.receiveEnergy(10,false)==0,"Shared port cross-bound adjacent complete gates");
        level.setBlock(shared,Blocks.AIR.defaultBlockState(),3);
        level.setBlock(left.offset(0,0,1),BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        level.setBlock(right.offset(0,0,1),BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        h.assertTrue(a.formedTier()==1&&b.formedTier()==1,"Separate service ports failed adjacent-gate recovery");
        level.setBlock(left,Blocks.AIR.defaultBlockState(),3);level.setBlock(right,Blocks.AIR.defaultBlockState(),3);
        level.setBlock(shared,BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
        var ambiguous=(SurvivalGateBlockEntity)level.getBlockEntity(shared);
        h.assertTrue(ambiguous.formedTier()==0&&ambiguous.energy().receiveEnergy(10,false)==0,"One controller claimed two complete centres");h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_flexible",template="equipment_empty",timeoutTicks=100)
    public static void opposite_tier_six_ports_receive_real_generator_energy(GameTestHelper h){
        var level=h.getLevel();BlockPos centre=h.absolutePos(new BlockPos(8,4,8));place(h,centre,6,Direction.NORTH);
        BlockPos controller=centre.offset(0,1,-7);level.setBlock(controller,BlockInit.GATE_CONTROLLER.get().defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.EAST),3);
        for(int x:new int[]{-2,-1,1,2})level.setBlock(centre.offset(x,1,7),BlockInit.GATE_ENERGY_PORT.get().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(controller);h.assertTrue(gate.formedTier()==6,"Opposite-side Tier6 fixture invalid");
        BlockPos cablePos=centre.offset(-3,1,7),sourcePos=centre.offset(-4,1,7);
        var cableBlock=net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:copper_energy_conduit"));
        level.setBlock(cablePos,cableBlock.defaultBlockState(),3);level.setBlock(sourcePos,BlockInit.COMBUSTION_GENERATOR.get().defaultBlockState(),3);
        var cable=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(cablePos);
        var source=(net.zerog.tweaks.machine.CombustionBlockEntity)level.getBlockEntity(sourcePos);
        source.fuel.setStackInSlot(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.CHARCOAL,2));
        for(int i=0;i<10;i++){
            net.zerog.tweaks.machine.CombustionBlockEntity.tick(level,sourcePos,source.getBlockState(),source);
            net.zerog.tweaks.transport.TransportBlockEntity.tick(level,cablePos,cable.getBlockState(),cable);
        }
        h.assertTrue(gate.stored>0&&gate.stored+source.stored+cable.stored==500,"Opposite service port lost/rejected/duplicated real generated FE");h.succeed();
    }
}
