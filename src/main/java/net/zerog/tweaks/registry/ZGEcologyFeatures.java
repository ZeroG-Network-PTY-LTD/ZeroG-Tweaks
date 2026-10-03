package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.bus.api.IEventBus;
import net.zerog.tweaks.worldgen.DimensionEcologyFeature;

public final class ZGEcologyFeatures {
    private static final DeferredRegister<Feature<?>> FEATURES=DeferredRegister.create(Registries.FEATURE,"zerog_tweaks");
    static { FEATURES.register("dimension_ecology",DimensionEcologyFeature::new); }
    public static void register(IEventBus bus){ FEATURES.register(bus); }
    private ZGEcologyFeatures(){}
}
