package net.zerog.tweaks.registry;

import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.items.SlotItemHandler;

/**
 * Ore refinery menu: 0=input, 1=optional catalyst (aeroapiary stardust),
 * 2=output. Player inventory below; mirrors the aeroapiary zerog_machine
 * menu pattern.
 */
public class OreRefineryMenu extends AbstractContainerMenu {

    private final OreRefineryBlockEntity machine;

    public OreRefineryMenu(MenuType<?> type, int windowId, Inventory playerInv,
            OreRefineryBlockEntity machine) {
        super(type, windowId);
        this.machine = machine;
        IItemHandler inv = machine.inventory();

        this.addSlot(new SlotItemHandler(inv, 0, 57, 36));     // ore input
        this.addSlot(new SlotItemHandler(inv, 1, 93, 36));     // catalyst
        this.addSlot(new OutputSlot(inv, 2, 129, 36));         // output (x+1)

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInv, col + row * 9 + 9, 8 + col * 18, 84 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInv, col, 8 + col * 18, 142));
        }
    }

    public OreRefineryBlockEntity machine() {
        return this.machine;
    }

    private static class OutputSlot extends SlotItemHandler {
        public OutputSlot(IItemHandler handler, int index, int x, int y) {
            super(handler, index, x, y);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return false; // output-only
        }
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        return ItemStack.EMPTY; // TODO shift-click routing
    }

    @Override
    public boolean stillValid(Player player) {
        return this.machine.stillValid(player);
    }

    public static Component title() {
        return Component.translatable("block.zerog_tweaks.ore_refinery");
    }

    public static Component catalystHint() {
        return Component.translatable("block.zerog_tweaks.ore_refinery.catalyst_hint");
    }
}