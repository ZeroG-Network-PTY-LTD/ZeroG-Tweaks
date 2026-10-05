package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;
import net.zerog.tweaks.genetics.*;
import net.zerog.tweaks.transport.*;
import net.zerog.tweaks.storage.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class AlvearyServiceGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void controller_is_terminal_not_external_energy_or_fluid_port(GameTestHelper h){
        var owner=shell(h,3);update(owner);
        for(var side:Direction.values()){
            h.assertTrue(h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,owner.getBlockPos(),side)==null,"Cable can bypass energy port by connecting to controller");
            h.assertTrue(h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.FluidHandler.BLOCK,owner.getBlockPos(),side)==null,"Pipe can bypass fluid hatch by connecting to controller");
            h.assertTrue(h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.ItemHandler.BLOCK,owner.getBlockPos(),side)==null,"Item tube can bypass item hatch by connecting to controller");
        }h.succeed();
    }
    private static BlockEntity shell(GameTestHelper h,int tier){return shellAt(h,tier,new BlockPos(4,1,4));}
    private static BlockEntity shellAt(GameTestHelper h,int tier,BlockPos origin){for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){boolean air=(y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3;String role=y==4?"roof":x==0&&y==0&&z==0?"controller":x==1&&y==0&&z==0?"energy_port":"casing";if(!BuiltInRegistries.BLOCK.getKey(h.getBlockState(origin.offset(-x,y,-z)).getBlock()).getPath().equals("tier"+tier+"_controller"))h.setBlock(origin.offset(-x,y,-z),air?Blocks.AIR:BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier"+tier+"_"+role)));}return h.getBlockEntity(origin);}
    private static TransportBlockEntity port(GameTestHelper h,BlockPos pos,String family,TransportBlock.PortMode mode){var state=BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+family+"_port")).defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH).setValue(TransportBlock.MODE,mode);h.setBlock(pos,state);return(TransportBlockEntity)h.getBlockEntity(pos);}
    private static void update(BlockEntity be){try{be.getClass().getMethod("updateFormation").invoke(be);}catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void service_base_accepts_second_row_controller_on_each_wall(GameTestHelper h){
        var base=new BlockPos(4,1,4);
        for(int tier=1;tier<=7;tier++)for(var location:new BlockPos[]{new BlockPos(0,1,2),new BlockPos(4,1,2),new BlockPos(2,1,0),new BlockPos(2,1,4),new BlockPos(0,1,0),new BlockPos(4,1,4)}){
            for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){
                boolean core=(y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3;
                String part=y==4?"roof":"casing";
                if(x==location.getX()&&y==1&&z==location.getZ())part="controller";
                h.setBlock(base.offset(-x,y,-z),core?Blocks.AIR:BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier"+tier+"_"+part)));
            }
            port(h,base,"energy",TransportBlock.PortMode.INPUT);
            port(h,base.offset(-1,0,0),"item",TransportBlock.PortMode.INPUT);
            port(h,base.offset(-2,0,0),"item",TransportBlock.PortMode.OUTPUT);
            port(h,base.offset(-3,0,0),"fluid",TransportBlock.PortMode.INPUT);
            port(h,base.offset(-4,0,0),"fluid",TransportBlock.PortMode.OUTPUT);
            var owner=h.getBlockEntity(base.offset(-location.getX(),1,-location.getZ()));update(owner);
            h.assertTrue(AlvearyRuntime.formed(owner),"Second-row controller rejected at tier "+tier+" / "+location+": "+AlvearyFormation.locate(h.getLevel(),owner.getBlockPos(),tier).error());
            h.assertTrue(AlvearyPorts.controller(h.getLevel(),h.absolutePos(base))==owner,"Bottom energy hatch failed to find relocated controller");
            if(tier>=3){
                var energy=(TransportBlockEntity)h.getBlockEntity(base);energy.stored=2000;
                AlvearyServiceModules.tick(owner);
                h.assertTrue(energy.stored==1000&&AlvearyRuntime.energy(owner).getEnergyStored()==1000,"Relocated controller lost buffered energy transfer");
            }
            h.setBlock(base.offset(-1,0,0),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier"+tier+"_casing")));update(owner);
            h.assertTrue(!AlvearyRuntime.formed(owner),"Missing required second item port still formed");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void zerog_ports_form_transfer_buffers_and_expose_front_only(GameTestHelper h){var owner=shell(h,3);var energy=port(h,new BlockPos(3,1,4),"energy",TransportBlock.PortMode.INPUT);var item=port(h,new BlockPos(2,1,4),"item",TransportBlock.PortMode.INPUT);var fluid=port(h,new BlockPos(1,1,4),"fluid",TransportBlock.PortMode.OUTPUT);update(owner);h.assertTrue(AlvearyRuntime.formed(owner)&&AlvearyPorts.controller(h.getLevel(),energy.getBlockPos())==owner,"Original ZeroG ports rejected from shell");energy.stored=5000;var honey=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:moon_honey"));new AlvearyFluids(owner).fill(new FluidStack(honey,750),FluidAction.EXECUTE);AlvearyServiceModules.tick(owner);h.assertTrue(energy.stored==4000&&AlvearyRuntime.energy(owner).getEnergyStored()==1000,"Buffered power transfer lost/duplicated FE");h.assertTrue(fluid.tank.getFluidAmount()==250&&new AlvearyFluids(owner).getFluidInTank(0).getAmount()==500,"Buffered honey export not conserved");h.assertTrue(energy.energy(Direction.SOUTH).canReceive()&&!energy.energy(Direction.NORTH).canReceive()&&!item.itemHandler(Direction.NORTH).isItemValid(0,new ItemStack(Items.DIAMOND)),"Formed service port exposed inward casing face");item.items.setStackInSlot(0,GeneticsRuntime.product("proven_frame").copyWithCount(3));AlvearyServiceModules.transferItems(owner,item);int frames=0;for(int i=0;i<27;i++)frames+=AlvearyRuntime.frames(owner).getStackInSlot(i).getCount();h.assertTrue(frames==3&&item.items.getStackInSlot(0).isEmpty(),"Frame input did not enter actual housing handler");h.getLevel().setBlock(item.getBlockPos(),item.getBlockState().setValue(TransportBlock.MODE,TransportBlock.PortMode.OUTPUT),3);AlvearyRuntime.state(owner).putBoolean("eject",true);GeneticsRuntime.inventory(owner).setStackInSlot(AlvearyRuntime.outputStart(owner),new ItemStack(Items.DIAMOND,5));AlvearyServiceModules.transferItems(owner,item);h.assertTrue(item.items.getStackInSlot(0).getCount()==4&&GeneticsRuntime.inventory(owner).getStackInSlot(AlvearyRuntime.outputStart(owner)).getCount()==1,"Real products not conserved through output buffer");h.assertTrue(item.itemHandler(Direction.NORTH).extractItem(0,4,false).isEmpty()&&item.itemHandler(Direction.SOUTH).extractItem(0,4,true).getCount()==4,"Output front/inside extraction reversed");h.getLevel().setBlock(energy.getBlockPos(),energy.getBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.NORTH),3);update(owner);h.assertTrue(!AlvearyRuntime.formed(owner),"Inward-facing terminal incorrectly formed");var standalone=port(h,new BlockPos(8,1,8),"energy",TransportBlock.PortMode.BOTH);h.assertTrue(standalone.energy(Direction.EAST).canReceive()&&standalone.energy(Direction.WEST).canExtract(),"Standalone port behavior changed");h.getLevel().setBlock(energy.getBlockPos(),energy.getBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH),3);var second=shellAt(h,3,new BlockPos(8,1,4));var shared=port(h,new BlockPos(4,2,4),"item",TransportBlock.PortMode.OUTPUT);update(owner);update(second);shared.items.setStackInSlot(0,new ItemStack(Items.DIAMOND,2));h.assertTrue(AlvearyRuntime.formed(owner)&&AlvearyRuntime.formed(second)&&AlvearyPorts.controller(h.getLevel(),shared.getBlockPos())==null&&!shared.output(Direction.NORTH)&&shared.output(Direction.SOUTH),"Ambiguous service port exposed inward face or chose an owner");AlvearyServiceModules.transferItems(owner,shared);h.assertTrue(shared.items.getStackInSlot(0).getCount()==2,"Ambiguous buffered service port transferred contents");h.succeed();}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void energy_cells_storage_catalyst_and_strict_shell_roles(GameTestHelper h){var owner=shell(h,6);h.setBlock(new BlockPos(3,1,4),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_energy_cell")));var cell=(TransportBlockEntity)h.getBlockEntity(new BlockPos(3,1,4));java.util.Arrays.fill(cell.modes,2);cell.modes[Direction.NORTH.ordinal()]=1;cell.stored=2000;h.setBlock(new BlockPos(2,1,4),StorageTankRegistry.BLOCKS.get(0).get());var tank=(StorageTankBlockEntity)h.getBlockEntity(new BlockPos(2,1,4));var light=BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:liquid_starlight"));tank.tank.fill(new FluidStack(light,2000),FluidAction.EXECUTE);update(owner);h.assertTrue(AlvearyRuntime.formed(owner),"Cell/tank service substitutions rejected");AlvearyServiceModules.tick(owner);h.assertTrue(cell.stored==1000&&AlvearyRuntime.energy(owner).getEnergyStored()==1000&&tank.tank.getFluidAmount()==1000&&new AlvearyFluids(owner).getFluidInTank(1).getAmount()==1000,"Cell/catalyst buffer conservation failed");java.util.Arrays.fill(cell.modes,2);java.util.Arrays.fill(tank.modes,3);AlvearyServiceModules.tick(owner);h.assertTrue(cell.stored==1000&&tank.tank.getFluidAmount()==1000,"Disabled inward cell/tank sides transferred");for(var tier:TransportTier.ALL){h.assertTrue(AlvearyFormation.role(BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+tier.name()+"_energy_cell")).defaultBlockState())==AlvearyFormation.Role.ENERGY,"Missing energy-cell tier in whitelist");}for(var block:StorageTankRegistry.BLOCKS)h.assertTrue(AlvearyFormation.role(block.get().defaultBlockState())==AlvearyFormation.Role.FLUID,"Missing storage-tank tier in whitelist");h.setBlock(new BlockPos(1,5,1),StorageTankRegistry.BLOCKS.get(5).get());update(owner);h.assertTrue(!AlvearyRuntime.formed(owner),"Service tank replaced mandatory roof");h.setBlock(new BlockPos(1,5,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier6_roof")));h.setBlock(new BlockPos(2,2,2),StorageTankRegistry.BLOCKS.get(5).get());update(owner);h.assertTrue(!AlvearyRuntime.formed(owner),"Service tank filled required flight chamber");h.succeed();}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void real_product_paging_separates_legacy_frame_recovery(GameTestHelper h){h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier7_controller")));var owner=h.getBlockEntity(new BlockPos(1,1,1));var inventory=GeneticsRuntime.inventory(owner);inventory.setStackInSlot(2,GeneticsRuntime.product("proven_frame").copyWithCount(64));int output=AlvearyRuntime.outputStart(owner);inventory.setStackInSlot(output,new ItemStack(Items.DIAMOND,7));var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(owner.getBlockPos().getCenter());var menu=new AlvearyMenu(1,player.getInventory(),owner);h.assertTrue(menu.slots.get(output).isActive()&&menu.slots.get(output).x==140&&menu.slots.get(output).y==23&&!menu.slots.get(2).isActive(),"Products displayed legacy frame positions on first page");h.assertTrue(!menu.slots.get(output).mayPlace(new ItemStack(Items.STONE))&&!menu.slots.get(1).isActive(),"Output accepts input or empty recovery pretends to be drone slot");h.assertTrue(menu.quickMoveStack(player,output).getCount()==7&&inventory.getStackInSlot(output).isEmpty(),"Product shift-click did not reach player");for(int i=0;i<menu.outputPages();i++)h.assertTrue(menu.clickMenuButton(player,2),"Product paging rejected");h.assertTrue(menu.recoveryPage()&&menu.slots.get(2).isActive()&&!menu.slots.get(output).isActive()&&inventory.getStackInSlot(2).getCount()==37,"Legacy recovery hidden/overwritten by new output paging");h.assertTrue(menu.quickMoveStack(player,2).getCount()==37&&inventory.getStackInSlot(2).isEmpty(),"Legacy frame recovery lost contents");int frames=0;for(int i=0;i<27;i++)frames+=AlvearyRuntime.frames(owner).getStackInSlot(i).getCount();h.assertTrue(frames==27,"Recovery removed real housing frames");h.succeed();}
}
