package net.zerog.tweaks.entity;

import java.util.List;

import javax.annotation.Nullable;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.common.IShearable;

import net.zerog.tweaks.registry.ItemInit;

/**
 * Crystal Stag (Cerulon): shearable crystal antlers, 1-2 Starlite,
 * regrow in 5 minutes. Breeds with Starbloom. Loot data already ships.
 */
public class CrystalStag extends Animal implements IShearable {
    private static final net.minecraft.network.syncher.EntityDataAccessor<Boolean> SHEARED =
            net.minecraft.network.syncher.SynchedEntityData.defineId(CrystalStag.class,
                    net.minecraft.network.syncher.EntityDataSerializers.BOOLEAN);
    private int regrowTicks;

    public CrystalStag(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0)
                .add(Attributes.MOVEMENT_SPEED, 0.25);
    }

    @Nullable
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.AMETHYST_BLOCK_CHIME; }

    @Override
    protected void defineSynchedData(net.minecraft.network.syncher.SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(SHEARED, false);
    }

    @Override
    public boolean isShearable(@Nullable Player player, ItemStack item, net.minecraft.world.level.Level level, BlockPos pos) {
        return !this.isBaby() && !this.entityData.get(SHEARED) && !this.isRemoved();
    }

    @Override
    public List<ItemStack> onSheared(@Nullable Player player, ItemStack item, net.minecraft.world.level.Level level, BlockPos pos) {
        this.entityData.set(SHEARED, true);
        this.regrowTicks = 6000;                       // antlers regrow in 5 minutes
        level.playSound(null, this, SoundEvents.AMETHYST_CLUSTER_BREAK, SoundSource.NEUTRAL, 1.0f, 1.0f);
        return List.of(new ItemStack(ItemInit.STARLITE.get(), 1 + this.random.nextInt(2)));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!this.level().isClientSide && this.entityData.get(SHEARED) && --this.regrowTicks <= 0) {
            this.entityData.set(SHEARED, false);
            this.regrowTicks = 0;
        }
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ItemInit.STARBLOOM_ITEM.get());
    }

    @Override
    public CrystalStag getBreedOffspring(net.minecraft.server.level.ServerLevel level,
            net.minecraft.world.entity.AgeableMob partner) {
        return net.zerog.tweaks.registry.EntityInit.CRYSTAL_STAG.get().create(level);
    }
}