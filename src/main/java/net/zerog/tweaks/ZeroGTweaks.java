package net.zerog.tweaks;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;
import net.zerog.tweaks.registry.CreativeTabs;

@Mod(ZeroGTweaks.MODID)
public final class ZeroGTweaks {
    public static final String MODID = "zerog_tweaks";

    public ZeroGTweaks(IEventBus modBus) {
        BlockInit.register(modBus);
        ItemInit.register(modBus);
        CreativeTabs.register(modBus);
    }
}