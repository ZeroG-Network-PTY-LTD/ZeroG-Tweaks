package net.zerog.tweaks.registry;

import net.minecraft.world.MenuProvider;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.core.BlockPos;

/**
 * BE-side MenuProvider so openMenu can be called from the block's
 * useWithoutItem with pos in the buffer (extended menu pattern).
 */
public record OreRefineryMenuProvider(BlockPos pos) implements MenuProvider {
    @Override
    public Component getDisplayName() {
        return OreRefineryMenu.title();
    }

    @Override
    public AbstractContainerMenu createMenu(int windowId, Inventory inv, Player player) {
        BlockEntity be = player.level().getBlockEntity(pos);
        if (be instanceof OreRefineryBlockEntity refinery) {
            return new net.zerog.tweaks.machine.ProcessingMenu(windowId, inv, refinery);
        }
        return null;
    }

    public static OreRefineryMenuProvider of(BlockPos pos) {
        return new OreRefineryMenuProvider(pos);
    }
}
