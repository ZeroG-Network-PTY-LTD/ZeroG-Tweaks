package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.Tidewraith;
import net.zerog.tweaks.entity.TidewraithBoss;

/** Approved regular/boss pair. No automatic world spawning until habitat rules are approved. */
public final class EntityInit {
    private static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(Registries.ENTITY_TYPE, ZeroGTweaks.MODID);
    public static final DeferredHolder<EntityType<?>, EntityType<Tidewraith>> TIDEWRAITH =
            ENTITIES.register("tidewraith", () -> EntityType.Builder.<Tidewraith>of(Tidewraith::new, MobCategory.MONSTER)
                    .sized(1.6F, 1.8F).clientTrackingRange(12).build("zerog_tweaks:tidewraith"));
    public static final DeferredHolder<EntityType<?>, EntityType<TidewraithBoss>> TIDEWRAITH_BOSS =
            ENTITIES.register("tidewraith_boss", () -> EntityType.Builder.<TidewraithBoss>of(TidewraithBoss::new, MobCategory.MONSTER)
                    .sized(2.4F, 2.125F).clientTrackingRange(16).build("zerog_tweaks:tidewraith_boss"));

    public static void register(IEventBus bus) {
        ENTITIES.register(bus);
        bus.addListener(EntityInit::attributes);
    }

    private static void attributes(EntityAttributeCreationEvent event) {
        event.put(TIDEWRAITH.get(), Tidewraith.createAttributes().build());
        event.put(TIDEWRAITH_BOSS.get(), TidewraithBoss.createAttributes().build());
    }

    private EntityInit() {}
}
