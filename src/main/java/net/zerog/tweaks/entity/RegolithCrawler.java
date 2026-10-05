package net.zerog.tweaks.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.network.syncher.*;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.*;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Surface ambusher. State belongs to the entity's server thread, never worldgen. */
public final class RegolithCrawler extends Monster implements GeoEntity, ZGGeoMob {
    private static final EntityDataAccessor<Boolean> BURIED = SynchedEntityData.defineId(RegolithCrawler.class, EntityDataSerializers.BOOLEAN);
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private int idleTicks, emergenceTicks, lungeCooldown;
    public RegolithCrawler(EntityType<? extends Monster> type, Level level) { super(type, level); }
    public static AttributeSupplier.Builder createAttributes() { return Monster.createMonsterAttributes()
        .add(Attributes.MAX_HEALTH,14).add(Attributes.ATTACK_DAMAGE,3).add(Attributes.MOVEMENT_SPEED,.2).add(Attributes.FOLLOW_RANGE,16); }
    @Override protected void defineSynchedData(SynchedEntityData.Builder builder) { super.defineSynchedData(builder); builder.define(BURIED,false); }
    @Override protected void registerGoals() {
        goalSelector.addGoal(0,new FloatGoal(this));
        goalSelector.addGoal(1,new MeleeAttackGoal(this,1.2,true) {
            @Override public boolean canUse() { return !entityData.get(BURIED) && emergenceTicks==0 && super.canUse(); }
            @Override public boolean canContinueToUse() { return !entityData.get(BURIED) && emergenceTicks==0 && super.canContinueToUse(); }
        });
        goalSelector.addGoal(3,new WaterAvoidingRandomStrollGoal(this,.7));
        goalSelector.addGoal(4,new LookAtPlayerGoal(this,Player.class,8));
        targetSelector.addGoal(1,new HurtByTargetGoal(this));
        targetSelector.addGoal(2,new NearestAttackableTargetGoal<>(this,Player.class,true));
    }
    @Override public void aiStep() {
        super.aiStep();
        if (level().isClientSide) return;
        if (tickCount%110==0) triggerAnim("eyes","blink");
        if (lungeCooldown>0) lungeCooldown--;
        if (emergenceTicks>0) { emergenceTicks--; getNavigation().stop(); }
        if (entityData.get(BURIED)) {
            getNavigation().stop(); setDeltaMovement(0,getDeltaMovement().y,0);
            var player=level().getNearestPlayer(this,3);
            if (player!=null && !player.isShiftKeyDown() && !player.isCreative() && !player.isSpectator()) {
                entityData.set(BURIED,false); emergenceTicks=20; setTarget(player); idleTicks=0;
            }
        } else if (getTarget()==null && ++idleTicks>=200 && level().getBlockState(blockPosition().below()).is(net.zerog.tweaks.registry.BlockInit.REGOLITH.get())) {
            entityData.set(BURIED,true); idleTicks=0;
        } else if (getTarget()!=null && emergenceTicks==0 && lungeCooldown==0 && distanceToSqr(getTarget())<=9 && onGround()) {
            var delta=getTarget().position().subtract(position()).normalize();
            setDeltaMovement(delta.x*.45,.18,delta.z*.45); lungeCooldown=60;
        }
    }
    @Override public boolean isPushable() { return !entityData.get(BURIED) && super.isPushable(); }
    @Override public boolean hurt(DamageSource source,float amount) {
        boolean buried=entityData.get(BURIED);
        boolean hit=super.hurt(source,buried?amount*.5F:amount);
        if(hit && !level().isClientSide) { entityData.set(BURIED,false); emergenceTicks=20; idleTicks=0; }
        return hit;
    }
    @Override public boolean doHurtTarget(Entity target) {
        boolean hit=super.doHurtTarget(target);
        if(hit) { triggerAnim("action","attack"); if(target instanceof net.minecraft.world.entity.LivingEntity living)
            living.addEffect(new net.minecraft.world.effect.MobEffectInstance(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN,60,0)); }
        return hit;
    }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c) {
        String p="animation.zerog_tweaks.regolith_crawler.";
        c.add(new AnimationController<>(this,"body",4,s->s.setAndContinue(RawAnimation.begin().thenLoop(p+(entityData.get(BURIED)?"burrow":s.isMoving()?"walk":"idle")))));
        c.add(new AnimationController<>(this,"eyes",0,s->PlayState.STOP).triggerableAnim("blink",RawAnimation.begin().thenPlay(p+"blink")));
        c.add(new AnimationController<>(this,"action",2,s->PlayState.STOP).triggerableAnim("attack",RawAnimation.begin().thenPlay(p+"attack")));
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
    @Override public void addAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Buried",entityData.get(BURIED));
        tag.putInt("AmbushIdleTicks",idleTicks);
        tag.putInt("EmergenceTicks",emergenceTicks);
        tag.putInt("LungeCooldown",lungeCooldown);
    }
    @Override public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        entityData.set(BURIED,tag.getBoolean("Buried"));
        idleTicks=Math.clamp(tag.getInt("AmbushIdleTicks"),0,200);
        emergenceTicks=Math.clamp(tag.getInt("EmergenceTicks"),0,20);
        lungeCooldown=Math.clamp(tag.getInt("LungeCooldown"),0,60);
    }
}
