package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/** Additive spawn eggs: existing registry names are never changed. */
public final class TidewraithItems {
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ZeroGTweaks.MODID);
    private static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ZeroGTweaks.MODID);
    public static final DeferredItem<DeferredSpawnEggItem> TIDEWRAITH_EGG = ITEMS.register(
            "tidewraith_spawn_egg", () -> new DeferredSpawnEggItem(
                    EntityInit.TIDEWRAITH, 0x122A3B, 0x82D5E9, new Item.Properties()));
    public static final DeferredItem<DeferredSpawnEggItem> BOSS_EGG = ITEMS.register(
            "tidewraith_boss_spawn_egg", () -> new DeferredSpawnEggItem(
                    EntityInit.TIDEWRAITH_BOSS, 0x07383D, 0xBAFFED, new Item.Properties()));
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> SPAWN_EGGS = TABS.register(
            "spawn_eggs", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.zerog_tweaks.spawn_eggs"))
                    .icon(() -> new ItemStack(TIDEWRAITH_EGG.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(TIDEWRAITH_EGG.get());
                        output.accept(BOSS_EGG.get());
                    }).build());

    public static void register(IEventBus bus) { ITEMS.register(bus); TABS.register(bus); }
    private TidewraithItems() {}
}
