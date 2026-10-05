package net.zerog.tweaks.storage;

import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Container;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.ContainerOpenersCounter;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;

/** Single-block themed chest/barrel. Expanded slots are independent per placed container. */
public final class WoodStorageBlockEntity extends RandomizableContainerBlockEntity {
    private NonNullList<ItemStack> items = NonNullList.withSize(54, ItemStack.EMPTY);
    private boolean expanded;
    private final ContainerOpenersCounter openers = new ContainerOpenersCounter() {
        @Override protected void onOpen(Level level, BlockPos pos, BlockState state) { setOpen(state, true); }
        @Override protected void onClose(Level level, BlockPos pos, BlockState state) { setOpen(state, false); }
        @Override protected void openerCountChanged(Level level, BlockPos pos, BlockState state, int oldCount, int count) {}
        @Override protected boolean isOwnContainer(Player player) { return player.containerMenu instanceof ChestMenu menu && menu.getContainer() == WoodStorageBlockEntity.this; }
    };
    public WoodStorageBlockEntity(BlockPos pos, BlockState state) { super(WoodStorageRegistry.TYPE.get(), pos, state); }
    public boolean expanded() { return expanded; }
    public boolean expand() {
        if (expanded || openers.getOpenerCount() > 0) return false;
        expanded = true;
        setChanged();
        return true;
    }
    @Override public int getContainerSize() { return expanded ? 54 : 27; }
    @Override protected NonNullList<ItemStack> getItems() { return items; }
    @Override protected void setItems(NonNullList<ItemStack> value) { items = NonNullList.withSize(54, ItemStack.EMPTY); for (int i=0;i<Math.min(54,value.size());i++) items.set(i,value.get(i)); }
    @Override protected Component getDefaultName() { return getBlockState().getBlock().getName(); }
    @Override protected AbstractContainerMenu createMenu(int id, Inventory inventory) { return expanded ? ChestMenu.sixRows(id, inventory, this) : ChestMenu.threeRows(id, inventory, this); }
    @Override protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putBoolean("Expanded", expanded);
        if (!trySaveLootTable(tag)) ContainerHelper.saveAllItems(tag, items, registries);
    }
    @Override protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        expanded = tag.getBoolean("Expanded");
        items = NonNullList.withSize(54, ItemStack.EMPTY);
        if (!tryLoadLootTable(tag)) ContainerHelper.loadAllItems(tag, items, registries);
    }
    @Override public void startOpen(Player player) { if (!remove && !player.isSpectator()) openers.incrementOpeners(player, level, worldPosition, getBlockState()); }
    @Override public void stopOpen(Player player) { if (!remove && !player.isSpectator()) openers.decrementOpeners(player, level, worldPosition, getBlockState()); }
    public void recheckOpen() { if (!remove) openers.recheckOpeners(level, worldPosition, getBlockState()); }
    private void setOpen(BlockState state, boolean open) {
        if (level == null) return;
        level.setBlock(worldPosition, state.setValue(BlockStateProperties.OPEN, open), 3);
        boolean barrel = state.getBlock() instanceof WoodStorageBlock.Barrel;
        level.playSound(null, worldPosition, barrel ? (open ? SoundEvents.BARREL_OPEN : SoundEvents.BARREL_CLOSE) : (open ? SoundEvents.CHEST_OPEN : SoundEvents.CHEST_CLOSE), SoundSource.BLOCKS, .5F, .95F);
    }
}
