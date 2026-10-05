package net.zerog.tweaks.entity;

import java.util.List;

import javax.annotation.Nullable;

import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.ai.goal.Goal;
import net.zerog.tweaks.registry.BlockInit;
import software.bernie.geckolib.animation.*;
import net.neoforged.neoforge.common.IShearable;

import net.zerog.tweaks.registry.ItemInit;

/**
 * Frost Yak (Eidolon): 1-2 wool per shearing; wool returns after grazing
 * snowpack/frozen regolith, as the approved sheep/cow-pattern specification states.
 */
public class FrostYak extends AnimatedPlanetAnimal implements IShearable {
    @Override protected String animationId() { return "frost_yak"; }
    private static final net.minecraft.network.syncher.EntityDataAccessor<Boolean> SHEARED =
            net.minecraft.network.syncher.SynchedEntityData.defineId(FrostYak.class,
                    net.minecraft.network.syncher.EntityDataSerializers.BOOLEAN);

    public FrostYak(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.MOVEMENT_SPEED, 0.2)
                .add(Attributes.FOLLOW_RANGE, 16.0);
    }

    @Nullable
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.COW_AMBIENT; }

    @Override
    protected void defineSynchedData(net.minecraft.network.syncher.SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(SHEARED, false);
    }

    @Override
    public boolean isShearable(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
        return level == level() && isAlive() && !this.isBaby() && !isSheared() && !this.isRemoved();
    }

    @Override
    public List<ItemStack> onSheared(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
        if (level.isClientSide || !isShearable(player,item,level,pos)) return List.of();
        this.entityData.set(SHEARED, true);
        level.playSound(null, this, SoundEvents.SHEEP_SHEAR, SoundSource.NEUTRAL, 1.0f, 1.0f);
        return List.of(new ItemStack(ItemInit.YAK_WOOL.get(), 1 + this.random.nextInt(2)));
    }

    public boolean isSheared() { return entityData.get(SHEARED); }
    @Override public boolean canFreeze() { return false; }
    @Override protected void registerGoals() {
        super.registerGoals();
        goalSelector.addGoal(5,new GrazeGoal(this));
    }
    /** Finds only the two approved feed blocks at the feet; never loads a chunk. */
    private BlockPos grazingBlock() {
        var feet=blockPosition();
        if(!level().hasChunkAt(feet)||!level().hasChunkAt(feet.below())) return null;
        if(level().getBlockState(feet).is(BlockInit.SNOWPACK.get())) return feet;
        var below=level().getBlockState(feet.below());
        return below.is(BlockInit.FROZEN_REGOLITH.get())||below.is(BlockInit.SNOWPACK.get())?feet.below():null;
    }
    public boolean canGrazeForWool() { return isAlive() && !isBaby() && isSheared() && grazingBlock()!=null; }
    /** The actual goal completion seam, also checked in isolated runtime tests. */
    public boolean grazeForWool() {
        if(!(level() instanceof ServerLevel server)||!canGrazeForWool()) return false;
        BlockPos at=grazingBlock();var state=server.getBlockState(at);
        if(net.neoforged.neoforge.event.EventHooks.canEntityGrief(server,this)) {
            server.levelEvent(2001,at,net.minecraft.world.level.block.Block.getId(state));
            server.destroyBlock(at,false);
        }
        // Like sheep, mobGriefing=false protects the terrain without preventing feeding.
        entityData.set(SHEARED,false);return true;
    }
    public static final class GrazeGoal extends Goal {
        private final FrostYak yak;private int remaining;
        public GrazeGoal(FrostYak yak){this.yak=yak;setFlags(java.util.EnumSet.of(Flag.MOVE,Flag.LOOK,Flag.JUMP));}
        @Override public boolean canUse(){return yak.canGrazeForWool()&&yak.getRandom().nextInt(1000)==0;}
        @Override public void start(){remaining=adjustedTickDelay(40);yak.getNavigation().stop();yak.triggerAnim("grazing","graze");}
        @Override public boolean canContinueToUse(){return remaining>0&&yak.isSheared();}
        @Override public void stop(){remaining=0;}
        @Override public void tick(){remaining=Math.max(0,remaining-1);if(remaining==adjustedTickDelay(4))yak.grazeForWool();}
    }
    @Override public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        super.registerControllers(controllers);
        String prefix="animation.zerog_tweaks.frost_yak.";
        controllers.add(new AnimationController<>(this,"coat",2,state->isSheared()
                ?state.setAndContinue(RawAnimation.begin().thenLoop(prefix+"sheared")):PlayState.STOP));
        controllers.add(new AnimationController<>(this,"grazing",2,state->PlayState.STOP)
                .triggerableAnim("graze",RawAnimation.begin().thenPlay(prefix+"graze")));
    }
    @Override public void addAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Sheared", entityData.get(SHEARED));
    }
    @Override public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        entityData.set(SHEARED, tag.getBoolean("Sheared"));
        // Legacy timer data is deliberately ignored: only grazing restores wool.
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ItemInit.FROSTFERN_ITEM.get());
    }

    @Override
    public FrostYak getBreedOffspring(net.minecraft.server.level.ServerLevel level,
            net.minecraft.world.entity.AgeableMob partner) {
        return net.zerog.tweaks.registry.EntityInit.FROST_YAK.get().create(level);
    }
}
