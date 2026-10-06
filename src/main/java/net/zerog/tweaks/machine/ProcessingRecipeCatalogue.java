package net.zerog.tweaks.machine;

import java.util.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

/** Read-only recipe pages from the live manager, shared by the GUI and gameplay checks. */
public final class ProcessingRecipeCatalogue {
    public record Page(ResourceLocation id,List<ProcessingRecipe.Counted> inputs,
            Optional<ProcessingRecipe.Counted> catalyst,List<ProcessingRecipe.Output> outputs,
            int baseEnergy,int baseTicks,int energy,int ticks) {}
    public static List<Page> pages(ProcessingBlockEntity machine,ItemStack selected){
        if(machine.getLevel()==null)return List.of();
        return machine.getLevel().getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(machine.kind).get()).stream()
            .filter(holder->{var recipe=holder.value();return selected.isEmpty()
                ||recipe.inputs().stream().anyMatch(input->input.ingredient().test(selected))
                ||recipe.catalyst().map(input->input.ingredient().test(selected)).orElse(false)
                ||recipe.outputs().stream().anyMatch(output->ItemStack.isSameItemSameComponents(output.stack(),selected));})
            .sorted(Comparator.comparing(holder->holder.id().toString()))
            .map(holder->{var recipe=holder.value();var outputs=new ArrayList<ProcessingRecipe.Output>();
                for(int i=0;i<recipe.outputs().size();i++)outputs.add(new ProcessingRecipe.Output(machine.output(recipe,i),recipe.outputs().get(i).chance()));
                return new Page(holder.id(),List.copyOf(recipe.inputs()),recipe.catalyst(),List.copyOf(outputs),
                    recipe.energy(),recipe.time(),machine.energyCost(recipe),machine.duration(recipe));}).toList();
    }
    private ProcessingRecipeCatalogue(){}
}
