package net.zerog.tweaks.entity;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.AbstractFish;
import net.minecraft.world.entity.animal.AbstractSchoolingFish;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.registry.ItemInit;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Glimmerfish (Cerulon, mob spec glimmerfish): schooling fish, 4-8 per school, glowing scales (glowmask). Water bucket ->
 * Bucket of Glimmerfish. Drops Glimmerfish and sometimes a Glimmer Scale (loot_table/entities/glimmerfish).
 */
public class Glimmerfish extends AbstractSchoolingFish implements GeoEntity, ZGGeoMob {
    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);

    public Glimmerfish(EntityType<? extends AbstractSchoolingFish> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, 3.0).add(Attributes.FOLLOW_RANGE, 16.0);
    }

    @Override
    public int getMaxSchoolSize() { return 8; }

    @Override
    public ItemStack getBucketItemStack() { return new ItemStack(ItemInit.GLIMMERFISH_BUCKET.get()); }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.TROPICAL_FISH_AMBIENT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.TROPICAL_FISH_DEATH; }
    @Override protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.TROPICAL_FISH_HURT; }
    @Override protected SoundEvent getFlopSound() { return SoundEvents.TROPICAL_FISH_FLOP; }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        ZGGeoMob.registerControllers(this, controllers, "glimmerfish", "swim");
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }
}
