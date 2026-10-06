package net.zerog.tweaks.machine;

import net.minecraft.world.level.block.entity.BlockEntity;

/** The standard menu data channel, shared by native and optional addon menus. */
public interface MachineSideMenu {
    BlockEntity sideMachine();
    int sideMode(int face);
}
