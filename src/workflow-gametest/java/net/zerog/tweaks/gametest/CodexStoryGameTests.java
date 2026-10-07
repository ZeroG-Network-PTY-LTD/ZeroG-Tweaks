package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.item.ConcordCodexItem;
import net.zerog.tweaks.lore.ConcordPrologue;

@GameTestHolder("zerog_codex_steps") @PrefixGameTestTemplate(false)
public final class CodexStoryGameTests {
    @GameTest(templateNamespace="zerog_codex_steps",template="equipment_empty",timeoutTicks=200)
    public static void milestone_pages_do_not_reveal_future_acts_or_other_readers(GameTestHelper h){
        h.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("productivebees"),"Use isolated no-PB mock reader world");
        var player=h.makeMockServerPlayerInLevel();
        player.setShiftKeyDown(true);
        var hand=net.minecraft.world.InteractionHand.MAIN_HAND;
        var item=net.zerog.tweaks.registry.ItemInit.CONCORD_CODEX.get();
        var book=new net.minecraft.world.item.ItemStack(item);player.setItemInHand(hand,book);
        ConcordPrologue.grant(player,"nova_pearl","has_nova_pearl");
        ConcordPrologue.grant(player,"heart_of_solvane","has_heart_of_solvane");
        h.assertTrue(!ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.act5_revelation"),"Inventory milestone spoiled an unvisited world");
        ConcordPrologue.grant(player,"root","has_raw_nullifite");item.use(h.getLevel(),player,hand);
        h.assertTrue(ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.step_signal")&&!ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.step_courier"),"Signal completed the next task automatically");
        ConcordPrologue.grant(player,"falling_star","found_pod");item.use(h.getLevel(),player,hand);
        h.assertTrue(ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.step_courier"),"Courier completion did not unlock instructions");
        var target=h.getLevel().getServer().getLevel(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:solvane")));
        h.assertTrue(target!=null,"Use lore preset for the arrival test; not an ecology/travel test");player.setServerLevel(target);item.use(target,player,hand);
        h.assertTrue(ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.act5_revelation")&&ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.act5_heart"),"Actual arrival plus milestones did not unlock final pages");
        var other=h.makeMockServerPlayerInLevel();other.setShiftKeyDown(true);other.setItemInHand(hand,book.copy());item.use(h.getLevel(),other,hand);
        var pages=other.getItemInHand(hand).get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages();
        h.assertTrue(pages.size()==4,"Borrowed book exposed another player's completed chapters");
        player.setServerLevel(h.getLevel());var saved=player.saveWithoutId(new net.minecraft.nbt.CompoundTag());player.load(saved);item.use(h.getLevel(),player,hand);
        h.assertTrue(ConcordCodexItem.pageKeys(player).contains("codex.zerog_tweaks.act5_revelation"),"Reload lost completed story pages");h.succeed();
    }
}
