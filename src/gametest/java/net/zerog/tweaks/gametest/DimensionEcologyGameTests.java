package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.ColoredFallingBlock;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGDimensionFluids;
import net.zerog.tweaks.event.DailyPlanetImpacts;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class DimensionEcologyGameTests {
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void saplings_and_crops_accept_all_planet_soils(GameTestHelper helper){
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(8,3,8));
        for(var soil:ZGDimensionTerrain.SOILS.values()) {
            level.setBlockAndUpdate(pos,soil.get().defaultBlockState());level.setBlockAndUpdate(pos.above(),Blocks.AIR.defaultBlockState());
            for(var sapling:java.util.List.of(net.zerog.tweaks.registry.BlockInit.CHARWOOD_SAPLING,net.zerog.tweaks.registry.BlockInit.GILDWOOD_SAPLING,net.zerog.tweaks.registry.BlockInit.HOARWOOD_SAPLING,net.zerog.tweaks.registry.BlockInit.SHARDWOOD_SAPLING)) {
                helper.assertTrue(sapling.get().defaultBlockState().canSurvive(level,pos.above()),"Planet soil rejects existing sapling");
            }
            helper.assertTrue(Blocks.OAK_SAPLING.defaultBlockState().canSurvive(level,pos.above()),"Planet soil rejects vanilla oak");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void six_blaze_types_preserve_randomized_palettes_and_have_rods(GameTestHelper helper){
        var level=helper.getLevel();
        helper.assertTrue(net.zerog.tweaks.registry.ZGPlanetBlazes.TYPES.size()==6,"Missing cosmic blaze types");
        for(var entry:net.zerog.tweaks.registry.ZGPlanetBlazes.TYPES.entrySet()){
            var entity=entry.getValue().get().create(level);helper.assertTrue(entity!=null&&entity.fireImmune(),"Not vanilla-compatible fire immune blaze");
            var tag=new net.minecraft.nbt.CompoundTag();entity.addAdditionalSaveData(tag);
            var restored=entry.getValue().get().create(level);restored.readAdditionalSaveData(tag);
            helper.assertTrue(entity.palette()==restored.palette()&&entity.palette()>=0&&entity.palette()<3,"Palette did not persist");
            var rod=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",entry.getKey()+"_blaze_rod"));
            helper.assertTrue(rod!=net.minecraft.world.item.Items.AIR,"Missing matching rod");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void variant_hive_harvest_returns_its_honey_and_comb(GameTestHelper helper){
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(8,3,8));
        var player=helper.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        var hit=new net.minecraft.world.phys.BlockHitResult(net.minecraft.world.phys.Vec3.atCenterOf(pos),net.minecraft.core.Direction.NORTH,pos,false);
        for(var f:net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.values()) {
            for(var input:java.util.List.of(net.minecraft.world.item.Items.GLASS_BOTTLE,net.minecraft.world.item.Items.BUCKET)) {
                var state=f.hive.get().defaultBlockState().setValue(net.minecraft.world.level.block.BeehiveBlock.HONEY_LEVEL,5);
                level.setBlockAndUpdate(pos,state);player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new net.minecraft.world.item.ItemStack(input));
                state.useItemOn(player.getMainHandItem(),level,player,net.minecraft.world.InteractionHand.MAIN_HAND,hit);
                helper.assertTrue(player.getMainHandItem().is(input==net.minecraft.world.item.Items.BUCKET?f.bucket.get():f.bottle.get()),"Harvest returned wrong honey for "+f.id);
                helper.assertTrue(level.getBlockState(pos).getValue(net.minecraft.world.level.block.BeehiveBlock.HONEY_LEVEL)==0,"Harvest did not reset hive");
            }
            var state=f.hive.get().defaultBlockState().setValue(net.minecraft.world.level.block.BeehiveBlock.HONEY_LEVEL,5);level.setBlockAndUpdate(pos,state);
            player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.SHEARS));
            state.useItemOn(player.getMainHandItem(),level,player,net.minecraft.world.InteractionHand.MAIN_HAND,hit);
            helper.assertTrue(level.getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,new net.minecraft.world.phys.AABB(pos).inflate(2)).stream().anyMatch(i->i.getItem().is(f.comb.get())&&i.getItem().getCount()==3),"Wrong sheared comb for "+f.id);
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void twelve_half_size_bees_have_valid_hives_and_preserve_species(GameTestHelper helper){
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(8,3,8));
        helper.assertTrue(net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.size()==12,"Missing bee families");
        for(var entry:net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.entrySet()) {
            var f=entry.getValue(); var type=net.zerog.tweaks.registry.ZGGlowbugs.TYPES.get(entry.getKey()).get();
            helper.assertTrue(Math.abs(type.getWidth()-.35F)<.001&&Math.abs(type.getHeight()-.3F)<.001,"Not half vanilla bee hitbox");
            level.setBlockAndUpdate(pos,f.hive.get().defaultBlockState());
            helper.assertTrue(net.minecraft.world.level.block.entity.BlockEntityType.BEEHIVE.isValid(level.getBlockState(pos)),"Hive not valid for vanilla storage");
            helper.assertTrue(type.is(net.minecraft.tags.EntityTypeTags.BEEHIVE_INHABITORS),"Bee cannot leave hive");
            var bee=type.create(level);helper.assertTrue(bee!=null,"Cannot create bee");bee.setHivePos(pos);
            var occupant=net.minecraft.world.level.block.entity.BeehiveBlockEntity.Occupant.of(bee);
            helper.assertTrue(occupant.entityData().copyTag().getString("id").equals(net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(type).toString()),"Hive lost custom species");
            var storage=(net.minecraft.world.level.block.entity.BeehiveBlockEntity)level.getBlockEntity(pos);storage.storeBee(occupant);
            helper.assertTrue(storage.getOccupantCount()==1,"Occupant not stored");
            helper.assertTrue(f.source.get()!=f.flowing.get()&&f.bucket.get()!=null&&f.bottle.get()!=null&&f.comb.get()!=null,"Missing matching honey products");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=40)
    public static void all_34_farms_hydrate_revert_and_grow_wheat(GameTestHelper helper){
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(8,3,8));
        helper.assertTrue(ZGDimensionTerrain.dimensions().size()==34,"Missing dimension families");
        for(String id:ZGDimensionTerrain.dimensions()) {
            var farm=ZGDimensionTerrain.FARMLANDS.get(id).get();var soil=ZGDimensionTerrain.SOILS.get(id).get();
            var sand=BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id+"_star_sand"));
            helper.assertTrue(sand instanceof ColoredFallingBlock,id+" sand must fall");
            level.setBlockAndUpdate(pos,farm.defaultBlockState());level.setBlockAndUpdate(pos.above(),Blocks.AIR.defaultBlockState());
            level.setBlockAndUpdate(pos.east(),Blocks.WATER.defaultBlockState());farm.defaultBlockState().randomTick(level,pos,RandomSource.create(5));
            helper.assertTrue(level.getBlockState(pos).getValue(FarmBlock.MOISTURE)==7,id+" does not hydrate");
            helper.assertTrue(Blocks.WHEAT.defaultBlockState().canSurvive(level,pos.above()),id+" cannot support vanilla wheat");
            level.setBlockAndUpdate(pos.east(),Blocks.STONE.defaultBlockState());
            level.setBlockAndUpdate(pos,farm.defaultBlockState());farm.defaultBlockState().randomTick(level,pos,RandomSource.create(5));
            helper.assertTrue(level.getBlockState(pos).is(soil),id+" reverted to wrong soil");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void five_fluids_have_source_flow_bucket_and_pool_features(GameTestHelper helper){
        var registry=helper.getLevel().registryAccess().registryOrThrow(Registries.CONFIGURED_FEATURE);
        for(var liquid:ZGDimensionFluids.ALL){
            helper.assertTrue(liquid.source.get()!=liquid.flowing.get(),"Source and flow collapsed");
            helper.assertTrue(liquid.block.get().defaultBlockState().getFluidState().is(liquid.source.get()),"Wrong source block");
            helper.assertTrue(liquid.block.get().defaultBlockState().getLightEmission()==liquid.light,"Incorrect fluid light");
            helper.assertTrue(liquid.bucket.get() instanceof net.minecraft.world.item.BucketItem,"Missing bucket");
            helper.assertTrue(registry.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","lake_"+liquid.id))!=null,"Missing natural pool");
        }
        helper.succeed();
    }
    @GameTest(template="equipment_empty",timeoutTicks=20)
    public static void impacts_refuse_containers_and_ledger_roundtrips(GameTestHelper helper){
        var centre=helper.absolutePos(new BlockPos(8,3,8));helper.getLevel().setBlockAndUpdate(centre,Blocks.CHEST.defaultBlockState());
        helper.assertFalse(DailyPlanetImpacts.impact(helper.getLevel(),centre,2,"moon"),"Impact destroyed container");
        helper.assertTrue(helper.getLevel().getBlockState(centre).is(Blocks.CHEST),"Refused impact still changed terrain");
        var ledger=new DailyPlanetImpacts.Ledger();ledger.days.put("moon",12L);
        var saved=ledger.save(new net.minecraft.nbt.CompoundTag(),helper.getLevel().registryAccess());
        var restored=DailyPlanetImpacts.Ledger.load(saved,helper.getLevel().registryAccess());
        helper.assertTrue(restored.days.get("moon")==12L,"Lost last impact day");helper.succeed();
    }
}
