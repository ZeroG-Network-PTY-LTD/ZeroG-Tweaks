package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_void") @PrefixGameTestTemplate(false)
public final class VoidFilterGameTests {
    @GameTest(templateNamespace="zerog_void",template="equipment_empty",timeoutTicks=200)
    public static void selected_new_outputs_void_only_with_installed_card(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ORE_REFINERY.get());
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        var card=new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:void_upgrade_card")));
        h.assertTrue(!card.isEmpty(),"Void card must be registered");
        h.assertTrue(be.inventory.insertItem(be.kind.upgrades()+3,card,false).isEmpty(),"Void socket rejected its card");
        var recipe=h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).getFirst().value();
        for(int i=0;i<recipe.inputs().size();i++)be.inventory.insertItem(i,recipe.inputs().get(i).ingredient().getItems()[0].copyWithCount(64),false);
        recipe.catalyst().ifPresent(c->be.inventory.insertItem(be.kind.catalyst(),c.ingredient().getItems()[0].copyWithCount(c.count()),false));
        be.inventory.setStackInSlot(be.kind.output(),new ItemStack(Items.STONE,64));
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        var cursor=recipe.outputs().getFirst().stack().copyWithCount(16);menu.setCarried(cursor);
        h.assertTrue(menu.clickMenuButton(player,300),"Upgrades tab refused valid player");
        h.assertTrue(menu.clickMenuButton(player,400),"Void ghost filter refused cursor item");
        h.assertTrue(menu.getCarried().getCount()==16,"Ghost selection consumed player item");
        int before=be.inventory.getStackInSlot(0).getCount();
        be.energyInput(Direction.UP).receiveEnergy(be.energyCost(recipe),false);
        for(int t=0;t<be.duration(recipe);t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==before-recipe.inputs().getFirst().count(),"Selected output did not allow processing");
        h.assertTrue(be.inventory.getStackInSlot(be.kind.output()).is(Items.STONE)&&be.inventory.getStackInSlot(be.kind.output()).getCount()==64,"Void deleted existing stored outputs");
        be.inventory.extractItem(be.kind.upgrades()+3,1,false);
        be.energyInput(Direction.UP).receiveEnergy(be.energyCost(recipe),false);
        int power=be.energyInput(Direction.UP).getEnergyStored(),inputs=be.inventory.getStackInSlot(0).getCount();
        for(int t=0;t<be.duration(recipe);t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==inputs&&be.energyInput(Direction.UP).getEnergyStored()==power,"Removed Void card still discarded outputs or consumed power");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_void",template="equipment_empty",timeoutTicks=200)
    public static void paged_filters_reload_without_losing_existing_upgrade_slots(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        String[] ids={"acceleration_upgrade_card_t2","item_compact_upgrade_card_t3","energy_coil_upgrade_card_t4","void_upgrade_card"};
        for(int i=0;i<ids.length;i++)be.inventory.insertItem(be.kind.upgrades()+i,stack(ids[i]),false);
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new ProcessingMenu(1,player.getInventory(),be);
        h.assertTrue(menu.clickMenuButton(player,300)&&menu.value(25)==1,"Upgrades tab is not synchronized");
        h.assertTrue(!menu.clickMenuButton(player,301),"Filter page scrolled below zero");
        for(int n=0;n<3;n++)h.assertTrue(menu.clickMenuButton(player,302),"Filter page refused valid next page");
        h.assertTrue(menu.value(26)==3&&!menu.clickMenuButton(player,302),"Filter page exceeded four pages");
        menu.setCarried(new ItemStack(Items.STONE,16));h.assertTrue(menu.clickMenuButton(player,408),"Last ghost entry rejected");
        h.assertTrue(menu.getCarried().getCount()==16,"Paged ghost entry consumed cursor items");
        int encoded=(menu.value(44)&65535)|(menu.value(45)<<16);
        h.assertTrue(encoded==BuiltInRegistries.ITEM.getId(Items.STONE)+1,"Last ghost entry missing from synchronized page");
        var loaded=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());loaded.setLevel(h.getLevel());
        h.assertTrue(loaded.voids(new ItemStack(Items.STONE)),"Saved Void selection lost on reload");
        for(int i=0;i<ids.length;i++)h.assertTrue(loaded.inventory.getStackInSlot(loaded.kind.upgrades()+i).is(stack(ids[i]).getItem()),"Existing card save index shifted");
        // A previous version had three card sockets. Its saved Size must not shrink
        // the newly appended Void socket on loading a normal old machine.
        be.inventory.extractItem(be.kind.upgrades()+3,1,false);
        var legacy=be.saveWithFullMetadata(h.getLevel().registryAccess());legacy.getCompound("Inventory").putInt("Size",be.kind.slots()-1);
        var migrated=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),legacy,h.getLevel().registryAccess());migrated.setLevel(h.getLevel());
        h.assertTrue(migrated.inventory.getSlots()==migrated.kind.slots()&&migrated.inventory.insertItem(migrated.kind.upgrades()+3,stack("void_upgrade_card"),false).isEmpty(),"Old inventory cannot accept appended Void socket");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_void",template="equipment_empty",timeoutTicks=200)
    public static void empty_nonmatching_filters_and_invalid_commands_do_not_discard(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.SALVAGE_STATION.get());var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new ProcessingMenu(1,player.getInventory(),be);
        menu.setCarried(new ItemStack(Items.STONE,16));menu.clickMenuButton(player,300);
        h.assertTrue(!menu.clickMenuButton(player,400),"Filter accepts edits without Void card");
        be.inventory.insertItem(be.kind.upgrades()+3,stack("void_upgrade_card"),false);
        var recipe=h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).stream().filter(r->r.id().getPath().equals("salvaging/cryo_pod")).findFirst().orElseThrow().value();
        be.inventory.insertItem(0,stack("cryo_pod").copyWithCount(16),false);
        be.inventory.setStackInSlot(be.kind.output(),new ItemStack(Items.STONE,64));
        be.energyInput(Direction.UP).receiveEnergy(2000,false);
        for(int t=0;t<100;t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==16&&be.energyInput(Direction.UP).getEnergyStored()==2000,"Empty Void filter discarded products");
        h.assertTrue(menu.clickMenuButton(player,400),"Matching control did not accept valid cursor");
        for(int id:new int[]{399,409,419,429,Integer.MAX_VALUE,-1})h.assertTrue(!menu.clickMenuButton(player,id),"Out-of-range filter command accepted");
        for(int t=0;t<100;t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==16&&be.energyInput(Direction.UP).getEnergyStored()==2000,"Nonmatching filter bypassed blocked output");
        h.assertTrue(menu.clickMenuButton(player,420)&&!be.voids(new ItemStack(Items.STONE)),"Clear filter entry failed");
        menu.setCarried(stack("hull_plating"));menu.clickMenuButton(player,400);
        be.inventory.setStackInSlot(be.kind.output()+1,new ItemStack(Items.STONE,64));
        for(int t=0;t<100;t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==16&&be.energyInput(Direction.UP).getEnergyStored()==2000,"One selected output bypassed another blocked product");
        player.setPos(be.getBlockPos().getCenter().add(30,0,0));
        h.assertTrue(!menu.clickMenuButton(player,420)&&be.voids(stack("hull_plating")),"Remote player changed Void filter");
        player.setPos(be.getBlockPos().getCenter());menu.clickMenuButton(player,300);
        h.assertTrue(!menu.clickMenuButton(player,420),"Closed tab accepted filter edit");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_void",template="equipment_empty",timeoutTicks=200)
    public static void voided_jobs_preserve_reusable_catalysts_and_real_break_drops(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        be.inventory.insertItem(be.kind.upgrades()+3,stack("void_upgrade_card"),false);
        String[] inputs={"cryocite","frost_crystal","wraithsteel_ingot"};
        for(int i=0;i<3;i++)be.inventory.insertItem(i,stack(inputs[i]).copyWithCount(64),false);
        be.inventory.insertItem(be.kind.catalyst(),stack("stardust").copyWithCount(16),false);
        be.inventory.setStackInSlot(be.kind.output(),stack("cryo_core").copyWithCount(5));
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new ProcessingMenu(1,player.getInventory(),be);
        menu.clickMenuButton(player,300);menu.setCarried(stack("cryo_core"));menu.clickMenuButton(player,400);
        menu.setCarried(stack("stardust").copyWithCount(16));menu.clickMenuButton(player,401);
        be.energyInput(Direction.UP).receiveEnergy(40000,false);
        for(int t=0;t<400;t++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==60&&be.inventory.getStackInSlot(1).getCount()==62&&be.inventory.getStackInSlot(2).getCount()==63,"Voided job changed recipe input counts");
        h.assertTrue(be.inventory.getStackInSlot(be.kind.catalyst()).getCount()==16&&menu.getCarried().getCount()==16,"Void filter deleted reusable catalyst or player cursor");
        h.assertTrue(be.inventory.getStackInSlot(be.kind.output()).getCount()==5&&be.energyInput(Direction.UP).getEnergyStored()==0,"Void job failed exact product/power contract");
        h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);
        var drops=h.getLevel().getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,new net.minecraft.world.phys.AABB(be.getBlockPos()).inflate(2));
        int output=drops.stream().filter(e->e.getItem().is(stack("cryo_core").getItem())).mapToInt(e->e.getItem().getCount()).sum();
        int catalyst=drops.stream().filter(e->e.getItem().is(stack("stardust").getItem())).mapToInt(e->e.getItem().getCount()).sum();
        int cards=drops.stream().filter(e->e.getItem().is(stack("void_upgrade_card").getItem())).mapToInt(e->e.getItem().getCount()).sum();
        h.assertTrue(output==5&&catalyst==16&&cards==1,"Break drops discarded real items or materialized ghost templates");
        h.assertTrue(!menu.clickMenuButton(player,420),"Stale destroyed-machine menu accepted edits");
        h.succeed();
    }
    private static ItemStack stack(String id){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)));}
}
