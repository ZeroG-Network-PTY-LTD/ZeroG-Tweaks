package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemNameBlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.zerog.tweaks.worldgen.PlanetEcologyProfile;

/** Thirty native pollinatable plants and twelve regrowing, planet-tree fruit pods. */
public final class ZGPlanetBotany {
    public static final Map<String,List<String>> FLOWERS=Map.of(
        "moon",List.of("selenite_bell","lunar_lotus","crater_daisy"),
        "mars",List.of("copper_poppy","dust_orchid","rust_lily"),
        "cerulon",List.of("tidal_iris","coral_lantern","reef_anemone"),
        "skarn",List.of("ember_torchflower","cinder_dahlia","basalt_bloom"),
        "eidolon",List.of("frost_snowdrop","ghost_camellia","rime_bell"),
        "solvane",List.of("sun_crown","corona_hibiscus","flare_tulip"));
    public static final Map<String,List<String>> SHRUBS=Map.of(
        "moon",List.of("silverfern","moon_thistle"),"mars",List.of("red_dune_brush","filter_fern"),
        "cerulon",List.of("azure_coral_bush","pearl_fern"),"skarn",List.of("ash_fan","scorched_heather"),
        "eidolon",List.of("frostlace","winter_fan"),"solvane",List.of("golden_brush","aurora_fern"));
    public static final Map<String,List<String>> FRUITS=Map.of(
        "moon",List.of("moon_plum","selenite_fig"),"mars",List.of("ares_apricot","dust_date"),
        "cerulon",List.of("lagoon_pear","cerulite_cherry"),"skarn",List.of("ember_guava","coalberry"),
        "eidolon",List.of("rime_apple","ghost_persimmon"),"solvane",List.of("solar_mango","corona_pomegranate"));
    public static final Map<String,DeferredBlock<? extends Block>> PLANTS=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<FruitBud>> BUDS=new LinkedHashMap<>();
    public static void init() {
        for(String theme:List.of("moon","mars","cerulon","skarn","eidolon","solvane")) {
            for(String id:FLOWERS.get(theme)) {
                var block=BlockInit.BLOCKS.register(id,()->new ZGFlowerBlock(MobEffects.NIGHT_VISION,5,
                        BlockBehaviour.Properties.ofFullCopy(Blocks.TORCHFLOWER).lightLevel(s->id.contains("lantern")||id.contains("ember")?4:0)));
                PLANTS.put(id,block);ItemInit.ITEMS.registerSimpleBlockItem(id,block);
            }
            for(String id:SHRUBS.get(theme)) {
                var block=BlockInit.BLOCKS.register(id,()->new ZGPlantBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.FERN)));
                PLANTS.put(id,block);ItemInit.ITEMS.registerSimpleBlockItem(id,block);
            }
            for(String id:FRUITS.get(theme)) {
                var bud=BlockInit.BLOCKS.register(id+"_buds",()->new FruitBud(BlockBehaviour.Properties.ofFullCopy(Blocks.COCOA).noCollission(),
                        theme,()->BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id))));
                BUDS.put(id,bud);
                ItemInit.ITEMS.register(id,()->new ItemNameBlockItem(bud.get(),new Item.Properties().food(
                        new FoodProperties.Builder().nutrition(4).saturationModifier(.4F).build())));
            }
        }
    }
    public static class FruitBud extends CocoaBlock {
        private final String home;
        private final Supplier<Item> fruit;
        public FruitBud(Properties properties,String home,Supplier<Item> fruit) {super(properties);this.home=home;this.fruit=fruit;}
        @Override protected boolean canSurvive(BlockState state,LevelReader level,BlockPos pos) {
            var key=BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos.relative(state.getValue(FACING))).getBlock());
            if(!key.getNamespace().equals("zerog_tweaks"))return false;
            String id=key.getPath();
            String tree=PlanetEcologyProfile.tree(home);
            return id.equals(tree+"_log")||id.equals(tree+"_wood")||id.equals("stripped_"+tree+"_log")||id.equals("stripped_"+tree+"_wood");
        }
        @Override protected InteractionResult useWithoutItem(BlockState state,Level level,BlockPos pos,Player player,BlockHitResult hit) {
            if(state.getValue(AGE)!=2)return InteractionResult.PASS;
            if(!level.isClientSide) {
                popResource(level,pos,new ItemStack(fruit.get(),2));
                level.setBlock(pos,state.setValue(AGE,0),3);
                level.playSound(null,pos,SoundEvents.SWEET_BERRY_BUSH_PICK_BERRIES,SoundSource.BLOCKS,1,1);
            }
            return InteractionResult.sidedSuccess(level.isClientSide);
        }
        @Override public ItemStack getCloneItemStack(LevelReader level,BlockPos pos,BlockState state) {return new ItemStack(fruit.get());}
    }
    public static void decorateTree(WorldGenLevel level,net.minecraft.util.RandomSource random,BlockPos trunk,String theme) {
        for(int y=1;y<=5;y++)for(var side:Direction.Plane.HORIZONTAL) {
            if(random.nextInt(6)!=0)continue;
            var pos=trunk.above(y).relative(side);if(!level.isEmptyBlock(pos))continue;
            var ids=FRUITS.get(theme);if(ids==null)return;
            var state=BUDS.get(ids.get(random.nextInt(ids.size()))).get().defaultBlockState()
                    .setValue(CocoaBlock.FACING,side.getOpposite()).setValue(CocoaBlock.AGE,random.nextInt(3));
            if(state.canSurvive(level,pos))level.setBlock(pos,state,2);
        }
    }
    private ZGPlanetBotany() {}
}
