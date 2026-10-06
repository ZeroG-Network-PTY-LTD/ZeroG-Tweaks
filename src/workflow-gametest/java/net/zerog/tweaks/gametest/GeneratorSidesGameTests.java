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
