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
 * Rust Beetle (Mars): neutral grazer on Rust Lichen, rams back when hit
 * (damage via Attributes.ATTACK_DAMAGE wired in the goals below), herds.
 * Loot data already ships (beetle_grub).
 */
public class RustBeetle extends Animal {
    public RustBeetle(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0)
                .add(Attributes.MOVEMENT_SPEED, 0.2)
                .add(Attributes.ATTACK_DAMAGE, 4.0);
    }

    @Nullable
    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.BEE_LOOP; }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ItemInit.RUST_LICHEN_ITEM.get());
    }

    @Override
    public RustBeetle getBreedOffspring(net.minecraft.server.level.ServerLevel level,
            net.minecraft.world.entity.AgeableMob partner) {
        return net.zerog.tweaks.registry.EntityInit.RUST_BEETLE.get().create(level);
    }
}