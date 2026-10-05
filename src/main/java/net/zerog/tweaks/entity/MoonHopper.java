package net.zerog.tweaks.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.damagesource.DamageSource;
import net.zerog.tweaks.registry.*;

public final class MoonHopper extends AnimatedPlanetAnimal {
    private int hopCooldown;
    public MoonHopper(EntityType<? extends Animal> type, Level level) { super(type, level); }
    public static AttributeSupplier.Builder createAttributes() { return Mob.createMobAttributes()
        .add(Attributes.MAX_HEALTH, 6).add(Attributes.MOVEMENT_SPEED, .25).add(Attributes.FOLLOW_RANGE, 16); }
    @Override protected String animationId() { return "moon_hopper"; }
    @Override protected String movementClip() { return "hop"; }
    @Override public boolean isFood(ItemStack stack) { return stack.is(ItemInit.LUNAR_LICHEN_ITEM.get()); }
    @Override public MoonHopper getBreedOffspring(net.minecraft.server.level.ServerLevel level, net.minecraft.world.entity.AgeableMob partner) {
        return EntityInit.MOON_HOPPER.get().create(level);
    }
    @Override public void aiStep() {
        super.aiStep();
        if(!level().isClientSide) {
            var gravity=getAttribute(Attributes.GRAVITY);
            if(gravity!=null)gravity.setBaseValue(level().dimension().location().getPath().equals("moon")?.04:.08);
        }
        if (!level().isClientSide && --hopCooldown <= 0 && onGround() && !getNavigation().isDone()) {
            jumpFromGround();
            var v = getDeltaMovement();
            setDeltaMovement(v.x, level().dimension().location().getPath().equals("moon") ? .55 : .35, v.z);
            hopCooldown = 16;
        }
    }
    @Override public boolean causeFallDamage(float distance, float multiplier, DamageSource source) { return false; }
}
