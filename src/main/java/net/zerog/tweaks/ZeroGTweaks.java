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

    public ZeroGTweaks(IEventBus modBus) {
        ModInit.register(modBus);
        ZGArmorMaterials.register(modBus);
        TidewraithContent.register(modBus);
        ZGStructures.register(modBus);
        net.zerog.tweaks.registry.ZGFluids.register(modBus);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::incomingDamage);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::breakSpeed);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::playerTick);
    }
}
