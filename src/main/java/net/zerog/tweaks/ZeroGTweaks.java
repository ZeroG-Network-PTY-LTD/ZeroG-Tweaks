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
        ModInit.register(modBus);
        ZGArmorMaterials.register(modBus);
        TidewraithContent.register(modBus);
        ZGStructures.register(modBus);
        net.zerog.tweaks.registry.ZGFluids.register(modBus);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::incomingDamage);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::breakSpeed);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::playerTick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.event.DailyPlanetImpacts::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::started);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::tick);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::interact);
        NeoForge.EVENT_BUS.addListener(net.zerog.tweaks.travel.PlanetTestHub::commands);
        modBus.addListener(net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent.class,event ->
                event.registerBlock(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,
                    (level,pos,state,be,side) -> level instanceof net.minecraft.server.level.ServerLevel server ?
                        net.zerog.tweaks.travel.GateLedger.get(server.getServer()).input(server,pos) : null,
                    net.zerog.tweaks.registry.BlockInit.GATE_ENERGY_PORT.get()));
    }
}
