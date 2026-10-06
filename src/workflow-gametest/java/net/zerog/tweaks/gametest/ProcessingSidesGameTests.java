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
