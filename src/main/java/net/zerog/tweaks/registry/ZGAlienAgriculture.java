package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemNameBlockItem;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;

/** Additive crop IDs; native crop hydration and stem/attached-stem growth. */
public final class ZGAlienAgriculture {
    public static final Map<String,String> HOMES=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<ZGPlanetCrops.PlanetCrop>> CROPS=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<Block>> GOURDS=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<StemBlock>> STEMS=new LinkedHashMap<>();
    public static final List<String> GOURD_IDS=List.of("nebula_melon","eclipse_pumpkin","aurora_melon","solar_melon");
    static {
        add("moon","lunar_turnip","pearl_carrot","orbit_pea");
        add("mars","rust_beet","ares_chili","copper_onion");
        add("cerulon","tidal_cucumber","reef_lettuce","azure_bean");
        add("skarn","ember_radish","cinder_pepper","obsidian_aubergine");
        add("eidolon","frost_cabbage","rime_parsnip","ghost_garlic");
        add("solvane","solar_tomato","corona_corn","sunburst_squash");
        HOMES.put("nebula_melon","cerulon");HOMES.put("eclipse_pumpkin","moon");
        add("moon","lunar_snap_pea");add("mars","martian_okra");add("cerulon","reef_artichoke");
        add("skarn","cinder_asparagus");add("eidolon","glacier_broccoli");add("solvane","sunroot_beet");
        HOMES.put("aurora_melon","eidolon");HOMES.put("solar_melon","solvane");
    }
    private static void add(String home,String... ids) {for(String id:ids) HOMES.put(id,home);}
    private static <T> ResourceKey<T> key(ResourceKey<? extends net.minecraft.core.Registry<T>> registry,String id) {
        return ResourceKey.create(registry,ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id));
    }
    public static List<String> vegetables(String theme) {return CROPS.keySet().stream().filter(id->HOMES.get(id).equals(theme)).toList();}
    public static void init() {
        HOMES.forEach((id,theme)-> {
            if(GOURD_IDS.contains(id)) return;
            var produce=ItemInit.ITEMS.registerSimpleItem(id,new Item.Properties().food(new FoodProperties.Builder().nutrition(3).saturationModifier(.35F).build()));
            var crop=BlockInit.BLOCKS.register(id+"_crop",()->new ZGPlanetCrops.PlanetCrop(BlockBehaviour.Properties.ofFullCopy(Blocks.WHEAT),
                    ()->net.minecraft.core.registries.BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id+"_seeds")),produce));
            CROPS.put(id,crop);
            ItemInit.ITEMS.register(id+"_seeds",()->new ItemNameBlockItem(crop.get(),new Item.Properties()));
        });
        for(String id:GOURD_IDS) {
            var fruit=BlockInit.BLOCKS.registerSimpleBlock(id,BlockBehaviour.Properties.ofFullCopy(id.endsWith("melon")?Blocks.MELON:Blocks.PUMPKIN));
            GOURDS.put(id,fruit);ItemInit.ITEMS.registerSimpleBlockItem(id,fruit);
            ItemInit.ITEMS.registerSimpleItem(id+"_slice",new Item.Properties().food(new FoodProperties.Builder().nutrition(3).saturationModifier(.3F).build()));
            var stem=BlockInit.BLOCKS.<StemBlock>register(id+"_stem",()->new ZGSpaceStemBlock(key(Registries.BLOCK,id),key(Registries.BLOCK,id+"_attached_stem"),key(Registries.ITEM,id+"_seeds"),BlockBehaviour.Properties.ofFullCopy(Blocks.MELON_STEM)));
            STEMS.put(id,stem);
            BlockInit.BLOCKS.register(id+"_attached_stem",()->new AttachedStemBlock(key(Registries.BLOCK,id+"_stem"),key(Registries.BLOCK,id),key(Registries.ITEM,id+"_seeds"),BlockBehaviour.Properties.ofFullCopy(Blocks.ATTACHED_MELON_STEM)));
            ItemInit.ITEMS.register(id+"_seeds",()->new ItemNameBlockItem(stem.get(),new Item.Properties()));
        }
    }
    private ZGAlienAgriculture() {}
}
