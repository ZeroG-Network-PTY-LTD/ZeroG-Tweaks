package net.zerog.tweaks.entity;

import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.*;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Ironfall add: the ember Splinter Mite the Meteor Maw spits out (ability_call_adds). Drawn with the Shattered Skies
 * splinter_mite_cinder art; fast, fragile, fire-immune, and its bite sets you alight.
 */
public final class CinderMite extends Monster implements GeoEntity, ZGGeoMob {
    private static final String ART = "shatteredskies:splinter_mite_cinder", CLIP = "animation.shatteredskies.splinter_mite_cinder.";
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public CinderMite(EntityType<? extends Monster> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder createAttributes() { return Monster.createMonsterAttributes()
        .add(Attributes.MAX_HEALTH, 8).add(Attributes.ATTACK_DAMAGE, 3).add(Attributes.MOVEMENT_SPEED, .3)
        .add(Attributes.FOLLOW_RANGE, 24).add(Attributes.ARMOR, 2); }

    @Override protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.2, false));
        goalSelector.addGoal(2, new WaterAvoidingRandomStrollGoal(this, .8));
        goalSelector.addGoal(3, new LookAtPlayerGoal(this, Player.class, 8));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override public String assetId(String base) { return ART; }

    @Override public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && tickCount % 90 == 0) triggerAnim("eyes", "blink");
    }

    @Override public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) { triggerAnim("action", "attack"); target.igniteForSeconds(2); }
        return hit;
    }

    /** Called by the Meteor Maw right after spitting this mite out. */
    public void playSpawn() { triggerAnim("action", "spawn"); }

    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c) {
        RawAnimation idle = RawAnimation.begin().thenLoop(CLIP + "idle"), walk = RawAnimation.begin().thenLoop(CLIP + "walk");
        c.add(new AnimationController<>(this, "body", 4, s -> s.setAndContinue(s.isMoving() ? walk : idle)));
        c.add(new AnimationController<>(this, "eyes", 0, s -> PlayState.STOP)
            .triggerableAnim("blink", RawAnimation.begin().thenPlay(CLIP + "blink")));
        c.add(new AnimationController<>(this, "action", 2, s -> PlayState.STOP)
            .triggerableAnim("attack", RawAnimation.begin().thenPlay(CLIP + "attack"))
            .triggerableAnim("spawn", RawAnimation.begin().thenPlay(CLIP + "spawn")));
    }

    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
}
