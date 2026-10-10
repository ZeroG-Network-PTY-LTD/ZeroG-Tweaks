package net.zerog.tweaks.gametest;

import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.item.*;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.power.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class GeneratorRecipeGameTests {
    @GameTest(templateNamespace="zerog_recipe_generators",template="equipment_empty",timeoutTicks=100)
    public static void combustion_catalogue_matches_complete_burns(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        for(var item:new net.minecraft.world.level.ItemLike[]{Items.COAL,Items.OAK_PLANKS,Items.STICK,ItemInit.EMBERITE.get()})for(int modules=0;modules<=3;modules++){
            h.setBlock(pos,Blocks.AIR);h.setBlock(pos,BlockInit.COMBUSTION_GENERATOR.get());
            var be=(CombustionBlockEntity)h.getBlockEntity(pos);
            for(var side:Direction.values())be.setFaceDisabled(side,false,true);
            for(int i=0;i<modules;i++)h.assertTrue(be.installModule(),"Module install failed");
            var fuel=new ItemStack(item,2);var budget=GeneratorRecipeCatalogue.combustion(fuel,modules);
            h.assertTrue(budget.ticks()>0,"Catalogue lost valid fuel");be.fuel.insertItem(0,fuel,false);
            long produced=0;
            for(int tick=0;tick<budget.ticks();tick++){
                CombustionBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
                produced+=be.energy.extractEnergy(Integer.MAX_VALUE,false);
            }
            h.assertTrue(produced==budget.energy()&&be.burn==0&&be.fuel.getStackInSlot(0).getCount()==1,"Catalogue disagrees with real combustion burn");
            be.stored=be.capacity();CombustionBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
            h.assertTrue(be.burn==0&&be.fuel.getStackInSlot(0).getCount()==1,"Full buffer consumed next fuel");
            h.assertTrue(GeneratorRecipeCatalogue.combustion(new ItemStack(ItemInit.FUSION_DUST.get()),modules).ticks()==0,"Dust advertised as combustion fuel");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_recipe_generators",template="equipment_empty",timeoutTicks=100)
    public static void fusion_catalogue_and_synced_configuration(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        for(int modules=0;modules<=3;modules++){
            h.setBlock(pos,Blocks.AIR);h.setBlock(pos,BlockInit.FUSION_REACTOR.get());var be=(PowerBlockEntity)h.getBlockEntity(pos);
            for(var side:Direction.values())be.setOutputDisabled(side,true);
            for(int i=0;i<modules;i++)be.installModule();
            var budget=GeneratorRecipeCatalogue.fusion(PowerConfig.FUSION_RATE.get(),PowerConfig.FUSION_TICKS.get(),modules,be.capacity());
            be.fuel.insertItem(0,new ItemStack(ItemInit.FUSION_DUST.get(),2),false);long produced=0;
            for(int tick=0;tick<budget.ticks();tick++){
                PowerBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
                while(be.stored>0)produced+=be.energy.extractEnergy(Integer.MAX_VALUE,false);
            }
            h.assertTrue(produced==budget.energy()&&be.burn==0&&be.fuel.getStackInSlot(0).getCount()==1,"Fusion catalogue disagrees with real burn");
            var player=h.makeMockPlayer(GameType.SURVIVAL);var menu=new PowerMenu(1,player.getInventory(),be);
            h.assertTrue(menu.configured(0)==PowerConfig.FUSION_RATE.get()&&menu.configured(1)==PowerConfig.FUSION_TICKS.get()&&menu.configured(2)==PowerConfig.TRANSFER.get(),"Recipe menu lost authoritative configuration");
            h.assertTrue(!menu.getSlot(0).mayPlace(new ItemStack(Items.COAL)),"Fusion menu accepts wrong fuel");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_recipe_generators",template="equipment_empty",timeoutTicks=100)
    public static void solar_recipe_has_no_fuel_and_preserves_controls(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.SOLAR_ARRAY.get());var be=(PowerBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new PowerMenu(1,player.getInventory(),be);
        h.assertTrue(menu.solar()&&menu.slots.size()==37&&!menu.getSlot(0).mayPlace(new ItemStack(Items.COAL)),"Solar catalogue implies a fuel input");
        h.setBlock(pos.above(),Blocks.STONE);PowerBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(menu.value(4)==0,"Covered solar page advertises generation");
        h.assertTrue(menu.clickMenuButton(player,100)&&menu.outputDisabled(0),"Appended recipe data broke power controls");
        h.assertTrue(!menu.clickMenuButton(player,200),"Solar accepted imaginary fuel-face control");h.succeed();
    }
}
