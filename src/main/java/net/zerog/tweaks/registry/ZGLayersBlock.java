package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** Thin 'layers' overlay blocks (ashfall / crater_dust / snowpack): state-safe decorative cube. */
public class ZGLayersBlock extends Block {
    public ZGLayersBlock(Properties props) { super(props); }
    @Override public boolean canSurvive(BlockState state, net.minecraft.world.level.LevelReader level, BlockPos pos) { return true; }
}