package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.worldgen.PlanetSettlementFeature;

@GameTestHolder("zerog_lore") @PrefixGameTestTemplate(false)
public final class SolLoreGameTests {
    @GameTest(templateNamespace="zerog_lore",template="equipment_empty",timeoutTicks=200)
    public static void every_rustborn_layout_contains_a_ground_level_aresite_shrine(GameTestHelper h){
        var level=h.getLevel();var centre=h.absolutePos(new BlockPos(96,24,96));
        for(int x=(centre.getX()-24)>>4;x<=(centre.getX()+24)>>4;x++)for(int z=(centre.getZ()-24)>>4;z<=(centre.getZ()+24)>>4;z++)level.getChunk(x,z);
        for(int layout=0;layout<4;layout++){
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,10,22)))level.setBlock(at,Blocks.AIR.defaultBlockState(),2);
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,0,22)))level.setBlock(at,ZGDimensionTerrain.SOILS.get("mars").get().defaultBlockState(),2);
            h.assertTrue(PlanetSettlementFeature.build(level,centre,"mars",layout,RandomSource.create(23)),"Rustborn layout rejected");
            int cores=0;
            for(var at:BlockPos.betweenClosed(centre.offset(-17,1,-17),centre.offset(17,5,17)))if(level.getBlockState(at).is(BlockInit.ARESITE_BLOCK.get())){
                cores++;h.assertTrue(level.getBlockState(at.below()).is(BlockInit.MARTIAN_STONE_BRICKS.get()),"Aresite core has no Mars pedestal");
            }
            h.assertTrue(cores==1,"Rustborn village must contain exactly one Aresite shrine, layout "+layout);
            h.assertTrue(level.getBlockState(centre).is(BlockInit.SETTLEMENT_ANCHOR.get()),"Shrine replaced settlement anchor");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_lore",template="equipment_empty",timeoutTicks=200)
    public static void codex_pages_localize_and_unlock_only_for_visited_planets(GameTestHelper h){
        h.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("productivebees"),"Mock book readers require isolated no-PB world: no real client handshake");
        var server=h.getLevel().getServer();
        var moon=server.getLevel(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:moon")));
        var mars=server.getLevel(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:mars")));
        h.assertTrue(moon!=null&&mars!=null,"Use planetary test preset: Moon/Mars levels must exist");
        var player=h.makeMockServerPlayerInLevel();
        player.setShiftKeyDown(true);
        var codex=net.zerog.tweaks.registry.ItemInit.CONCORD_CODEX.get();
        var book=new net.minecraft.world.item.ItemStack(codex);
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,book);
        codex.use(h.getLevel(),player,net.minecraft.world.InteractionHand.MAIN_HAND);
        h.assertTrue(book.get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages().size()==5,"Unvisited Act I pages revealed or builder instructions missing");
        // Real level context and real item use; this is not a portal/network test.
        player.setServerLevel(mars);codex.use(mars,player,net.minecraft.world.InteractionHand.MAIN_HAND);
        var pages=book.get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages();
        h.assertTrue(pages.size()==8,"Mars arrival must unlock its story and task pages only");
        h.assertTrue(pages.get(6).raw().getContents() instanceof net.minecraft.network.chat.contents.TranslatableContents c&&c.getKey().equals("codex.zerog_tweaks.mars_waystation"),"Mars page must use its language key");
        player.setServerLevel(moon);codex.use(moon,player,net.minecraft.world.InteractionHand.MAIN_HAND);
        pages=book.get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages();
        h.assertTrue(pages.size()==10,"Both visits must unlock both story/task pairs");
        h.assertTrue(pages.get(6).raw().getContents() instanceof net.minecraft.network.chat.contents.TranslatableContents c&&c.getKey().equals("codex.zerog_tweaks.moon_relay"),"Moon page must use its language key");
        player.setServerLevel(h.getLevel());codex.use(h.getLevel(),player,net.minecraft.world.InteractionHand.MAIN_HAND);
        h.assertTrue(book.get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages().size()==10,"Return to Overworld lost unlocked pages");
        var saved=player.saveWithoutId(new net.minecraft.nbt.CompoundTag());
        player.load(saved);codex.use(h.getLevel(),player,net.minecraft.world.InteractionHand.MAIN_HAND);
        h.assertTrue(player.getItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND).get(net.minecraft.core.component.DataComponents.WRITTEN_BOOK_CONTENT).pages().size()==10,"Saved player lost arrival unlocks");
        h.succeed();
    }
}
