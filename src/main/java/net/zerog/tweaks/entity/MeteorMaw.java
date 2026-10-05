package net.zerog.tweaks.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.world.BossEvent;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.*;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Ironfall encounter: approved authored size, server-side leap/slam and heat pulse. */
public final class MeteorMaw extends Monster implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    private final ServerBossEvent bar=new ServerBossEvent(getDisplayName(),BossEvent.BossBarColor.PURPLE,BossEvent.BossBarOverlay.PROGRESS);
    private boolean slamPending;
    public MeteorMaw(EntityType<? extends Monster> type,Level level) { super(type,level); }
    public static AttributeSupplier.Builder createAttributes() { return Monster.createMonsterAttributes()
        .add(Attributes.MAX_HEALTH,200).add(Attributes.ATTACK_DAMAGE,8).add(Attributes.MOVEMENT_SPEED,.22)
        .add(Attributes.FOLLOW_RANGE,32).add(Attributes.KNOCKBACK_RESISTANCE,1).add(Attributes.ARMOR,8); }
    @Override protected void registerGoals() {
        goalSelector.addGoal(0,new FloatGoal(this));
        goalSelector.addGoal(1,new MeleeAttackGoal(this,1.1,true));
        goalSelector.addGoal(2,new WaterAvoidingRandomStrollGoal(this,.7));
        goalSelector.addGoal(3,new LookAtPlayerGoal(this,Player.class,16));
        targetSelector.addGoal(1,new HurtByTargetGoal(this));
        targetSelector.addGoal(2,new NearestAttackableTargetGoal<>(this,Player.class,true));
    }
    @Override public boolean removeWhenFarAway(double distance) { return false; }
    @Override public void startSeenByPlayer(ServerPlayer p) { super.startSeenByPlayer(p);bar.addPlayer(p); }
    @Override public void stopSeenByPlayer(ServerPlayer p) { super.stopSeenByPlayer(p);bar.removePlayer(p); }
    @Override public String assetId(String base) { return "meteor_maw_ironfall"; }
    @Override public void aiStep() {
        super.aiStep();
        if(!(level() instanceof ServerLevel server))return;
        bar.setProgress(getHealth()/getMaxHealth());
        if(tickCount%110==0)triggerAnim("eyes","blink");
        if(getTarget()==null)return;
        if(tickCount%200==0 && onGround() && distanceToSqr(getTarget())<144) {
            var delta=getTarget().position().subtract(position()).normalize();
            setDeltaMovement(delta.x*.7,.7,delta.z*.7);slamPending=true;
            triggerAnim("ability","leap");
        } else if(slamPending && onGround()) {
            slamPending=false;
            server.sendParticles(net.minecraft.core.particles.ParticleTypes.EXPLOSION,getX(),getY()+.2,getZ(),12,2,.3,2,0);
            for(Player p:server.getEntitiesOfClass(Player.class,getBoundingBox().inflate(4)))
                if(!p.isCreative()&&!p.isSpectator())p.hurt(damageSources().mobAttack(this),6);
        }
        if(tickCount%400==0) {
            triggerAnim("ability","pulse");
            server.sendParticles(net.minecraft.core.particles.ParticleTypes.FLAME,getX(),getY()+1,getZ(),40,3,.5,3,.03);
            for(Player p:server.getEntitiesOfClass(Player.class,getBoundingBox().inflate(5)))
                if(!p.isCreative()&&!p.isSpectator() && hasLineOfSight(p))p.hurt(damageSources().mobAttack(this),4);
        }
    }
    @Override public boolean doHurtTarget(Entity target) { boolean hit=super.doHurtTarget(target);if(hit)triggerAnim("action","attack");return hit; }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c) {
        ZGGeoMob.registerControllers(this,c,"meteor_maw_ironfall","walk");
        String p="animation.zerog_tweaks.meteor_maw_ironfall.";
        c.add(new AnimationController<>(this,"ability",2,s->PlayState.STOP)
            .triggerableAnim("leap",RawAnimation.begin().thenPlay(p+"ability_leap_slam"))
            .triggerableAnim("pulse",RawAnimation.begin().thenPlay(p+"ability_effect_pulse")));
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
}
