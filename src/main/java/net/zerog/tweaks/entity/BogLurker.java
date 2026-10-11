package net.zerog.tweaks.entity;

import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.*;
import net.minecraft.world.entity.ai.navigation.*;
import net.minecraft.world.entity.monster.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.fluids.FluidType;
import net.zerog.tweaks.registry.*;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

public final class BogLurker extends Monster implements RangedAttackMob,GeoEntity,ZGGeoMob {
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    public BogLurker(EntityType<? extends Monster> type,Level level){super(type,level);}
    public static AttributeSupplier.Builder createAttributes(){return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH,28)
        .add(Attributes.ATTACK_DAMAGE,5).add(Attributes.MOVEMENT_SPEED,.2).add(Attributes.FOLLOW_RANGE,16);}
    @Override protected PathNavigation createNavigation(Level level){return new AmphibiousPathNavigation(this,level);}
    @Override protected void registerGoals(){
        goalSelector.addGoal(0,new FloatGoal(this){@Override public boolean canUse(){return !inAcid()&&super.canUse();}});
        goalSelector.addGoal(1,new RangedAttackGoal(this,1,40,10){
            @Override public boolean canUse(){return getTarget()!=null&&distanceToSqr(getTarget())>4&&super.canUse();}
            @Override public boolean canContinueToUse(){return canUse();}
        });
        goalSelector.addGoal(2,new MeleeAttackGoal(this,1,true));
        goalSelector.addGoal(4,new RandomStrollGoal(this,.7));
        targetSelector.addGoal(1,new HurtByTargetGoal(this));
        targetSelector.addGoal(2,new NearestAttackableTargetGoal<>(this,Player.class,true));
    }
    private boolean inAcid(){return isInFluidType(ZGDimensionFluids.ACID.type.get());}
    @Override public boolean canSwimInFluidType(FluidType type){return type==ZGDimensionFluids.ACID.type.get()||super.canSwimInFluidType(type);}
    @Override public boolean canDrownInFluidType(FluidType type){return false;}
    @Override public boolean canBeAffected(MobEffectInstance effect){return !effect.is(MobEffects.POISON)&&super.canBeAffected(effect);}
    @Override public boolean isInvulnerableTo(DamageSource source){return source.is(net.minecraft.resources.ResourceKey.create(
        net.minecraft.core.registries.Registries.DAMAGE_TYPE,net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:acid")))||super.isInvulnerableTo(source);}
    @Override public void travel(Vec3 input){if(inAcid()&&isControlledByLocalInstance()){
        moveRelative(getSpeed()*2.5F,input);move(MoverType.SELF,getDeltaMovement());setDeltaMovement(getDeltaMovement().scale(.8));
        calculateEntityAnimation(false);
    }else super.travel(input);}
    @Override public void aiStep(){super.aiStep();if(!level().isClientSide){
        if(tickCount%110==0)triggerAnim("eyes","blink");
        if(inAcid()&&getTarget()==null){getNavigation().stop();var state=level().getFluidState(blockPosition());
            double surface=blockPosition().getY()+state.getHeight(level(),blockPosition())+.05;
            setDeltaMovement(0,Math.clamp((surface-getEyeY())*.15,-.08,.08),0);}
    }}
    @Override public void performRangedAttack(LivingEntity target,float strength){
        if(level().isClientSide||distanceToSqr(target)>100||!hasLineOfSight(target))return;
        var spit=EntityInit.BOG_ACID_SPIT.get().create(level());spit.setOwner(this);spit.setPos(getX(),getEyeY(),getZ());
        var delta=target.getEyePosition().subtract(spit.position());spit.shoot(delta.x,delta.y+delta.horizontalDistance()*.1,delta.z,1.2F,2F);
        level().addFreshEntity(spit);triggerAnim("action","attack");
    }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c){ZGGeoMob.registerControllers(this,c,"bog_lurker","walk");}
    @Override public AnimatableInstanceCache getAnimatableInstanceCache(){return cache;}
}
