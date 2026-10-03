package net.zerog.tweaks.entity;

import java.util.EnumSet;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.util.TimeUtil;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.NeutralMob;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowParentGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.TemptGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.goal.target.ResetUniversalAngerTargetGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.Vec3;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Mossback (zerog_tweaks:mossback; Shattered Skies design, docs/shattered-skies/models/mossback*.json): a big, mossy grazer
 * of the Azure Moss plains. Neutral: it grazes and ignores you until hit, then fights back with head tosses and a
 * Leap Slam (charges, leaps, and lands with a shockwave). Herd members join in.
 *
 * Four styles share the rig and the abilities, each with its own model, animations and texture, rolled at spawn:
 * Mossback 65%, Autumn 20%, Ruinback 10%, Blossom 5% (the sheet's rare one). Calves keep a parent's style.
 */
public class Mossback extends Animal implements NeutralMob, GeoEntity, ZGGeoMob {
    public enum Style {
        MOSSBACK("mossback", 65), AUTUMN("mossback_autumn", 20), RUINBACK("mossback_ruinback", 10), BLOSSOM("mossback_blossom", 5);

        public final String id;
        public final int weight;

        Style(String id, int weight) {
            this.id = id;
            this.weight = weight;
        }

        public static Style byId(int i) {
            Style[] all = values();
            return all[Mth.clamp(i, 0, all.length - 1)];
        }

        /** Weighted pick: roll in [0, 100). */
        public static Style forRoll(int roll) {
            for (Style s : values()) {
                if (roll < s.weight) return s;
                roll -= s.weight;
            }
            return MOSSBACK;
        }
    }

    private static final EntityDataAccessor<Integer> STYLE = SynchedEntityData.defineId(Mossback.class, EntityDataSerializers.INT);
    private static final UniformInt PERSISTENT_ANGER_TIME = TimeUtil.rangeOfSeconds(20, 39);
    public static final float SLAM_DAMAGE = 7.0F;

    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);
    private int remainingPersistentAngerTime;
    @Nullable private UUID persistentAngerTarget;

    public Mossback(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes().add(Attributes.MAX_HEALTH, 40.0).add(Attributes.ATTACK_DAMAGE, 7.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.0).add(Attributes.ARMOR, 4.0).add(Attributes.MOVEMENT_SPEED, 0.23)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6).add(Attributes.FOLLOW_RANGE, 20.0);
    }

    // ---- style ---------------------------------------------------------------------------------------------------------------

    public Style getStyle() { return Style.byId(entityData.get(STYLE)); }
    public void setStyle(Style style) { entityData.set(STYLE, style.ordinal()); }

    @Override
    public String assetId(String base) { return getStyle().id; }

    @Override
    protected Component getTypeName() {
        Style s = getStyle();
        return s == Style.MOSSBACK ? super.getTypeName() : Component.translatable("entity.zerog_tweaks." + s.id);
    }

    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType type,
                                        @Nullable SpawnGroupData data) {
        if (type != MobSpawnType.BREEDING) setStyle(Style.forRoll(level.getRandom().nextInt(100)));
        return super.finalizeSpawn(level, difficulty, type, data);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(STYLE, 0);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Style", getStyle().ordinal());
        addPersistentAngerSaveData(tag);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        setStyle(Style.byId(tag.getInt("Style")));
        readPersistentAngerSaveData(level(), tag);
    }

    // ---- AI ------------------------------------------------------------------------------------------------------------------

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new LeapSlamGoal());
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.3, true));
        goalSelector.addGoal(3, new BreedGoal(this, 1.0));
        goalSelector.addGoal(4, new TemptGoal(this, 1.1, this::isFood, false));
        goalSelector.addGoal(5, new FollowParentGoal(this, 1.1));
        goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, 0.9));
        goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, true, false, this::isAngryAt));
        targetSelector.addGoal(3, new ResetUniversalAngerTargetGoal<>(this, false));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide) {
            updatePersistentAnger((ServerLevel) level(), true);
            if ((tickCount + getId() * 7) % 110 == 0) triggerAnim("eyes", "blink_" + getStyle().id);
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) triggerAnim("action", "attack_" + getStyle().id);
        return hit;
    }

    @Override
    public boolean isFood(ItemStack stack) { return stack.is(ItemInit.AZURE_MOSS_ITEM.get()); }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        Mossback calf = EntityInit.MOSSBACK.get().create(level);
        if (calf != null) calf.setStyle(random.nextBoolean() || !(partner instanceof Mossback other) ? getStyle() : other.getStyle());
        return calf;
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return distance > 6 && super.causeFallDamage(distance - 6, multiplier, source);   // the slam lands it safely
    }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.HOGLIN_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.HOGLIN_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.HOGLIN_DEATH; }
    @Override protected float getSoundVolume() { return 0.8F; }
    @Override public float getVoicePitch() { return 0.75F + random.nextFloat() * 0.1F; }

    // ---- NeutralMob ----------------------------------------------------------------------------------------------------------

    @Override public int getRemainingPersistentAngerTime() { return remainingPersistentAngerTime; }
    @Override public void setRemainingPersistentAngerTime(int time) { remainingPersistentAngerTime = time; }
    @Nullable @Override public UUID getPersistentAngerTarget() { return persistentAngerTarget; }
    @Override public void setPersistentAngerTarget(@Nullable UUID target) { persistentAngerTarget = target; }
    @Override public void startPersistentAngerTimer() { setRemainingPersistentAngerTime(PERSISTENT_ANGER_TIME.sample(random)); }

    // ---- GeckoLib ------------------------------------------------------------------------------------------------------------

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "body", 4, state -> {
            String p = "animation.zerog_tweaks." + getStyle().id + ".";
            String clip = !state.isMoving() ? "idle" : isAggressive() ? "run" : "walk";
            return state.setAndContinue(RawAnimation.begin().thenLoop(p + clip));
        }));
        // one-shot clips per style (triggerable animations are fixed when the controller is built)
        var eyes = new AnimationController<>(this, "eyes", 0, state -> PlayState.STOP);
        var action = new AnimationController<>(this, "action", 2, state -> PlayState.STOP);
        for (Style s : Style.values()) {
            String p = "animation.zerog_tweaks." + s.id + ".";
            eyes.triggerableAnim("blink_" + s.id, RawAnimation.begin().thenPlay(p + "blink"));
            action.triggerableAnim("attack_" + s.id, RawAnimation.begin().thenPlay(p + "attack"));
            action.triggerableAnim("leap_" + s.id, RawAnimation.begin().thenPlay(p + "ability_leap_slam"));
        }
        controllers.add(eyes);
        controllers.add(action);
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }

    /** When angry and its target is 5-12 blocks off: lowers its head, leaps, and lands with a 2.5-block shockwave. */
    private final class LeapSlamGoal extends Goal {
        private int cooldown = 60;
        private int airTicks;
        private boolean leaping;

        LeapSlamGoal() { setFlags(EnumSet.of(Flag.MOVE, Flag.JUMP, Flag.LOOK)); }

        @Override
        public boolean canUse() {
            if (--cooldown > 0 || !onGround() || isBaby()) return false;
            LivingEntity t = getTarget();
            if (t == null || !t.isAlive()) return false;
            double d = distanceToSqr(t);
            return d > 25 && d < 144 && hasLineOfSight(t);
        }

        @Override
        public boolean canContinueToUse() { return leaping && airTicks < 40; }

        @Override
        public void start() {
            LivingEntity t = getTarget();
            if (t == null) return;
            leaping = true;
            airTicks = 0;
            triggerAnim("action", "leap_" + getStyle().id);
            getLookControl().setLookAt(t, 30, 30);
            Vec3 dir = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ()).normalize();
            setDeltaMovement(dir.x * 1.1, 0.55, dir.z * 1.1);
            playSound(SoundEvents.HOGLIN_ANGRY, 1.2F, 0.7F);
        }

        @Override
        public void tick() {
            if (++airTicks > 4 && onGround()) slam();
        }

        private void slam() {
            leaping = false;
            cooldown = 100 + random.nextInt(60);
            if (!(level() instanceof ServerLevel server)) return;
            for (LivingEntity e : server.getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(2.5), e -> e != Mossback.this
                    && !(e instanceof Mossback) && e.isAlive())) {
                if (e.hurt(damageSources().mobAttack(Mossback.this), SLAM_DAMAGE)) {
                    Vec3 push = e.position().subtract(position()).normalize().scale(0.9);
                    e.push(push.x, 0.35, push.z);
                }
            }
            server.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, BlockInit.AZURE_MOSS.get().defaultBlockState()),
                    getX(), getY() + 0.1, getZ(), 50, 1.4, 0.1, 1.4, 0.15);
            playSound(SoundEvents.GENERIC_EXPLODE.value(), 0.6F, 1.4F);
        }
    }
}
