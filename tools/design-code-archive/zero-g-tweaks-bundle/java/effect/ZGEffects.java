package net.zerog.tweaks.effect;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.tags.DamageTypeTags;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.living.MobEffectEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Custom effects for ZeroG Tweaks foods.
 *  - Freeze Ward: immune to freezing (powder snow, Freezing damage, Frost Warden/Rime Stalker chills).
 *  - Surefoot: Slowness cannot be applied, and any Slowness is removed.
 * Register in your mod constructor: ZGEffects.EFFECTS.register(modEventBus);
 */
public final class ZGEffects {
    private ZGEffects() {}

    public static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(Registries.MOB_EFFECT, ZeroGTweaks.MODID);

    public static final DeferredHolder<MobEffect, MobEffect> FREEZE_WARD = EFFECTS.register("freeze_ward", FreezeWardEffect::new);
    public static final DeferredHolder<MobEffect, MobEffect> SUREFOOT = EFFECTS.register("surefoot", SurefootEffect::new);

    public static void register(IEventBus modBus) { EFFECTS.register(modBus); }

    public static class FreezeWardEffect extends MobEffect {
        public FreezeWardEffect() { super(MobEffectCategory.BENEFICIAL, 0x78DCF0); }
        @Override public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) { return true; }
        @Override public boolean applyEffectTick(LivingEntity entity, int amplifier) {
            if (entity.getTicksFrozen() > 0) entity.setTicksFrozen(0);   // thaw every tick
            return true;
        }
    }

    public static class SurefootEffect extends MobEffect {
        public SurefootEffect() { super(MobEffectCategory.BENEFICIAL, 0xC8AA6E); }
        @Override public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) { return duration % 10 == 0; }
        @Override public boolean applyEffectTick(LivingEntity entity, int amplifier) {
            if (entity.hasEffect(MobEffects.MOVEMENT_SLOWDOWN)) entity.removeEffect(MobEffects.MOVEMENT_SLOWDOWN);
            return true;
        }
    }

    /** Game-bus events that make the effects airtight. */
    @EventBusSubscriber(modid = ZeroGTweaks.MODID)
    public static final class Events {
        @SubscribeEvent
        public static void onIncomingDamage(LivingIncomingDamageEvent event) {
            if (event.getSource().is(DamageTypeTags.IS_FREEZING) && event.getEntity().hasEffect(FREEZE_WARD)) event.setCanceled(true);
        }
        @SubscribeEvent
        public static void onEffectApplicable(MobEffectEvent.Applicable event) {
            if (event.getEffectInstance().is(MobEffects.MOVEMENT_SLOWDOWN) && event.getEntity().hasEffect(SUREFOOT))
                event.setResult(MobEffectEvent.Applicable.Result.DO_NOT_APPLY);
        }
    }
}
