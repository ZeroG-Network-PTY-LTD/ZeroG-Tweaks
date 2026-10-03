package net.zerog.tweaks.entity;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.*;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.npc.*;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.registry.ZGPlanetVillagers;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.*;
import software.bernie.geckolib.util.GeckoLibUtil;

/** Native villager brain and trading, with the authored planetary appearance. */
public final class PlanetVillager extends Villager implements GeoEntity {
    private static final EntityDataAccessor<Integer> STYLE=SynchedEntityData.defineId(PlanetVillager.class,EntityDataSerializers.INT);
    private final AnimatableInstanceCache cache=GeckoLibUtil.createInstanceCache(this);
    public PlanetVillager(EntityType<? extends Villager> type,Level level){super(type,level);}
    public String species(){return BuiltInRegistries.ENTITY_TYPE.getKey(getType()).getPath();}
    public int style(){return entityData.get(STYLE);}
    public void setStyle(int style){entityData.set(STYLE,Math.floorMod(style,3));}
    @Override public SpawnGroupData finalizeSpawn(net.minecraft.world.level.ServerLevelAccessor world,
            net.minecraft.world.DifficultyInstance difficulty,MobSpawnType reason,SpawnGroupData group){
        var result=super.finalizeSpawn(world,difficulty,reason,group);
        setStyle(getRandom().nextInt(3));return result;
    }
    @Override protected void defineSynchedData(SynchedEntityData.Builder builder){super.defineSynchedData(builder);builder.define(STYLE,0);}
    @Override public void addAdditionalSaveData(CompoundTag tag){super.addAdditionalSaveData(tag);tag.putInt("PlanetStyle",style());}
    @Override public void readAdditionalSaveData(CompoundTag tag){super.readAdditionalSaveData(tag);setStyle(tag.getInt("PlanetStyle"));}
    @Override public Villager getBreedOffspring(ServerLevel level,AgeableMob parent){
        var child=ZGPlanetVillagers.TYPES.get(species()).get().create(level);
        if(child!=null){child.setStyle(style());child.setVillagerData(getVillagerData().setProfession(VillagerProfession.NONE).setLevel(1));}
        return child;
    }
    @Override public boolean canFreeze(){return !species().equals("hollow_kin")&&super.canFreeze();}
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar controllers){
        String prefix="animation."+species()+".";
        controllers.add(new AnimationController<>(this,"native_motion",4,state->state.setAndContinue(
                RawAnimation.begin().thenLoop(prefix+(getUnhappyCounter()>0?"no":state.isMoving()?"walk":"idle")))));
        if(species().equals("sunwarden")) controllers.add(new AnimationController<>(this,"corona",0,
                state->state.setAndContinue(RawAnimation.begin().thenLoop(prefix+"halo_spin"))));
    }
    @Override public AnimatableInstanceCache getAnimatableInstanceCache(){return cache;}
}
