package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.storage.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class WoodStorageGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void eight_containers_upgrade_reload_and_automation(GameTestHelper h) {
        int i=0;
        for (var holder : WoodStorageRegistry.CONTAINERS.values()) {
            var pos=new BlockPos(1+i%4,1,1+i/4);i++;
            h.setBlock(pos,holder.get());
            var be=(WoodStorageBlockEntity)h.getBlockEntity(pos);
            h.assertTrue(be.getContainerSize()==27,"Base container not 27 slots");
            var handler=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),Direction.DOWN);
            h.assertTrue(handler!=null&&handler.insertItem(0,new ItemStack(Items.DIAMOND,5),false).isEmpty(),"Storage automation failed");
            h.assertTrue(be.expand()&&!be.expand()&&handler.getSlots()==54,"Independent expansion limit/capability failed");
            be.setItem(53,new ItemStack(Items.EMERALD,3));
            var copy=(WoodStorageBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
            h.assertTrue(copy!=null&&copy.expanded()&&copy.getItem(0).getCount()==5&&copy.getItem(53).getCount()==3,"Expanded contents lost during reload");
            var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
            player.setPos(be.getBlockPos().getCenter());
            var menu=be.createMenu(1,player.getInventory(),player);
            h.assertTrue(menu!=null&&menu.slots.size()==90,"Expanded menu slot geometry failed");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void break_drops_contents_and_one_expansion_module(GameTestHelper h) {
        var pos=new BlockPos(2,1,2);
        h.setBlock(pos,WoodStorageRegistry.CONTAINERS.get("shardwood_chest").get());
        var be=(WoodStorageBlockEntity)h.getBlockEntity(pos);
        be.expand();be.setItem(0,new ItemStack(Items.DIAMOND,5));be.setItem(53,new ItemStack(Items.EMERALD,3));
        h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
        var absolute=h.absolutePos(pos);
        var drops=h.getLevel().getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,new net.minecraft.world.phys.AABB(absolute).inflate(2));
        int diamonds=0,emeralds=0,modules=0;
        for(var drop:drops){var stack=drop.getItem();if(stack.is(Items.DIAMOND))diamonds+=stack.getCount();if(stack.is(Items.EMERALD))emeralds+=stack.getCount();if(stack.is(WoodStorageRegistry.EXPANSION.get()))modules+=stack.getCount();}
        h.assertTrue(diamonds==5&&emeralds==3&&modules==1,"Container destruction lost or duplicated contents/module");
        h.succeed();
    }
}
