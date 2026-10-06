package net.zerog.tweaks.gametest;

import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.item.*;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.genetics.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class LegacySidesGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=120)
    public static void genetics_real_hopper_cannot_bypass_disabled_item_face(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:geno_station")));
        var be=h.getBlockEntity(p);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new GeneticsMenu(1,player.getInventory(),be);h.assertTrue(menu.clickMenuButton(player,507),"Top item Off rejected");
        h.setBlock(p.above(),net.minecraft.world.level.block.Blocks.HOPPER);
        var hopper=(net.minecraft.world.level.block.entity.HopperBlockEntity)h.getBlockEntity(p.above());hopper.setItem(0,new ItemStack(Items.HONEY_BOTTLE,2));
        h.runAfterDelay(30,()->{
            h.assertTrue(hopper.getItem(0).getCount()==2&&GeneticsRuntime.inventory(be).getStackInSlot(2).isEmpty(),"Vanilla hopper bypassed item Off");
            h.assertTrue(menu.clickMenuButton(player,505),"Top item Input rejected");
            h.runAfterDelay(30,()->{h.assertTrue(GeneticsRuntime.inventory(be).getStackInSlot(2).getCount()>0&&hopper.getItem(0).getCount()<2,"Enabled genetics hopper input failed");h.succeed();});
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void powered_and_genetics_fluid_faces_are_independent_and_persist(GameTestHelper h){
        try {
            for(String id:java.util.List.of("geno_station","genetic_splicer","centrifuge","starmetal_smelter")){
                var p=new BlockPos(1,1,1);h.setBlock(p,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));
                var be=h.getBlockEntity(p);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
                AbstractContainerMenu menu=GeneticsRuntime.handles(id)?new GeneticsMenu(1,player.getInventory(),be):(AbstractContainerMenu)be.getClass().getMethod("createMenu",int.class,net.minecraft.world.entity.player.Inventory.class,net.minecraft.world.entity.player.Player.class).invoke(be,1,player.getInventory(),player);
                for(var face:Direction.values()){
                    var cached=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
                    h.assertTrue(cached!=null&&menu.clickMenuButton(player,527+face.ordinal()*4),"Power face command missing: "+id);
                    h.assertTrue(cached.receiveEnergy(100,false)==0,"Power Off accepted FE");
                    h.assertTrue(menu.clickMenuButton(player,525+face.ordinal()*4)&&cached.receiveEnergy(100,false)==0,"Stale FE handler revived");
                    var fresh=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
                    h.assertTrue(fresh.receiveEnergy(100,true)==100&&fresh.receiveEnergy(100,false)==100,"Input FE transfer failed");
                    h.assertTrue(!menu.clickMenuButton(player,524+face.ordinal()*4),"Input-only machine accepted Both power");
                    if(GeneticsRuntime.handles(id)){
                        var fluid=h.getLevel().getCapability(Capabilities.FluidHandler.BLOCK,be.getBlockPos(),face);
                        String name=id.equals("geno_station")?"moon_honey":"royal_jelly";
                        var content=new net.neoforged.neoforge.fluids.FluidStack(BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:"+name)),100);
                        h.assertTrue(!content.isEmpty(),"Test source fluid missing");
                        h.assertTrue(menu.clickMenuButton(player,551+face.ordinal()*4)&&fluid.fill(content,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==0,"Fluid Off failed");
                        h.assertTrue(menu.clickMenuButton(player,549+face.ordinal()*4)&&fluid.fill(content,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==0,"Stale fluid handler revived");
                        var input=h.getLevel().getCapability(Capabilities.FluidHandler.BLOCK,be.getBlockPos(),face);
                        h.assertTrue(input.fill(content,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==100&&input.drain(100,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE).isEmpty(),"Input fluid direction failed");
                        h.assertTrue(menu.clickMenuButton(player,550+face.ordinal()*4),"Fluid Output rejected");
                        var output=h.getLevel().getCapability(Capabilities.FluidHandler.BLOCK,be.getBlockPos(),face);
                        h.assertTrue(output.fill(content,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==0&&output.drain(100,net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE).getAmount()==100,"Fluid Output failed");
                    }else h.assertTrue(!menu.clickMenuButton(player,551+face.ordinal()*4),"Tankless machine accepted fluid controls");
                }
                menu.clickMenuButton(player,527);menu.clickMenuButton(player,503);
                var tag=be.saveWithoutMetadata(h.getLevel().registryAccess());be.loadWithComponents(tag,h.getLevel().registryAccess());
                h.assertTrue(h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),Direction.DOWN)==null&&h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.DOWN).getSlots()==0,"Face settings lost after reload");
            }
            h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void machine_item_face_commands_restrict_automation_and_revoke_cached_access(GameTestHelper h){
        try {
            for(String id:java.util.List.of("geno_station","genetic_splicer","centrifuge","starmetal_smelter","silk_weaver","frame_infusion_altar","stardust_smelter","gravitational_centrifuge","frame_assembler","frame_component_assembler","infusion_altar")){
                if(!BuiltInRegistries.BLOCK.containsKey(ResourceLocation.parse("aeroapiary:"+id)))continue;
                var p=new BlockPos(1,1,1);h.setBlock(p,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));
                var be=h.getBlockEntity(p);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
                AbstractContainerMenu menu=GeneticsRuntime.handles(id)?new GeneticsMenu(1,player.getInventory(),be):(AbstractContainerMenu)be.getClass().getMethod("createMenu",int.class,net.minecraft.world.entity.player.Inventory.class,net.minecraft.world.entity.player.Player.class).invoke(be,1,player.getInventory(),player);
                int output=switch(id){case "centrifuge","gravitational_centrifuge"->1;case "stardust_smelter","frame_assembler","frame_component_assembler","infusion_altar"->2;default->3;};
                for(var face:Direction.values()){
                    var cached=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
                    h.assertTrue(cached!=null,"Default item capability missing: "+id);
                    GeneticsRuntime.inventory(be).setStackInSlot(output,new ItemStack(Items.DIAMOND,2));
                    h.assertTrue(menu.clickMenuButton(player,503+face.ordinal()*4),"Item face command missing: "+id);
                    h.assertTrue(cached.extractItem(output,2,false).isEmpty(),"Off face extracted items: "+id);
                    h.assertTrue(menu.clickMenuButton(player,502+face.ordinal()*4),"Output face command rejected: "+id);
                    h.assertTrue(cached.extractItem(output,2,false).isEmpty(),"Stale item handler revived: "+id);
                    var fresh=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
                    h.assertTrue(fresh.extractItem(output,2,false).getCount()==2,"Output face failed: "+id);
                    h.assertTrue(fresh.insertItem(0,new ItemStack(Items.DIRT),false).getCount()==1,"Output face accepted input: "+id);
                }
                h.assertTrue(!menu.clickMenuButton(player,572),"Forged face command accepted");
                player.setPos(be.getBlockPos().getCenter().add(100,0,0));h.assertTrue(!menu.clickMenuButton(player,503),"Remote face command accepted");
            }
            h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
}
