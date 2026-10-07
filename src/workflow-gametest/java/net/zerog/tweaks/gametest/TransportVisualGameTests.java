package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.transport.TransportBlockEntity;

@GameTestHolder("zerog_transport_visual") @PrefixGameTestTemplate(false)
public final class TransportVisualGameTests {
    @GameTest(templateNamespace="zerog_transport_visual",template="equipment_empty",timeoutTicks=100)
    public static void wave_axis_tracks_both_legs_of_every_junction(GameTestHelper h) {
        for(var incoming:Direction.values())for(var outgoing:Direction.values()) {
            h.assertTrue(net.zerog.tweaks.transport.TransportMotion.ribbonAxis(incoming,outgoing,.25F)==incoming.getAxis(),"Incoming wave follows wrong junction axis");
            h.assertTrue(net.zerog.tweaks.transport.TransportMotion.ribbonAxis(incoming,outgoing,.75F)==outgoing.getAxis(),"Outgoing wave follows wrong junction axis");
        }
        h.succeed();
    }
    private static TransportBlockEntity place(GameTestHelper h, int x, String id) {
        var p=new BlockPos(x,1,1);
        h.setBlock(p,BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id)));
        return (TransportBlockEntity)h.getBlockEntity(p);
    }
    @GameTest(templateNamespace="zerog_transport_visual",template="equipment_empty",timeoutTicks=100)
    public static void gas_canisters_fill_drain_and_preserve_contents_on_reload(GameTestHelper h) {
        var oxygen=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:oxygen"));
        h.assertTrue(oxygen!=net.minecraft.world.level.material.Fluids.EMPTY,"Oxygen is not registered");
        var item=BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:gas_canister"));
        var stack=new net.minecraft.world.item.ItemStack(item);
        var handler=net.neoforged.neoforge.fluids.FluidUtil.getFluidHandler(stack).orElseThrow();
        var action=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE;
        var simulate=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE;
        h.assertTrue(handler.fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,1200),simulate)==1000
            &&handler.getFluidInTank(0).isEmpty(),"Canister simulation mutated contents");
        h.assertTrue(handler.fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,1200),action)==1000,"Canister capacity is not 1000 mB");
        h.assertTrue(handler.fill(new net.neoforged.neoforge.fluids.FluidStack(net.minecraft.world.level.material.Fluids.WATER,1),action)==0,"Canister accepted liquid water");
        var saved=stack.save(h.getLevel().registryAccess());
        var restored=net.minecraft.world.item.ItemStack.parse(h.getLevel().registryAccess(),saved).orElseThrow();
        var recovered=net.neoforged.neoforge.fluids.FluidUtil.getFluidHandler(restored).orElseThrow();
        h.assertTrue(recovered.drain(400,action).getAmount()==400&&recovered.getFluidInTank(0).getAmount()==600,
            "Gas identity/quantity lost across item persistence");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_transport_visual",template="equipment_empty",timeoutTicks=100)
    public static void gas_networks_are_separate_bounded_and_conserved(GameTestHelper h) {
        h.assertTrue(BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_gas_tube"))!=net.minecraft.world.level.block.Blocks.AIR,"Gas tubes are not registered");
        var high=place(h,1,"astrium_gas_tube");var low=place(h,2,"copper_gas_tube");
        var liquid=place(h,3,"copper_fluid_pipe");var sink=place(h,4,"fluid_port");
        var oxygen=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:oxygen"));
        var hydrogen=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:hydrogen"));
        var action=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE;
        var highHandler=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.FluidHandler.BLOCK,high.getBlockPos(),Direction.WEST);
        var lowHandler=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.FluidHandler.BLOCK,low.getBlockPos(),Direction.EAST);
        h.assertTrue(highHandler!=null&&lowHandler!=null,"Gas tubes have no standard fluid capability");
        h.assertTrue(highHandler.fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,1000),action)==1000,"Oxygen fill rejected");
        h.assertTrue(lowHandler.fill(new net.neoforged.neoforge.fluids.FluidStack(hydrogen,10),action)==0,"Mixed gases accepted across connected tubes");
        h.assertTrue(lowHandler.fill(new net.neoforged.neoforge.fluids.FluidStack(net.minecraft.world.level.material.Fluids.WATER,10),action)==0,"Gas tube accepted liquid");
        h.assertTrue(liquid.fluidHandler(null).fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,10),action)==0,"Liquid pipe accepted gas");
        h.assertTrue(high.synchronizedLimit()==250&&low.synchronizedLimit()==250,"Connected gas rate ignores weakest tier");
        h.assertTrue(high.push(h.getLevel(),sink.getBlockPos(),Direction.EAST,"fluid",250)==250
            &&highHandler.getFluidInTank(0).getAmount()==750&&sink.fluidHandler(null).getFluidInTank(0).getAmount()==250,"Gas transfer lost or created mB");
        sink.fluidHandler(null).fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,20000),action);
        h.assertTrue(high.push(h.getLevel(),sink.getBlockPos(),Direction.EAST,"fluid",250)==0&&highHandler.getFluidInTank(0).getAmount()==750,"Blocked gas delivery lost contents");
        var saved=high.saveWithFullMetadata(h.getLevel().registryAccess());
        h.getLevel().setBlock(high.getBlockPos(),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        h.getLevel().setBlock(high.getBlockPos(),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:astrium_gas_tube")).defaultBlockState(),2);
        var loaded=h.getLevel().getBlockEntity(high.getBlockPos());loaded.loadWithComponents(saved,h.getLevel().registryAccess());
        var restored=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.FluidHandler.BLOCK,loaded.getBlockPos(),Direction.WEST);
        h.assertTrue(restored.getFluidInTank(0).getFluid()==oxygen&&restored.getFluidInTank(0).getAmount()==750,"Gas buffer lost identity/quantity on reload");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_transport_visual",template="equipment_empty",timeoutTicks=100)
    public static void gas_network_ticks_and_canister_exchange_conserve_millibuckets(GameTestHelper h) {
        var source=place(h,1,"astrium_gas_tube");var segment=place(h,2,"copper_gas_tube");var sink=place(h,3,"fluid_port");
        var oxygen=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:oxygen"));
        var action=net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE;
        var stack=new net.minecraft.world.item.ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:gas_canister")));
        var handler=net.neoforged.neoforge.fluids.FluidUtil.getFluidHandler(stack).orElseThrow();
        handler.fill(new net.neoforged.neoforge.fluids.FluidStack(oxygen,1000),action);
        var emptied=net.neoforged.neoforge.fluids.FluidUtil.tryEmptyContainer(stack,source.fluidHandler(null),1000,null,true);
        h.assertTrue(emptied.isSuccess()&&source.fluidHandler(null).getFluidInTank(0).getAmount()==1000
            &&net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(emptied.getResult()).isEmpty(),"Canister exchange lost gas or kept a duplicate");
        for(var node:new TransportBlockEntity[]{source,segment,sink})java.util.Arrays.fill(node.modes,3);
        source.modes[Direction.EAST.ordinal()]=0;segment.modes[Direction.WEST.ordinal()]=0;
        segment.modes[Direction.EAST.ordinal()]=1;sink.modes[Direction.WEST.ordinal()]=2;
        TransportBlockEntity.tick(h.getLevel(),source.getBlockPos(),source.getBlockState(),source);
        TransportBlockEntity.tick(h.getLevel(),segment.getBlockPos(),segment.getBlockState(),segment);
        h.assertTrue(source.fluidHandler(null).getFluidInTank(0).getAmount()==750
            &&sink.fluidHandler(null).getFluidInTank(0).getAmount()==250,"Automatic network ticks do not share the 250 mB budget");
        var collected=net.neoforged.neoforge.fluids.FluidUtil.tryFillContainer(emptied.getResult(),sink.fluidHandler(Direction.WEST),1000,null,true);
        // Input-only ports cannot be drained, including through a cached capability.
        h.assertTrue(!collected.isSuccess(),"Canister drained an input-only port");
        sink.modes[Direction.WEST.ordinal()]=0;
        collected=net.neoforged.neoforge.fluids.FluidUtil.tryFillContainer(emptied.getResult(),sink.fluidHandler(Direction.WEST),1000,null,true);
        h.assertTrue(collected.isSuccess()&&sink.fluidHandler(null).getFluidInTank(0).isEmpty()
            &&net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(collected.getResult()).orElseThrow().getAmount()==250,"Canister collection failed to conserve partial contents");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_transport_visual",template="equipment_empty",timeoutTicks=100)
    public static void committed_power_is_visible_and_blocked_delivery_has_no_pulse(GameTestHelper h) {
        var source=place(h,1,"copper_energy_conduit");var sink=place(h,2,"energy_port");
        source.stored=1000;
        h.assertTrue(source.push(h.getLevel(),sink.getBlockPos(),Direction.EAST,"energy",400)==400,
            "Actual power delivery rejected");
        h.assertTrue(source.stored==600&&sink.stored==400,"Power transfer was not conserved");
        var packet=source.getUpdateTag(h.getLevel().registryAccess());
        h.assertTrue(packet.getInt("motion_energy")==400&&packet.getInt("from")==Direction.WEST.ordinal()
            &&packet.getInt("to")==Direction.EAST.ordinal(),"Committed power lacks directional client pulse");
        sink.stored=sink.capacity();source.motionTick=-1000;
        h.assertTrue(source.push(h.getLevel(),sink.getBlockPos(),Direction.EAST,"energy",400)==0
            &&source.stored==600&&source.motionTick==-1000,"Blocked transfer emitted a pulse or lost FE");
        h.succeed();
    }
}
