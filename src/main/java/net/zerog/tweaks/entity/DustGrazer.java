package net.zerog.tweaks.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.damagesource.DamageSource;
import net.zerog.tweaks.registry.*;

/** Mars herds flee together, rather than becoming permanently hostile. */
public final class DustGrazer extends AnimatedPlanetAnimal {
    public DustGrazer(EntityType<? extends Animal> type, Level level) { super(type, level); }
    public static AttributeSupplier.Builder createAttributes() { return Mob.createMobAttributes()
        .add(Attributes.MAX_HEALTH, 24).add(Attributes.MOVEMENT_SPEED, .25).add(Attributes.FOLLOW_RANGE, 16); }
    @Override protected String animationId() { return "dust_grazer"; }
    @Override public boolean isFood(ItemStack stack) { return stack.is(ItemInit.RUST_TUBER.get()); }
    @Override public DustGrazer getBreedOffspring(net.minecraft.server.level.ServerLevel level, net.minecraft.world.entity.AgeableMob partner) {
        return EntityInit.DUST_GRAZER.get().create(level);
    }
    @Override public boolean hurt(DamageSource source, float amount) {
        boolean hit = super.hurt(source, amount);
        if (hit && !level().isClientSide && source.getEntity() != null) {
            var away = position().subtract(source.getEntity().position()).normalize().scale(10);
            for (DustGrazer herd : level().getEntitiesOfClass(DustGrazer.class, getBoundingBox().inflate(12)))
                herd.getNavigation().moveTo(herd.getX()+away.x, herd.getY(), herd.getZ()+away.z, 1.6);
        }
        return hit;
    }
}
