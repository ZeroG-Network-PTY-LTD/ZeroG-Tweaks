package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_compact") @PrefixGameTestTemplate(false)
public final class CompactStorageGameTests {
    @GameTest(templateNamespace="zerog_compact",template="equipment_empty",timeoutTicks=200)
    public static void compact_tiers_bound_pipe_storage_and_preserve_inputs_after_card_removal(GameTestHelper h){
        int[] capacities={212,360,508,656,804,952};
        for(int tier=1;tier<=6;tier++){
            var pos=new BlockPos(tier*2,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());
            var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
            var card=stack("item_compact_upgrade_card_t"+tier,1);
            h.assertTrue(!card.isEmpty(),"Compact card not registered, tier "+tier);
            h.assertTrue(be.inventory.insertItem(be.kind.upgrades()+1,card,false).isEmpty(),"Compact socket rejected card");
            var pipe=be.itemsFor(Direction.UP);int accepted=0;
            for(int n=0;n<16;n++){
                var incoming=stack("cyrrium_ingot",64);
                int count=64-pipe.insertItem(0,incoming,false).getCount();accepted+=count;
                h.assertTrue(incoming.getCount()==64,"Pipe insertion mutated caller stack");
                h.assertTrue(pipe.getStackInSlot(0).getCount()<=64,"Oversized ItemStack exposed to network");
            }
            h.assertTrue(accepted==capacities[tier-1],"Compact capacity wrong for tier "+tier);
            h.assertTrue(pipe.insertItem(0,stack("cyrrium_ingot",1),true).getCount()==1,"Full reserve accepted simulation");
            var loaded=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
            loaded.setLevel(h.getLevel());
            h.assertTrue(loaded.inventory.extractItem(loaded.kind.upgrades()+1,1,false).getCount()==1,"Compact card removal failed");
            h.assertTrue(loaded.itemsFor(Direction.UP).insertItem(0,stack("cyrrium_ingot",1),false).getCount()==1,"Over-capacity input accepted after removal");
            int recovered=0;
            for(int n=0;n<20;n++){
                var extracted=loaded.inventory.extractItem(0,64,false);
                h.assertTrue(extracted.getCount()<=64,"Oversized recovery ItemStack");recovered+=extracted.getCount();
            }
            h.assertTrue(recovered==capacities[tier-1],"Reload/card removal lost or duplicated stored inputs");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_compact",template="equipment_empty",timeoutTicks=200)
    public static void compact_menu_deposits_show_total_and_breaking_recovers_every_input(GameTestHelper h){
        var blocks=java.util.List.of(BlockInit.ALLOY_FORGE.get(),BlockInit.ORE_REFINERY.get(),BlockInit.CRYSTAL_GROWTH_CHAMBER.get(),BlockInit.SALVAGE_STATION.get());
        for(int b=0;b<blocks.size();b++){
            var pos=new BlockPos(1+b*8,1,1);h.setBlock(pos,blocks.get(b));var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
            var recipe=h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).getFirst().value();
            var material=recipe.inputs().getFirst().ingredient().getItems()[0].copyWithCount(64);
            // Keep other reagent slots occupied to test this logical input's capacity.
            for(int i=1;i<be.kind.inputCount;i++)be.inventory.setStackInSlot(i,new ItemStack(net.minecraft.world.item.Items.STONE,64));
            be.inventory.insertItem(be.kind.upgrades()+1,stack("item_compact_upgrade_card_t1",1),false);
            var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
            var menu=new ProcessingMenu(1,player.getInventory(),be);
            for(int n=0;n<4;n++){player.getInventory().setItem(9,material.copy());menu.quickMoveStack(player,be.kind.slots());}
            h.assertTrue(player.getInventory().getItem(9).getCount()==44,"Menu did not deposit exactly212 into compact input");
            h.assertTrue(menu.value(21)==212,"Menu missing full compact quantity");
            h.assertTrue(menu.slots.get(0).getItem().getCount()<=64,"Menu synced oversized stack");
            h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
            int recovered=h.getLevel().getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,new net.minecraft.world.phys.AABB(be.getBlockPos()).inflate(2)).stream()
                .filter(e->ItemStack.isSameItemSameComponents(e.getItem(),material)).mapToInt(e->e.getItem().getCount()).sum();
            h.assertTrue(recovered==212,"Breaking lost compact input reserve for "+be.kind);
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_compact",template="equipment_empty",timeoutTicks=200)
    public static void compact_processing_and_menu_withdrawals_preserve_exact_counts(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        var recipe=h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).getFirst().value();
        be.inventory.insertItem(be.kind.upgrades()+1,stack("item_compact_upgrade_card_t1",1),false);
        for(int i=0;i<recipe.inputs().size();i++){
            var input=recipe.inputs().get(i).ingredient().getItems()[0];
            for(int n=0;n<4;n++)be.inventory.insertItem(i,input.copyWithCount(64),false);
        }
        recipe.catalyst().ifPresent(c->be.inventory.insertItem(be.kind.catalyst(),c.ingredient().getItems()[0].copyWithCount(c.count()),false));
        int before=be.inventory.total(0);
        be.energyInput(Direction.UP).receiveEnergy(be.energyCost(recipe),false);
        for(int t=0;t<be.duration(recipe);t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        int expected=before-(recipe.inputs().getFirst().consumed()?recipe.inputs().getFirst().count():0);
        h.assertTrue(be.inventory.total(0)==expected,"Processing lost or duplicated reserve inputs");
        h.assertTrue(be.inventory.getStackInSlot(be.kind.output()).getCount()>0,"Powered processing produced no output");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        for(int n=0;n<4;n++)menu.quickMoveStack(player,0);
        var input=recipe.inputs().getFirst().ingredient().getItems()[0];
        int recovered=0;
        for(int i=0;i<player.getInventory().getContainerSize();i++){
            var item=player.getInventory().getItem(i);
            h.assertTrue(item.getCount()<=item.getMaxStackSize(),"Menu withdrawal produced oversized player stack");
            if(ItemStack.isSameItemSameComponents(item,input))recovered+=item.getCount();
        }
        h.assertTrue(recovered==expected&&be.inventory.total(0)==0,"Menu withdrawal lost or duplicated reserve");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_compact",template="equipment_empty",timeoutTicks=200)
    public static void compact_normal_clicks_and_swaps_preserve_reserves(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        be.inventory.insertItem(be.kind.upgrades()+1,stack("item_compact_upgrade_card_t1",1),false);
        for(int n=0;n<4;n++)be.inventory.insertItem(0,stack("cyrrium_ingot",64),false);
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        menu.clicked(0,0,net.minecraft.world.inventory.ClickType.PICKUP,player);
        h.assertTrue(menu.getCarried().getCount()==64&&be.inventory.total(0)==148,"Normal pickup lost reserve");
        menu.clicked(be.kind.slots(),0,net.minecraft.world.inventory.ClickType.PICKUP,player);
        menu.clicked(0,1,net.minecraft.world.inventory.ClickType.PICKUP,player);
        h.assertTrue(menu.getCarried().getCount()==32&&be.inventory.total(0)==116,"Half-stack pickup lost reserve");
        menu.clicked(0,1,net.minecraft.world.inventory.ClickType.PICKUP,player);
        h.assertTrue(menu.getCarried().getCount()==32&&be.inventory.total(0)==116,"Full visible slot duplicated reserve on deposit");
        var other=stack("moonsteel_ingot",64);
        h.assertTrue(!other.isEmpty(),"Hotbar swap fixture must be registered");
        player.getInventory().setItem(0,other);
        menu.clicked(0,0,net.minecraft.world.inventory.ClickType.SWAP,player);
        h.assertTrue(be.inventory.total(0)==116&&player.getInventory().getItem(0).is(other.getItem()),"Different-type hotbar swap overwrote reserve");
        h.succeed();
    }
    private static ItemStack stack(String id,int count){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)),count);}
}
