package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemNameBlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;

/** Four visually distinct growth stages; vanilla hydration/light/bonemeal behaviour. */
public final class ZGPlanetCrops {
    public static final Map<String, DeferredBlock<PlanetCrop>> CROPS = new LinkedHashMap<>();
    public static final Map<String, String> PLANET_CROPS = Map.of(
            "moon", "moon_millet", "mars", "rustgrain", "cerulon", "azure_rice",
            "skarn", "ember_wheat", "eidolon", "frost_barley", "solvane", "sunspike");
    public static class PlanetCrop extends ZGCropBlock {
        private final Supplier<? extends ItemLike> seed;
        private final Supplier<? extends Item> harvest;
        public PlanetCrop(Properties properties, Supplier<? extends ItemLike> seed, Supplier<? extends Item> harvest) {
            super(properties); this.seed=seed; this.harvest=harvest;
        }
        @Override protected ItemLike getBaseSeedId() { return seed.get(); }
        @Override public ItemStack produce() { return new ItemStack(harvest.get()); }
        @Override protected net.minecraft.world.phys.shapes.VoxelShape getShape(
                net.minecraft.world.level.block.state.BlockState state,net.minecraft.world.level.BlockGetter level,
                net.minecraft.core.BlockPos pos,net.minecraft.world.phys.shapes.CollisionContext ctx) {
            return net.minecraft.world.level.block.Block.box(0,0,0,16,2+getAge(state)*4,16);
        }
    }
    public static void init() {
        PLANET_CROPS.values().stream().sorted().forEach(name -> {
            var harvest=ItemInit.ITEMS.registerSimpleItem(name, new Item.Properties().food(
                    new FoodProperties.Builder().nutrition(2).saturationModifier(.2F).build()));
            var crop=BlockInit.BLOCKS.register(name+"_crop", () -> new PlanetCrop(
                    BlockBehaviour.Properties.ofFullCopy(Blocks.WHEAT),
                    () -> net.minecraft.core.registries.BuiltInRegistries.ITEM.get(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name+"_seeds")), harvest));
            CROPS.put(name,crop);
            ItemInit.ITEMS.register(name+"_seeds", () -> new ItemNameBlockItem(crop.get(),new Item.Properties()));
        });
        var solflower=BlockInit.BLOCKS.register("solflower_crop", () -> new PlanetCrop(
                BlockBehaviour.Properties.ofFullCopy(Blocks.WHEAT), () -> ItemInit.SOLFLOWER_SEEDS.get(), () -> ItemInit.SOLFLOWER_ITEM.get()));
        CROPS.put("solflower",solflower);
    }
    private ZGPlanetCrops() {}
}
