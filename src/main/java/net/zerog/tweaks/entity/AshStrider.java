package net.zerog.tweaks.entity;

import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.monster.Strider;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.*;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Approved lava mount; inherits vanilla saddle, steering and lava buoyancy, not Nether jockey spawning. */
public final class AshStrider extends Strider implements NeutralMob, GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    private int anger;
    @Nullable private UUID angryAt;
    public AshStrider(EntityType<? extends Strider> type,Level level){super(type,level);}
    public static AttributeSupplier.Builder createAttributes(){return Strider.createAttributes()
        .add(Attributes.MAX_HEALTH,30).add(Attributes.ATTACK_DAMAGE,6).add(Attributes.MOVEMENT_SPEED,.25);}
    @Override protected void registerGoals(){super.registerGoals();
        goalSelector.removeAllGoals(g->g instanceof PanicGoal||g instanceof TemptGoal);
        goalSelector.addGoal(1,new MeleeAttackGoal(this,1,true));
        goalSelector.addGoal(3,new TemptGoal(this,1.4,this::isFood,false));
        targetSelector.addGoal(1,new HurtByTargetGoal(this).setAlertOthers());
    }
    @Override public boolean isFood(ItemStack stack){return stack.is(net.zerog.tweaks.registry.ItemInit.CINDER_CAP_ITEM.get());}
    @Override public AshStrider getBreedOffspring(ServerLevel level,AgeableMob partner){return net.zerog.tweaks.registry.EntityInit.ASH_STRIDER.get().create(level);}
    /** No vanilla piglin/baby-Strider jockeys on alien planets; babies come from breeding. */
    @Override public SpawnGroupData finalizeSpawn(ServerLevelAccessor level,DifficultyInstance difficulty,MobSpawnType reason,@Nullable SpawnGroupData data){return data;}
    @Override public void aiStep(){super.aiStep();if(level() instanceof ServerLevel server){updatePersistentAnger(server,true);if(tickCount%110==0)triggerAnim("eyes","blink");}}
    @Override public boolean doHurtTarget(Entity target){boolean hit=super.doHurtTarget(target);if(hit)triggerAnim("action","attack");return hit;}
    @Override public int getRemainingPersistentAngerTime(){return anger;}
    @Override public void setRemainingPersistentAngerTime(int ticks){anger=Math.max(0,ticks);}
    @Override public UUID getPersistentAngerTarget(){return angryAt;}
    @Override public void setPersistentAngerTarget(@Nullable UUID target){angryAt=target;}
    @Override public void startPersistentAngerTimer(){anger=400+random.nextInt(400);}
    @Override public void addAdditionalSaveData(CompoundTag tag){super.addAdditionalSaveData(tag);addPersistentAngerSaveData(tag);}
    @Override public void readAdditionalSaveData(CompoundTag tag){super.readAdditionalSaveData(tag);readPersistentAngerSaveData(level(),tag);}
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar c){ZGGeoMob.registerControllers(this,c,"ash_strider","walk");}
    @Override public AnimatableInstanceCache getAnimatableInstanceCache(){return cache;}
}
