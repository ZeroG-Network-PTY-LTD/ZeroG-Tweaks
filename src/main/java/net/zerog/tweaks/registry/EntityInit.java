package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.CrystalStag;
import net.zerog.tweaks.entity.DuneBurrower;
import net.zerog.tweaks.entity.FrostYak;
import net.zerog.tweaks.entity.Prismling;
import net.zerog.tweaks.entity.RustBeetle;
import net.zerog.tweaks.entity.Tidewraith;
import net.zerog.tweaks.entity.TidewraithBoss;

/** Entity types: the five mob-data mobs become live (ids are the authority set). */
public final class EntityInit {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(Registries.ENTITY_TYPE, ZeroGTweaks.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<CrystalStag>> CRYSTAL_STAG =
            ENTITIES.register("crystal_stag", () -> EntityType.Builder.<CrystalStag>of(CrystalStag::new, MobCategory.CREATURE)
                    .sized(0.9f, 1.8f).build("crystal_stag"));
    public static final DeferredHolder<EntityType<?>, EntityType<FrostYak>> FROST_YAK =
            ENTITIES.register("frost_yak", () -> EntityType.Builder.<FrostYak>of(FrostYak::new, MobCategory.CREATURE)
                    .sized(0.9f, 1.4f).build("frost_yak"));
    public static final DeferredHolder<EntityType<?>, EntityType<Prismling>> PRISMLING_HOLDER =
            ENTITIES.register("prismling", () -> EntityType.Builder.<Prismling>of(Prismling::new, MobCategory.MONSTER)
                    .sized(0.5f, 0.75f).build("prismling"));
    public static final DeferredHolder<EntityType<?>, EntityType<RustBeetle>> RUST_BEETLE =
            ENTITIES.register("rust_beetle", () -> EntityType.Builder.<RustBeetle>of(RustBeetle::new, MobCategory.CREATURE)
                    .sized(0.8f, 0.7f).build("rust_beetle"));
    public static final DeferredHolder<EntityType<?>, EntityType<DuneBurrower>> DUNE_BURROWER =
            ENTITIES.register("dune_burrower", () -> EntityType.Builder.<DuneBurrower>of(DuneBurrower::new, MobCategory.CREATURE)
                    .sized(0.9f, 0.6f).build("dune_burrower"));
    // Approved regular/boss pair. No automatic world spawning until habitat rules are approved.
    public static final DeferredHolder<EntityType<?>, EntityType<Tidewraith>> TIDEWRAITH =
            ENTITIES.register("tidewraith", () -> EntityType.Builder.<Tidewraith>of(Tidewraith::new, MobCategory.MONSTER)
                    .sized(1.6F, 1.8F).clientTrackingRange(12).build("zerog_tweaks:tidewraith"));
    public static final DeferredHolder<EntityType<?>, EntityType<TidewraithBoss>> TIDEWRAITH_BOSS =
            ENTITIES.register("tidewraith_boss", () -> EntityType.Builder.<TidewraithBoss>of(TidewraithBoss::new, MobCategory.MONSTER)
                    .sized(2.4F, 2.125F).clientTrackingRange(16).build("zerog_tweaks:tidewraith_boss"));

    private EntityInit() {}

    public static void register(IEventBus modBus) {
        ENTITIES.register(modBus);
        modBus.addListener(EntityInit::attributes);
    }

    private static void attributes(EntityAttributeCreationEvent event) {
        event.put(TIDEWRAITH.get(), Tidewraith.createAttributes().build());
        event.put(TIDEWRAITH_BOSS.get(), TidewraithBoss.createAttributes().build());
    }
}