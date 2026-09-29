package net.zerog.tweaks.registry;

import javax.annotation.Nullable;
import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CaveVines;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.gameevent.GameEvent;

/** Shared berry-picking logic for Pyrevine — mirrors {@code CaveVines.use} but drops Pyrefruit. */
public final class ZGCaveVines {
    private ZGCaveVines() {}

    public static InteractionResult use(@Nullable Entity entity, BlockState state, Level level, BlockPos pos) {
        if (!state.getValue(CaveVines.BERRIES)) {
            return InteractionResult.PASS;
        }
        Block.popResource(level, pos, new ItemStack(ItemInit.PYREFRUIT.get(), 1));
        float pitch = Mth.randomBetween(level.random, 0.8F, 1.2F);
        level.playSound(null, pos, SoundEvents.CAVE_VINES_PICK_BERRIES, SoundSource.BLOCKS, 1.0F, pitch);
        BlockState picked = state.setValue(CaveVines.BERRIES, false);
        level.setBlock(pos, picked, 2);
        level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(entity, picked));
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
}
