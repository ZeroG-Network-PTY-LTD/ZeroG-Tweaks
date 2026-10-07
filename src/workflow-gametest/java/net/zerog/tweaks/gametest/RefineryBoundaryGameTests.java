package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_blockers") @PrefixGameTestTemplate(false)
public final class RefineryBoundaryGameTests {
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void legacy_yield_reserves_capacity_and_reloads_paid_job(GameTestHelper h) {
        var local=new BlockPos(1,1,1);h.setBlock(local,BlockInit.ORE_REFINERY.get());
        var be=(OreRefineryBlockEntity)h.getBlockEntity(local);
        var energy=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),Direction.UP);
        h.assertTrue(energy!=null,"Missing refinery energy port");energy.receiveEnergy(100_000,false);
        var remainder=be.inventory().insertItem(3,new ItemStack(BlockInit.CYRRIUM_CASING.get(),2),false);
        h.assertTrue(remainder.getCount()==2&&be.inventory().getStackInSlot(3).isEmpty(),"New casing upgrades bypass the approved card-only migration");
        // Fixture represents an already-installed pre-card casing, not new player insertion.
        be.inventory().setStackInSlot(3,new ItemStack(BlockInit.CYRRIUM_CASING.get()));
        be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_NULLIFITE_BLOCK_ITEM.get()));
        be.inventory().setStackInSlot(2,new ItemStack(ItemInit.NULLIFITE_INGOT.get(),40));
        for(int i=0;i<200;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.stored==100_000&&be.progress()==0&&be.inventory().getStackInSlot(0).getCount()==1,"Upgraded27 output was not reserved before spending FE");
        be.inventory().setStackInSlot(2,ItemStack.EMPTY);
        for(int i=0;i<80;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        var restored=(OreRefineryBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(restored!=null&&restored.progress()==80&&restored.stored==82_900,"Upgraded partially paid job did not survive reload");
        restored.setLevel(h.getLevel());for(int i=0;i<80;i++)OreRefineryBlockEntity.tick(h.getLevel(),restored.getBlockPos(),restored.getBlockState(),restored);
        h.assertTrue(restored.inventory().getStackInSlot(2).getCount()==27&&restored.stored==65_800&&restored.inventory().getStackInSlot(0).isEmpty(),"Upgraded job duplicated charge/output or changed nine-raw yield");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void refinery_requires_real_energy_and_preserves_raw_block_yield(GameTestHelper h) {
        var local=new BlockPos(1,1,1);h.setBlock(local,BlockInit.ORE_REFINERY.get());
        var be=(OreRefineryBlockEntity)h.getBlockEntity(local);
        be.inventory().setStackInSlot(0,new ItemStack(ItemInit.RAW_NULLIFITE_BLOCK_ITEM.get()));
        for(int i=0;i<400;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory().getStackInSlot(2).isEmpty(),"Refinery manufactured unpaid output");
        var energy=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),Direction.UP);
        h.assertTrue(energy!=null&&energy.receiveEnergy(100_000,false)>0,"Refinery has no actual FE input");
        for(int i=0;i<400;i++)OreRefineryBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory().getStackInSlot(2).is(ItemInit.NULLIFITE_INGOT.get())&&be.inventory().getStackInSlot(2).getCount()==18,"Nine raw units must refine to eighteen, not two");
        h.succeed();
    }
}
