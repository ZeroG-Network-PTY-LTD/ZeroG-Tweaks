package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.transport.TransportBlockEntity;

@GameTestHolder("zerog_blockers") @PrefixGameTestTemplate(false)
public final class TransportBlockerGameTests {
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void disabled_and_rejoined_edge_revokes_both_cached_graphs(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:astrium_fluid_pipe")));
        h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_fluid_pipe")));
        var high=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var low=(TransportBlockEntity)h.getBlockEntity(new BlockPos(2,1,1));
        var acid=new net.neoforged.neoforge.fluids.FluidStack(BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:acid")),100);
        var simulate=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE;
        h.assertTrue(high.fluidHandler(null).fill(acid,simulate)==0,"Weak connected pipe accepted acid");
        for(int n=0;n<3;n++)low.cycleFace(net.minecraft.core.Direction.WEST);
        h.assertTrue(high.fluidHandler(null).fill(acid,simulate)==100,"Disconnected copper remained in cached graph");
        low.cycleFace(net.minecraft.core.Direction.WEST);
        h.assertTrue(high.fluidHandler(null).fill(acid,simulate)==0&&high.tank.isEmpty(),"Same-tick rejoin bypassed acid safety or mutated simulation");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void all_dangerous_fluids_respect_each_connected_tier(GameTestHelper h){
        var execute=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE;
        var simulate=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE;
        for(String id:new String[]{"null_fluid","acid","magma_slag","cryo_fluid","solar_plasma"}){
            var fluid=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:"+id));
            h.assertTrue(fluid!=net.minecraft.world.level.material.Fluids.EMPTY,"Missing hazardous fluid "+id);
            int required=net.zerog.tweaks.transport.TransportTier.minimumFluidTier(id);
            // Descending includes a same-tick strong-to-weak replacement safety check.
            for(int tier=5;tier>=0;tier--){
                h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:astrium_fluid_pipe")));
                h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+net.zerog.tweaks.transport.TransportTier.ALL[tier].name()+"_fluid_pipe")));
                var high=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
                high.tank.setFluid(net.neoforged.neoforge.fluids.FluidStack.EMPTY);
                var handler=high.fluidHandler(null);
                var sample=new net.neoforged.neoforge.fluids.FluidStack(fluid,100);
                int expected=tier>=required?100:0;
                h.assertTrue(handler.fill(sample,simulate)==expected&&high.tank.isEmpty(),"Simulation bypassed tier or mutated "+id+" tier"+tier);
                h.assertTrue(handler.fill(sample,execute)==expected&&high.tank.getFluidAmount()==expected,"Connected weak segment accepted unsafe "+id+" tier"+tier);
            }
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void alternate_path_includes_segment_with_one_disabled_face(GameTestHelper h){
        var high=BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:astrium_fluid_pipe"));
        for(var pos:new BlockPos[]{new BlockPos(1,1,1),new BlockPos(1,1,0),new BlockPos(2,1,0)})h.setBlock(pos,high);
        h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_fluid_pipe")));
        var low=(TransportBlockEntity)h.getBlockEntity(new BlockPos(2,1,1));low.modes[net.minecraft.core.Direction.WEST.ordinal()]=3;
        var first=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        h.assertTrue(first.synchronizedLimit()==250,"Valid alternate path omitted lowest-tier segment after a disabled-face encounter");h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void hazardous_fill_checks_lowest_connected_pipe(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:astrium_fluid_pipe")));
        h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_fluid_pipe")));
        var high=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var acid=new net.neoforged.neoforge.fluids.FluidStack(BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:acid")),1000);
        h.assertTrue(high.fluidHandler(null).fill(acid,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE)==0,"Hazardous fluid entered mixed-tier network in simulation");
        h.assertTrue(high.fluidHandler(null).fill(acid,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==0&&high.tank.isEmpty(),"Hazardous fill bypassed copper segment");h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void nearest_routes_from_buffer_not_leader_position(GameTestHelper h){
        var block=BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_item_tube"));
        for(int x=1;x<=3;x++)h.setBlock(new BlockPos(x,1,1),block);
        h.setBlock(new BlockPos(0,1,1),net.minecraft.world.level.block.Blocks.CHEST);
        h.setBlock(new BlockPos(4,1,1),net.minecraft.world.level.block.Blocks.CHEST);
        var first=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var source=(TransportBlockEntity)h.getBlockEntity(new BlockPos(3,1,1));
        source.items.setStackInSlot(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.DIAMOND));
        h.runAtTickTime(20,()->{
            TransportBlockEntity.tick(h.getLevel(),first.getBlockPos(),first.getBlockState(),first);
            var near=(net.minecraft.world.level.block.entity.ChestBlockEntity)h.getBlockEntity(new BlockPos(4,1,1));
            var far=(net.minecraft.world.level.block.entity.ChestBlockEntity)h.getBlockEntity(new BlockPos(0,1,1));
            h.assertTrue(!near.isEmpty()&&far.isEmpty(),"Nearest routed to leader-side chest instead of closest buffer endpoint");h.succeed();
        });
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void connected_257_pipes_keep_one_live_transfer_budget(GameTestHelper h){
        var block=BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_energy_conduit"));
        for(int i=0;i<257;i++)h.setBlock(new BlockPos(i%5,10+i/25,(i/5)%5),block);
        var first=(TransportBlockEntity)h.getBlockEntity(new BlockPos(0,10,0));
        h.assertTrue(first.synchronizedLimit()==1000,"A 257-node loaded network silently lost its transfer budget");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void routing_from_nonleader_updates_connected_terminal(GameTestHelper h){
        var block=BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_item_tube"));
        h.setBlock(new BlockPos(1,1,1),block);h.setBlock(new BlockPos(2,1,1),block);
        var first=(TransportBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var second=(TransportBlockEntity)h.getBlockEntity(new BlockPos(2,1,1));
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(second.getBlockPos().getCenter());
        var editor=new net.zerog.tweaks.transport.TransportMenu(1,player.getInventory(),second);
        h.assertTrue(editor.clickMenuButton(player,1),"Routing click rejected");
        var other=new net.zerog.tweaks.transport.TransportMenu(2,player.getInventory(),first);
        h.assertTrue(other.value(4)==1,"Route change on nonleader did not reach connected terminal");h.succeed();
    }
}
