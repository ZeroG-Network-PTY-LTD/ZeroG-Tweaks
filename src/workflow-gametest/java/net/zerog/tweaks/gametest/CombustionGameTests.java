package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.machine.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class CombustionGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void coal_generation_pause_reload_and_input_filter(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BlockInit.COMBUSTION_GENERATOR.get());var be=(CombustionBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        h.assertTrue(!be.fuel.isItemValid(0,new ItemStack(Items.STONE)),"Invalid fuel accepted");be.fuel.setStackInSlot(0,new ItemStack(Items.CHARCOAL,2));
        CombustionBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.stored==50&&be.burn==1599&&be.fuel.getStackInSlot(0).getCount()==1,"Charcoal did not produce FE");
        be.stored=100000;int burn=be.burn;CombustionBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);h.assertTrue(be.burn==burn,"Full generator wasted fuel");
        var copy=(CombustionBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(copy.stored==100000&&copy.burn==burn&&copy.fuel.getStackInSlot(0).getCount()==1,"Generator state lost on reload");h.succeed();
    }
}
