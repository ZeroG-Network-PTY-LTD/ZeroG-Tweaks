package net.zerog.tweaks.gametest;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;
@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class UpgradeCardGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void six_card_tiers_show_approved_recipe_costs_for_all_native_processors(GameTestHelper h){
        var blocks=java.util.List.of(BlockInit.ALLOY_FORGE.get(),BlockInit.ORE_REFINERY.get(),BlockInit.CRYSTAL_GROWTH_CHAMBER.get(),BlockInit.SALVAGE_STATION.get());
        int[] speeds={125,150,175,200,225,250}, savings={5,10,15,20,25,30};
        for(int b=0;b<blocks.size();b++){
            var pos=new BlockPos(1+b*2,1,1);h.setBlock(pos,blocks.get(b));var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
            var recipe=h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).getFirst().value();
            for(int tier=1;tier<=6;tier++){
                be.inventory.setStackInSlot(be.kind.upgrades(),ItemStack.EMPTY);be.inventory.setStackInSlot(be.kind.upgrades()+2,ItemStack.EMPTY);
                h.assertTrue(be.inventory.insertItem(be.kind.upgrades(),stack("acceleration_upgrade_card_t"+tier,1),false).isEmpty(),"Acceleration compatibility rejected");
                h.assertTrue(be.inventory.insertItem(be.kind.upgrades()+2,stack("energy_coil_upgrade_card_t"+tier,1),false).isEmpty(),"Coil compatibility rejected");
                var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);var menu=new ProcessingMenu(1,player.getInventory(),be);
                h.assertTrue(menu.value(20)==speeds[tier-1],"Menu did not expose exact approved speed");
                var page=ProcessingRecipeCatalogue.pages(be,ItemStack.EMPTY).stream().filter(p->p.id().equals(h.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).getFirst().id())).findFirst().orElseThrow();
                h.assertTrue(page.energy()==(recipe.energy()*(100-savings[tier-1])+99)/100,"Recipe catalogue did not show approved coil saving");
            }
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void cards_preserve_legacy_items_and_paid_jobs_across_reload(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(pos);
        be.inventory.setStackInSlot(be.kind.upgrades(),stack("astrium_casing",1));be.inventory.setStackInSlot(be.kind.upgrades()+1,stack("cryo_core",1));
        be.inventory.setStackInSlot(be.kind.upgrades()+2,stack("fusion_dust",1));
        var old=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(pos,be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        old.setLevel(h.getLevel());
        h.assertTrue(old.inventory.getStackInSlot(old.kind.upgrades()).getCount()==1&&old.speedPercent()==250,"Legacy items/effects lost on load");
        h.assertTrue(old.inventory.extractItem(old.kind.upgrades(),1,false).getCount()==1,"Legacy casing unrecoverable");
        h.assertTrue(old.inventory.insertItem(old.kind.upgrades(),stack("acceleration_upgrade_card_t6",1),false).isEmpty(),"Replacement card rejected");
        var recipe=ProcessingRecipeCatalogue.pages(old,stack("cyrrium_casing",1)).getFirst();
        h.assertTrue(recipe.energy()==8000&&recipe.ticks()==80&&old.inventory.getStackInSlot(old.kind.upgrades()+2).getCount()==1,"Card stacks legacy dust bonuses or deletes legacy items");
        be.inventory.setStackInSlot(be.kind.upgrades(),stack("acceleration_upgrade_card_t6",1));be.inventory.setStackInSlot(be.kind.upgrades()+2,stack("energy_coil_upgrade_card_t6",1));
        be.inventory.setStackInSlot(0,stack("cyrrium_ingot",3));be.inventory.setStackInSlot(1,stack("pulsar_dust",2));be.stored=5600;
        be.inventory.setStackInSlot(be.kind.output(),stack("cyrrium_casing",64));ProcessingBlockEntity.tick(h.getLevel(),pos,be.getBlockState(),be);
        h.assertTrue(be.stored==5600&&be.progress==0,"Blocked upgraded output spent FE");
        be.inventory.setStackInSlot(be.kind.output(),ItemStack.EMPTY);for(int i=0;i<40;i++)ProcessingBlockEntity.tick(h.getLevel(),pos,be.getBlockState(),be);
        var loaded=(ProcessingBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(pos,be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(loaded.progress==40&&loaded.stored==2800,"Paid card job lost on reload");
        for(int i=0;i<40;i++)ProcessingBlockEntity.tick(h.getLevel(),pos,loaded.getBlockState(),loaded);
        h.assertTrue(loaded.stored==0&&loaded.inventory.getStackInSlot(loaded.kind.output()).getCount()==2,"Reload created unpaid product or lost job");h.succeed();
    }
    private static ItemStack stack(String id,int count){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)),count);}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void processor_cards_are_filtered_bounded_and_process_at_exact_cost(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new ProcessingMenu(1,player.getInventory(),be);
        var acceleration=stack("acceleration_upgrade_card_t6",1);var coil=stack("energy_coil_upgrade_card_t6",1);
        h.assertTrue(!acceleration.isEmpty()&&!coil.isEmpty(),"Upgrade cards are not registered");
        int speed=be.kind.upgrades(),efficiency=speed+2;
        h.assertTrue(menu.slots.get(speed).mayPlace(acceleration)&&!menu.slots.get(speed).mayPlace(coil)&&menu.slots.get(efficiency).mayPlace(coil),"Card family filters wrong");
        h.assertTrue(!menu.slots.get(speed).mayPlace(stack("cyrrium_casing",1)),"New casing insertion is still an upgrade");
        h.assertTrue(be.inventory.insertItem(speed,acceleration,false).isEmpty()&&be.inventory.insertItem(efficiency,coil,false).isEmpty(),"Valid cards rejected");
        h.assertTrue(be.inventory.insertItem(speed,acceleration,false).getCount()==1,"Multiple same-family cards accepted");
        be.inventory.setStackInSlot(0,stack("cyrrium_ingot",3));be.inventory.setStackInSlot(1,stack("pulsar_dust",2));be.stored=5600;
        var recipe=ProcessingRecipeCatalogue.pages(be,stack("cyrrium_casing",1)).getFirst();
        h.assertTrue(recipe.energy()==5600&&recipe.ticks()==80,"Tier6 page exceeds approved bounds");
        for(int i=0;i<80;i++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);
        h.assertTrue(be.stored==0&&be.inventory.getStackInSlot(be.kind.output()).getCount()==2,"Card processing cost/output incorrect");h.succeed();
    }
}
