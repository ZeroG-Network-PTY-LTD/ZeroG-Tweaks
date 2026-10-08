package net.zerog.tweaks.machine;

import java.util.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.zerog.tweaks.genetics.*;

/** Read-only discovery adapter for verified legacy processing contracts. */
public final class LegacyRecipeCatalogue {
    public static boolean supports(String id){return id.equals("centrifuge")||id.equals("starmetal_smelter")||id.equals("silk_weaver");}
    public static List<ProcessingRecipeCatalogue.Page> basePages(String id){
        if(!supports(id))return List.of();
        try{
            var families=Class.forName("com.zerog.aeroapiary.ZeroGSlotFamilies");
            if(id.equals("silk_weaver")){
                var input=GeneticsRuntime.product("silk_thread");var output=GeneticsRuntime.product("woven_silk");
                return input.isEmpty()||output.isEmpty()?List.of():List.of(page(id,input,List.of(output),Optional.empty(),0,200));
            }
            var result=new ArrayList<ProcessingRecipeCatalogue.Page>();
            var method=id.equals("centrifuge")?families.getDeclaredMethod("centrifugeProducts",ItemStack.class):families.getDeclaredMethod("starmetal",ItemStack.class,ItemStack.class);
            method.setAccessible(true);
            for(var item:BuiltInRegistries.ITEM){
                var input=new ItemStack(item);List<ItemStack> outputs;
                if(id.equals("centrifuge")){
                    @SuppressWarnings("unchecked") var products=(List<ItemStack>)method.invoke(null,input.copy());outputs=products;
                }else{
                    var product=(ItemStack)method.invoke(null,input.copy(),new ItemStack(Items.REDSTONE));
                    outputs=product.isEmpty()?List.of():List.of(product);
                }
                if(outputs.isEmpty()||outputs.stream().anyMatch(ItemStack::isEmpty))continue;
                var flux=id.equals("starmetal_smelter")?Optional.of(new ProcessingRecipe.Counted(Ingredient.of(Items.REDSTONE),1,true)):Optional.<ProcessingRecipe.Counted>empty();
                result.add(page(id,input,outputs,flux,201*LegacyMachinePower.cost(id),201));
            }
            result.sort(Comparator.comparing(p->p.id().toString()));return List.copyOf(result);
        }catch(ReflectiveOperationException|LinkageError ex){return List.of();} // Optional addon/API absent: no invented recipes.
    }
    private static ProcessingRecipeCatalogue.Page page(String id,ItemStack input,List<ItemStack> outputs,Optional<ProcessingRecipe.Counted> catalyst,int energy,int ticks){
        var key=BuiltInRegistries.ITEM.getKey(input.getItem());
        return new ProcessingRecipeCatalogue.Page(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","legacy/"+id+"/"+key.getNamespace()+"/"+key.getPath()),
            List.of(new ProcessingRecipe.Counted(Ingredient.of(input.copyWithCount(1)),1,true)),catalyst,
            outputs.stream().map(stack->new ProcessingRecipe.Output(stack.copy(),1)).toList(),energy,ticks,energy,ticks);
    }
    public static List<ProcessingRecipeCatalogue.Page> adjusted(BlockEntity machine,List<ProcessingRecipeCatalogue.Page> pages,ItemStack selected){
        var matching=pages.stream().filter(p->selected.isEmpty()||p.inputs().stream().anyMatch(i->i.ingredient().test(selected))
            ||p.catalyst().map(i->i.ingredient().test(selected)).orElse(false)
            ||p.outputs().stream().anyMatch(o->ItemStack.isSameItemSameComponents(o.stack(),selected))).toList();
        if(matching.isEmpty()||machine==null||machine.getLevel()==null)return matching;
        boolean powered=GeneticsRuntime.legacyPowered(GeneticsRuntime.id(machine));
        int speed=powered?LegacyMachineCards.speed(machine):100,saving=powered?LegacyMachineCards.saving(machine):0;
        int baseEnergy=powered?201*LegacyMachinePower.cost(GeneticsRuntime.id(machine)):0;
        return matching.stream().map(p->new ProcessingRecipeCatalogue.Page(p.id(),p.inputs(),p.catalyst(),p.outputs(),baseEnergy,p.baseTicks(),
            (int)(((long)baseEnergy*(100-saving)+99)/100),(p.baseTicks()*100+speed-1)/speed)).toList();
    }
    private LegacyRecipeCatalogue(){}
}
