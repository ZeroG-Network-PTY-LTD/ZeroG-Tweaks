package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.machine.ProcessingMenu;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class OreRefineryGameTests {
    private static OreRefineryBlockEntity place(GameTestHelper h){h.setBlock(new BlockPos(1,1,1),BlockInit.ORE_REFINERY.get());return (OreRefineryBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));}
    private static void tick(GameTestHelper h,OreRefineryBlockEntity be,int count){for(int i=0;i<count;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);}
    private static void power(GameTestHelper h,OreRefineryBlockEntity be){var cap=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),Direction.UP);h.assertTrue(cap!=null,"Missing refinery FE capability");cap.receiveEnergy(100_000,false);}

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void powered_recipe_boundary_invalid_catalyst_and_output_capacity(GameTestHelper h){
        var be=place(h);power(h,be);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_CYRRIUM.get(),2));
        be.inventory().setStackInSlot(1,new ItemStack(Items.DIAMOND,2));tick(h,be,199);
        h.assertTrue(be.progress()==199&&be.inventory().getStackInSlot(2).isEmpty(),"Refinery completed before200 ticks");tick(h,be,1);
        h.assertTrue(be.progress()==0&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(2).is(ItemInit.CYRRIUM_INGOT.get())&&be.inventory().getStackInSlot(2).getCount()==2,"Powered raw recipe did not produce two ingots");
        h.assertTrue(be.inventory().getStackInSlot(1).getCount()==2,"Unrelated catalyst was consumed");
        be.inventory().setStackInSlot(2,new ItemStack(ItemInit.CYRRIUM_INGOT.get(),63));int energy=be.stored;tick(h,be,220);
        h.assertTrue(be.progress()==0&&be.stored==energy&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(2).getCount()==63,"Blocked output spent FE or ingredients");
        be.inventory().setStackInSlot(2,ItemStack.EMPTY);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.CYRRIUM_ORE_ITEM.get()));tick(h,be,200);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.RAW_CYRRIUM.get())&&be.inventory().getStackInSlot(2).getCount()==2,"Authored ore-to-raw recipe was not loaded");h.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void actual_processing_menu_sided_ports_and_shift_click(GameTestHelper h){
        var be=place(h);power(h,be);var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        h.assertTrue(menu.slots.size()==43&&menu.stillValid(player),"Seven refinery machine slots/authority mismatch");
        h.assertTrue(!menu.getSlot(0).mayPlace(new ItemStack(Items.STONE))&&menu.getSlot(0).mayPlace(new ItemStack(ItemInit.RAW_CYRRIUM.get()))&&!menu.getSlot(1).mayPlace(new ItemStack(Items.DIAMOND))&&!menu.getSlot(2).mayPlace(new ItemStack(ItemInit.CYRRIUM_INGOT.get())),"Recipe input/catalyst/output filters failed");
        var output=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.DOWN);
        h.assertTrue(output!=null&&output.insertItem(0,new ItemStack(Items.STONE),false).getCount()==1,"Sided output accepted insertion");
        player.getInventory().setItem(9,new ItemStack(ItemInit.RAW_CYRRIUM.get(),3));h.assertTrue(!menu.quickMoveStack(player,7).isEmpty()&&be.inventory().getStackInSlot(0).getCount()==3&&player.getInventory().getItem(9).isEmpty(),"Refinery shift-click failed");
        tick(h,be,40);h.assertTrue(menu.value(2)==40&&menu.energy()==99_200,"Real progress/FE are not synchronized");
        be.inventory().setStackInSlot(2,new ItemStack(ItemInit.CYRRIUM_INGOT.get(),2));player.setPos(be.getBlockPos().getCenter().add(100,0,0));
        h.assertTrue(!menu.stillValid(player)&&menu.quickMoveStack(player,2).isEmpty(),"Remote menu extracted output");
        player.setPos(be.getBlockPos().getCenter());h.assertTrue(!menu.quickMoveStack(player,2).isEmpty()&&be.inventory().getStackInSlot(2).isEmpty(),"Output shift-click failed");h.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void paid_reload_and_real_stardust_catalyst(GameTestHelper h){
        var be=place(h);power(h,be);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_CYRRIUM.get(),2));tick(h,be,77);
        var restored=(OreRefineryBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(restored!=null&&restored.progress()==77&&restored.inventory().getSlots()==7&&restored.stored==98_460,"Paid job/slots/FE lost on reload");restored.setLevel(h.getLevel());tick(h,restored,123);
        h.assertTrue(restored.progress()==0&&restored.inventory().getStackInSlot(2).getCount()==2&&restored.stored==96_000,"Paid resumed job charged incorrectly");
        be.clearContent();be.inventory().setStackInSlot(0,new ItemStack(ItemInit.ARESITE.get(),2));tick(h,be,200);h.assertTrue(be.progress()==0&&be.inventory().getStackInSlot(2).isEmpty(),"Aresite boost ran without catalyst");
        be.inventory().setStackInSlot(1,new ItemStack(ItemInit.STARDUST.get(),2));tick(h,be,200);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.ARESITE.get())&&be.inventory().getStackInSlot(2).getCount()==5&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(1).getCount()==1,"Registered ZeroG Stardust route/catalyst count incorrect");
        var legacy=be.saveWithFullMetadata(h.getLevel().registryAccess());legacy.remove("RefiningFormat");legacy.putInt("Progress",199);legacy.getCompound("Inventory").putInt("Size",3);
        var migrated=(OreRefineryBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),legacy,h.getLevel().registryAccess());
        h.assertTrue(migrated!=null&&migrated.progress()==0&&migrated.inventory().getSlots()==7&&migrated.inventory().getStackInSlot(2).getCount()==5,"Legacy slots/output lost or unpaid progress inherited");h.succeed();
    }
}
