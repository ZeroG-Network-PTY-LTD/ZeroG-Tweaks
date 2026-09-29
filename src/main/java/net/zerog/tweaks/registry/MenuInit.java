package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import net.zerog.tweaks.ZeroGTweaks;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.level.block.entity.BlockEntity;

/**
 * Machine menu types. Extended factory carries the block pos through the
 * network buffer so client+server agree on the BE (aeroapiary pattern,
 * verified against ModMenus there).
 */
public final class MenuInit {
    public static final DeferredRegister<MenuType<?>> MENUS =
            DeferredRegister.create(Registries.MENU, ZeroGTweaks.MODID);

    public static final DeferredHolder<MenuType<?>, MenuType<OreRefineryMenu>> ORE_REFINERY =
            MENUS.register("ore_refinery", () -> IMenuTypeExtension.create(
                    (int windowId, Inventory inv, RegistryFriendlyByteBuf buf) -> {
                        BlockPos pos = buf.readBlockPos();
                        BlockEntity be = inv.player.level().getBlockEntity(pos);
                        if (be instanceof OreRefineryBlockEntity machine) {
                            return new OreRefineryMenu(MenuInit.ORE_REFINERY.get(), windowId, inv, machine);
                        }
                        return null;
                    }));

    private MenuInit() {}

    public static void register(IEventBus modBus) {
        MENUS.register(modBus);
    }
}