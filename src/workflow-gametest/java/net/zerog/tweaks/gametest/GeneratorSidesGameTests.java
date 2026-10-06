package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.power.PowerBlockEntity;
import net.zerog.tweaks.power.PowerMenu;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_tweaks") @PrefixGameTestTemplate(false)
public final class GeneratorSidesGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void fusion_hopper_obeys_saved_fuel_faces(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.FUSION_REACTOR.get());var be=(PowerBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new PowerMenu(1,player.getInventory(),be);
        h.setBlock(pos.above(),net.minecraft.world.level.block.Blocks.HOPPER);
        var hopper=(net.minecraft.world.level.block.entity.HopperBlockEntity)h.getBlockEntity(pos.above());
        hopper.setItem(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.FUSION_DUST.get(),2));
        h.assertTrue(menu.clickMenuButton(player,203),"Fuel Off rejected");
        var tag=be.saveWithoutMetadata(h.getLevel().registryAccess());be.loadWithComponents(tag,h.getLevel().registryAccess());
        h.runAfterDelay(30,()->{
            h.assertTrue(hopper.getItem(0).getCount()==2&&menu.fuelDisabled(Direction.UP.ordinal()),"Disabled saved face accepted hopper fuel");
            h.assertTrue(menu.clickMenuButton(player,202),"Fuel Input rejected");
            h.runAfterDelay(30,()->{h.assertTrue(hopper.getItem(0).getCount()<2,"Restored fuel face rejected actual hopper");h.succeed();});
        });
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void combustion_fuel_and_power_faces_are_independent_and_revoke_stale_access(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.COMBUSTION_GENERATOR.get());
        var be=(net.zerog.tweaks.machine.CombustionBlockEntity)h.getBlockEntity(pos);be.stored=1000;
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new net.zerog.tweaks.machine.CombustionMenu(1,player.getInventory(),be);
        for(var face:Direction.values()){
            var fuel=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            var power=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
            h.assertTrue(fuel!=null&&power!=null,"Combustion lost default faces");
            h.assertTrue(menu.clickMenuButton(player,201+2*face.ordinal()),"Combustion fuel-face command is missing");
            var coal=new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.COAL);
            h.assertTrue(fuel.insertItem(0,coal,false).getCount()==1,"Off fuel face accepted coal");
            h.assertTrue(power.extractEnergy(10,false)==10,"Fuel Off unexpectedly disabled power");
            h.assertTrue(menu.clickMenuButton(player,200+2*face.ordinal()),"Fuel Input restore rejected");
            h.assertTrue(fuel.insertItem(0,coal,false).getCount()==1,"Stale combustion fuel handler revived");
            var fresh=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(fresh.insertItem(0,coal,false).isEmpty()&&fresh.extractItem(0,1,false).isEmpty(),"Fuel Input filter/extraction failed");
            be.fuel.extractItem(0,1,false);
            h.assertTrue(menu.clickMenuButton(player,100+face.ordinal())&&power.extractEnergy(10,false)==0,"Power Off did not revoke cached output");
            h.assertTrue(menu.clickMenuButton(player,106+face.ordinal())&&power.extractEnergy(10,false)==0,"Stale combustion power handler revived");
        }
        h.assertTrue(!menu.clickMenuButton(player,212),"Forged combustion command accepted");
        player.setPos(be.getBlockPos().getCenter().add(100,0,0));h.assertTrue(!menu.clickMenuButton(player,100),"Remote combustion command accepted");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void fusion_fuel_faces_preserve_defaults_filters_and_cached_handler_safety(GameTestHelper h) {
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.FUSION_REACTOR.get());
        var be=(PowerBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new PowerMenu(1,player.getInventory(),be);
        for(var face:Direction.values()){
            var initial=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(face==Direction.UP?initial!=null:initial==null||!initial.isItemValid(0,new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.FUSION_DUST.get())),"Old fuel-face defaults changed");
            h.assertTrue(menu.clickMenuButton(player,200+face.ordinal()*2),"Fusion fuel-input face command is missing");
            var cached=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            var dust=new net.minecraft.world.item.ItemStack(net.zerog.tweaks.registry.ItemInit.FUSION_DUST.get());
            h.assertTrue(cached!=null&&cached.insertItem(0,dust,true).isEmpty()&&be.fuel.getStackInSlot(0).isEmpty(),"Fuel simulation changed contents");
            h.assertTrue(cached.insertItem(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.COAL),false).getCount()==1,"Fusion accepted non-fusion fuel");
            h.assertTrue(menu.clickMenuButton(player,201+face.ordinal()*2),"Fusion fuel-off command missing");
            h.assertTrue(cached.insertItem(0,dust,false).getCount()==1,"Disabled cached fuel handler accepted insertion");
            h.assertTrue(menu.clickMenuButton(player,200+face.ordinal()*2),"Fusion fuel restore rejected");
            h.assertTrue(cached.insertItem(0,dust,false).getCount()==1,"Cached fuel handler revived after mode round trip");
            var fresh=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),face);
            h.assertTrue(fresh.insertItem(0,dust,false).isEmpty(),"Enabled fuel face rejected valid fuel");
            h.assertTrue(fresh.extractItem(0,1,false).isEmpty(),"Input-only automation stole fuel");
            be.fuel.extractItem(0,1,false);
        }
        h.assertTrue(!menu.clickMenuButton(player,212),"Forged fuel command accepted");
        player.setPos(be.getBlockPos().getCenter().add(100,0,0));
        h.assertTrue(!menu.clickMenuButton(player,200),"Remote fuel command accepted");
        h.setBlock(pos,BlockInit.SOLAR_ARRAY.get());be=(PowerBlockEntity)h.getBlockEntity(pos);
        player.setPos(be.getBlockPos().getCenter());menu=new PowerMenu(2,player.getInventory(),be);
        h.assertTrue(!menu.clickMenuButton(player,200),"Solar array accepted imaginary fuel configuration");
        h.assertTrue(h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.UP)==null,"Solar array exposed imaginary fuel slots");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void output_faces_disable_real_capabilities_and_reject_stale_handlers(GameTestHelper h) {
        var pos=new BlockPos(1,1,1);
        for(var block:new net.minecraft.world.level.block.Block[]{BlockInit.SOLAR_ARRAY.get(),BlockInit.FUSION_REACTOR.get()})
        for(var face:Direction.values()) {
            h.setBlock(pos,block);var be=(PowerBlockEntity)h.getBlockEntity(pos);be.stored=1000;
            var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
            var menu=new PowerMenu(1,player.getInventory(),be);
            var cached=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
            h.assertTrue(cached!=null&&cached.extractEnergy(100,true)==100&&be.stored==1000,"Default generator output simulation failed");
            h.assertTrue(menu.clickMenuButton(player,100+face.ordinal()),"Generator disable-output GUI command is missing");
            h.assertTrue(!cached.canExtract()&&cached.extractEnergy(100,false)==0&&be.stored==1000,"Disabled cached output extracted power");
            var saved=be.saveWithoutMetadata(h.getLevel().registryAccess());
            var restored=new PowerBlockEntity(be.getBlockPos(),be.getBlockState());
            restored.loadWithComponents(saved,h.getLevel().registryAccess());
            h.assertTrue(restored.outputDisabled(face)&&restored.stored==1000,"Generator output configuration did not survive reload");
            h.assertTrue(menu.outputDisabled(face.ordinal()),"Generator menu did not synchronize disabled face");
            h.assertTrue(menu.clickMenuButton(player,106+face.ordinal()),"Generator restore-output command missing");
            h.assertTrue(cached.extractEnergy(100,false)==0,"Stale output revived after mode round-trip");
            var fresh=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),face);
            h.assertTrue(fresh!=null&&fresh.extractEnergy(100,false)==100&&be.stored==900,"Fresh output did not conserve FE");
            h.assertTrue(!menu.clickMenuButton(player,112),"Forged generator command accepted");
            player.setPos(be.getBlockPos().getCenter().add(100,0,0));
            h.assertTrue(!menu.clickMenuButton(player,100+face.ordinal()),"Remote generator command accepted");
            h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
            h.assertTrue(fresh.extractEnergy(100,false)==0,"Removed generator retained output authority");
        }
        h.succeed();
    }
}
