package net.zerog.tweaks.registry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.BucketItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.FlowingFluid;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForgeMod;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidInteractionRegistry;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.minecraft.world.level.material.Fluid;

/** Five additional design-doc fluids; existing Liquid Starlight registrations are retained. */
public final class ZGDimensionFluids {
    public static final class Liquid {
        public final String id;
        public final int light, fog;
        public DeferredHolder<FluidType, FluidType> type;
        public DeferredHolder<Fluid, FlowingFluid> source, flowing;
        public DeferredBlock<LiquidBlock> block;
        public DeferredItem<BucketItem> bucket;
        private Liquid(String id, int light, int fog) { this.id = id; this.light = light; this.fog = fog; }
    }
    public static final Liquid ACID = make("acid", 4, 0x73A01F, 1400, 2000, false);
    public static final Liquid MAGMA = make("magma_slag", 12, 0x8A2A08, 3500, 8000, true);
    public static final Liquid CRYO = make("cryo_fluid", 2, 0x8FD0E6, 1100, 1600, false);
    public static final Liquid SOLAR = make("solar_plasma", 15, 0xFFB040, 2500, 5000, true);
    public static final Liquid NULL = make("null_fluid", 6, 0x1A1030, 400, 1200, false);
    public static final List<Liquid> ALL = List.of(ACID, MAGMA, CRYO, SOLAR, NULL);
    private static final ResourceKey<DamageType> PLASMA_DAMAGE = ResourceKey.create(Registries.DAMAGE_TYPE,
            ResourceLocation.fromNamespaceAndPath("zerog_tweaks", "solar_plasma"));

    private static Liquid make(String id, int light, int fog, int density, int viscosity, boolean hot) {
        Liquid liquid = new Liquid(id, light, fog);
        liquid.type = ZGFluids.TYPES.register(id, () -> new FluidType(FluidType.Properties.create()
                .descriptionId("fluid_type.zerog_tweaks." + id).density(density).viscosity(viscosity)
                .lightLevel(light).temperature(hot ? 1600 : (id.equals("cryo_fluid") ? 250 : 300))
                .canSwim(!hot).canDrown(!hot).canExtinguish(!hot).canHydrate(false)
                .canConvertToSource(false).supportsBoating(!hot).motionScale(hot ? 0.0023 : 0.007)));
        Supplier<BaseFlowingFluid.Properties> properties = () -> new BaseFlowingFluid.Properties(liquid.type, liquid.source, liquid.flowing)
                .block(liquid.block).bucket(liquid.bucket).slopeFindDistance(3).levelDecreasePerBlock(2)
                .tickRate(hot ? 30 : 10).explosionResistance(100F);
        liquid.source = ZGFluids.FLUIDS.register(id, () -> new BaseFlowingFluid.Source(properties.get()));
        liquid.flowing = ZGFluids.FLUIDS.register("flowing_" + id, () -> new BaseFlowingFluid.Flowing(properties.get()));
        liquid.block = BlockInit.BLOCKS.register(id, () -> new DimensionLiquidBlock(liquid.source.get(), id,
                BlockBehaviour.Properties.ofFullCopy(Blocks.WATER).lightLevel(s -> light)));
        liquid.bucket = ItemInit.ITEMS.register(id + "_bucket", () -> new BucketItem(liquid.source.get(),
                new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1)));
        return liquid;
    }
    public static void init() { /* Class initialization registers entries before any bus registration. */ }
    public static void setup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            FluidType water = NeoForgeMod.WATER_TYPE.value(), lava = NeoForgeMod.LAVA_TYPE.value();
            mix(ACID.type.get(), water, BlockInit.SLUDGESTONE); mix(ACID.type.get(), lava, BlockInit.TOXIC_MUD);
            mix(ZGFluids.LIQUID_STARLIGHT_TYPE.get(), water, BlockInit.CRYSTAL_SAND);
            mix(ZGFluids.LIQUID_STARLIGHT_TYPE.get(), lava, BlockInit.PRISMSTONE);
            mix(MAGMA.type.get(), water, BlockInit.SLAG); mix(MAGMA.type.get(), ZGFluids.LIQUID_STARLIGHT_TYPE.get(), BlockInit.RIFT_GLASS);
            mix(CRYO.type.get(), water, BlockInit.GLACIAL_ICE); mix(CRYO.type.get(), lava, BlockInit.FROSTROCK);
            mix(water, CRYO.type.get(), BlockInit.GLACIAL_ICE);
            mix(SOLAR.type.get(), water, BlockInit.SLAG_GLASS); mix(SOLAR.type.get(), CRYO.type.get(), BlockInit.SUNSPOT_ROCK);
            mix(NULL.type.get(), lava, BlockInit.DEEPSLATE_NULLIFITE_ORE);
        });
    }
    private static void mix(FluidType source, FluidType other, Supplier<? extends Block> result) {
        FluidInteractionRegistry.addInteraction(source, new FluidInteractionRegistry.InteractionInformation(other,
                state -> result.get().defaultBlockState()));
    }

    private static final class DimensionLiquidBlock extends LiquidBlock {
        private final String id;
        DimensionLiquidBlock(FlowingFluid fluid, String id, Properties properties) { super(fluid, properties); this.id = id; }
        @Override
        protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
            super.entityInside(state, level, pos, entity);
            if (level.isClientSide) return;
            long tick = level.getGameTime();
            String contactKey = "ZeroGFluidContact_" + id;
            if (entity.getPersistentData().contains(contactKey) && entity.getPersistentData().getLong(contactKey) == tick) return;
            entity.getPersistentData().putLong(contactKey, tick);
            switch (id) {
                case "acid" -> {
                    if (entity instanceof ItemEntity item) {
                        var data = item.getPersistentData();
                        if (!data.contains("ZeroGAcidStart") || data.getLong("ZeroGAcidLast") < tick - 1) data.putLong("ZeroGAcidStart", tick);
                        data.putLong("ZeroGAcidLast", tick);
                        if (tick - data.getLong("ZeroGAcidStart") >= 100) item.discard();
                    }
                    if (entity instanceof LivingEntity living && tick % 20 == 0) {
                        living.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1));
                        for (EquipmentSlot slot : List.of(EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET)) {
                            living.getItemBySlot(slot).hurtAndBreak(1, living, slot);
                        }
                    }
                }
                case "magma_slag" -> {
                    if (!entity.fireImmune()) {
                        entity.igniteForSeconds(8);
                        if (tick % 10 == 0) entity.hurt(level.damageSources().lava(), 3F);
                    }
                }
                case "cryo_fluid" -> {
                    if (entity instanceof LivingEntity living && !eidoliteSet(living)) {
                        living.setTicksFrozen(Math.min(living.getTicksRequiredToFreeze() + 40, living.getTicksFrozen() + 4));
                        if (tick % 20 == 0) {
                            living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                            if (living.isFullyFrozen()) living.hurt(level.damageSources().freeze(), 1F);
                        }
                    }
                }
                case "solar_plasma" -> {
                    if (entity instanceof LivingEntity living && heatproofSet(living)) break;
                    entity.igniteForSeconds(10);
                    if (tick % 10 == 0) entity.hurt(new DamageSource(level.registryAccess().registryOrThrow(Registries.DAMAGE_TYPE)
                            .getHolderOrThrow(PLASMA_DAMAGE)), 5F);
                }
                case "null_fluid" -> {
                    var motion = entity.getDeltaMovement();
                    entity.setDeltaMovement(motion.x, Math.min(motion.y + 0.02, 0.12), motion.z);
                    entity.fallDistance = 0;
                }
                default -> { }
            }
        }
        private static boolean eidoliteSet(LivingEntity entity) { return fullSet(entity, "eidolite"); }
        private static boolean heatproofSet(LivingEntity entity) { return fullSet(entity, "skarnite") || fullSet(entity, "eidolite") || fullSet(entity, "solvanite"); }
        private static boolean fullSet(LivingEntity entity, String family) {
            for (EquipmentSlot slot : List.of(EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET)) {
                var key = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(entity.getItemBySlot(slot).getItem());
                if (!key.getNamespace().equals("zerog_tweaks") || !key.getPath().startsWith(family + "_")) return false;
            }
            return true;
        }
    }
    private ZGDimensionFluids() {}
}
