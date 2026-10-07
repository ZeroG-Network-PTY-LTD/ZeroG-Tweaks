package net.zerog.tweaks.gametest;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.BooleanOp;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.transport.TransportBlock;

@GameTestHolder("zerog_gate_power") @PrefixGameTestTemplate(false)
public final class TransportShapeCacheGameTests {
    private static TransportBlock.Wire wire(String tier,String family){return (TransportBlock.Wire)BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+tier+"_"+family));}
    private static VoxelShape reference(TransportBlock.Wire block,BlockState state){
        double lo=block.family.startsWith("energy")?6:block.family.startsWith("item")?4:5,hi=16-lo;
        var shape=net.minecraft.world.level.block.Block.box(lo,lo,lo,hi,hi,hi);
        for(var side:Direction.values()){
            var connection=state.getValue(TransportBlock.SIDES.get(side));if(connection==TransportBlock.Connection.NONE)continue;
            shape=Shapes.or(shape,face(side,lo,hi,0,lo));
            if(connection!=TransportBlock.Connection.PIPE)shape=Shapes.or(shape,face(side,4,12,0,2));
        }
        return shape.optimize();
    }
    private static VoxelShape face(Direction side,double min,double max,double near,double far){return switch(side){
        case NORTH->net.minecraft.world.level.block.Block.box(min,min,near,max,max,far);
        case SOUTH->net.minecraft.world.level.block.Block.box(min,min,16-far,max,max,16-near);
        case WEST->net.minecraft.world.level.block.Block.box(near,min,min,far,max,max);
        case EAST->net.minecraft.world.level.block.Block.box(16-far,min,min,16-near,max,max);
        case DOWN->net.minecraft.world.level.block.Block.box(min,near,min,max,far,max);
        case UP->net.minecraft.world.level.block.Block.box(min,16-far,min,max,16-near,max);
    };}
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=1000)
    public static void all_pipe_states_share_at_most_1522_shapes_across_families_and_tiers(GameTestHelper h){
        Set<VoxelShape> identities=Collections.newSetFromMap(new IdentityHashMap<>());long count=0;
        for(var tier:net.zerog.tweaks.transport.TransportTier.ALL)for(String family:new String[]{"energy_conduit","fluid_pipe","gas_tube","item_tube"}){
            var block=wire(tier.name(),family);
            for(var state:block.getStateDefinition().getPossibleStates()){
                identities.add(state.getShape(h.getLevel(),BlockPos.ZERO));count++;
            }
        }
        h.assertTrue(count==375000,"Did not inspect every registered wire state: "+count);
        h.assertTrue(identities.size()<=1522,"Wire geometry duplicated per state/tier: "+identities.size());
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=1000)
    public static void shared_shapes_preserve_reference_core_arms_and_machine_plates(GameTestHelper h){
        for(String family:new String[]{"energy_conduit","fluid_pipe","gas_tube","item_tube"}){
            var block=wire("copper",family);
            for(int encoded=0;encoded<729;encoded++){
                int value=encoded;var state=block.defaultBlockState();
                for(var side:Direction.values()){
                    var connection=switch(value%3){case 0->TransportBlock.Connection.NONE;case 1->TransportBlock.Connection.PIPE;default->TransportBlock.Connection.NORMAL;};
                    state=state.setValue(TransportBlock.SIDES.get(side),connection);value/=3;
                }
                var actual=state.getShape(h.getLevel(),BlockPos.ZERO);
                h.assertTrue(!Shapes.joinIsNotEmpty(actual,reference(block,state),BooleanOp.NOT_SAME),"Hitbox changed for "+family+" geometry "+encoded);
                var changed=state;
                for(var side:Direction.values())if(changed.getValue(TransportBlock.SIDES.get(side))==TransportBlock.Connection.NORMAL)
                    changed=changed.setValue(TransportBlock.SIDES.get(side),TransportBlock.Connection.PUSH);
                h.assertTrue(actual==changed.getShape(h.getLevel(),BlockPos.ZERO),"Push mode rebuilt identical shape");
            }
        }
        h.succeed();
    }
    private TransportShapeCacheGameTests(){}
}
