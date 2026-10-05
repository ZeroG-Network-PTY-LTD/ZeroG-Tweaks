package net.zerog.tweaks.entity;

import javax.annotation.Nullable;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

import net.zerog.tweaks.registry.ItemInit;

/**
 * Dune Burrower (Dune/Desert wasteland): burrowing passive mob.
 * Loot data ships (sand_sift).
 */
public class DuneBurrower extends AnimatedPlanetAnimal {
    @Override protected String animationId() { return "dune_burrower"; }
    public DuneBurrower(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0)
                .add(Attributes.MOVEMENT_SPEED, 0.22);
    }

    @Nullable
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.SAND_BREAK; }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ItemInit.RUST_TUBER.get());
    }

    @Override
    public DuneBurrower getBreedOffspring(net.minecraft.server.level.ServerLevel level,
            net.minecraft.world.entity.AgeableMob partner) {
        return net.zerog.tweaks.registry.EntityInit.DUNE_BURROWER.get().create(level);
    }
}
