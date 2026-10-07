package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** Cosmetic wasteland vent: no block entity, server ticker or damage effect. */
public final class VentRockBlock extends Block {
    public VentRockBlock(Properties properties) { super(properties); }

    @Override public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (!level.getBlockState(pos.above()).isAir() || random.nextInt(3) != 0) return;
        // Use the caller's local animation random, never the shared server world random.
        level.addParticle(ParticleTypes.CAMPFIRE_COSY_SMOKE,
                pos.getX()+0.5+(random.nextDouble()-0.5)*0.25, pos.getY()+1.05,
                pos.getZ()+0.5+(random.nextDouble()-0.5)*0.25, 0, 0.03, 0);
    }
}
