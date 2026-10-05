package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class OreRefineryGameTests {
    private static OreRefineryBlockEntity place(GameTestHelper h){h.setBlock(new BlockPos(1,1,1),BlockInit.ORE_REFINERY.get());return (OreRefineryBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));}
    private static void tick(GameTestHelper h,OreRefineryBlockEntity be,int count){for(int i=0;i<count;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);}

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void exact_recipe_time_unrelated_catalyst_and_output_capacity(GameTestHelper h){
        var be=place(h);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_CYRRIUM.get(),2));
        // Old saves can contain invalid catalysts: preserve them, never eat them.
        be.inventory().setStackInSlot(1,new ItemStack(Items.DIAMOND,2));tick(h,be,199);
        h.assertTrue(be.progress()==199&&be.inventory().getStackInSlot(2).isEmpty(),"Refinery completed before200 ticks");tick(h,be,1);
        h.assertTrue(be.progress()==0&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(2).is(ItemInit.CYRRIUM_INGOT.get())&&be.inventory().getStackInSlot(2).getCount()==2,"Refinery did not complete exactly at200 ticks");
        h.assertTrue(be.inventory().getStackInSlot(1).getCount()==2,"Unrelated catalyst was consumed by catalyst-free recipe");
        be.inventory().setStackInSlot(2,new ItemStack(ItemInit.CYRRIUM_INGOT.get(),63));tick(h,be,220);
        h.assertTrue(be.progress()==0&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(2).getCount()==63,"Blocked output consumed or overfilled recipe");
        be.inventory().setStackInSlot(2,ItemStack.EMPTY);tick(h,be,50);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.ARESITE_ORE_ITEM.get()));
        h.assertTrue(be.progress()==0,"Input change inherited another recipe's partial progress");tick(h,be,200);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.ARESITE.get())&&be.inventory().getStackInSlot(2).getCount()==3&&be.inventory().getStackInSlot(1).getCount()==2,"Aresite ore recipe/catalyst conservation failed");
        be.inventory().setStackInSlot(2,ItemStack.EMPTY);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.CYRRIUM_ORE_ITEM.get()));tick(h,be,200);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.CYRRIUM_INGOT.get())&&be.inventory().getStackInSlot(2).getCount()==3,"Existing Cyrrium Ore yield changed");
        be.inventory().setStackInSlot(2,ItemStack.EMPTY);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_NULLIFITE_BLOCK_ITEM.get()));tick(h,be,200);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.NULLIFITE_INGOT.get())&&be.inventory().getStackInSlot(2).getCount()==2&&be.inventory().getStackInSlot(1).getCount()==2,"Existing Raw Nullifite Block yield/catalyst changed");h.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void three_machine_slots_filters_shift_click_and_authority(GameTestHelper h){
        var be=place(h);var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new OreRefineryMenu(MenuInit.ORE_REFINERY.get(),1,player.getInventory(),be);
        h.assertTrue(menu.slots.size()==39&&menu.stillValid(player),"Refinery slots/authority mismatch");
        h.assertTrue(!menu.getSlot(0).mayPlace(new ItemStack(Items.STONE))&&menu.getSlot(0).mayPlace(new ItemStack(ItemInit.RAW_CYRRIUM.get()))&&!menu.getSlot(1).mayPlace(new ItemStack(Items.DIAMOND))&&!menu.getSlot(2).mayPlace(new ItemStack(ItemInit.CYRRIUM_INGOT.get())),"Input/catalyst/output filters failed");
        h.assertTrue(be.inventory().insertItem(2,new ItemStack(Items.STONE),false).getCount()==1,"Handler output accepted insertion");
        player.getInventory().setItem(9,new ItemStack(ItemInit.RAW_CYRRIUM.get(),3));h.assertTrue(!menu.quickMoveStack(player,3).isEmpty()&&be.inventory().getStackInSlot(0).getCount()==3&&player.getInventory().getItem(9).isEmpty(),"Refinery input shift-click failed");
        tick(h,be,40);h.assertTrue(menu.progressPercent()==20,"Server menu progress not synchronized from real processing");
        player.getInventory().setItem(10,new ItemStack(Items.STONE,4));h.assertTrue(menu.quickMoveStack(player,4).isEmpty()&&player.getInventory().getItem(10).getCount()==4,"Invalid item shift-click mutated inventory");
        be.inventory().setStackInSlot(2,new ItemStack(ItemInit.CYRRIUM_INGOT.get(),2));player.setPos(be.getBlockPos().getCenter().add(100,0,0));
        h.assertTrue(!menu.stillValid(player)&&menu.quickMoveStack(player,2).isEmpty()&&be.inventory().getStackInSlot(2).getCount()==2,"Remote menu extracted output");
        player.setPos(be.getBlockPos().getCenter());h.assertTrue(!menu.quickMoveStack(player,2).isEmpty()&&be.inventory().getStackInSlot(2).isEmpty(),"Output shift-click failed");h.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void progress_persistence_and_optional_stardust_recipe(GameTestHelper h){
        var be=place(h);be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_CYRRIUM.get(),2));tick(h,be,77);
        var restored=(OreRefineryBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(restored!=null&&restored.progress()==77&&restored.inventory().getStackInSlot(0).getCount()==2,"Refinery job/inventory lost on reload");restored.setLevel(h.getLevel());tick(h,restored,123);
        h.assertTrue(restored.progress()==0&&restored.inventory().getStackInSlot(2).getCount()==2&&restored.inventory().getStackInSlot(0).getCount()==1,"Resumed job did not complete at saved200-tick boundary");
        be.clearContent();be.inventory().setStackInSlot(0,new ItemStack(ItemInit.ARESITE.get(),2));tick(h,be,200);h.assertTrue(be.progress()==0&&be.inventory().getStackInSlot(2).isEmpty()&&be.inventory().getStackInSlot(0).getCount()==2,"Aresite boost ran without required stardust");
        var id=ResourceLocation.parse("aeroapiary:stardust");if(BuiltInRegistries.ITEM.containsKey(id)){
            var dust=new ItemStack(BuiltInRegistries.ITEM.get(id),2);h.assertTrue(be.inventory().isItemValid(1,dust),"Optional registered stardust rejected");be.inventory().setStackInSlot(1,dust);tick(h,be,200);
            h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.ARESITE.get())&&be.inventory().getStackInSlot(2).getCount()==5&&be.inventory().getStackInSlot(0).getCount()==1&&be.inventory().getStackInSlot(1).getCount()==1,"Stardust boost did not consume exactly one actual catalyst");
        }h.succeed();
    }
}
