package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;

@GameTestHolder("zerog_tweaks") @PrefixGameTestTemplate(false)
public final class ProcessingSidesGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void processing_item_faces_route_only_outputs_and_revoke_cached_roles(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        for(String machine:new String[]{"alloy_forge","ore_refinery","crystal_growth_chamber","salvage_station"})for(var face:Direction.values()){
            h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",machine)));
            var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
            var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
            var menu=new ProcessingMenu(1,player.getInventory(),be);
            // IDs 200..229 select Auto/Input/Catalyst/Output/Off for each world face.
            int button=200+face.ordinal()*5;
            h.assertTrue(menu.clickMenuButton(player,button+3),"Item Output face control is missing");
            be.inventory.setStackInSlot(be.kind.output(),new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.DIAMOND,7));
            var output=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(output!=null&&output.extractItem(0,2,true).getCount()==2&&be.inventory.getStackInSlot(be.kind.output()).getCount()==7,"Output simulation changed contents");
            h.assertTrue(output.extractItem(0,2,false).getCount()==2&&be.inventory.getStackInSlot(be.kind.output()).getCount()==5,"Output face did not extract exact quantity");
            h.assertTrue(output.insertItem(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.STONE),false).getCount()==1,"Output face accepted insertion");
            h.assertTrue(menu.clickMenuButton(player,button+4)&&output.extractItem(0,1,false).isEmpty(),"Cached output bypassed Off mode");
            var power=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
            h.assertTrue(power!=null&&power.receiveEnergy(10,false)==10,"Item Off unexpectedly disabled power");
            h.assertTrue(menu.clickMenuButton(player,button+1)&&output.extractItem(0,1,false).isEmpty(),"Cached output bypassed Input mode");
            h.assertTrue(menu.value(14+face.ordinal())==1,"Item mode missing from menu synchronization");
            var input=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(input!=null&&input.extractItem(0,1,false).isEmpty(),"Input face extracted products");
            if(machine.equals("ore_refinery"))h.assertTrue(input.insertItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.RAW_CYRRIUM.get(),2),false).isEmpty(),"Input face rejected real refining reagent");
            h.assertTrue(menu.clickMenuButton(player,button+2),"Catalyst mode rejected");
            var catalyst=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(catalyst!=null&&catalyst.getSlots()==1&&!catalyst.isItemValid(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.DIAMOND)),"Catalyst face ignored recipe filter");
            if(machine.equals("ore_refinery"))h.assertTrue(catalyst.insertItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.STARDUST.get(),2),false).isEmpty(),"Catalyst face rejected real Stardust");
            h.assertTrue(!menu.clickMenuButton(player,230),"Forged item-side command accepted");
            player.setPos(be.getBlockPos().getCenter().add(100,0,0));
            h.assertTrue(!menu.clickMenuButton(player,button+3),"Remote item command accepted");
            player.setPos(be.getBlockPos().getCenter());menu.clickMenuButton(player,button+3);
            h.assertTrue(output.extractItem(0,1,false).isEmpty(),"Old output handler revived after role round-trip");
            var restored=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
            restored.setLevel(h.getLevel());
            h.assertTrue(restored.itemsFor(face).extractItem(0,5,false).getCount()==5,"Saved Output role or products lost on reload");
            h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
            h.assertTrue(catalyst.insertItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.STARDUST.get()),false).getCount()==1,"Replaced machine retained item insertion authority");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void real_hopper_obeys_refinery_item_input_and_off(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        h.setBlock(pos,net.zerog.tweaks.registry.BlockInit.ORE_REFINERY.get());
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        h.assertTrue(menu.clickMenuButton(player,206),"Up Input control rejected");
        h.setBlock(pos.above(),net.minecraft.world.level.block.Blocks.HOPPER);
        var hopper=(net.minecraft.world.level.block.entity.HopperBlockEntity)h.getBlockEntity(pos.above());
        hopper.setItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.RAW_CYRRIUM.get(),3));
        h.runAtTickTime(30,()->{
            h.assertTrue(be.inventory.getStackInSlot(0).getCount()==3&&hopper.getItem(0).isEmpty(),"Actual hopper failed to supply three raw materials");
            h.assertTrue(menu.clickMenuButton(player,209),"Up Off control rejected");
            hopper.setItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.RAW_CYRRIUM.get(),2));
            h.runAtTickTime(60,()->{h.assertTrue(be.inventory.getStackInSlot(0).getCount()==3&&hopper.getItem(0).getCount()==2,"Actual hopper bypassed Off mode");h.succeed();});
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void disabled_processing_face_revokes_cached_power_and_survives_reload(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        for(String machine:new String[]{"alloy_forge","ore_refinery","crystal_growth_chamber","salvage_station"}){
        for(var face:Direction.values()){
        h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",machine)));
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(GameType.SURVIVAL);
        player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        var power=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
        h.assertTrue(power!=null&&power.receiveEnergy(100,false)==100,"Default face lost power access");
        // IDs 100..105 disable the six world faces. IDs 106..111 restore legacy routing.
        h.assertTrue(menu.clickMenuButton(player,100+face.ordinal()),"Server rejected disable-face control");
        h.assertTrue(menu.value(8+face.ordinal())==1,"Disabled face not synchronized to menu");
        h.assertTrue(power.receiveEnergy(100,false)==0&&!power.canReceive(),"Cached power handler bypassed disabled face");
        var restored=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        restored.setLevel(h.getLevel());
        h.assertTrue(restored.energyInput(face).receiveEnergy(100,false)==0,"Disabled face lost on reload");
        player.setPos(be.getBlockPos().getCenter().add(100,0,0));
        h.assertTrue(!menu.clickMenuButton(player,106+face.ordinal()),"Distant player re-enabled power face");
        player.setPos(be.getBlockPos().getCenter());
        h.assertTrue(menu.clickMenuButton(player,106+face.ordinal())&&power.receiveEnergy(100,false)==100,"Re-enabled face did not resume power");
        h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
        h.assertTrue(power.receiveEnergy(100,false)==0&&!menu.clickMenuButton(player,100+face.ordinal()),"Replaced machine retained cached/menu authority");
        }
        }
        h.succeed();
    }
}
