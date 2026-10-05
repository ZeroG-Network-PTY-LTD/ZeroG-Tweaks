package net.zerog.tweaks.gametest;

import com.google.gson.JsonParser;
import java.nio.charset.StandardCharsets;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.entity.npc.VillagerTrades;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.LiquidBlock;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class SolRuntimeGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void all_four_planet_tree_families_grow_on_planet_grass(GameTestHelper helper){
        var level=helper.getLevel();BlockPos root=helper.absolutePos(new BlockPos(8,4,8));
        for(String planet:new String[]{"moon","mars","cerulon","solvane"}){
            for(var pos:BlockPos.betweenClosed(root.offset(-4,0,-4),root.offset(4,12,4)))level.setBlock(pos,Blocks.AIR.defaultBlockState(),2);
            for(var pos:BlockPos.betweenClosed(root.offset(-3,-2,-3),root.offset(3,-1,3)))level.setBlock(pos,ZGDimensionTerrain.SOILS.get(planet).get().defaultBlockState(),2);
            for(var pos:BlockPos.betweenClosed(root.offset(-3,-1,-3),root.offset(3,-1,3)))level.setBlock(pos,ZGDimensionTerrain.GRASS.get(planet).get().defaultBlockState(),2);
            String family=net.zerog.tweaks.worldgen.PlanetEcologyProfile.tree(planet);
            var configured=level.registryAccess().registryOrThrow(net.minecraft.core.registries.Registries.CONFIGURED_FEATURE).get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",family+"_tree"));
            helper.assertTrue(configured!=null&&configured.place(level,level.getChunkSource().getGenerator(),RandomSource.create(711),root),"Configured tree cannot grow on planetary grass "+planet);
            helper.assertTrue(BuiltInRegistries.BLOCK.getKey(level.getBlockState(root).getBlock()).getPath().equals(family+"_log"),"Tree family trunk mismatched "+planet);
        }helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void sol_signatures_are_wired_and_use_caller_random(GameTestHelper helper){
        var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","sol_biome_signatures");
        var feature=BuiltInRegistries.FEATURE.get(id);helper.assertTrue(feature instanceof net.zerog.tweaks.worldgen.SolBiomeSignatureFeature,"Sol signature feature missing");
        var configured=helper.getLevel().registryAccess().registryOrThrow(net.minecraft.core.registries.Registries.CONFIGURED_FEATURE).get(id);
        helper.assertTrue(configured!=null&&configured.feature()==feature,"Signature configured feature binding wrong");
        helper.assertTrue(helper.getLevel().registryAccess().registryOrThrow(net.minecraft.core.registries.Registries.PLACED_FEATURE).get(id)!=null,"Signature placed feature missing");
        for(String biome:new String[]{"shadowed_craters","lunar_mare","lunar_highlands","polar_caps","oxide_badlands","rust_plains"}){
            helper.assertTrue(net.zerog.tweaks.worldgen.SolBiomeSignatureFeature.signature(biome)!=null,"Biome has no signature "+biome);
            var json=JsonParser.parseString(resource("data/zerog_tweaks/worldgen/biome/"+biome+".json")).getAsJsonObject();
            helper.assertTrue(json.getAsJsonArray("features").get(7).getAsJsonArray().toString().contains("zerog_tweaks:sol_biome_signatures"),"Biome signature missing from local modifications "+biome);
        }
        class OwnedRandom extends net.minecraft.world.level.levelgen.LegacyRandomSource {int calls;OwnedRandom(){super(871);}@Override public int nextInt(int bound){calls++;return super.nextInt(bound);}}
        var random=new OwnedRandom();var level=helper.getLevel();
        ((net.zerog.tweaks.worldgen.SolBiomeSignatureFeature)feature).placeSignature(new net.minecraft.world.level.levelgen.feature.FeaturePlaceContext<>(java.util.Optional.empty(),level,level.getChunkSource().getGenerator(),random,helper.absolutePos(new BlockPos(4,2,4)),net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration.INSTANCE),net.zerog.tweaks.worldgen.SolBiomeSignatureFeature.Signature.CRATER_ICE);
        helper.assertTrue(random.calls>=4,"Signature borrowed shared world random instead of feature context");helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void sol_blocks_have_real_ice_falling_metal_and_stair_properties(GameTestHelper helper){
        var level=helper.getLevel();BlockPos pos=helper.absolutePos(new BlockPos(2,2,2));
        helper.assertTrue(BlockInit.CRATER_ICE.get() instanceof net.minecraft.world.level.block.IceBlock,"Crater Ice is not actual ice");
        helper.assertTrue(BlockInit.CRATER_ICE.get().getFriction()==Blocks.ICE.getFriction(),"Crater Ice lost vanilla slippery friction");
        helper.assertTrue(BlockInit.REGOLITH.get() instanceof net.minecraft.world.level.block.FallingBlock&&BlockInit.RUSTSAND.get() instanceof net.minecraft.world.level.block.FallingBlock,"Planet sands no longer fall");
        helper.assertTrue(BlockInit.MARE_BASALT.get().defaultBlockState().getSoundType()==net.minecraft.world.level.block.SoundType.BASALT,"Mare Basalt has wrong sound");
        var plating=BlockInit.OLYMPIUM_PLATING.get().defaultBlockState();
        helper.assertTrue(plating.getDestroySpeed(level,pos)==5&&plating.getSoundType()==net.minecraft.world.level.block.SoundType.METAL&&plating.getBlock().getExplosionResistance()==9,"Olympium metal strength/sound wrong");
        helper.assertTrue(BlockInit.SMOOTH_MARE_BASALT_STAIRS.get() instanceof net.minecraft.world.level.block.StairBlock,"Planet stairs are not actual stairs");
        helper.assertTrue(BlockInit.SMOOTH_MARE_BASALT_STAIRS.get().getExplosionResistance()==BlockInit.SMOOTH_MARE_BASALT.get().getExplosionResistance(),"Stairs delegate to vanilla stone instead of their real base");
        helper.assertTrue(BlockInit.SMOOTH_MARE_BASALT_STAIRS.get().defaultBlockState().getDestroySpeed(level,pos)==BlockInit.SMOOTH_MARE_BASALT.get().defaultBlockState().getDestroySpeed(level,pos),"Stair hardness differs from own material");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void sol_mobs_attributes_and_spawn_egg_lookup_are_live(GameTestHelper helper){
        var level=helper.getLevel();
        var crawler=EntityInit.REGOLITH_CRAWLER.get().create(level);var hopper=EntityInit.MOON_HOPPER.get().create(level);var grazer=EntityInit.DUST_GRAZER.get().create(level);var maw=EntityInit.METEOR_MAW.get().create(level);
        helper.assertTrue(crawler!=null&&hopper!=null&&grazer!=null&&maw!=null,"Sol entity factory failed");
        helper.assertTrue(crawler.getMaxHealth()==14&&hopper.getMaxHealth()==6&&grazer.getMaxHealth()==24&&maw.getMaxHealth()==200,"Sol health attributes not registered");
        helper.assertTrue(crawler.getAttributeValue(Attributes.ATTACK_DAMAGE)==3&&maw.getAttributeValue(Attributes.ATTACK_DAMAGE)==8,"Hostile attack attributes missing");
        helper.assertTrue(ZGSpawnEggs.REGOLITH_CRAWLER.get().entityType()==EntityInit.REGOLITH_CRAWLER.get(),"Crawler egg unresolved");
        helper.assertTrue(ZGSpawnEggs.MOON_HOPPER.get().entityType()==EntityInit.MOON_HOPPER.get(),"Hopper egg unresolved");
        helper.assertTrue(ZGSpawnEggs.DUST_GRAZER.get().entityType()==EntityInit.DUST_GRAZER.get(),"Grazer egg unresolved");
        helper.assertTrue(ZGSpawnEggs.METEOR_MAW.get().entityType()!=null,"Meteor Maw egg unresolved");
        helper.assertTrue(hopper.isFood(new ItemStack(ItemInit.LUNAR_LICHEN_ITEM.get()))&&!hopper.isFood(new ItemStack(Items.DIAMOND)),"Hopper food predicate wrong");
        helper.assertTrue(grazer.isFood(new ItemStack(ItemInit.RUST_TUBER.get()))&&!grazer.isFood(new ItemStack(Items.DIAMOND)),"Grazer food predicate wrong");
        helper.assertTrue(hopper.getBreedOffspring(level,hopper)!=null&&grazer.getBreedOffspring(level,grazer)!=null,"Animal breeding returns no offspring");
        helper.assertTrue(maw.assetId("meteor_maw").equals("meteor_maw_ironfall"),"Meteor Maw runtime asset variant wrong");
        for(String id:new String[]{"regolith_crawler","moon_hopper","dust_grazer","meteor_maw_ironfall"})assertResource(helper,"assets/zerog_tweaks/geo/"+id+".geo.json");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void planetary_kelp_grows_paired_collects_and_binds_art(GameTestHelper helper){
        var level=helper.getLevel();int column=0;
        helper.assertTrue(ZGPlanetAquatic.FAMILIES.size()==6,"Missing planetary kelp family");
        for(var entry:ZGPlanetAquatic.FAMILIES.entrySet()){
            String theme=entry.getKey();var family=entry.getValue();BlockPos head=helper.absolutePos(new BlockPos(1+column++*2,2,2));
            level.setBlock(head.below(),Blocks.STONE.defaultBlockState(),3);
            for(int y=0;y<=5;y++)level.setBlock(head.above(y),Blocks.WATER.defaultBlockState(),3);
            var state=family.head().get().defaultBlockState().setValue(GrowingPlantHeadBlock.AGE,0);level.setBlock(head,state,3);
            helper.assertTrue(state.canSurvive(level,head),"Kelp cannot survive on submerged stone "+theme);
            family.head().get().performBonemeal(level,RandomSource.create(917),head,state);
            helper.assertTrue(level.getBlockState(head).is(family.body().get()),"Growing head converted to another family's body "+theme);
            helper.assertTrue(level.getBlockState(head.above()).is(family.head().get())||level.getBlockState(head.above()).is(family.body().get()),"Kelp did not grow upward "+theme);
            var item=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",theme+"_kelp"));
            helper.assertTrue(item!=Items.AIR,"Kelp planting item missing "+theme);
            var drops=Block.getDrops(family.body().get().defaultBlockState(),level,head,null);
            helper.assertTrue(drops.stream().anyMatch(s->s.is(item)),"Kelp body cannot be collected as matching item "+theme);
            BlockPos flowing=head.offset(0,0,5);level.setBlock(flowing.below(),Blocks.STONE.defaultBlockState(),3);level.setBlock(flowing,state,3);level.setBlock(flowing.above(),Blocks.WATER.defaultBlockState().setValue(LiquidBlock.LEVEL,5),3);
            family.head().get().performBonemeal(level,RandomSource.create(917),flowing,state);
            helper.assertTrue(level.getBlockState(flowing.above()).is(Blocks.WATER)&&level.getFluidState(flowing.above()).getAmount()<8,"Kelp grew into flowing water "+theme);
            String model="assets/zerog_tweaks/models/item/"+theme+"_kelp.json";
            var json=JsonParser.parseString(resource(model)).getAsJsonObject();String texture=json.getAsJsonObject("textures").get("layer0").getAsString();
            helper.assertTrue(texture.equals("zerog_tweaks:item/"+theme+"_kelp"),"Inventory texture binding mismatch "+theme);
            assertResource(helper,"assets/zerog_tweaks/textures/item/"+theme+"_kelp.png");assertResource(helper,"assets/zerog_tweaks/textures/block/"+theme+"_kelp.png");assertResource(helper,"assets/zerog_tweaks/textures/block/"+theme+"_kelp.png.mcmeta");
        }helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void polar_frost_is_slowing_but_not_damaging(GameTestHelper helper){
        var player=helper.makeMockPlayer(GameType.SURVIVAL);float health=player.getHealth();int frozen=player.getTicksFrozen();BlockPos pos=helper.absolutePos(new BlockPos(4,2,4));
        var frost=BlockInit.POLAR_FROST.get().defaultBlockState();helper.getLevel().setBlock(pos,frost,3);
        for(int i=0;i<100;i++)frost.getBlock().stepOn(helper.getLevel(),pos,frost,player);
        helper.assertTrue(player.hasEffect(MobEffects.MOVEMENT_SLOWDOWN),"Polar Frost does not slow grounded player");
        helper.assertTrue(player.getHealth()==health&&player.getTicksFrozen()==frozen,"Visual-only frost accumulated damage/freezing");
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void sol_professions_have_matching_pois_and_live_offers(GameTestHelper helper){
        var level=helper.getLevel();var villager=new Villager(net.minecraft.world.entity.EntityType.VILLAGER,level);
        helper.assertTrue(ZGSolTrades.REFINERY.get().matchingStates().contains(BlockInit.ORE_REFINERY.get().defaultBlockState()),"Refiner POI wrong");
        helper.assertTrue(ZGSolTrades.GENERATOR.get().matchingStates().contains(BlockInit.COMBUSTION_GENERATOR.get().defaultBlockState()),"Mechanic POI wrong");
        for(var profession:new net.minecraft.world.entity.npc.VillagerProfession[]{ZGSolTrades.REFINER.get(),ZGSolTrades.MECHANIC.get()}){
            var tiers=VillagerTrades.TRADES.get(profession);helper.assertTrue(tiers!=null,"Profession trades never wired "+profession.name());
            for(int tier=1;tier<=3;tier++){
                helper.assertTrue(tiers.get(tier)!=null&&tiers.get(tier).length>0,"Empty trade tier "+tier);
                var offer=tiers.get(tier)[0].getOffer(villager,RandomSource.create(17));helper.assertTrue(offer!=null&&!offer.getResult().isEmpty()&&offer.getMaxUses()>0,"Unusable profession offer");
            }
        }helper.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void configured_ore_uses_registered_feature_and_bounded_config(GameTestHelper helper){
        var feature=BuiltInRegistries.FEATURE.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","configured_planet_ore"));
        helper.assertTrue(feature instanceof net.zerog.tweaks.worldgen.ConfiguredPlanetOreFeature,"Ore wrapper unregistered");
        double rarity=net.zerog.tweaks.config.ZGProgressionConfig.ORE_MULTIPLIER.get();helper.assertTrue(rarity>=.1&&rarity<=10,"Ore attempts unbounded");
        var level=helper.getLevel();BlockPos origin=helper.absolutePos(new BlockPos(8,4,8));
        for(var at:BlockPos.betweenClosed(origin.offset(-4,-2,-4),origin.offset(4,2,4)))level.setBlock(at,Blocks.STONE.defaultBlockState(),2);
        class OwnedRandom extends net.minecraft.world.level.levelgen.LegacyRandomSource {int doubles;OwnedRandom(){super(1817);}@Override public double nextDouble(){doubles++;return super.nextDouble();}}
        var random=new OwnedRandom();
        var config=new net.minecraft.world.level.levelgen.feature.configurations.OreConfiguration(new net.minecraft.world.level.levelgen.structure.templatesystem.BlockMatchTest(Blocks.STONE),Blocks.DIAMOND_ORE.defaultBlockState(),4);
        ((net.zerog.tweaks.worldgen.ConfiguredPlanetOreFeature)feature).place(new net.minecraft.world.level.levelgen.feature.FeaturePlaceContext<>(java.util.Optional.empty(),level,level.getChunkSource().getGenerator(),random,origin,config));
        helper.assertTrue(random.doubles>0,"Rarity wrapper did not consume its caller-owned context random");
        helper.succeed();
    }
    private static String resource(String path){try(var stream=SolRuntimeGameTests.class.getClassLoader().getResourceAsStream(path)){if(stream==null)throw new IllegalStateException("Missing runtime resource "+path);return new String(stream.readAllBytes(),StandardCharsets.UTF_8);}catch(java.io.IOException e){throw new IllegalStateException(e);}}
    private static void assertResource(GameTestHelper helper,String path){helper.assertTrue(resource(path).length()>0,"Empty resource "+path);}
}
