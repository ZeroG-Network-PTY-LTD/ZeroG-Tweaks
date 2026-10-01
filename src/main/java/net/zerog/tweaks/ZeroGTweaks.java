package net.zerog.tweaks;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;
import net.zerog.tweaks.registry.ZGArmorMaterials;
import net.neoforged.neoforge.common.NeoForge;
import net.zerog.tweaks.item.ZGArmorSetBonuses;
import net.zerog.tweaks.registry.CreativeTabs;
import net.zerog.tweaks.registry.TidewraithContent;

@Mod(ZeroGTweaks.MODID)
public final class ZeroGTweaks {
    public static final String MODID = "zerog_tweaks";

    public ZeroGTweaks(IEventBus modBus) {
        BlockInit.register(modBus);
        ZGArmorMaterials.register(modBus);
        TidewraithContent.register(modBus);
        ItemInit.register(modBus);
        CreativeTabs.register(modBus);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::incomingDamage);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::breakSpeed);
        NeoForge.EVENT_BUS.addListener(ZGArmorSetBonuses::playerTick);
    }
}
