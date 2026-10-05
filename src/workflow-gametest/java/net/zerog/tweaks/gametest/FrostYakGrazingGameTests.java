package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.entity.FrostYak;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.EntityInit;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class FrostYakGrazingGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void shearing_cannot_repeat_and_only_approved_ground_regrows_wool(GameTestHelper h){
        FrostYak yak=EntityInit.FROST_YAK.get().create(h.getLevel());
        var feet=h.absolutePos(new BlockPos(2,2,2));yak.setPos(feet.getX()+.5,feet.getY(),feet.getZ()+.5);
        var shears=new ItemStack(Items.SHEARS);
        h.assertTrue(!yak.onSheared(null,shears,h.getLevel(),feet).isEmpty()&&yak.isSheared(),"First shearing failed");
        h.assertTrue(yak.onSheared(null,shears,h.getLevel(),feet).isEmpty(),"Repeated direct shearing duplicates wool");
        h.getLevel().setBlockAndUpdate(feet.below(),net.minecraft.world.level.block.Blocks.STONE.defaultBlockState());
        h.assertTrue(!yak.grazeForWool()&&yak.isSheared(),"Unapproved ground regrew wool");
        var tag=new net.minecraft.nbt.CompoundTag();yak.addAdditionalSaveData(tag);
        FrostYak restored=EntityInit.FROST_YAK.get().create(h.getLevel());restored.readAdditionalSaveData(tag);
        h.assertTrue(restored.isSheared(),"Sheared state lost on reload");
        h.getLevel().setBlockAndUpdate(feet.below(),BlockInit.FROZEN_REGOLITH.get().defaultBlockState());
        h.assertTrue(yak.grazeForWool()&&!yak.isSheared(),"Approved frozen regolith did not restore wool");
        h.succeed();
    }
}
