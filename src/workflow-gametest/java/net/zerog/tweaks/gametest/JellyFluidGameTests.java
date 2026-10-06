package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.BucketItem;
import net.minecraft.world.level.block.BucketPickup;
import net.neoforged.neoforge.fluids.FluidUtil;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_blockers") @PrefixGameTestTemplate(false)
public final class JellyFluidGameTests {
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void royal_jelly_bucket_places_collectable_source(GameTestHelper h) {
        collect(h,"royal_jelly");
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void cosmic_jelly_bucket_places_collectable_source(GameTestHelper h) {
        collect(h,"cosmic_jelly");
    }
    private static void collect(GameTestHelper h,String name) {
        var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name);
        var bucketId=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name+"_bucket");
        h.assertTrue(BuiltInRegistries.FLUID.containsKey(id),"Royal Jelly has no registered fluid for the splicer");
        h.assertTrue(BuiltInRegistries.ITEM.containsKey(bucketId),"Royal Jelly has no collectable bucket");
        var fluid=BuiltInRegistries.FLUID.get(id);
        var bucket=BuiltInRegistries.ITEM.get(bucketId);
        h.assertTrue(bucket instanceof BucketItem,"Jelly container is not a vanilla-compatible bucket");
        var pos=h.absolutePos(new BlockPos(2,2,2));
        h.assertTrue(((BucketItem)bucket).emptyContents(h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL),h.getLevel(),pos,null),"Jelly bucket cannot place its source");
        var state=h.getLevel().getBlockState(pos);
        h.assertTrue(state.getBlock() instanceof BucketPickup,"Jelly source cannot be picked up");
        var filled=((BucketPickup)state.getBlock()).pickupBlock(null,h.getLevel(),pos,state);
        h.assertTrue(filled.is(bucket),"Picking up Jelly did not return its own bucket");
        h.assertTrue(FluidUtil.getFluidContained(filled).map(s->s.getFluid()==fluid&&s.getAmount()==1000).orElse(false),"Collected bucket does not contain 1000 mB Jelly");
        h.assertTrue(h.getLevel().getFluidState(pos).isEmpty(),"Bucket pickup duplicated the source");
        h.succeed();
    }
}
