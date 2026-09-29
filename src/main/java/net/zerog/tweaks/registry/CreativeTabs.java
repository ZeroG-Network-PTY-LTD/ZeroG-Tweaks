package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.zerog.tweaks.ZeroGTweaks;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class CreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ZeroGTweaks.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.zerog_tweaks"))
            .icon(() -> new ItemStack(ItemInit.NULLIFITE_INGOT.get()))
            .displayItems((params, out) -> {
                for (var e : net.minecraft.core.registries.BuiltInRegistries.ITEM) {
                    if (e.builtInRegistryHolder().key().location().getNamespace().equals(ZeroGTweaks.MODID)) {
                        out.accept(new ItemStack(e));
                    }
                }
            })
            .build());

    public static void register(IEventBus bus) {
        TABS.register(bus);
    }

    private CreativeTabs() {}
}