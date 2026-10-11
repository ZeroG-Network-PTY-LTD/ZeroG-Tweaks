package net.zerog.tweaks.gametest;

import java.util.ArrayList;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.ZGManufacturingComponents;

@GameTestHolder("zerog_manufacturing") @PrefixGameTestTemplate(false)
public final class ManufacturingRecipeGameTests {
    private static ItemStack item(String id){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse(id.contains(":")?id:"zerog_tweaks:"+id)));}
    private static CraftingRecipe recipe(GameTestHelper h,String id){return (CraftingRecipe)h.getLevel().getRecipeManager().byKey(ResourceLocation.parse("zerog_tweaks:"+id)).orElseThrow().value();}
    private static CraftingInput input(String... ids){var items=new ArrayList<ItemStack>();for(String id:ids)items.add(id.isEmpty()?ItemStack.EMPTY:item(id));return CraftingInput.of(3,3,items);}
    private static void output(GameTestHelper h,CraftingRecipe recipe,CraftingInput input,String id,int count){
        h.assertTrue(recipe.matches(input,h.getLevel()),"Recipe rejects valid materials: "+id);
        var stack=recipe.assemble(input,h.getLevel().registryAccess());
        h.assertTrue(stack.is(item(id).getItem())&&stack.getCount()==count,"Wrong result: "+id);
        h.assertTrue(recipe.getRemainingItems(input).stream().allMatch(ItemStack::isEmpty),"Unexpected reusable metal remainder");
    }
    @GameTest(templateNamespace="zerog_manufacturing",template="equipment_empty",timeoutTicks=100)
    public static void all_dimension_metal_parts_have_exact_costs_and_no_wrong_metal_shortcut(GameTestHelper h){
        for(String metal:ZGManufacturingComponents.METALS){
            var ingot=metal+"_ingot";
            var plate=recipe(h,"manufacturing/"+metal+"_plate");
            output(h,plate,input(ingot,"","",ingot,"","","","",""),metal+"_plate",1);
            h.assertTrue(!plate.matches(input(ingot,"","","","","","","",""),h.getLevel()),"Plate works with one ingot");
            var cog=recipe(h,"manufacturing/"+metal+"_cog");
            output(h,cog,input("",ingot,"",ingot,"",ingot,"",ingot,""),metal+"_cog",1);
            h.assertTrue(!cog.matches(input("",ingot,"",ingot,"","","",ingot,""),h.getLevel()),"Cog works with three ingots");
            h.assertTrue(!cog.matches(input("","minecraft:iron_ingot","","minecraft:iron_ingot","","minecraft:iron_ingot","","minecraft:iron_ingot",""),h.getLevel()),"Vanilla metal substitution allowed");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_manufacturing",template="equipment_empty",timeoutTicks=100)
    public static void four_casing_stages_accept_all_star_glass_colours_but_not_missing_parts(GameTestHelper h){
        String[][] stages={{"cyrrium","pulsar_dust","minecraft:iron_block"},{"tectium","tremor_dust","cyrrium_casing"},
            {"wraithsteel","spectral_dust","tectium_casing"},{"astrium","fusion_dust","wraithsteel_casing"}};
        for(var stage:stages){var metal=stage[0];var r=recipe(h,metal+"_casing");
            for(String glass:new String[]{"star_glass","star_glass_blue","star_glass_teal"})
                output(h,r,input(metal+"_plate",metal+"_cog",metal+"_plate",stage[1],stage[2],stage[1],"",glass,""),metal+"_casing",2);
            h.assertTrue(!r.matches(input(metal+"_plate",metal+"_cog",metal+"_plate",stage[1],stage[2],stage[1],"","minecraft:glass",""),h.getLevel()),"Ordinary glass bypasses Star Glass");
            h.assertTrue(!r.matches(input(metal+"_plate","",metal+"_plate",stage[1],stage[2],stage[1],"","star_glass",""),h.getLevel()),"Casing works without cog");
            h.assertTrue(!r.matches(input(metal+"_plate",metal+"_cog",metal+"_plate",stage[1],"",stage[1],"","star_glass",""),h.getLevel()),"Missing predecessor core accepted");
            h.assertTrue(!r.matches(input(metal+"_plate",metal+"_cog",metal+"_plate",stage[1],stage[2],stage[1],"minecraft:diamond","star_glass",""),h.getLevel()),"Reserved space consumes unrelated item");
        }h.succeed();
    }
}
