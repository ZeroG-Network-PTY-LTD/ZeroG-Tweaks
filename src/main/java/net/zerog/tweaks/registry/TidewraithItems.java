package net.zerog.tweaks.registry;

import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/** Additive spawn eggs: existing registry names are never changed. The regular egg lives in ZGSpawnEggs. */
public final class TidewraithItems {
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ZeroGTweaks.MODID);
    public static final DeferredItem<ZGSpawnEggItem> TIDEWRAITH_EGG = ZGSpawnEggs.TIDEWRAITH;
    public static final DeferredItem<DeferredSpawnEggItem> BOSS_EGG = ITEMS.register(
            "tidewraith_boss_spawn_egg", () -> new DeferredSpawnEggItem(
                    EntityInit.TIDEWRAITH_BOSS, 0x07383D, 0xBAFFED, new Item.Properties()));

    public static void register(IEventBus bus) { ITEMS.register(bus); }
    private TidewraithItems() {}
}
