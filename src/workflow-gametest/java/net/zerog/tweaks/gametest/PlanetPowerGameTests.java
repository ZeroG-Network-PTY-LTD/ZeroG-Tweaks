package net.zerog.tweaks.gametest;

import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.*;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.zerog.tweaks.power.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class PlanetPowerGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void fusion_fuel_pause_upgrade_reload_and_ports(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.FUSION_REACTOR.get());var be=(PowerBlockEntity)h.getBlockEntity(pos);
        h.assertTrue(be.fuel.insertItem(0,new ItemStack(Items.COAL),false).getCount()==1,"Fusion accepted non-Fusion Dust");
        h.assertTrue(h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.UP)!=null&&h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.DOWN)==null,"Fuel ports are not top-only");
        be.fuel.insertItem(0,new ItemStack(ItemInit.FUSION_DUST.get(),2),false);
        PowerBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.stored==PowerConfig.FUSION_RATE.get()&&be.burn==PowerConfig.FUSION_TICKS.get()-1&&be.fuel.getStackInSlot(0).getCount()==1,"Fusion burn not conserved");
        for(int i=0;i<3;i++)h.assertTrue(be.installModule(),"Module rejected");h.assertTrue(!be.installModule()&&be.capacity()==PowerConfig.BUFFER.get()*4,"Module bound failed");
        be.stored=be.capacity();int burn=be.burn;PowerBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);h.assertTrue(be.burn==burn,"Full generator wasted fuel");
        h.assertTrue(be.energy.receiveEnergy(100,false)==0&&be.energy.extractEnergy(-1,false)==0,"Energy extraction-only contract failed");
        int before=be.stored,n=be.energy.extractEnergy(100,true);h.assertTrue(n==100&&be.stored==before,"Simulate extraction mutated");be.energy.extractEnergy(100,false);h.assertTrue(be.stored==before-100,"Extraction lost conservation");
        var tag=be.saveWithFullMetadata(h.getLevel().registryAccess());var copy=(PowerBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),tag,h.getLevel().registryAccess());
        h.assertTrue(copy!=null&&copy.burn==burn&&copy.modules()==3&&copy.stored==be.stored&&copy.fuel.getStackInSlot(0).getCount()==1,"Reload lost fuel/output/modules");
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new PowerMenu(1,player.getInventory(),be);h.assertTrue(menu.value(0)==be.stored&&menu.value(1)==be.capacity()&&menu.value(5)==3&&!menu.getSlot(0).mayPlace(new ItemStack(Items.COAL)),"GUI truncated capacity or wrong fuel filter");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void solar_dimension_balance_and_no_fuel_storage(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.SOLAR_ARRAY.get());var be=(PowerBlockEntity)h.getBlockEntity(p);
        h.assertTrue(PowerBlockEntity.dimensionMultiplier("zerog_tweaks:eidolon")<PowerBlockEntity.dimensionMultiplier("minecraft:overworld")&&PowerBlockEntity.dimensionMultiplier("zerog_tweaks:solvane")>1,"Solar dimension balance failed");
        h.assertTrue(h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.UP)==null&&be.fuel.insertItem(0,new ItemStack(ItemInit.FUSION_DUST.get()),false).getCount()==1,"Solar exposed irrelevant fuel storage");
        h.setBlock(p.above(),net.minecraft.world.level.block.Blocks.STONE);h.assertTrue(be.solarRate(h.getLevel())==0,"Solar generated through roof");
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new PowerMenu(1,player.getInventory(),be);h.assertTrue(menu.slots.size()==37&&menu.solar(),"Solar module slot missing");
        var module=new ItemStack(net.zerog.tweaks.machine.CombustionRegistry.FLUX_MODULE.get(),3);
        h.assertTrue(menu.getSlot(0).mayPlace(module)&&!menu.getSlot(0).mayPlace(new ItemStack(Items.COAL)),"Solar module filter wrong");
        be.moduleInput.insertItem(0,module.copyWithCount(1),false);
        player.getInventory().setItem(9,module.copyWithCount(2));menu.quickMoveStack(player,1);
        h.assertTrue(be.modules()==3&&player.getInventory().getItem(9).isEmpty(),"Shift-click failed to install modules");
        be.stored=be.capacity();h.assertTrue(be.moduleInput.extractItem(0,3,false).isEmpty()&&be.modules()==3,"Module removal lost stored energy");
        be.stored=0;menu.quickMoveStack(player,0);h.assertTrue(be.modules()==0&&player.getInventory().countItem(net.zerog.tweaks.machine.CombustionRegistry.FLUX_MODULE.get())==3,"Module removal duplicated/lost items");h.succeed();
    }
}
