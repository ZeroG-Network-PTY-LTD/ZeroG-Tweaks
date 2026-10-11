package net.zerog.tweaks.entity;

import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.*;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Approved frozen-wasteland predator. Custom weather remains paused. */
public final class RimeStalker extends Monster implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    public RimeStalker(EntityType<? extends Monster> type,Level level){super(type,level);}
    public static AttributeSupplier.Builder createAttributes(){return Monster.createMonsterAttributes()
        .add(Attributes.MAX_HEALTH,24).add(Attributes.ATTACK_DAMAGE,5)
        .add(Attributes.MOVEMENT_SPEED,.33).add(Attributes.FOLLOW_RANGE,24);}
    @Override protected void registerGoals(){
        goalSelector.addGoal(0,new FloatGoal(this));
        goalSelector.addGoal(1,new BehindTargetGoal());
        goalSelector.addGoal(2,new MeleeAttackGoal(this,1.2,false));
        goalSelector.addGoal(3,new WaterAvoidingRandomStrollGoal(this,.8));
        goalSelector.addGoal(4,new LookAtPlayerGoal(this,Player.class,8));
        targetSelector.addGoal(1,new HurtByTargetGoal(this));
        targetSelector.addGoal(2,new NearestAttackableTargetGoal<>(this,Player.class,true));
    }
    /** Reposition behind an aware target, but yield when close enough to bite. */
    private final class BehindTargetGoal extends Goal {
        BehindTargetGoal(){setFlags(java.util.EnumSet.of(Flag.MOVE));}
        @Override public boolean canUse(){var target=getTarget();return target!=null&&target.isAlive()
            &&distanceToSqr(target)>9&&distanceToSqr(target)<24*24
            &&target.getLookAngle().dot(position().subtract(target.position()).normalize())>.3;}
        @Override public boolean canContinueToUse(){return canUse();}
        @Override public void tick(){var target=getTarget();if(target==null)return;
            var behind=target.position().subtract(target.getLookAngle().multiply(4,0,4));
            if(tickCount%10==0)getNavigation().moveTo(behind.x,target.getY(),behind.z,1.05);}
        @Override public void stop(){getNavigation().stop();}
    }
    @Override public boolean canFreeze(){return false;}
    @Override public boolean doHurtTarget(Entity target){boolean hit=super.doHurtTarget(target);
        if(hit){triggerAnim("action","attack");if(target instanceof LivingEntity living)
            living.setTicksFrozen(living.getTicksFrozen()+100);}return hit;}
    @Override public void aiStep(){super.aiStep();if(!level().isClientSide&&tickCount%110==0)triggerAnim("eyes","blink");}
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c){ZGGeoMob.registerControllers(this,c,"rime_stalker","walk");}
    @Override public AnimatableInstanceCache getAnimatableInstanceCache(){return cache;}
}
