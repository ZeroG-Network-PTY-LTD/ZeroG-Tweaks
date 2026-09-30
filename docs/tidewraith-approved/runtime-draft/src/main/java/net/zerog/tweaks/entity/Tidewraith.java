package net.zerog.tweaks.entity;

import java.util.EnumSet;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.FlyingMob;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Approved two-eye Tidewraith. Flight, blinking and mouth motion use authored clips. */
public class Tidewraith extends FlyingMob implements Enemy, GeoEntity {
    private static final EntityDataAccessor<Integer> VARIANT =
            SynchedEntityData.defineId(Tidewraith.class, EntityDataSerializers.INT);
    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);
    private int attackCooldown;

    public Tidewraith(EntityType<? extends Tidewraith> type, Level level) {
        super(type, level);
        this.moveControl = new FlyingMoveControl(this, 10, true);
        this.setNoGravity(true);
        this.xpReward = 5;
    }

    public boolean isBoss() { return false; }
    public int getVariant() { return this.entityData.get(VARIANT); }
    public void setVariant(int variant) { this.entityData.set(VARIANT, Mth.clamp(variant, 0, 3)); }
    public String assetId() { return isBoss() ? "tidewraith_boss" : "tidewraith"; }

    public static AttributeSupplier.Builder createAttributes() {
        // Initial test balance, not a replacement for the campaign boss specification.
        return Mob.createMobAttributes().add(Attributes.MAX_HEALTH, 30)
                .add(Attributes.MOVEMENT_SPEED, 0.25).add(Attributes.FLYING_SPEED, 0.35)
                .add(Attributes.FOLLOW_RANGE, 24).add(Attributes.ATTACK_DAMAGE, 4);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(VARIANT, 0);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Variant", getVariant());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        setVariant(tag.getInt("Variant"));
    }

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation navigation = new FlyingPathNavigation(this, level);
        navigation.setCanFloat(true);
        return navigation;
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(1, new FlightGoal());
        this.targetSelector.addGoal(1, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        this.setNoGravity(true);
        if (!this.level().isClientSide) {
            if (attackCooldown > 0) attackCooldown--;
            // Server-triggered eyes: all clients see the same blink, with per-entity offsets.
            if ((this.tickCount + this.getId() * 7) % 100 == 0) triggerAnim("eyes", "blink");
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && !this.level().isClientSide) triggerAnim("mouth", "mouth_open");
        return hit;
    }

    @Override
    protected boolean shouldDespawnInPeaceful() { return true; }
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.PHANTOM_AMBIENT; }
    @Override
    protected SoundEvent getHurtSound(net.minecraft.world.damagesource.DamageSource source) {
        return SoundEvents.PHANTOM_HURT;
    }
    @Override
    protected SoundEvent getDeathSound() { return SoundEvents.PHANTOM_DEATH; }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        String prefix = "animation.zerog_tweaks." + assetId() + ".";
        RawAnimation fly = RawAnimation.begin().thenLoop(prefix + "fly");
        controllers.add(new AnimationController<>(this, "flight", 5,
                state -> state.setAndContinue(fly)));
        controllers.add(new AnimationController<>(this, "eyes", 0, state -> PlayState.STOP)
                .triggerableAnim("blink", RawAnimation.begin().thenPlay(prefix + "blink")));
        controllers.add(new AnimationController<>(this, "mouth", 2, state -> PlayState.STOP)
                .triggerableAnim("mouth_open", RawAnimation.begin().thenPlay(prefix + "mouth_open")));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }

    /** Bounded hovering patrol / direct visible-target flight, without ground-only melee navigation. */
    private final class FlightGoal extends Goal {
        private Vec3 destination;
        private int patrolTicks;

        FlightGoal() { setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK)); }
        @Override
        public boolean canUse() { return true; }
        @Override
        public boolean requiresUpdateEveryTick() { return true; }
        @Override
        public void tick() {
            var target = getTarget();
            if (target != null && target.isAlive() && hasLineOfSight(target)) {
                destination = new Vec3(target.getX(), target.getY() + 0.2, target.getZ());
                getLookControl().setLookAt(target, 20, 20);
                if (attackCooldown == 0 && isWithinMeleeAttackRange(target)) {
                    doHurtTarget(target);
                    attackCooldown = isBoss() ? 40 : 30;
                }
            } else if (destination == null || --patrolTicks <= 0 || horizontalCollision
                    || position().distanceToSqr(destination) < 1) {
                // Roam near the current location, staying inside the level's build bounds.
                destination = position().add(random.nextInt(17) - 8,
                        random.nextInt(7) - 3, random.nextInt(17) - 8);
                destination = new Vec3(destination.x,
                        Mth.clamp(destination.y, level().getMinBuildHeight() + 2,
                                level().getMaxBuildHeight() - 4), destination.z);
                patrolTicks = 60;
            }
            if (destination != null) getMoveControl().setWantedPosition(
                    destination.x, destination.y, destination.z, 1);
            yBodyRot = getYRot();
        }
    }
}
