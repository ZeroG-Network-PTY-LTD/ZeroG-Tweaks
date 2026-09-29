package net.zerog.tweaks.entity;

import javax.annotation.Nullable;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

import net.zerog.tweaks.registry.ItemInit;

/**
 * Prismling (renamed from Shardling, Cerulon): small hostile swarm mob,
 * shatters into 2-3 crystal shards on death that deal 1 damage nearby.
 */
public class Prismling extends Monster {
    public Prismling(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 8.0)
                .add(Attributes.MOVEMENT_SPEED, 0.35)
                .add(Attributes.ATTACK_DAMAGE, 2.0);
    }

    @Nullable
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.AMETHYST_CLUSTER_STEP; }

    @Override
    protected void dropCustomDeathLoot(net.minecraft.server.level.ServerLevel level,
            net.minecraft.world.damagesource.DamageSource source, boolean recentlyHit) {
        super.dropCustomDeathLoot(level, source, recentlyHit);
        int n = 2 + this.random.nextInt(2);
        for (int i = 0; i < n; i++) {
            this.spawnAtLocation(ItemInit.CRYSTAL_SHARD_ITEM.get());
        }
    }
}