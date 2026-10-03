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
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Prismling (renamed from Shardling, Cerulon): small hostile swarm mob,
 * shatters into 2-3 crystal shards on death that deal 1 damage nearby.
 * AI follows mob spec prismling; spawns only underground in the dark (ZGSpawnRules). Drawn by ZGGeoMobRenderer.
 */
public class Prismling extends Monster implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);

    public Prismling(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new net.minecraft.world.entity.ai.goal.FloatGoal(this));
        goalSelector.addGoal(1, new net.minecraft.world.entity.ai.goal.MeleeAttackGoal(this, 1.2, false));
        goalSelector.addGoal(2, new net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal(this, 0.8));
        goalSelector.addGoal(3, new net.minecraft.world.entity.ai.goal.LookAtPlayerGoal(this,
                net.minecraft.world.entity.player.Player.class, 8.0F));
        targetSelector.addGoal(1, new net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(2, new net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal<>(this,
                net.minecraft.world.entity.player.Player.class, true));
    }

    @Override
    public boolean doHurtTarget(net.minecraft.world.entity.Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) triggerAnim("action", "attack");
        return hit;
    }

    @Override
    public void die(net.minecraft.world.damagesource.DamageSource source) {
        super.die(source);
        // the shatter: crystal shards cut anyone standing right next to it
        if (level() instanceof net.minecraft.server.level.ServerLevel server) {
            for (var p : server.getEntitiesOfClass(net.minecraft.world.entity.player.Player.class, getBoundingBox().inflate(2))) {
                p.hurt(damageSources().mobAttack(this), 1.0F);
            }
            server.sendParticles(new net.minecraft.core.particles.BlockParticleOption(
                    net.minecraft.core.particles.ParticleTypes.BLOCK, net.zerog.tweaks.registry.BlockInit.CERULITE_CLUSTER.get()
                            .defaultBlockState()), getX(), getY() + 0.4, getZ(), 20, 0.3, 0.3, 0.3, 0.1);
        }
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        ZGGeoMob.registerControllers(this, controllers, "prismling", "walk");
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 8.0)
                .add(Attributes.MOVEMENT_SPEED, 0.35)
                .add(Attributes.ATTACK_DAMAGE, 2.0)
                .add(Attributes.FOLLOW_RANGE, 16.0);
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