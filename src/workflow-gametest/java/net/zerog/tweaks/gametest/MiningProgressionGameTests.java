package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

@GameTestHolder("zerog_blockers") @PrefixGameTestTemplate(false)
public final class MiningProgressionGameTests {
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void moonsteel_requires_ferrox_and_reports_requirement(GameTestHelper h){
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        var ore=BlockInit.MOONSTEEL_ORE.get().defaultBlockState();
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(ItemInit.NULLIFITE_PICKAXE.get()));
        h.assertTrue(!player.hasCorrectToolForDrops(ore),"Nullifite bypasses approved Ferrox gate");
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(ItemInit.FERROX_PICKAXE.get()));
        h.assertTrue(player.hasCorrectToolForDrops(ore),"Ferrox cannot mine Moonsteel");
        h.assertTrue(net.zerog.tweaks.event.MiningRequirements.requirement(ore).getString().contains("Ferrox"),"Moonsteel requirement is not shown");
        var pos=h.absolutePos(new net.minecraft.core.BlockPos(2,2,2));h.getLevel().setBlock(pos,ore,3);
        var drops=net.minecraft.world.level.block.Block.getDrops(ore,h.getLevel(),pos,null,player,player.getMainHandItem());
        h.assertTrue(drops.stream().anyMatch(s->s.is(ItemInit.RAW_MOONSTEEL.get())),"Valid Moonsteel loot lacks raw material");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void all_tier_tagged_blocks_require_tools(GameTestHelper h){
        for(var block:net.minecraft.core.registries.BuiltInRegistries.BLOCK){
            var key=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(block);if(!key.getNamespace().equals("zerog_tweaks"))continue;
            if(block.builtInRegistryHolder().tags().anyMatch(t->t.location().getPath().startsWith("needs_")&&t.location().getPath().endsWith("_tool")))
                h.assertTrue(block.defaultBlockState().requiresCorrectToolForDrops(),"Tier-tagged block bypasses mining gate: "+key);
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_blockers",template="equipment_empty",timeoutTicks=100)
    public static void cerulite_rejects_bare_hand_and_low_tier_accepts_correct_pick(GameTestHelper h){
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);var ore=BlockInit.CERULITE_ORE.get().defaultBlockState();
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,ItemStack.EMPTY);
        h.assertTrue(!player.hasCorrectToolForDrops(ore),"Bare hand bypasses Cerulite mining gate");
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(Items.WOODEN_PICKAXE));
        h.assertTrue(!player.hasCorrectToolForDrops(ore),"Wooden pick bypasses Cerulite mining gate");
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(ItemInit.CERULITE_PICKAXE.get()));
        h.assertTrue(player.hasCorrectToolForDrops(ore),"Cerulite pick rejected by its own ore");
        h.succeed();
    }
}
