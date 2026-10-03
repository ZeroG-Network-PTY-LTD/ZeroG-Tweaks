package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.entity.AzureFowl;
import net.zerog.tweaks.entity.CrystalStag;
import net.zerog.tweaks.entity.Glimmerfish;
import net.zerog.tweaks.entity.Mossback;
import net.zerog.tweaks.entity.DuneBurrower;
import net.zerog.tweaks.entity.FrostYak;
import net.zerog.tweaks.entity.PrismSentinel;
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

    // Cerulon natural mobs (art already on 1.21.x: geo, animations, textures)
    public static final DeferredHolder<EntityType<?>, EntityType<AzureFowl>> AZURE_FOWL =
            ENTITIES.register("azure_fowl", () -> EntityType.Builder.<AzureFowl>of(AzureFowl::new, MobCategory.CREATURE)
                    .sized(0.4F, 0.8F).clientTrackingRange(10).build("zerog_tweaks:azure_fowl"));
    public static final DeferredHolder<EntityType<?>, EntityType<Glimmerfish>> GLIMMERFISH =
            ENTITIES.register("glimmerfish", () -> EntityType.Builder.<Glimmerfish>of(Glimmerfish::new, MobCategory.WATER_AMBIENT)
                    .sized(0.5F, 0.4F).eyeHeight(0.26F).clientTrackingRange(4).build("zerog_tweaks:glimmerfish"));
    // Shattered Skies grazer, roams Cerulon's Azure Moss plains (2.5 x 2 hitbox per its sheet)
    public static final DeferredHolder<EntityType<?>, EntityType<Mossback>> MOSSBACK =
            ENTITIES.register("mossback", () -> EntityType.Builder.<Mossback>of(Mossback::new, MobCategory.CREATURE)
                    .sized(2.5F, 2.0F).clientTrackingRange(10).build("zerog_tweaks:mossback"));
    // Galaxy 2 guardian: raised by the Concord Prism in its Cerulon arena; no natural spawning.
    public static final DeferredHolder<EntityType<?>, EntityType<PrismSentinel>> PRISM_SENTINEL =
            ENTITIES.register("prism_sentinel", () -> EntityType.Builder.<PrismSentinel>of(PrismSentinel::new, MobCategory.MONSTER)
                    .sized(3.6F, 10.8F).fireImmune().clientTrackingRange(16).build("zerog_tweaks:prism_sentinel"));

    private EntityInit() {}

    public static void register(IEventBus modBus) {
        ENTITIES.register(modBus);
        modBus.addListener(EntityInit::attributes);
    }

    private static void attributes(EntityAttributeCreationEvent event) {
        event.put(TIDEWRAITH.get(), Tidewraith.createAttributes().build());
        event.put(TIDEWRAITH_BOSS.get(), TidewraithBoss.createAttributes().build());
        event.put(PRISM_SENTINEL.get(), PrismSentinel.createAttributes().build());
        event.put(AZURE_FOWL.get(), AzureFowl.createAttributes().build());
        event.put(GLIMMERFISH.get(), Glimmerfish.createAttributes().build());
        event.put(MOSSBACK.get(), Mossback.createAttributes().build());
    }
}