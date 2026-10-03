package net.zerog.tweaks.entity;

import javax.annotation.Nullable;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowParentGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.TemptGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Azure Fowl (Cerulon, mob spec azure_fowl): chicken-like. Glides slowly when it falls (no fall damage), lays a Blue Egg
 * every 5-10 minutes, breeds with Skyberries. Drops Raw Fowl and Azure Feathers (loot_table/entities/azure_fowl).
 */
public class AzureFowl extends Animal implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);
    private int eggTime;

    public AzureFowl(EntityType<? extends Animal> type, Level level) {
        super(type, level);
        this.eggTime = nextEggTime();
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes().add(Attributes.MAX_HEALTH, 4.0).add(Attributes.MOVEMENT_SPEED, 0.25)
                .add(Attributes.FOLLOW_RANGE, 16.0);
    }

    private int nextEggTime() {
        return 6000 + this.random.nextInt(6000);   // 5-10 minutes
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new PanicGoal(this, 1.4));
        goalSelector.addGoal(2, new BreedGoal(this, 1.0));
        goalSelector.addGoal(3, new TemptGoal(this, 1.0, this::isFood, false));
        goalSelector.addGoal(4, new FollowParentGoal(this, 1.1));
        goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 1.0));
        goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 6.0F));
    }

    /** True while gliding down (the glide clip plays). */
    public boolean isGliding() {
        return !onGround() && getDeltaMovement().y < 0 && !isInWater();
    }

    @Override
    public void aiStep() {
        super.aiStep();
        Vec3 v = getDeltaMovement();
        if (!onGround() && v.y < 0) setDeltaMovement(v.multiply(1, 0.6, 1));   // the glide
        if (!level().isClientSide && isAlive() && !isBaby() && --eggTime <= 0) {
            playSound(SoundEvents.CHICKEN_EGG, 1.0F, (random.nextFloat() - random.nextFloat()) * 0.2F + 1.0F);
            spawnAtLocation(ItemInit.BLUE_EGG.get());
            gameEvent(net.minecraft.world.level.gameevent.GameEvent.ENTITY_PLACE);
            eggTime = nextEggTime();
        }
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) { return false; }

    @Override
    public boolean isFood(ItemStack stack) { return stack.is(ItemInit.SKYBERRIES.get()); }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        return EntityInit.AZURE_FOWL.get().create(level);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("EggLayTime", eggTime);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (tag.contains("EggLayTime")) eggTime = tag.getInt("EggLayTime");
    }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.CHICKEN_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.CHICKEN_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.CHICKEN_DEATH; }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        String p = "animation.zerog_tweaks.azure_fowl.";
        var idle = software.bernie.geckolib.animation.RawAnimation.begin().thenLoop(p + "idle");
        var walk = software.bernie.geckolib.animation.RawAnimation.begin().thenLoop(p + "walk");
        var glide = software.bernie.geckolib.animation.RawAnimation.begin().thenLoop(p + "glide");
        controllers.add(new software.bernie.geckolib.animation.AnimationController<>(this, "body", 4,
                s -> s.setAndContinue(isGliding() ? glide : s.isMoving() ? walk : idle)));
        controllers.add(new software.bernie.geckolib.animation.AnimationController<>(this, "eyes", 0,
                s -> software.bernie.geckolib.animation.PlayState.STOP)
                .triggerableAnim("blink", software.bernie.geckolib.animation.RawAnimation.begin().thenPlay(p + "blink")));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }
}
