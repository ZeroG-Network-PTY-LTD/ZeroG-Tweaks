package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class CombustionUpgradeGameTests {
    private static CombustionBlockEntity place(GameTestHelper h,BlockPos pos){h.setBlock(pos,BlockInit.COMBUSTION_GENERATOR.get());return (CombustionBlockEntity)h.getBlockEntity(pos);}
    private static void ticks(GameTestHelper h,CombustionBlockEntity be,int count){for(int i=0;i<count;i++)CombustionBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);}

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void modules_output_reload_and_single_break_refund(GameTestHelper h){
        var pos=new BlockPos(1,1,1);var be=place(h,pos);var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(CombustionRegistry.FLUX_MODULE.get(),4));
        var hit=new BlockHitResult(be.getBlockPos().getCenter(),Direction.NORTH,be.getBlockPos(),false);
        for(int level=0;level<=3;level++){
            if(level>0){be.getBlockState().useItemOn(player.getMainHandItem(),h.getLevel(),player,InteractionHand.MAIN_HAND,hit);h.assertTrue(be.upgrades()==level&&player.getMainHandItem().getCount()==4-level,"Module use did not consume exactly one installation");}
            h.assertTrue(be.capacity()==100000*(level+1)&&be.energy.getMaxEnergyStored()==be.capacity(),"Upgrade buffer mismatch");
            be.stored=0;be.burn=be.burnTotal=100;be.output=50;ticks(h,be,4);
            h.assertTrue(be.stored==200+level*50&&be.burn==96,"Quarter-FE upgrade output lost precision or burned extra fuel");
        }
        int before=be.stored;be.getBlockState().useItemOn(player.getMainHandItem(),h.getLevel(),player,InteractionHand.MAIN_HAND,hit);
        h.assertTrue(be.upgrades()==3&&player.getMainHandItem().getCount()==1&&be.stored==before,"Fourth module consumed or generated energy");
        be.stored=be.capacity();int burn=be.burn;ticks(h,be,1);h.assertTrue(be.burn==burn&&be.stored==400000,"Full upgraded buffer wasted fuel");
        be.stored=0;ticks(h,be,1);var tag=be.saveWithFullMetadata(h.getLevel().registryAccess());
        var copy=(CombustionBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),tag,h.getLevel().registryAccess());
        h.assertTrue(copy!=null&&copy.upgrades()==3&&copy.capacity()==400000&&copy.stored==87&&copy.burn==burn-1&&tag.getInt("quarter_remainder")==2,"Upgrade save/reload lost fractional output or burn state");
        copy.setLevel(h.getLevel());ticks(h,copy,1);h.assertTrue(copy.stored==175,"Reloaded fractional remainder was lost");
        tag.remove("flux_modules");tag.remove("quarter_remainder");tag.putInt("energy",100000);
        var legacy=(CombustionBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),tag,h.getLevel().registryAccess());
        h.assertTrue(legacy!=null&&legacy.upgrades()==0&&legacy.capacity()==100000&&legacy.stored==100000,"Legacy save compatibility failed");
        be.fuel.setStackInSlot(0,new ItemStack(Items.COAL,2));be.stored=12345;h.setBlock(pos,Blocks.AIR);h.setBlock(pos,Blocks.AIR);
        int modules=0,coal=0;for(var drop:h.getLevel().getEntitiesOfClass(ItemEntity.class,new AABB(be.getBlockPos()).inflate(2))){if(drop.getItem().is(CombustionRegistry.FLUX_MODULE.get()))modules+=drop.getItem().getCount();if(drop.getItem().is(Items.COAL))coal+=drop.getItem().getCount();}
        h.assertTrue(modules==3&&coal==2&&be.stored==0&&be.burn==0,"Break duplicated/lost modules or fuel, or retained stored energy");h.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void menu_slots_sync_filters_shift_click_and_authority(GameTestHelper h){
        var be=place(h,new BlockPos(1,1,1));var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        be.installModule();be.installModule();be.installModule();be.stored=399999;be.burn=70;be.burnTotal=100;be.output=50;
        var menu=new CombustionMenu(1,player.getInventory(),be);
        h.assertTrue(menu.getType()==CombustionRegistry.MENU.get()&&menu.slots.size()==37&&menu.stillValid(player),"Generator menu type/slots/authority mismatch");
        h.assertTrue(menu.energy()==399999&&menu.capacity()==400000&&menu.value(2)==70&&menu.value(3)==100&&menu.value(4)==3&&menu.value(5)==350,"GUI energy/burn/module/rate data truncated");
        h.assertTrue(!menu.getSlot(0).mayPlace(new ItemStack(Items.STONE))&&menu.getSlot(0).mayPlace(new ItemStack(Items.COAL)),"GUI fuel filter accepts invalid items");
        player.getInventory().setItem(9,new ItemStack(Items.COAL,3));h.assertTrue(!menu.quickMoveStack(player,1).isEmpty()&&be.fuel.getStackInSlot(0).getCount()==3&&player.getInventory().getItem(9).isEmpty(),"Fuel shift-click not conserved");
        player.getInventory().setItem(10,new ItemStack(Items.STONE,2));h.assertTrue(menu.quickMoveStack(player,2).isEmpty()&&player.getInventory().getItem(10).getCount()==2,"Invalid shift-click changed inventory");
        player.setPos(be.getBlockPos().getCenter().add(100,0,0));h.assertTrue(!menu.stillValid(player)&&menu.quickMoveStack(player,0).isEmpty()&&be.fuel.getStackInSlot(0).getCount()==3,"Remote menu removed fuel");
        player.setPos(be.getBlockPos().getCenter());h.assertTrue(!menu.quickMoveStack(player,0).isEmpty()&&be.fuel.getStackInSlot(0).isEmpty(),"Fuel extraction shift-click failed");
        var replacement=new CombustionBlockEntity(be.getBlockPos(),be.getBlockState());h.getLevel().setBlockEntity(replacement);
        h.assertTrue(!menu.stillValid(player),"Stale generator menu remained valid after block-entity replacement");h.succeed();
    }
}
