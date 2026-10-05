package net.zerog.tweaks.genetics;

import java.util.*;
import java.util.function.Supplier;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.item.crafting.RecipeType;

/** Optional PB 13.14 bridge: uses the server's reloaded recipes, never guessed bee products. */
public final class ProductiveBeeProduction {
    public record Output(ItemStack item,int min,int max,float chance,int productivity) {
        public Output(ItemStack item,int min,int max,float chance){this(item,min,max,chance,0);}
        public Output { item=item.copy(); }
        public ItemStack maximum(){return item.copyWithCount(productiveQuantity(max,productivity));}
        public ItemStack roll(ServerLevel level){return level.random.nextFloat()<chance?item.copyWithCount(productiveQuantity(min+level.random.nextInt(max-min+1),productivity)):ItemStack.EMPTY;}
    }
    /** PB13.14 AdvancedBeehiveBlockEntity.lambda$beeReleasePostAction$1, verbatim arithmetic. */
    public static int productiveQuantity(int count,int value){if(count<=0||value<=0)return count;return count==1?count+value:count+Math.round((1.0f/(value+2.0f)+(value+1.0f)/2.0f)*count);}
    @SuppressWarnings({"rawtypes","unchecked"})
    public static List<Output> outputs(ItemStack cage,ServerLevel level) {
        var genes=ProductiveBeeGenes.read(cage);if(genes.size()!=5)return List.of();
        // read() validates the enum domain against the installed PB GeneValue API.
        int productivity=ProductiveBeeGenes.numeric(genes.get("productivity"));
        var data=cage.get(DataComponents.CUSTOM_DATA);if(data==null)return List.of();var tag=data.copyTag();
        var entityId=ResourceLocation.tryParse(tag.getString("entity"));var beeType=ResourceLocation.tryParse(tag.getString("type"));
        if(entityId==null||!entityId.getNamespace().equals("productivebees"))return List.of();
        var recipeId=ResourceLocation.fromNamespaceAndPath("productivebees","advanced_beehive");
        if(!BuiltInRegistries.RECIPE_TYPE.containsKey(recipeId))return List.of();
        RecipeType type=BuiltInRegistries.RECIPE_TYPE.get(recipeId);
        try {
            for(Object raw:level.getRecipeManager().getAllRecipesFor(type)) {
                Object recipe=((RecipeHolder<?>)raw).value();
                if(!recipe.getClass().getName().equals("cy.jdkdigital.productivebees.common.recipe.AdvancedBeehiveRecipe"))continue;
                Object ingredient=((Supplier<?>)recipe.getClass().getField("ingredient").get(recipe)).get();
                Object entity=ingredient.getClass().getMethod("getBeeEntity").invoke(ingredient);
                if(entity!=BuiltInRegistries.ENTITY_TYPE.get(entityId))continue;
                boolean configurable=(Boolean)ingredient.getClass().getMethod("isConfigurable").invoke(ingredient);
                if(configurable&&(beeType==null||!beeType.equals(ingredient.getClass().getMethod("getBeeType").invoke(ingredient))))continue;
                var results=(Map<?,?>)recipe.getClass().getMethod("getRecipeOutputs").invoke(recipe);
                var outputs=new ArrayList<Output>();
                for(var entry:results.entrySet()) {
                    if(!(entry.getKey() instanceof ItemStack item)||item.isEmpty())return List.of();
                    Object value=entry.getValue();int min=(Integer)value.getClass().getMethod("min").invoke(value),max=(Integer)value.getClass().getMethod("max").invoke(value);
                    float chance=(Float)value.getClass().getMethod("chance").invoke(value);
                    if(min<0||max<min||max>item.getMaxStackSize()||!Float.isFinite(chance)||chance<0||chance>1)return List.of();
                    if(max>0&&chance>0)outputs.add(new Output(item,min,max,chance,productivity));
                }
                return List.copyOf(outputs);
            }
        } catch(ReflectiveOperationException|ClassCastException|LinkageError ex) { return List.of(); }
        return List.of();
    }
    private ProductiveBeeProduction(){}
}
