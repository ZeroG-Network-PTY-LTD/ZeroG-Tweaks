package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BaseContainerBlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.items.ItemStackHandler;

/**
 * Shared BE for ZeroG-Tweaks machines (ore refinery today; more later).
 * Slots: 0=input ore, 1=optional catalyst, 2=output (output-only).
 * Mirrors the aeroapiary ZeroGMachineBlockEntity bridge pattern.
 */
public class OreRefineryBlockEntity extends BaseContainerBlockEntity {

    public static final int PROCESS_TICKS = 200;

    private final ItemStackHandler inventory = new ItemStackHandler(3) {
        @Override
        protected void onContentsChanged(int slot) {
            setChanged();
        }
    };
    private int progress;

    public OreRefineryBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }

    public ItemStackHandler inventory() {
        return this.inventory;
    }

    public int progress() {
        return this.progress;
    }

    public int progressPercent() {
        return Math.min(100, this.progress * 100 / PROCESS_TICKS);
    }

    /** Server tick entry (mirrors the aeroapiary machine tick pattern). */
    public static void tick(net.minecraft.world.level.Level level, BlockPos pos,
            BlockState state, OreRefineryBlockEntity be) {
        if (level.isClientSide) {
            return;
        }
        ItemStack in = be.inventory.getStackInSlot(0);
        ItemStack cat = be.inventory.getStackInSlot(1);
        ItemStack out = be.inventory.getStackInSlot(2);

        ItemStack result = Recipes.resolve(in, cat);
        boolean slotOk = !result.isEmpty() && (out.isEmpty()
                || (ItemStack.isSameItemSameComponents(out, result)
                    && out.getCount() + result.getCount() <= out.getMaxStackSize()));

        if (!slotOk) {
            be.progress = 0;
            return;
        }
        if (be.progress >= PROCESS_TICKS) {
            if (out.isEmpty()) {
                be.inventory.setStackInSlot(2, result.copy());
            } else {
                out.grow(result.getCount());
            }
            in.shrink(1);
            if (!cat.isEmpty()) {
                cat.shrink(1);
            }
            be.progress = 0;
        } else {
            be.progress++;
        }
    }

    // ===== BaseContainerBlockEntity abstracts =====

    @Override
    protected Component getDefaultName() {
        return Component.translatable("block.zerog_tweaks.ore_refinery");
    }

    @Override
    protected NonNullList<ItemStack> getItems() {
        NonNullList<ItemStack> list = NonNullList.withSize(this.inventory.getSlots(), ItemStack.EMPTY);
        for (int i = 0; i < this.inventory.getSlots(); i++) {
            list.set(i, this.inventory.getStackInSlot(i));
        }
        return list;
    }

    @Override
    protected void setItems(NonNullList<ItemStack> items) {
        for (int i = 0; i < this.inventory.getSlots() && i < items.size(); i++) {
            this.inventory.setStackInSlot(i, items.get(i));
        }
    }

    @Override
    protected AbstractContainerMenu createMenu(int windowId, Inventory inv) {
        return new OreRefineryMenu(MenuInit.ORE_REFINERY.get(), windowId, inv, this);
    }

    // ===== Container bridge to the ItemStackHandler =====

    @Override
    public int getContainerSize() {
        return this.inventory.getSlots();
    }

    @Override
    public boolean isEmpty() {
        for (int i = 0; i < this.inventory.getSlots(); i++) {
            if (!this.inventory.getStackInSlot(i).isEmpty()) {
                return false;
            }
        }
        return true;
    }

    @Override
    public ItemStack getItem(int slot) {
        return this.inventory.getStackInSlot(slot);
    }

    @Override
    public ItemStack removeItem(int slot, int amount) {
        var stack = this.inventory.extractItem(slot, amount, false);
        if (!stack.isEmpty()) {
            this.setChanged();
        }
        return stack;
    }

    @Override
    public ItemStack removeItemNoUpdate(int slot) {
        var s = this.inventory.getStackInSlot(slot);
        this.inventory.setStackInSlot(slot, ItemStack.EMPTY);
        return s;
    }

    @Override
    public void setItem(int slot, ItemStack stack) {
        this.inventory.setStackInSlot(slot, stack);
        this.setChanged();
    }

    @Override
    public boolean stillValid(Player player) {
        return this.level != null
                && this.level.getBlockEntity(this.worldPosition) == this
                && player.distanceToSqr(
                        this.worldPosition.getX() + 0.5, this.worldPosition.getY() + 0.5,
                        this.worldPosition.getZ() + 0.5) <= 64.0;
    }

    @Override
    public void clearContent() {
        for (int i = 0; i < this.inventory.getSlots(); i++) {
            this.inventory.setStackInSlot(i, ItemStack.EMPTY);
        }
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.put("Inventory", this.inventory.serializeNBT(registries));
        tag.putInt("Progress", this.progress);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        if (tag.contains("Inventory")) {
            this.inventory.deserializeNBT(registries, tag.getCompound("Inventory"));
        }
        this.progress = tag.getInt("Progress");
    }

    /** Recipe tables: vanilla-side always; aeroapiary catalyst when installed. */
    static final class Recipes {
        static ItemStack resolve(ItemStack in, ItemStack catalyst) {
            // vanilla-side (no dependency required) — doubled ore output per design doc
            if (in.is(ItemInit.RAW_CYRRIUM.get())) {
                return new ItemStack(ItemInit.CYRRIUM_INGOT.get(), 2);
            }
            if (in.is(ItemInit.CYRRIUM_ORE_ITEM.get())) {
                return new ItemStack(ItemInit.CYRRIUM_INGOT.get(), 3);
            }
            if (in.is(ItemInit.ARESITE_ORE_ITEM.get())) {
                return new ItemStack(ItemInit.ARESITE.get(), 3);
            }
            if (in.is(ItemInit.RAW_NULLIFITE_BLOCK_ITEM.get())) {
                return new ItemStack(ItemInit.NULLIFITE_INGOT.get(), 2);
            }
            // cross-mod catalyst: aeroapiary bee-industry stardust boosts aresite
            if (in.is(ItemInit.ARESITE.get())
                    && !catalyst.isEmpty()
                    && isAeroStardust(catalyst)) {
                return new ItemStack(ItemInit.ARESITE.get(), 5);
            }
            return ItemStack.EMPTY;
        }

        /** Namespace-safe check for the aeroapiary bee-industry stardust item. */
        static boolean isAeroStardust(ItemStack s) {
            var key = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(s.getItem());
            return key.getNamespace().equals("aeroapiary") && key.getPath().equals("stardust");
        }
    }
}