package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.genetics.GeneticsIntegration;
import net.zerog.tweaks.genetics.GeneticsTank;

@GameTestHolder("zerog_jelly_machine") @PrefixGameTestTemplate(false)
public final class JellyMachineInteractionGameTests {
    @GameTest(templateNamespace="zerog_jelly_machine",template="equipment_empty",timeoutTicks=100)
    public static void filled_bucket_click_fills_splicer_not_old_menu(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:genetic_splicer")));
        var be=h.getBlockEntity(pos);h.assertTrue(be!=null,"Addon splicer fixture missing");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:royal_jelly_bucket"))));
        var event=new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,be.getBlockPos(),new BlockHitResult(be.getBlockPos().getCenter(),Direction.NORTH,be.getBlockPos(),false));
        GeneticsIntegration.open(event);
        h.assertTrue(event.isCanceled()&&new GeneticsTank(be).amount()==1000,"Filled bucket click did not transfer jelly into splicer");
        h.assertTrue(player.getMainHandItem().is(Items.BUCKET),"Survival bucket was not returned");h.succeed();
    }
}
