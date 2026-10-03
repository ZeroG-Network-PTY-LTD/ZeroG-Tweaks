package net.zerog.tweaks.gametest;

import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicReference;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BeehiveBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.LegacyRandomSource;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.worldgen.DimensionEcologyFeature;

/** Executes the real feature on a worker; sparse terrain avoids expensive chunk setup.
 * The guarded world RNG makes a normally timing-dependent race deterministic.
 */
@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class EcologyThreadingGameTests {
    @GameTest(template="equipment_empty", timeoutTicks=40)
    public static void occupied_hive_worldgen_never_uses_server_random(GameTestHelper helper) throws Exception {
        var level=helper.getLevel();
        // GameTestServer omits mod dimensions. Select Cerulon's feature family only
        // during the synchronous worker probe; never modify a saved world.
        var dimensionField=Level.class.getDeclaredField("dimension");dimensionField.setAccessible(true);
        var originalDimension=level.dimension();
        var terrain=new HashMap<BlockPos,BlockState>();
        var hives=new HashMap<BlockPos,BeehiveBlockEntity>();
        WorldGenLevel region=(WorldGenLevel)Proxy.newProxyInstance(WorldGenLevel.class.getClassLoader(),
                new Class<?>[]{WorldGenLevel.class},(proxy,method,args)->switch(method.getName()) {
                    case "getLevel" -> level;
                    case "getHeight" -> 80;
                    case "getHeightmapPos" -> new BlockPos(((BlockPos)args[1]).getX(),80,((BlockPos)args[1]).getZ());
                    case "getBlockState" -> terrain.getOrDefault(args[0],((BlockPos)args[0]).getY()<80
                            ? ZGDimensionTerrain.SOILS.get("cerulon").get().defaultBlockState():Blocks.AIR.defaultBlockState());
                    case "isEmptyBlock" -> !terrain.containsKey(args[0]) && ((BlockPos)args[0]).getY()>=80;
                    case "setBlock" -> {
                        var pos=((BlockPos)args[0]).immutable();var state=(BlockState)args[1];terrain.put(pos,state);
                        if(state.getBlock() instanceof net.minecraft.world.level.block.BeehiveBlock)
                            hives.put(pos,new BeehiveBlockEntity(pos,state));
                        yield true;
                    }
                    case "getBlockEntity" -> hives.get(args[0]);
                    default -> method.invoke(level,args);
                });
        var contextRandom=new LegacyRandomSource(42) {
            @Override public int nextInt(int bound) { return bound==8?0:1%bound; }
        };
        var field=Level.class.getDeclaredField("random");field.setAccessible(true);
        var original=level.random;var owner=Thread.currentThread();
        var failure=new AtomicReference<Throwable>();
        field.set(level,new LegacyRandomSource(42) {
            @Override public int next(int bits) {
                if(Thread.currentThread()!=owner)
                    throw new IllegalStateException("Accessing LegacyRandomSource from multiple threads: worldgen used server RNG");
                return super.next(bits);
            }
        });
        try {
            dimensionField.set(level,ResourceKey.create(Registries.DIMENSION,
                    ResourceLocation.fromNamespaceAndPath("zerog_tweaks","cerulon")));
            var worker=new Thread(()->{
                try {
                    var context=new FeaturePlaceContext<>(Optional.empty(),region,level.getChunkSource().getGenerator(),
                            contextRandom,new BlockPos(0,80,0),NoneFeatureConfiguration.INSTANCE);
                    if(!new DimensionEcologyFeature().place(context)) throw new AssertionError("Feature did not generate");
                } catch(Throwable problem) { failure.set(problem); }
            },"ZeroG-worldgen-regression");
            worker.start();worker.join(5000);
            helper.assertFalse(worker.isAlive(),"Feature worker exceeded five seconds");
        } finally { field.set(level,original);dimensionField.set(level,originalDimension); }
        if(failure.get()!=null) {
            failure.get().printStackTrace();
            helper.assertTrue(false,"Worldgen worker failed: "+failure.get());
        }
        helper.assertTrue(hives.size()==1,"Regression must exercise occupied hive generation");
        var storage=hives.values().iterator().next();
        helper.assertTrue(storage.getOccupantCount()==2,"Generated hive lost its bees");
        var occupants=storage.collectComponents().get(net.minecraft.core.component.DataComponents.BEES);
        helper.assertTrue(occupants!=null&&occupants.size()==2,"Hive components lost occupant data");
        for(var occupant:occupants) {
            var bee=occupant.createEntity(level,storage.getBlockPos());
            helper.assertTrue(bee instanceof net.zerog.tweaks.entity.AlienGlowbug,"Hive did not release custom bee");
            helper.assertTrue(((net.minecraft.world.entity.animal.Bee)bee).getHivePos().equals(storage.getBlockPos()),"Released bee lost hive position");
            helper.assertTrue(occupant.minTicksInHive()==600,"Changed vanilla no-nectar residence time");
            bee.discard();
        }
        helper.succeed();
    }
}
