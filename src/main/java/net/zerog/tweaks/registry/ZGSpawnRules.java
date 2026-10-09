package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.animal.WaterAnimal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.RegisterSpawnPlacementsEvent;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Where Cerulon's natural mobs may appear (which biome lists them is data: neoforge/biome_modifier/spawns_cerulon_*).
 * Land animals need Azure Moss (or vanilla animal ground) and daylight-level light. Prismlings spawn in the dark:
 * on the surface only in #zerog_tweaks:prismling_surface biomes (Cerulean Peaks, Concord Quarries: at night), elsewhere
 * only below sea level or covered authored crystal caves (including highland caves);
 * Glimmerfish use the vanilla surface-water fish rule.
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID)
public final class ZGSpawnRules {
    /** Non-authored cave habitats need this many blocks of depth below sea level. */
    public static final int PRISMLING_DEPTH = 8;
    public static final net.minecraft.tags.TagKey<net.minecraft.world.level.biome.Biome> PRISMLING_SURFACE = net.minecraft.tags.TagKey.create(
            net.minecraft.core.registries.Registries.BIOME, net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "prismling_surface"));
    public static final net.minecraft.tags.TagKey<net.minecraft.world.level.biome.Biome> PRISMLING_CAVES = net.minecraft.tags.TagKey.create(
            net.minecraft.core.registries.Registries.BIOME, net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "prismling_caves"));

    @SubscribeEvent
    public static void register(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        event.register(EntityInit.MOON_HOPPER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.DUST_GRAZER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.REGOLITH_CRAWLER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                Monster::checkMonsterSpawnRules, replace);
        ZGPlanetBlazes.TYPES.values().forEach(type->event.register(type.get(),SpawnPlacementTypes.ON_GROUND,Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::rarePlanetBlaze,replace));
        ZGGlowbugs.TYPES.values().forEach(type->event.register(type.get(),SpawnPlacementTypes.ON_GROUND,Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                (entity,level,reason,pos,random)->level.getBlockState(pos.below()).is(BlockTags.ANIMALS_SPAWNABLE_ON)&&level.getRawBrightness(pos,0)>8,replace));
        event.register(EntityInit.CRYSTAL_STAG.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.FROST_YAK.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.RUST_BEETLE.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.DUNE_BURROWER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.AZURE_FOWL.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.MOSSBACK.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::landAnimal, replace);
        event.register(EntityInit.PRISMLING_HOLDER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                ZGSpawnRules::prismling, replace);
        event.register(EntityInit.GLIMMERFISH.get(), SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                WaterAnimal::checkSurfaceWaterAnimalSpawnRules, replace);
    }

    public static boolean landAnimal(EntityType<?> type, LevelAccessor level, MobSpawnType reason, BlockPos pos, RandomSource random) {
        var ground = level.getBlockState(pos.below());
        boolean grass = ground.is(BlockInit.AZURE_MOSS.get()) || ground.is(BlockTags.ANIMALS_SPAWNABLE_ON);
        if(type==EntityInit.RUST_BEETLE.get() || type==EntityInit.DUNE_BURROWER.get() || type==EntityInit.FROST_YAK.get()
                || type==EntityInit.MOON_HOPPER.get() || type==EntityInit.DUST_GRAZER.get())
            grass |= ground.is(net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.BLOCK,
                    net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID,"planet_natural_surfaces")))
                    && ground.isFaceSturdy(level,pos.below(),net.minecraft.core.Direction.UP);
        return grass && level.getRawBrightness(pos, 0) > 8;
    }

    /** Search-worthy natural encounters, not dense rod farms. Eggs/spawners retain vanilla rules.
     * Count only loaded entities on the server thread; never iterate server entities in worldgen.
     */
    public static boolean rarePlanetBlaze(EntityType<? extends Monster> type, ServerLevelAccessor level,
                                         MobSpawnType reason, BlockPos pos, RandomSource random) {
        if(reason==MobSpawnType.CHUNK_GENERATION) return false;
        if(reason==MobSpawnType.NATURAL) {
            if(!(level instanceof net.minecraft.server.level.ServerLevel server)
                    || !server.getServer().isSameThread()
                    || !server.dimension().location().getNamespace().equals(ZeroGTweaks.MODID)
                    || random.nextInt(8)!=0) return false;
            int count=0;
            for(var entity:server.getAllEntities()) {
                if(entity instanceof net.zerog.tweaks.entity.PlanetBlaze && entity.isAlive()) {
                    if(++count>=3 || entity.distanceToSqr(pos.getX()+.5,pos.getY(),pos.getZ()+.5)<128*128) return false;
                }
            }
        }
        return Monster.checkMonsterSpawnRules(type,level,reason,pos,random);
    }

    public static boolean prismling(EntityType<? extends Monster> type, ServerLevelAccessor level, MobSpawnType reason,
                                    BlockPos pos, RandomSource random) {
        if (reason == MobSpawnType.NATURAL && !prismlingHabitat(level,pos)) return false;
        return Monster.checkMonsterSpawnRules(type, level, reason, pos, random);
    }

    /** Crystal caves can occur above sea level in highlands. Only covered positions
     * in the authored cave biomes bypass the depth rule; night surface encounters
     * remain restricted to the existing explicit surface-biome tag.
     */
    public static boolean prismlingHabitat(LevelAccessor level,BlockPos pos) {
        return level.getBiome(pos).is(PRISMLING_SURFACE)
                || pos.getY()<=level.getSeaLevel()-PRISMLING_DEPTH
                || level.getBiome(pos).is(PRISMLING_CAVES)&&!level.canSeeSky(pos);
    }

    private ZGSpawnRules() {}
}
