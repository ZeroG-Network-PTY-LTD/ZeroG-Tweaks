package net.zerog.tweaks.fluid;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
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
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForgeMod;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidInteractionRegistry;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.effect.ZGEffects;
import net.zerog.tweaks.registry.ZGBlocks;
import net.zerog.tweaks.registry.ZGItems;

/**
 * The six ZeroG liquids (design doc v1.2): Acid, Liquid Starlight, Magma Slag, Cryo Fluid, Solar Plasma, Null Fluid.
 * Register: ZGFluids.FLUID_TYPES.register(modBus); ZGFluids.FLUIDS.register(modBus);
 * Blocks and buckets go through your ZGBlocks.BLOCKS / ZGItems.ITEMS registers.
 * Mixing rules are added in common setup (see Setup below). Client textures and fog: ZGClientExtensions.
 */
public final class ZGFluids {
    private ZGFluids() {}

    public static final DeferredRegister<FluidType> FLUID_TYPES = DeferredRegister.create(NeoForgeRegistries.Keys.FLUID_TYPES, ZeroGTweaks.MODID);
    public static final DeferredRegister<Fluid> FLUIDS = DeferredRegister.create(Registries.FLUID, ZeroGTweaks.MODID);

    /** One liquid: type, source, flowing, block and bucket. */
    public static final class Liquid {
        public final String id;
        public DeferredHolder<FluidType, FluidType> type;
        public DeferredHolder<Fluid, FlowingFluid> source, flowing;
        public DeferredBlock<LiquidBlock> block;
        public DeferredItem<BucketItem> bucket;
        Liquid(String id) { this.id = id; }
    }

    public static final Liquid ACID = liquid("acid", 1400, 2000, 4, 2, 2, MapColor.COLOR_LIGHT_GREEN, true, false);
    public static final Liquid LIQUID_STARLIGHT = liquid("liquid_starlight", 900, 800, 12, 1, 5, MapColor.COLOR_BLUE, true, false);
    public static final Liquid MAGMA_SLAG = liquid("magma_slag", 3500, 8000, 12, 3, 3, MapColor.COLOR_ORANGE, false, true);
    public static final Liquid CRYO_FLUID = liquid("cryo_fluid", 1100, 1600, 2, 2, 4, MapColor.ICE, true, false);
    public static final Liquid SOLAR_PLASMA = liquid("solar_plasma", 2500, 5000, 15, 2, 3, MapColor.COLOR_YELLOW, false, true);
    public static final Liquid NULL_FLUID = liquid("null_fluid", 400, 1200, 6, 1, 4, MapColor.COLOR_PURPLE, true, false);

    /**
     * @param levelDecrease 1 = spreads like water, 2 = like lava in the Overworld
     * @param slope        slope find distance (how far it flows toward holes)
     */
    private static Liquid liquid(String id, int density, int viscosity, int light, int levelDecrease, int slope, MapColor color, boolean swimmable, boolean hot) {
        Liquid l = new Liquid(id);
        l.type = FLUID_TYPES.register(id, () -> new FluidType(FluidType.Properties.create()
                .descriptionId("fluid_type." + ZeroGTweaks.MODID + "." + id)
                .density(density).viscosity(viscosity).lightLevel(light)
                .temperature(hot ? 1600 : 300)
                .canSwim(swimmable).canDrown(swimmable).canExtinguish(!hot)
                .supportsBoating(swimmable && !hot)
                .motionScale(hot ? 0.0023 : 0.007)));
        Supplier<BaseFlowingFluid.Properties> props = () -> new BaseFlowingFluid.Properties(l.type, l.source, l.flowing)
                .block(l.block).bucket(l.bucket)
                .levelDecreasePerBlock(levelDecrease).slopeFindDistance(slope).tickRate(hot ? 30 : 10);
        l.source = FLUIDS.register(id, () -> new BaseFlowingFluid.Source(props.get()));
        l.flowing = FLUIDS.register("flowing_" + id, () -> new BaseFlowingFluid.Flowing(props.get()));
        l.block = ZGBlocks.BLOCKS.register(id, () -> new ZGLiquidBlock(l.source.get(), id,
                BlockBehaviour.Properties.of().mapColor(color).replaceable().noCollission().strength(100f)
                        .pushReaction(PushReaction.DESTROY).noLootTable().liquid().lightLevel(s -> light)));
        l.bucket = ZGItems.ITEMS.register(id + "_bucket", () -> new BucketItem(l.source.get(),
                new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1)));
        return l;
    }

    /** Liquid block with each liquid's effect on anything inside it. */
    public static class ZGLiquidBlock extends LiquidBlock {
        private final String id;
        public ZGLiquidBlock(FlowingFluid fluid, String id, BlockBehaviour.Properties props) { super(fluid, props); this.id = id; }

        @Override
        public void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
            super.entityInside(state, level, pos, entity);
            if (level.isClientSide) return;
            long t = level.getGameTime();
            switch (id) {
                case "acid" -> {
                    if (entity instanceof ItemEntity item && item.getAge() > 100) item.discard();           // dissolves dropped items after 5 s
                    if (entity instanceof LivingEntity living && t % 20 == 0) {
                        // TODO: skip Bog Lurkers and anyone with the Neutralizer leggings upgrade
                        living.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1));
                        for (EquipmentSlot slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET})
                            living.getItemBySlot(slot).hurtAndBreak(1, living, slot);                        // corrodes armor
                    }
                }
                case "liquid_starlight" -> {
                    if (entity instanceof LivingEntity living && t % 20 == 0) {
                        living.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING, 100, 0));
                        living.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, 300, 0));
                    }
                }
                case "magma_slag" -> {
                    if (!entity.fireImmune()) { entity.igniteForSeconds(8); if (t % 10 == 0) entity.hurt(level.damageSources().lava(), 3f); }
                }
                case "cryo_fluid" -> {
                    if (entity instanceof LivingEntity living && !living.hasEffect(ZGEffects.FREEZE_WARD)) {
                        living.setTicksFrozen(Math.min(living.getTicksRequiredToFreeze() + 40, living.getTicksFrozen() + 4));
                        if (t % 20 == 0) living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                    }
                }
                case "solar_plasma" -> {
                    // Burns through Fire Resistance. TODO: skip players wearing Heatproof Plating or a full Skarnite+ set.
                    entity.igniteForSeconds(10);
                    if (t % 10 == 0) entity.hurt(level.damageSources().inFire(), 5f);
                }
                case "null_fluid" -> {
                    Vec3 v = entity.getDeltaMovement();
                    entity.setDeltaMovement(v.x, Math.min(v.y + 0.02, 0.12), v.z);                          // slow float upward
                    entity.fallDistance = 0;
                }
                default -> {}
            }
        }
    }

    /** Mixing rules: what each liquid makes when it meets another. */
    @EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD)
    public static final class Setup {
        @SubscribeEvent
        public static void commonSetup(FMLCommonSetupEvent event) {
            event.enqueueWork(() -> {
                FluidType water = NeoForgeMod.WATER_TYPE.value(), lava = NeoForgeMod.LAVA_TYPE.value();
                mix(ACID, water, ZGBlocks.SLUDGESTONE);          mix(ACID, lava, ZGBlocks.TOXIC_MUD);
                mix(LIQUID_STARLIGHT, water, ZGBlocks.CRYSTAL_SAND); mix(LIQUID_STARLIGHT, lava, ZGBlocks.PRISMSTONE);
                mix(MAGMA_SLAG, water, ZGBlocks.SLAG);            mix(MAGMA_SLAG, LIQUID_STARLIGHT.type.get(), ZGBlocks.RIFT_GLASS);
                mix(CRYO_FLUID, water, ZGBlocks.GLACIAL_ICE);     mix(CRYO_FLUID, lava, ZGBlocks.FROSTROCK);
                mix(SOLAR_PLASMA, water, ZGBlocks.SLAG_GLASS);    mix(SOLAR_PLASMA, CRYO_FLUID.type.get(), ZGBlocks.SUNSPOT_ROCK);
                mix(NULL_FLUID, lava, ZGBlocks.DEEPSLATE_NULLIFITE_ORE);
                // Cryo Fluid also freezes water it touches: water source next to Cryo Fluid becomes ice.
                FluidInteractionRegistry.addInteraction(water, new FluidInteractionRegistry.InteractionInformation(
                        CRYO_FLUID.type.get(), fluidState -> Blocks.ICE.defaultBlockState()));
            });
        }

        private static void mix(Liquid liquid, FluidType other, Supplier<? extends Block> result) {
            FluidInteractionRegistry.addInteraction(liquid.type.get(), new FluidInteractionRegistry.InteractionInformation(
                    other, fluidState -> result.get().defaultBlockState()));
        }
    }
}
