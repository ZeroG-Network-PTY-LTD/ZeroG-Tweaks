package net.zerog.tweaks.transport;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.bus.api.IEventBus;

public final class TransportMenus {
    public static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<MenuType<TransportMenu>> MENU=MENUS.register("transport_controls",()->IMenuTypeExtension.create((window,inv,buf)->new TransportMenu(window,inv,inv.player.level().getBlockEntity(buf.readBlockPos()))));
    public static final java.util.function.Supplier<MenuType<TransportFilterMenu>> FILTER=MENUS.register("transport_filter",()->IMenuTypeExtension.create((window,inv,buf)->new TransportFilterMenu(window,inv,buf.readEnum(net.minecraft.world.InteractionHand.class))));
    public static void register(IEventBus bus){MENUS.register(bus);}
    private TransportMenus(){}
}
