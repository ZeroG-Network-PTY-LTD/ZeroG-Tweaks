package net.zerog.tweaks.gametest;

import java.util.HashSet;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.BucketItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BucketPickup;
import net.minecraft.world.level.material.FlowingFluid;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.CreativeTabs;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class LiquidBucketGameTests {
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=200)
    public static void all_liquid_ids_bucket_collection_and_categories(GameTestHelper helper) {
        var level = helper.getLevel();
        var pos = helper.absolutePos(new BlockPos(3,130,3));
        var sources = BuiltInRegistries.FLUID.stream().filter(fluid ->
                BuiltInRegistries.FLUID.getKey(fluid).getNamespace().equals("zerog_tweaks")
                && fluid instanceof FlowingFluid && fluid.defaultFluidState().isSource()).toList();
        helper.assertTrue(sources.size()==20,"Expected 18 planetary/honey fluids plus Royal and Cosmic Jelly");
        var buckets = new HashSet<net.minecraft.world.item.Item>();
        for (var fluid : sources) {
            String id = BuiltInRegistries.FLUID.getKey(fluid).toString();
            helper.assertTrue(fluid.getBucket() instanceof BucketItem,"Missing bucket: "+id);
            var bucket = (BucketItem)fluid.getBucket();
            helper.assertTrue(net.neoforged.neoforge.fluids.FluidUtil.getFluidContained(new ItemStack(bucket))
                    .map(contents -> contents.getFluid()==fluid).orElse(false),"Bucket refers to wrong colour/family: "+id);
            helper.assertTrue(buckets.add(bucket),"Two fluid IDs share a bucket: "+id);
            var flowing = ((FlowingFluid)fluid).getFlowing();
            helper.assertTrue(flowing != fluid && fluid.isSame(flowing),"Missing compatible flowing form: "+id);
            helper.assertTrue(BuiltInRegistries.FLUID.getKey(flowing).getNamespace().equals("zerog_tweaks"),"Flowing form not registered: "+id);
            level.setBlock(pos.below(),Blocks.STONE.defaultBlockState(),3);
            level.setBlock(pos,Blocks.AIR.defaultBlockState(),3);
            helper.assertTrue(bucket.emptyContents(null,level,pos,null,new ItemStack(bucket)),"Cannot place bucket: "+id);
            var state = level.getBlockState(pos);
            helper.assertTrue(state.getFluidState().isSource() && state.getFluidState().getType()==fluid,"Wrong placed liquid: "+id);
            helper.assertTrue(state.getBlock() instanceof BucketPickup,"Liquid is not collectable: "+id);
            var collected = ((BucketPickup)state.getBlock()).pickupBlock(null,level,pos,state);
            helper.assertTrue(collected.is(bucket) && level.getBlockState(pos).isAir(),"Source collection returned wrong bucket: "+id);
            level.setBlock(pos,((FlowingFluid)fluid).getFlowing(3,false).createLegacyBlock(),3);
            var current = level.getBlockState(pos);
            helper.assertTrue(((BucketPickup)current.getBlock()).pickupBlock(null,level,pos,current).isEmpty(),"Flowing liquid incorrectly collectable: "+id);
            level.setBlock(pos,Blocks.AIR.defaultBlockState(),3);
        }
        helper.assertTrue(CreativeTabs.planetaryLiquidItems().size()==8,"Liquid tab must contain six planetary and two jelly buckets");
        helper.assertTrue(CreativeTabs.honeyLiquidItems().size()==12,"Honey tab must contain twelve buckets");
        var listed = new HashSet<>(CreativeTabs.planetaryLiquidItems());
        helper.assertTrue(listed.addAll(CreativeTabs.honeyLiquidItems()),"Honey category empty");
        helper.assertTrue(listed.equals(buckets) && CreativeTabs.liquidItems().size()==20,"Creative categories omit a bucket");
        helper.succeed();
    }
}
