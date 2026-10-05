package net.zerog.tweaks.machine;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.Level;
import java.util.*;

/** Data-driven machine recipes; real registry serializers, not a private JSON cache. */
public record ProcessingRecipe(ProcessingRegistry.Kind kind, List<Counted> inputs,
        Optional<Counted> catalyst, List<Output> outputs, int energy, int time,
        int upgradedCount) implements Recipe<ProcessingRecipe.Input> {
    public record Counted(Ingredient ingredient, int count, boolean consumed) {
        public static final Codec<Counted> CODEC=RecordCodecBuilder.create(i->i.group(
                Ingredient.CODEC_NONEMPTY.fieldOf("ingredient").forGetter(Counted::ingredient),
                Codec.intRange(1,64).optionalFieldOf("count",1).forGetter(Counted::count),
                Codec.BOOL.optionalFieldOf("consumed",true).forGetter(Counted::consumed)).apply(i,Counted::new));
        public boolean test(ItemStack stack){return stack.getCount()>=count&&ingredient.test(stack);}
    }
    public record Output(ItemStack stack, double chance) {
        public static final Codec<Output> CODEC=RecordCodecBuilder.create(i->i.group(
                ItemStack.STRICT_CODEC.fieldOf("stack").forGetter(Output::stack),
                Codec.doubleRange(0,1).optionalFieldOf("chance",1D).forGetter(Output::chance)).apply(i,Output::new));
    }
    public record Input(List<ItemStack> stacks,ItemStack catalyst) implements RecipeInput {
        @Override public ItemStack getItem(int index){return stacks.get(index);}
        @Override public int size(){return stacks.size();}
    }
    public static MapCodec<ProcessingRecipe> codec(ProcessingRegistry.Kind kind){return RecordCodecBuilder.mapCodec(i->i.group(
            Counted.CODEC.listOf().fieldOf("inputs").forGetter(ProcessingRecipe::inputs),
            Counted.CODEC.optionalFieldOf("catalyst").forGetter(ProcessingRecipe::catalyst),
            Output.CODEC.listOf().fieldOf("outputs").forGetter(ProcessingRecipe::outputs),
            Codec.intRange(1,10_000_000).fieldOf("energy").forGetter(ProcessingRecipe::energy),
            Codec.intRange(1,72_000).fieldOf("time").forGetter(ProcessingRecipe::time),
            Codec.intRange(0,64).optionalFieldOf("upgraded_result_count",0).forGetter(ProcessingRecipe::upgradedCount)
    ).apply(i,(a,b,c,d,e,f)->new ProcessingRecipe(kind,a,b,c,d,e,f)));}
    public static final class Serializer implements RecipeSerializer<ProcessingRecipe> {
        private final MapCodec<ProcessingRecipe> codec;private final StreamCodec<RegistryFriendlyByteBuf,ProcessingRecipe> stream;
        public Serializer(ProcessingRegistry.Kind kind){codec=ProcessingRecipe.codec(kind);stream=ByteBufCodecs.fromCodecWithRegistries(codec.codec());}
        @Override public MapCodec<ProcessingRecipe> codec(){return codec;}
        @Override public StreamCodec<RegistryFriendlyByteBuf,ProcessingRecipe> streamCodec(){return stream;}
    }
    /** Matching is count-aware, shapeless and assigns one input slot per ingredient. */
    public int[] assignment(Input input){
        if(inputs.isEmpty()||inputs.size()>kind.inputCount||outputs.isEmpty()||outputs.size()>kind.outputCount
                ||catalyst.isPresent()&&!catalyst.get().test(input.catalyst))return null;
        int[] used=new int[inputs.size()];Arrays.fill(used,-1);
        return assign(input,used,0)?used:null;
    }
    private boolean assign(Input input,int[] used,int n){
        if(n==inputs.size())return true;
        for(int slot=0;slot<input.size();slot++){
            boolean taken=false;for(int j=0;j<n;j++)if(used[j]==slot)taken=true;
            if(!taken&&inputs.get(n).test(input.getItem(slot))){used[n]=slot;if(assign(input,used,n+1))return true;}
        }
        return false;
    }
    @Override public boolean matches(Input input,Level level){return assignment(input)!=null;}
    @Override public ItemStack assemble(Input input,HolderLookup.Provider registries){return outputs.getFirst().stack.copy();}
    @Override public ItemStack getResultItem(HolderLookup.Provider registries){return outputs.getFirst().stack.copy();}
    @Override public boolean canCraftInDimensions(int width,int height){return width*height>=inputs.size();}
    @Override public RecipeSerializer<?> getSerializer(){return ProcessingRegistry.SERIALIZERS_BY_KIND.get(kind).get();}
    @Override public RecipeType<?> getType(){return ProcessingRegistry.TYPES_BY_KIND.get(kind).get();}
    @Override public boolean isSpecial(){return true;}
    @Override public NonNullList<Ingredient> getIngredients(){var out=NonNullList.<Ingredient>create();for(var input:inputs)out.add(input.ingredient);return out;}
}
