package net.zerog.tweaks.entity;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.*;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Blaze;
import net.minecraft.world.level.Level;

/** Vanilla Blaze AI/rig; persistent, synchronized palette variation only. */
public final class PlanetBlaze extends Blaze {
    private static final EntityDataAccessor<Integer> PALETTE=SynchedEntityData.defineId(PlanetBlaze.class,EntityDataSerializers.INT);
    public final String style;
    public PlanetBlaze(EntityType<? extends Blaze> type,Level level,String style){super(type,level);this.style=style;if(!level.isClientSide)entityData.set(PALETTE,random.nextInt(3));}
    @Override protected void defineSynchedData(SynchedEntityData.Builder builder){super.defineSynchedData(builder);builder.define(PALETTE,0);}
    public int palette(){return entityData.get(PALETTE);}
    @Override public void addAdditionalSaveData(CompoundTag tag){super.addAdditionalSaveData(tag);tag.putInt("ZeroGPalette",palette());}
    @Override public void readAdditionalSaveData(CompoundTag tag){super.readAdditionalSaveData(tag);entityData.set(PALETTE,Math.floorMod(tag.getInt("ZeroGPalette"),3));}
}
