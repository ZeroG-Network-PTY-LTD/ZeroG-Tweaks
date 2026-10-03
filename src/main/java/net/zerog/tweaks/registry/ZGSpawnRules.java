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
 * Land animals need Azure Moss (or vanilla animal ground) and daylight-level light; Prismlings spawn only underground,
 * well below sea level, in the dark (the spec puts them in geodes and crystal caves, not on the open plains);
 * Glimmerfish use the vanilla surface-water fish rule.
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID)
public final class ZGSpawnRules {
    /** Prismlings never spawn within this many blocks of sea level or above it. */
    public static final int PRISMLING_DEPTH = 8;

    @SubscribeEvent
    public static void register(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        event.register(EntityInit.CRYSTAL_STAG.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
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
        return grass && level.getRawBrightness(pos, 0) > 8;
    }

    public static boolean prismling(EntityType<? extends Monster> type, ServerLevelAccessor level, MobSpawnType reason,
                                    BlockPos pos, RandomSource random) {
        if (reason == MobSpawnType.NATURAL && pos.getY() > level.getSeaLevel() - PRISMLING_DEPTH) return false;
        return Monster.checkMonsterSpawnRules(type, level, reason, pos, random);
    }

    private ZGSpawnRules() {}
}
