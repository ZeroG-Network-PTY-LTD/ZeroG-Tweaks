package net.zerog.tweaks;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.zerog.tweaks.item.ZGArmorSetBonuses;
import net.zerog.tweaks.registry.ModInit;
import net.zerog.tweaks.registry.TidewraithContent;
import net.zerog.tweaks.registry.ZGArmorMaterials;
import net.zerog.tweaks.worldgen.ZGStructures;

@Mod(ZeroGTweaks.MODID)
public final class ZeroGTweaks {
    public static final String MODID = "zerog_tweaks";

    public ZeroGTweaks(IEventBus modBus, net.neoforged.fml.ModContainer container) {
        container.registerConfig(net.neoforged.fml.config.ModConfig.Type.COMMON, net.zerog.tweaks.registry.ZGEcologyConfig.SPEC);
        container.registerConfig(net.neoforged.fml.config.ModConfig.Type.CLIENT, net.zerog.tweaks.registry.ZGWeatherConfig.SPEC);
        container.registerConfig(net.neoforged.fml.config.ModConfig.Type.COMMON, net.zerog.tweaks.config.ZGProgressionConfig.SPEC, "zerog-progression-common.toml");
        net.zerog.tweaks.transport.TransportRegistry.register(modBus);
        net.zerog.tweaks.storage.WoodStorageRegistry.register(modBus);
        net.zerog.tweaks.storage.StorageTankRegistry.register(modBus);
        net.zerog.tweaks.transport.TransportMenus.register(modBus);
        net.zerog.tweaks.machine.CombustionRegistry.register(modBus);
        net.zerog.tweaks.machine.ProcessingRegistry.register(modBus);
        container.registerConfig(net.neoforged.fml.config.ModConfig.Type.SERVER, net.zerog.tweaks.machine.MachineUpgradeConfig.SPEC, "zerog-machine-upgrades-server.toml");
        net.zerog.tweaks.power.PowerRegistry.register(modBus);
        container.registerConfig(net.neoforged.fml.config.ModConfig.Type.SERVER, net.zerog.tweaks.power.PowerConfig.SPEC);
        net.zerog.tweaks.travel.SurvivalGates.register(modBus);
        net.zerog.tweaks.genetics.AlvearyRegistry.register(modBus);
        ModInit.register(modBus);
        ZGArmorMaterials.register(modBus);
        TidewraithContent.register(modBus);
        modBus.addListener(net.zerog.tweaks.genetics.GeneticsIntegration::capabilities);
        ZGStructures.register(modBus);
        net.zerog.tweaks.registry.ZGFluids.register(modBus);
        net.zerog.tweaks.registry.ZGSounds.register(modBus);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::incomingDamage);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::breakSpeed);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::playerTick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.registry.ZGSolTrades::trades);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.HandheldBeeSmoker::item);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.HandheldBeeSmoker::block);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.HandheldBeeSmoker::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.HandheldBeeSmoker::logout);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.HandheldBeeSmoker::stopped);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.DailyPlanetImpacts::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::pickup);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::interact);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::loot);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::placed);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.lore.ConcordPrologue::greeting);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.AlienFarmlandSensor::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::started);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::interact);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::commands);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.SurvivalGates::interact);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.PlanetGravity::changed);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.PlanetGravity::cloned);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.PlanetGravity::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::breaking);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::placing);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::fluid);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::piston);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::explosion);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::damage);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::spawn);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.ArrivalProtection::tick);
        modBus.addListener(net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent.class,event ->
                event.registerBlock(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,
                    (level,pos,state,be,side) -> {
                        if (!(level instanceof net.minecraft.server.level.ServerLevel server)) return null;
                        var legacy = net.zerog.tweaks.travel.GateLedger.get(server.getServer()).input(server,pos);
                        return legacy != null ? legacy : net.zerog.tweaks.travel.SurvivalGates.portEnergy(server,pos);
                    },
                    net.zerog.tweaks.registry.BlockInit.GATE_ENERGY_PORT.get()));
    }
}
