package net.zerog.tweaks.gametest;

import net.minecraft.core.component.DataComponents;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.ItemInit;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class FoodInteractionGameTests {
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void cooking_hide_and_flower_recipes_work(GameTestHelper helper) {
        var level=helper.getLevel();
        var recipes=level.getRecipeManager();
        for(var type:java.util.List.of(net.minecraft.world.item.crafting.RecipeType.SMELTING,
                net.minecraft.world.item.crafting.RecipeType.SMOKING,net.minecraft.world.item.crafting.RecipeType.CAMPFIRE_COOKING)) {
            var input=new net.minecraft.world.item.crafting.SingleRecipeInput(new ItemStack(ItemInit.GLIMMERFISH.get()));
            var recipe=recipes.getRecipeFor(type,input,level);
            helper.assertTrue(recipe.isPresent(),"Missing Glimmerfish cooking recipe "+type);
            helper.assertTrue(recipe.orElseThrow().value().getResultItem(level.registryAccess()).is(ItemInit.COOKED_GLIMMERFISH.get()),"Wrong cooking output");
        }
        var hide=net.minecraft.world.item.crafting.CraftingInput.of(1,1,java.util.List.of(new ItemStack(ItemInit.GRAZER_HIDE.get())));
        var leather=recipes.getRecipeFor(net.minecraft.world.item.crafting.RecipeType.CRAFTING,hide,level).orElseThrow()
                .value().assemble(hide,level.registryAccess());
        helper.assertTrue(leather.is(net.minecraft.world.item.Items.LEATHER),"Hide does not yield vanilla leather");
        var helmetInput=net.minecraft.world.item.crafting.CraftingInput.of(3,2,java.util.List.of(leather.copy(),leather.copy(),leather.copy(),
                leather.copy(),ItemStack.EMPTY,leather.copy()));
        var helmet=recipes.getRecipeFor(net.minecraft.world.item.crafting.RecipeType.CRAFTING,helmetInput,level).orElseThrow()
                .value().assemble(helmetInput,level.registryAccess());
        helper.assertTrue(helmet.is(net.minecraft.world.item.Items.LEATHER_HELMET),"Converted hide cannot make leather armour");
        var flower=net.minecraft.core.registries.BuiltInRegistries.ITEM.get(net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:moon_glow_flower"));
        var dyeInput=net.minecraft.world.item.crafting.CraftingInput.of(1,1,java.util.List.of(new ItemStack(flower)));
        var dye=recipes.getRecipeFor(net.minecraft.world.item.crafting.RecipeType.CRAFTING,dyeInput,level).orElseThrow()
                .value().assemble(dyeInput,level.registryAccess());
        helper.assertTrue(dye.is(net.minecraft.world.item.Items.PURPLE_DYE),"Alien flower does not yield its vanilla dye");
        var colourInput=net.minecraft.world.item.crafting.CraftingInput.of(2,1,java.util.List.of(helmet,dye));
        var coloured=recipes.getRecipeFor(net.minecraft.world.item.crafting.RecipeType.CRAFTING,colourInput,level).orElseThrow()
                .value().assemble(colourInput,level.registryAccess());
        helper.assertTrue(coloured.get(DataComponents.DYED_COLOR)!=null,"Planet dye cannot colour leather armour");
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void drinks_and_stews_return_containers(GameTestHelper helper) {
        for(var item:java.util.List.of(ItemInit.FROST_MILK.get(),ItemInit.FROSTFERN_TEA.get(),ItemInit.SHARDWOOD_SYRUP.get(),ItemInit.CINDER_CAP_STEW.get())) {
            var stack=new ItemStack(item);var food=stack.get(DataComponents.FOOD);
            var player=helper.makeMockPlayer(GameType.SURVIVAL);player.getFoodData().setFoodLevel(0);
            var result=stack.finishUsingItem(helper.getLevel(),player);
            helper.assertTrue(food.usingConvertsTo().isPresent(),"Missing drink/stew container");
            helper.assertTrue(result.is(food.usingConvertsTo().orElseThrow().getItem()),"Did not return bottle/bowl");
            if(item!=ItemInit.CINDER_CAP_STEW.get()) helper.assertTrue(item.getUseAnimation(new ItemStack(item))==net.minecraft.world.item.UseAnim.DRINK,"Drink uses eating animation");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void all_defined_foods_are_edible(GameTestHelper helper) throws Exception {
        for(var field:net.zerog.tweaks.item.ZGFoods.class.getFields()) {
            if(field.getType()!=net.minecraft.world.food.FoodProperties.class) continue;
            var id=net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",field.getName().toLowerCase(java.util.Locale.ROOT));
            var item=net.minecraft.core.registries.BuiltInRegistries.ITEM.get(id);
            var stack=new ItemStack(item,2);
            var food=stack.get(DataComponents.FOOD);
            helper.assertTrue(food!=null,"Missing food component: "+id);
            var expected=(net.minecraft.world.food.FoodProperties)field.get(null);
            helper.assertTrue(food.nutrition()==expected.nutrition(),"Wrong nutrition: "+id);
            var player=helper.makeMockPlayer(GameType.SURVIVAL);
            player.getFoodData().setFoodLevel(0);
            player.setItemInHand(InteractionHand.MAIN_HAND,stack);
            helper.assertTrue(item.use(helper.getLevel(),player,InteractionHand.MAIN_HAND).getResult().consumesAction(),"Cannot start eating: "+id);
            stack.finishUsingItem(helper.getLevel(),player);
            helper.assertTrue(player.getFoodData().getFoodLevel()==Math.min(20,food.nutrition()),"Food did not restore hunger: "+id);
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=100)
    public static void liquid_tab_and_layered_comet_are_complete(GameTestHelper helper) {
        var liquids=net.zerog.tweaks.registry.CreativeTabs.liquidItems();
        helper.assertTrue(liquids.size()==18,"Expected all eighteen liquid buckets");
        helper.assertTrue(liquids.stream().allMatch(i->i instanceof net.minecraft.world.item.BucketItem),"Non-bucket liquid entry");
        var cells=net.zerog.tweaks.event.CometRemnant.cells();
        for(var cell:cells) {
            helper.assertTrue(cells.stream().anyMatch(c->c.x()==9-cell.x()&&c.y()==cell.y()&&c.z()==cell.z()&&c.layer()==cell.layer()),"Asymmetric comet");
        }
        for(int axis=0;axis<3;axis++) {
            final int a=axis;
            var positions=cells.stream().mapToInt(c->a==0?c.x():a==1?c.y():c.z());
            helper.assertTrue(positions.max().orElse(-1)==9,"Comet does not reach ten blocks");
        }
        for(String theme:new String[]{"moon","mars","cerulon","skarn","eidolon","solvane"}) {
            var palette=net.zerog.tweaks.event.CometRemnant.palette(theme);
            var random=net.minecraft.util.RandomSource.create(42);
            for(var cell:cells) {
                var block=net.zerog.tweaks.event.CometRemnant.material(cell,palette,random);
                helper.assertTrue(block!=net.minecraft.world.level.block.Blocks.AIR,"Missing comet material: "+theme);
                var name=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(block).getPath();
                if(cell.layer()!=net.zerog.tweaks.event.CometRemnant.Layer.CORE)
                    helper.assertTrue(!name.equals(palette.rareOre())&&!name.equals(palette.gemOre()),"Rare mineral outside core");
            }
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=40)
    public static void cooked_glimmerfish_starts_eating_and_restores_hunger(GameTestHelper helper) {
        var stack=new ItemStack(ItemInit.COOKED_GLIMMERFISH.get(),2);
        helper.assertTrue(stack.get(DataComponents.FOOD)!=null,"Cooked Glimmerfish has no FOOD component; cannot be eaten");
        var player=helper.makeMockPlayer(GameType.SURVIVAL);
        player.getFoodData().setFoodLevel(10);player.setItemInHand(InteractionHand.MAIN_HAND,stack);
        var result=stack.getItem().use(helper.getLevel(),player,InteractionHand.MAIN_HAND);
        helper.assertTrue(result.getResult().consumesAction(),"Right-click did not start eating Cooked Glimmerfish");
        stack.finishUsingItem(helper.getLevel(),player);
        helper.assertTrue(player.getFoodData().getFoodLevel()==15,"Cooked Glimmerfish did not restore five hunger points");
        helper.assertTrue(stack.getCount()==1,"Food was not consumed once");
        helper.succeed();
    }
}
