package net.zerog.tweaks.registry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.BucketItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.neoforged.neoforge.common.SoundActions;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;

/** Native fluid catalysts. GeneticsTank retains its existing 250 mB job dose. */
public final class ZGGeneticsFluids {
    public static final class Jelly {
        public final String id, textureFamily;
        public final int fog;
        public DeferredHolder<FluidType,FluidType> type;
        public DeferredHolder<Fluid,FlowingFluid> source, flowing;
        public DeferredBlock<LiquidBlock> block;
        public DeferredItem<BucketItem> bucket;
        private Jelly(String id,String textureFamily,int fog){this.id=id;this.textureFamily=textureFamily;this.fog=fog;}
    }
    // Reuse approved original honey artwork until dedicated jelly art is reviewed.
    public static final Jelly ROYAL=make("royal_jelly","gold_dust_bee",0xD8AB54);
    public static final Jelly COSMIC=make("cosmic_jelly","midnight_bee",0x665199);
    public static final List<Jelly> ALL=List.of(ROYAL,COSMIC);

    private static Jelly make(String id,String textureFamily,int fog){
        Jelly jelly=new Jelly(id,textureFamily,fog);
        jelly.type=ZGFluids.TYPES.register(id,()->new FluidType(FluidType.Properties.create()
                .descriptionId("fluid_type.zerog_tweaks."+id).density(1400).viscosity(6000)
                .canConvertToSource(false).canHydrate(false).canSwim(true).canDrown(true).motionScale(.004)
                .sound(SoundActions.BUCKET_FILL,SoundEvents.BUCKET_FILL)
                .sound(SoundActions.BUCKET_EMPTY,SoundEvents.BUCKET_EMPTY)));
        Supplier<BaseFlowingFluid.Properties> properties=()->new BaseFlowingFluid.Properties(jelly.type,jelly.source,jelly.flowing)
                .block(jelly.block).bucket(jelly.bucket).tickRate(30).slopeFindDistance(2).levelDecreasePerBlock(2);
        jelly.source=ZGFluids.FLUIDS.register(id,()->new BaseFlowingFluid.Source(properties.get()));
        jelly.flowing=ZGFluids.FLUIDS.register("flowing_"+id,()->new BaseFlowingFluid.Flowing(properties.get()));
        jelly.block=BlockInit.BLOCKS.register(id,()->new LiquidBlock(jelly.source.get(),Block.Properties.ofFullCopy(Blocks.WATER)));
        jelly.bucket=ItemInit.ITEMS.register(id+"_bucket",()->new BucketItem(jelly.source.get(),
                new Item.Properties().stacksTo(1).craftRemainder(Items.BUCKET)));
        return jelly;
    }
    public static void init(){ /* Force registration before the common DeferredRegisters bind. */ }
    private ZGGeneticsFluids(){}
}
