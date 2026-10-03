package net.zerog.tweaks.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.SoundActions;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Liquid Starlight (design doc: pools in Cerulon's crystal caves; light 12; Slow Falling and Night Vision while you swim
 * in it, see LiquidStarlightBlock). Water-like and swimmable, a little thicker; it spreads 3 blocks and does not make
 * new sources. Textures: block/liquid_starlight_still + _flow (animated); bucket: item/liquid_starlight_bucket.
 */
public final class ZGFluids {
    public static final DeferredRegister<FluidType> TYPES = DeferredRegister.create(NeoForgeRegistries.Keys.FLUID_TYPES, ZeroGTweaks.MODID);
    public static final DeferredRegister<Fluid> FLUIDS = DeferredRegister.create(Registries.FLUID, ZeroGTweaks.MODID);

    public static final DeferredHolder<FluidType, FluidType> LIQUID_STARLIGHT_TYPE = TYPES.register("liquid_starlight",
            () -> new FluidType(FluidType.Properties.create()
                    .descriptionId("fluid_type.zerog_tweaks.liquid_starlight")
                    .lightLevel(12).density(1200).viscosity(1400)
                    .canSwim(true).canDrown(true).canExtinguish(true).canHydrate(false).canConvertToSource(false)
                    .fallDistanceModifier(0F).motionScale(0.010).supportsBoating(true)
                    .sound(SoundActions.BUCKET_FILL, SoundEvents.BUCKET_FILL)
                    .sound(SoundActions.BUCKET_EMPTY, SoundEvents.BUCKET_EMPTY)
                    .sound(SoundActions.FLUID_VAPORIZE, SoundEvents.FIRE_EXTINGUISH)));

    public static final DeferredHolder<Fluid, FlowingFluid> LIQUID_STARLIGHT = FLUIDS.register("liquid_starlight",
            () -> new BaseFlowingFluid.Source(properties()));
    public static final DeferredHolder<Fluid, FlowingFluid> FLOWING_LIQUID_STARLIGHT = FLUIDS.register("flowing_liquid_starlight",
            () -> new BaseFlowingFluid.Flowing(properties()));

    private static BaseFlowingFluid.Properties properties() {
        return new BaseFlowingFluid.Properties(LIQUID_STARLIGHT_TYPE, LIQUID_STARLIGHT, FLOWING_LIQUID_STARLIGHT)
                .block(BlockInit.LIQUID_STARLIGHT).bucket(ItemInit.LIQUID_STARLIGHT_BUCKET)
                .slopeFindDistance(3).levelDecreasePerBlock(2).tickRate(10).explosionResistance(100F);
    }

    public static void register(IEventBus modBus) {
        TYPES.register(modBus);
        FLUIDS.register(modBus);
    }

    private ZGFluids() {}
}
