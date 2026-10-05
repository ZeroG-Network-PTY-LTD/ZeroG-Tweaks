package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.bus.api.IEventBus;
import net.zerog.tweaks.worldgen.DimensionEcologyFeature;

public final class ZGEcologyFeatures {
    private static final DeferredRegister<Feature<?>> FEATURES=DeferredRegister.create(Registries.FEATURE,"zerog_tweaks");
    static {
        FEATURES.register("configured_planet_ore",net.zerog.tweaks.worldgen.ConfiguredPlanetOreFeature::new);
        FEATURES.register("dimension_ecology",DimensionEcologyFeature::new);
        FEATURES.register("planet_settlement",net.zerog.tweaks.worldgen.PlanetSettlementFeature::new);
        FEATURES.register("planet_mineshaft",net.zerog.tweaks.worldgen.PlanetMineshaftFeature::new);
        FEATURES.register("planet_cave_ecology",net.zerog.tweaks.worldgen.PlanetCaveEcologyFeature::new);
        FEATURES.register("sol_biome_signatures",net.zerog.tweaks.worldgen.SolBiomeSignatureFeature::new);
    }
    public static void register(IEventBus bus){ FEATURES.register(bus); }
    private ZGEcologyFeatures(){}
}
