package net.zerog.tweaks;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.zerog.tweaks.registry.ModInit;

@Mod(ZeroGTweaks.MODID)
public final class ZeroGTweaks {
    public static final String MODID = "zerog_tweaks";

    public ZeroGTweaks(IEventBus modBus) {
        ModInit.register(modBus);
    }
}