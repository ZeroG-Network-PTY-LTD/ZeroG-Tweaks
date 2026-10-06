package net.zerog.tweaks.registry;

import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.items.SlotItemHandler;

/**
 * Retained legacy menu registry compatibility. New block interactions use the
 * shared powered ProcessingMenu, including its three bounded upgrade slots.
 */
public class OreRefineryMenu extends AbstractContainerMenu {

    private final OreRefineryBlockEntity machine;
    private final ContainerData data;

    public OreRefineryMenu(MenuType<?> type, int windowId, Inventory playerInv,
            OreRefineryBlockEntity machine) {
        super(type, windowId);
        this.machine = machine;
        this.data = playerInv.player.level().isClientSide ? new SimpleContainerData(1) : new ContainerData() {
            public int get(int index) { return machine.progressPercent(); }
            public void set(int index, int value) {}
            public int getCount() { return 1; }
        };
        addDataSlots(this.data);
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

    public int progressPercent() { return Math.max(0, Math.min(100, data.get(0))); }

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
        if (!stillValid(player) || index < 0 || index >= slots.size()) return ItemStack.EMPTY;
        var slot = slots.get(index);
        if (!slot.hasItem()) return ItemStack.EMPTY;
        var stack = slot.getItem(); var original = stack.copy();
        boolean moved;
        if (index < 3) moved = moveItemStackTo(stack, 3, slots.size(), true);
        else if (machine.inventory().isItemValid(0,stack)) moved = moveItemStackTo(stack, 0, 1, false);
        else if (machine.inventory().isItemValid(1,stack)) moved = moveItemStackTo(stack, 1, 2, false);
        else return ItemStack.EMPTY;
        if (!moved) return ItemStack.EMPTY;
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY); else slot.setChanged();
        slot.onTake(player, stack); return original;
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
