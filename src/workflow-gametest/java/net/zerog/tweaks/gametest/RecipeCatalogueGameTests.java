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
public final class RecipeCatalogueGameTests {
    private static ItemStack stack(String id){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)));}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void catalogue_preserves_seed_feed_salvage_and_refinery_yields(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BlockInit.CRYSTAL_GROWTH_CHAMBER.get());
        var crystal=(ProcessingBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var growth=ProcessingRecipeCatalogue.pages(crystal,stack("lumenite")).getFirst();
        h.assertTrue(!growth.inputs().get(0).consumed()&&growth.inputs().get(1).consumed()&&growth.catalyst().isEmpty()&&growth.energy()==6000&&growth.ticks()==1200,"Crystal reusable seed/feed page wrong");
        h.setBlock(new BlockPos(3,1,1),BlockInit.SALVAGE_STATION.get());
        var salvage=(ProcessingBlockEntity)h.getBlockEntity(new BlockPos(3,1,1));
        var scrap=ProcessingRecipeCatalogue.pages(salvage,stack("meteorite_fragment")).getFirst();
        h.assertTrue(scrap.outputs().size()==2&&scrap.outputs().get(1).stack().is(net.minecraft.world.item.Items.IRON_NUGGET)&&scrap.outputs().get(1).stack().getCount()==4&&scrap.energy()==2000&&scrap.ticks()==100,"Salvage outputs page wrong");
        h.setBlock(new BlockPos(5,1,1),BlockInit.ORE_REFINERY.get());
        var refinery=(ProcessingBlockEntity)h.getBlockEntity(new BlockPos(5,1,1));
        var raw=ProcessingRecipeCatalogue.pages(refinery,stack("deepslate_nullifite_ore")).getFirst();
        h.assertTrue(raw.outputs().getFirst().stack().getCount()==2&&raw.energy()==4000&&raw.ticks()==200,"Base refinery yield wrong");
        refinery.inventory.setStackInSlot(refinery.kind.upgrades(),stack("cyrrium_casing"));
        h.assertTrue(ProcessingRecipeCatalogue.pages(refinery,stack("deepslate_nullifite_ore")).getFirst().outputs().getFirst().stack().getCount()==3,"Upgraded refinery yield absent");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void catalogue_shows_real_combinations_catalysts_and_upgrade_costs(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BlockInit.ALLOY_FORGE.get());
        var be=(ProcessingBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));
        var all=ProcessingRecipeCatalogue.pages(be,ItemStack.EMPTY);
        h.assertTrue(all.size()==10,"Catalogue omitted registered alloy combinations");
        var pages=ProcessingRecipeCatalogue.pages(be,stack("abyssal_pearl"));
        h.assertTrue(pages.size()==1,"Output click did not find its production recipe");
        var page=pages.getFirst();
        h.assertTrue(page.inputs().stream().map(ProcessingRecipe.Counted::count).toList().equals(java.util.List.of(2,4,2)),"Ingredient quantities wrong");
        h.assertTrue(page.catalyst().isPresent()&&page.catalyst().get().ingredient().test(stack("stardust"))&&!page.catalyst().get().consumed(),"Reusable Stardust catalyst not described");
        h.assertTrue(page.outputs().getFirst().stack().getCount()==1&&page.outputs().getFirst().chance()==1&&page.energy()==40000&&page.ticks()==400,"Base product/cost/time wrong");
        h.assertTrue(ProcessingRecipeCatalogue.pages(be,stack("stardust")).size()==4,"Catalyst click omitted recipes");
        be.inventory.setStackInSlot(be.kind.upgrades(),stack("astrium_casing"));
        be.inventory.setStackInSlot(be.kind.upgrades()+1,stack("cryo_core"));
        be.inventory.setStackInSlot(be.kind.upgrades()+2,stack("fusion_dust"));
        var upgraded=ProcessingRecipeCatalogue.pages(be,stack("abyssal_pearl")).getFirst();
        h.assertTrue(upgraded.energy()==24000&&upgraded.ticks()==160,"Catalogue did not reflect installed upgrades");
        h.assertTrue(be.stored==0&&be.inventory.getStackInSlot(be.kind.output()).isEmpty(),"Read-only browsing processed a recipe");h.succeed();
    }
}
