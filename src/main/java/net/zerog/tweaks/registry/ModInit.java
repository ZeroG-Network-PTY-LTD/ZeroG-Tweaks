package net.zerog.tweaks.registry;

/**
 * Registration index: every DeferredRegister lives here so the ctor order
 * is one line per system (same pattern as the aeroapiary main class).
 */
public final class ModInit {
    private ModInit() {}

    public static void register(net.neoforged.bus.api.IEventBus modBus) {
        ZGEcologyFeatures.register(modBus);
        ZGVillagerAttire.register(modBus);
        ZGSolTrades.register(modBus);
        ZGPlanetVillagers.init(modBus);
        ZGGasVents.init(modBus);
        ZGGlowbugs.init(modBus);
        ZGPlanetApiary.init(modBus);
        ZGGeneticsFluids.init();
        ZGPlanetBlazes.init(modBus);
        ZGPlanetMaterials.register(modBus);
        ZGPlanetCrops.init();
        ZGAlienAgriculture.init();
        ZGPlanetCaveVariants.init();
        ZGPlanetAquatic.init();
        ZGAlienVines.init();
        ZGPlanetBotany.init();
        EntityInit.register(modBus);
        BlockInit.register(modBus);
        ItemInit.register(modBus);
        BlockEntityInit.register(modBus);
        MenuInit.register(modBus);
        CreativeTabs.register(modBus);
        ModContentHooks.register(modBus);
        ComposterHooks.register(modBus);
    }
}
