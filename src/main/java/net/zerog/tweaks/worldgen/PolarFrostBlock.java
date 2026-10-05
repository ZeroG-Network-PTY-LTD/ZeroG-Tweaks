package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** Cold traction penalty only: no damage or vanilla freezing accumulation. */
public final class PolarFrostBlock extends Block {
    public PolarFrostBlock(Properties properties) { super(properties); }
    @Override public void stepOn(Level level, BlockPos pos, BlockState state, Entity entity) {
        super.stepOn(level,pos,state,entity);
        if (!level.isClientSide && entity instanceof LivingEntity living &&
                !(living instanceof net.minecraft.world.entity.player.Player p && p.getAbilities().flying))
            living.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN,30,0,false,false,true));
    }
}
