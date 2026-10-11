package net.zerog.tweaks.entity;

import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.TimeUtil;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.navigation.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Neutral floating scavenger. Barren habitats and all drops come from approved data. */
public final class CraterDrifter extends PathfinderMob implements NeutralMob, GeoEntity, ZGGeoMob {
    private static final UniformInt ANGER=TimeUtil.rangeOfSeconds(20,39);
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    private int anger,fragmentTicks=6000;
    @Nullable private UUID angryAt;
    public CraterDrifter(EntityType<? extends PathfinderMob> type,Level level){super(type,level);
        moveControl=new FlyingMoveControl(this,20,true);setNoGravity(true);}
    public static AttributeSupplier.Builder createAttributes(){return Mob.createMobAttributes()
        .add(Attributes.MAX_HEALTH,20).add(Attributes.ATTACK_DAMAGE,4)
        .add(Attributes.MOVEMENT_SPEED,.2).add(Attributes.FLYING_SPEED,.3).add(Attributes.FOLLOW_RANGE,16);}
    @Override protected PathNavigation createNavigation(Level level){var nav=new FlyingPathNavigation(this,level);nav.setCanFloat(true);return nav;}
    @Override protected void registerGoals(){
        goalSelector.addGoal(0,new FloatGoal(this));
        goalSelector.addGoal(1,new MeleeAttackGoal(this,1.0,true));
        goalSelector.addGoal(2,new DriftGoal());
        targetSelector.addGoal(1,new HurtByTargetGoal(this).setAlertOthers());
    }
    private final class DriftGoal extends Goal {
        DriftGoal(){setFlags(java.util.EnumSet.of(Flag.MOVE));}
        @Override public boolean canUse(){return getTarget()==null&&(!getMoveControl().hasWanted()||random.nextInt(40)==0);}
        @Override public void start(){double x=getX()+random.nextInt(17)-8,z=getZ()+random.nextInt(17)-8;
            BlockPos probe=BlockPos.containing(x,getY(),z);if(!level().hasChunkAt(probe))return;
            int floor=level().getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,probe.getX(),probe.getZ());
            double y=Math.min(level().getMaxBuildHeight()-2,floor+4+random.nextInt(7));
            getMoveControl().setWantedPosition(x,y,z,.8);}
    }
    @Override public void travel(Vec3 input){if(isControlledByLocalInstance()){
        moveRelative(getSpeed(),input);move(MoverType.SELF,getDeltaMovement());setDeltaMovement(getDeltaMovement().scale(.91));
    }else super.travel(input);calculateEntityAnimation(false);}
    @Override public void aiStep(){super.aiStep();if(!(level() instanceof ServerLevel server))return;
        updatePersistentAnger(server,true);
        if(tickCount%110==0)triggerAnim("eyes","blink");
        if(--fragmentTicks<=0){spawnAtLocation(net.zerog.tweaks.registry.ItemInit.METEORITE_FRAGMENT_ITEM.get());fragmentTicks=6000;}
    }
    @Override public boolean doHurtTarget(Entity target){boolean hit=super.doHurtTarget(target);if(hit)triggerAnim("action","attack");return hit;}
    @Override public int getRemainingPersistentAngerTime(){return anger;}
    @Override public void setRemainingPersistentAngerTime(int ticks){anger=Math.max(0,ticks);}
    @Override public UUID getPersistentAngerTarget(){return angryAt;}
    @Override public void setPersistentAngerTarget(@Nullable UUID target){angryAt=target;}
    @Override public void startPersistentAngerTimer(){anger=ANGER.sample(random);}
    @Override public void addAdditionalSaveData(CompoundTag tag){super.addAdditionalSaveData(tag);addPersistentAngerSaveData(tag);tag.putInt("FragmentTicks",fragmentTicks);}
    @Override public void readAdditionalSaveData(CompoundTag tag){super.readAdditionalSaveData(tag);readPersistentAngerSaveData(level(),tag);fragmentTicks=tag.contains("FragmentTicks")?Math.clamp(tag.getInt("FragmentTicks"),1,6000):6000;setNoGravity(true);}
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c){ZGGeoMob.registerControllers(this,c,"crater_drifter","float");}
    @Override public AnimatableInstanceCache getAnimatableInstanceCache(){return cache;}
}
