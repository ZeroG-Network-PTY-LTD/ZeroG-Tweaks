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
    /** Call Adds (design: ability_call_adds spits out Cinder Mites) at 75/50/25% health and every 30 s in a fight. */
    private static final int ADDS_PER_CALL=2, MAX_ADDS=4, ADDS_COOLDOWN=600;
    private float addsThreshold=.75F;
    private int addsCooldown=ADDS_COOLDOWN/2;
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
        boolean threshold=addsThreshold>0 && getHealth()/getMaxHealth()<=addsThreshold;
        if(threshold || --addsCooldown<=0) {
            if(threshold)addsThreshold-=.25F;
            addsCooldown=ADDS_COOLDOWN; callAdds(server);
        }
        if(tickCount%400==0) {
            triggerAnim("ability","pulse");
            server.sendParticles(net.minecraft.core.particles.ParticleTypes.FLAME,getX(),getY()+1,getZ(),40,3,.5,3,.03);
            for(Player p:server.getEntitiesOfClass(Player.class,getBoundingBox().inflate(5)))
                if(!p.isCreative()&&!p.isSpectator() && hasLineOfSight(p))p.hurt(damageSources().mobAttack(this),4);
        }
    }
    /** Spit Cinder Mites out of the maw at the current target, never more than MAX_ADDS alive around the Maw. */
    private void callAdds(ServerLevel server) {
        int room=MAX_ADDS-server.getEntitiesOfClass(CinderMite.class,getBoundingBox().inflate(24)).size();
        if(room<=0)return;
        triggerAnim("ability","adds");
        var look=getLookAngle();double mx=getX()+look.x*1.6,my=getY()+1.4,mz=getZ()+look.z*1.6;
        server.sendParticles(net.minecraft.core.particles.ParticleTypes.LAVA,mx,my,mz,8,.4,.3,.4,0);
        for(int i=0;i<Math.min(ADDS_PER_CALL,room);i++) {
            CinderMite mite=net.zerog.tweaks.registry.EntityInit.CINDER_MITE.get().create(server);
            if(mite==null)return;
            mite.moveTo(mx,my,mz,getYRot()+(i==0?-25:25),0);
            mite.setDeltaMovement(look.x*.45+(i==0?-.15:.15),.35,look.z*.45);
            mite.setTarget(getTarget());
            server.addFreshEntity(mite);mite.playSpawn();
        }
    }
    @Override public void addAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.addAdditionalSaveData(tag);tag.putFloat("AddsThreshold",addsThreshold);tag.putInt("AddsCooldown",addsCooldown);
    }
    @Override public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if(tag.contains("AddsThreshold"))addsThreshold=Math.clamp(tag.getFloat("AddsThreshold"),0F,.75F);
        if(tag.contains("AddsCooldown"))addsCooldown=Math.clamp(tag.getInt("AddsCooldown"),0,ADDS_COOLDOWN);
    }
    @Override public boolean doHurtTarget(Entity target) { boolean hit=super.doHurtTarget(target);if(hit)triggerAnim("action","attack");return hit; }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c) {
        ZGGeoMob.registerControllers(this,c,"meteor_maw_ironfall","walk");
        String p="animation.zerog_tweaks.meteor_maw_ironfall.";
        c.add(new AnimationController<>(this,"ability",2,s->PlayState.STOP)
            .triggerableAnim("leap",RawAnimation.begin().thenPlay(p+"ability_leap_slam"))
            .triggerableAnim("pulse",RawAnimation.begin().thenPlay(p+"ability_effect_pulse"))
            .triggerableAnim("adds",RawAnimation.begin().thenPlay(p+"ability_call_adds")));
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
}
