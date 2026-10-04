package net.zerog.tweaks.gametest;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.*;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;
import net.zerog.tweaks.lore.ConcordPrologue;

@GameTestHolder("zerog_prologue")
@PrefixGameTestTemplate(false)
public final class ConcordPrologueGameTests {
    @BeforeBatch(batch="prologue")
    public static void mature_disposable_world_clock(net.minecraft.server.level.ServerLevel level) {
        // Recovery timestamps must stay nonnegative. Age the disposable world
        // before test clocks start, never jump time during an active test.
        level.getServer().getWorldData().overworldData().setGameTime(ConcordPrologue.RECOVERY_TICKS+1000);
    }
    @GameTest(batch="prologue",templateNamespace="zerog_prologue",template="equipment_empty",timeoutTicks=400)
    public static void hard_recipe_codex_native_book_and_backup_loot(GameTestHelper helper) {
        var level=helper.getLevel();var recipe=level.getRecipeManager().byKey(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gate_controller")).orElseThrow().value();
        var ingredients=new ArrayList<ItemStack>();
        for(Item item:List.of(ItemInit.NULLIFITE_INGOT.get(),Items.TINTED_GLASS,ItemInit.NULLIFITE_INGOT.get(),
            Items.REDSTONE,ItemInit.NULLIFITE_GATE_FRAME_ITEM.get(),Items.REDSTONE,
            ItemInit.NULLIFITE_INGOT.get(),ItemInit.DORMANT_WISP.get(),ItemInit.NULLIFITE_INGOT.get()))ingredients.add(new ItemStack(item));
        var shaped=(net.minecraft.world.item.crafting.CraftingRecipe)recipe;
        var input=CraftingInput.of(3,3,ingredients);
        helper.assertTrue(shaped.matches(input,level),"Wisp recipe rejected");
        helper.assertTrue(shaped.assemble(input,level.registryAccess()).is(ItemInit.GATE_CONTROLLER_ITEM.get()),"Wrong crafted result");
        ingredients.set(7,new ItemStack(Items.REDSTONE_BLOCK));
        helper.assertTrue(!shaped.matches(CraftingInput.of(3,3,ingredients),level),"Legacy recipe bypasses hard gate");
        ingredients.set(7,ItemStack.EMPTY);
        helper.assertTrue(!shaped.matches(CraftingInput.of(3,3,ingredients),level),"Empty Wisp slot bypasses hard gate");
        var codex=new ItemStack(ItemInit.CONCORD_CODEX.get());
        helper.assertTrue(codex.get(DataComponents.WRITTEN_BOOK_CONTENT).pages().size()==3,"Native Codex pages missing");
        var player=helper.makeMockServerPlayerInLevel();player.setItemInHand(InteractionHand.MAIN_HAND,codex);
        ItemInit.CONCORD_CODEX.get().use(level,player,InteractionHand.MAIN_HAND);
        var advancement=player.server.getAdvancements().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","codex/builders_template"));
        helper.assertTrue(player.getAdvancements().getOrStartProgress(advancement).isDone(),"Codex read did not grant advancement");
        var ancient=player.server.reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,ResourceLocation.withDefaultNamespace("chests/ancient_city")));
        helper.assertTrue(ancient.getPool("zerog_dormant_wisp_backup")!=null,"Ancient city backup not injected");
        helper.succeed();
    }
    @GameTest(batch="prologue",templateNamespace="zerog_prologue",template="equipment_empty",timeoutTicks=400)
    public static void courier_structure_safe_sites_persistence_and_recovery(GameTestHelper helper) {
        var level=helper.getLevel();var player=helper.makeMockServerPlayerInLevel();
        var testPosition=helper.absolutePos(new BlockPos(3,1,3));
        // The test harness starts below terrain at Y=-59. Delivery requires a
        // real open surface; exercise that guard rather than removing it.
        var origin=new BlockPos(testPosition.getX(),63,testPosition.getZ());
        for(var pos:BlockPos.betweenClosed(origin,origin.offset(6,4,6)))level.setBlock(pos,pos.getY()==origin.getY()?Blocks.DIRT.defaultBlockState():Blocks.AIR.defaultBlockState(),2);
        helper.assertTrue(ConcordPrologue.safeSite(level,origin),"Flat open natural ground rejected");
        var obstruction=origin.offset(1,1,1);level.setBlock(obstruction,Blocks.DIAMOND_BLOCK.defaultBlockState(),2);
        var signal=new ConcordPrologue.Signal();
        helper.assertTrue(!ConcordPrologue.deliver(level,origin,player,signal),"Player build overwritten");
        helper.assertTrue(level.getBlockState(obstruction).is(Blocks.DIAMOND_BLOCK),"Refusal modified terrain");
        level.setBlock(obstruction,Blocks.WATER.defaultBlockState(),2);
        helper.assertTrue(!ConcordPrologue.safeSite(level,origin),"Water accepted");level.setBlock(obstruction,Blocks.AIR.defaultBlockState(),2);
        helper.assertTrue(ConcordPrologue.deliver(level,origin,player,signal),"Courier failed to place");
        var chest=(ChestBlockEntity)level.getBlockEntity(origin.offset(3,1,3));
        helper.assertTrue(chest.getItem(0).is(ItemInit.DORMANT_WISP.get()) && chest.getItem(1).is(ItemInit.CONCORD_CODEX.get()),"Courier cargo missing");
        helper.assertTrue(level.getBlockState(origin.offset(3,1,1)).is(BlockInit.BROKEN_CONSOLE.get()),"Console missing");
        helper.assertTrue(!ConcordPrologue.deliver(level,origin,player,signal),"Duplicate structure overwrote pod");
        var ore=new ItemStack(ItemInit.RAW_NULLIFITE.get());
        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.post(new net.neoforged.neoforge.event.entity.player.ItemEntityPickupEvent.Post(
            player,new net.minecraft.world.entity.item.ItemEntity(level,origin.getX(),65,origin.getZ(),ore),ore));
        var ledger=ConcordPrologue.ledger(player.server);var first=ledger.signals.get(player.getUUID());
        helper.assertTrue(first!=null,"Actual pickup event did not schedule Courier");
        var due=first.due;ConcordPrologue.begin(player);helper.assertTrue(first==ledger.signals.get(player.getUUID()) && first.due==due,"Repeated ore resets delivery");
        first.pods.add(origin);first.deliveries=1;first.deliveredAt=50;
        var loaded=ConcordPrologue.Ledger.load(ledger.save(new net.minecraft.nbt.CompoundTag(),level.registryAccess()),level.registryAccess()).signals.get(player.getUUID());
        helper.assertTrue(loaded.deliveries==1 && loaded.pods.contains(origin) && loaded.due==due,"Ledger lost state");
        helper.assertTrue(!ConcordPrologue.recoveryDue(49+ConcordPrologue.RECOVERY_TICKS,loaded),"Recovery early");
        helper.assertTrue(ConcordPrologue.recoveryDue(50+ConcordPrologue.RECOVERY_TICKS,loaded),"Seven-day recovery missing");
        loaded.deliveries=2;helper.assertTrue(!ConcordPrologue.recoveryDue(1000000,loaded),"Infinite replacement farming");
        helper.assertTrue(!ConcordPrologue.hasRecoveryItems(player,first),"Empty player counts as having Wisp");
        player.getInventory().add(new ItemStack(ItemInit.DORMANT_WISP.get()));
        helper.assertTrue(ConcordPrologue.hasRecoveryItems(player,first),"Owned Wisp ignored");
        var moon=player.server.getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.fromNamespaceAndPath("zerog_tweaks","moon")));
        var lunari=ZGPlanetVillagers.TYPES.get("lunari").get().create(moon);
        player.teleportTo(moon,0,280,0,0,0);
        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.post(new net.neoforged.neoforge.event.entity.player.PlayerInteractEvent.EntityInteract(
            player,InteractionHand.MAIN_HAND,lunari));
        helper.assertTrue(first.moonGreeted,"Lunari signal greeting did not run");
        helper.assertTrue(ConcordPrologue.Ledger.load(ledger.save(new net.minecraft.nbt.CompoundTag(),level.registryAccess()),level.registryAccess())
            .signals.get(player.getUUID()).moonGreeted,"Greeting not persisted");
        // Mock players have no negotiated custom weather channel. Restore the
        // Overworld immediately after the synchronous Moon interaction check.
        player.teleportTo(level,origin.getX(),65,origin.getZ(),0,0);
        helper.assertTrue(ConcordPrologue.nextNight(100)==13000 && ConcordPrologue.nextNight(13000)==37000,"Night scheduling wrong");
        ledger.signals.remove(player.getUUID());ledger.setDirty();helper.succeed();
    }
    @GameTest(batch="prologue",templateNamespace="zerog_prologue",template="equipment_empty",timeoutTicks=1200)
    public static void real_server_tick_delivers_once_then_one_recovery(GameTestHelper helper) {
        var world=helper.getLevel().getServer().overworld();var player=helper.makeMockServerPlayerInLevel();
        var test=helper.absolutePos(BlockPos.ZERO);var position=new BlockPos(test.getX()+1000,64,test.getZ()+1000);
        player.teleportTo(world,position.getX()+.5,64,position.getZ()+.5,0,0);
        // Native flat hub fixture gives open STONE ground, far from
        // other tests and the authored hub. Only disposable test chunks touched.
        var forced=new ArrayList<net.minecraft.world.level.ChunkPos>();
        int cx=position.getX()>>4,cz=position.getZ()>>4;
        for(int x=cx-7;x<=cx+7;x++)for(int z=cz-7;z<=cz+7;z++) {
            var chunk=new net.minecraft.world.level.ChunkPos(x,z);
            if(!world.getForcedChunks().contains(chunk.toLong())) {world.setChunkForced(x,z,true);forced.add(chunk);}
            world.getChunk(x,z);
        }
        long originalDay=world.getDayTime();world.setDayTime(1000);ConcordPrologue.begin(player);
        var ledger=ConcordPrologue.ledger(player.server);var signal=ledger.signals.get(player.getUUID());
        helper.assertTrue(signal.deliveries==0,"Courier arrived in daytime");world.setDayTime(13000);
        helper.startSequence().thenWaitUntil(()->helper.assertTrue(signal.deliveries==1,"Waiting for actual tick delivery"))
            .thenExecute(()->{
                helper.assertTrue(signal.pods.size()==1,"First delivery count wrong");
                var pod=signal.pods.getFirst();
                helper.assertTrue(pod.offset(3,0,3).distSqr(new BlockPos(position.getX(),pod.getY(),position.getZ()))<=100*100,"Pod farther than 100 blocks");
                helper.assertTrue(world.getBlockEntity(pod.offset(3,1,3)) instanceof ChestBlockEntity,"Tick delivery lacks chest");
                signal.deliveredAt=world.getGameTime()-ConcordPrologue.RECOVERY_TICKS;
            })
            .thenWaitUntil(()->helper.assertTrue(signal.deliveries==2,"Waiting for actual recovery delivery"))
            .thenIdle(120)
            .thenExecute(()->{
                helper.assertTrue(signal.deliveries==2 && signal.pods.size()==2,"More than one recovery Courier");
                forced.forEach(chunk->world.setChunkForced(chunk.x,chunk.z,false));
                world.setDayTime(originalDay);ledger.signals.remove(player.getUUID());ledger.setDirty();
            }).thenSucceed();
    }
}
