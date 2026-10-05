package net.zerog.tweaks.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Shared vanilla-style animal AI, not a replacement for each species' art or behaviour. */
public abstract class AnimatedPlanetAnimal extends Animal implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);
    protected AnimatedPlanetAnimal(EntityType<? extends Animal> type, Level level) { super(type, level); }
    protected abstract String animationId();
    protected String movementClip() { return "walk"; }
    @Override protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new PanicGoal(this, 1.5));
        goalSelector.addGoal(2, new BreedGoal(this, 1.0));
        goalSelector.addGoal(3, new TemptGoal(this, 1.0, this::isFood, false));
        goalSelector.addGoal(4, new FollowParentGoal(this, 1.1));
        goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 1.0));
        goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 6));
        goalSelector.addGoal(7, new RandomLookAroundGoal(this));
    }
    @Override public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && tickCount % 110 == 0) triggerAnim("eyes", "blink");
    }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        ZGGeoMob.registerControllers(this, controllers, animationId(), movementClip());
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }
}
