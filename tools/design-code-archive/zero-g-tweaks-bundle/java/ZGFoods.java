package net.zerog.tweaks.item;

import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Items;
import net.zerog.tweaks.effect.ZGEffects;

/** Generated from the ZeroG Tweaks food table (NeoForge 1.21.1). Values are proposals for playtesting. */
public final class ZGFoods {
    private ZGFoods() {}

    public static final FoodProperties CRAWLER_LEG = new FoodProperties.Builder().nutrition(2).saturationModifier(0.2f)
            .effect(new MobEffectInstance(MobEffects.HUNGER, 200, 0), 0.3f)
            .build();
    public static final FoodProperties ROASTED_CRAWLER_LEG = new FoodProperties.Builder().nutrition(5).saturationModifier(0.6f)
            .build();
    public static final FoodProperties HOPPER_MEAT = new FoodProperties.Builder().nutrition(2).saturationModifier(0.3f)
            .build();
    public static final FoodProperties COOKED_HOPPER = new FoodProperties.Builder().nutrition(6).saturationModifier(0.6f)
            .effect(new MobEffectInstance(MobEffects.JUMP, 400, 0), 1f)
            .build();
    public static final FoodProperties GRAZER_STEAK = new FoodProperties.Builder().nutrition(3).saturationModifier(0.3f)
            .build();
    public static final FoodProperties SEARED_GRAZER_STEAK = new FoodProperties.Builder().nutrition(8).saturationModifier(0.8f)
            .build();
    public static final FoodProperties BEETLE_GRUB = new FoodProperties.Builder().nutrition(1).saturationModifier(0.3f)
            .effect(new MobEffectInstance(MobEffects.CONFUSION, 80, 0), 0.3f)
            .build();
    public static final FoodProperties TOASTED_GRUB = new FoodProperties.Builder().nutrition(4).saturationModifier(0.6f)
            .build();
    public static final FoodProperties STAG_VENISON = new FoodProperties.Builder().nutrition(3).saturationModifier(0.3f)
            .build();
    public static final FoodProperties COOKED_VENISON = new FoodProperties.Builder().nutrition(8).saturationModifier(0.8f)
            .build();
    public static final FoodProperties FOWL = new FoodProperties.Builder().nutrition(2).saturationModifier(0.3f)
            .build();
    public static final FoodProperties ROAST_FOWL = new FoodProperties.Builder().nutrition(6).saturationModifier(0.6f)
            .build();
    public static final FoodProperties GLIMMERFISH = new FoodProperties.Builder().nutrition(2).saturationModifier(0.1f)
            .build();
    public static final FoodProperties COOKED_GLIMMERFISH = new FoodProperties.Builder().nutrition(5).saturationModifier(0.6f)
            .effect(new MobEffectInstance(MobEffects.NIGHT_VISION, 600, 0), 1f)
            .build();
    public static final FoodProperties BOAR_CHOP = new FoodProperties.Builder().nutrition(3).saturationModifier(0.3f)
            .build();
    public static final FoodProperties SMOKED_BOAR_CHOP = new FoodProperties.Builder().nutrition(8).saturationModifier(0.8f)
            .build();
    // Raw Scorch Tail sets the eater on fire for 2 s (ScorchTailItem).
    public static final FoodProperties SCORCH_TAIL = new FoodProperties.Builder().nutrition(2).saturationModifier(0.3f)
            .build();
    public static final FoodProperties GRILLED_SCORCH_TAIL = new FoodProperties.Builder().nutrition(6).saturationModifier(0.6f)
            .effect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 600, 0), 1f)
            .build();
    public static final FoodProperties YAK_MEAT = new FoodProperties.Builder().nutrition(3).saturationModifier(0.3f)
            .build();
    public static final FoodProperties YAK_ROAST = new FoodProperties.Builder().nutrition(8).saturationModifier(0.8f)
            .build();
    public static final FoodProperties GILDCRAB_MEAT = new FoodProperties.Builder().nutrition(2).saturationModifier(0.3f)
            .build();
    public static final FoodProperties COOKED_GILDCRAB = new FoodProperties.Builder().nutrition(7).saturationModifier(0.8f)
            .effect(new MobEffectInstance(MobEffects.ABSORPTION, 400, 0), 1f)
            .build();
    public static final FoodProperties EEL_FILLET = new FoodProperties.Builder().nutrition(2).saturationModifier(0.1f)
            .build();
    public static final FoodProperties COOKED_EEL = new FoodProperties.Builder().nutrition(6).saturationModifier(0.8f)
            .build();
    public static final FoodProperties BURROWER_STEAK = new FoodProperties.Builder().nutrition(3).saturationModifier(0.2f)
            .build();
    public static final FoodProperties COOKED_BURROWER_STEAK = new FoodProperties.Builder().nutrition(7).saturationModifier(0.7f)
            .build();
    public static final FoodProperties LURKER_LEG = new FoodProperties.Builder().nutrition(2).saturationModifier(0.2f)
            .effect(new MobEffectInstance(MobEffects.POISON, 80, 0), 0.6f)
            .build();
    public static final FoodProperties CRISPY_LURKER_LEG = new FoodProperties.Builder().nutrition(5).saturationModifier(0.6f)
            .build();
    public static final FoodProperties SKITTER_LEG = new FoodProperties.Builder().nutrition(2).saturationModifier(0.2f)
            .build();
    public static final FoodProperties ROASTED_SKITTER_LEG = new FoodProperties.Builder().nutrition(5).saturationModifier(0.6f)
            .build();
    public static final FoodProperties RUST_TUBER = new FoodProperties.Builder().nutrition(1).saturationModifier(0.3f)
            .build();
    public static final FoodProperties BAKED_TUBER = new FoodProperties.Builder().nutrition(5).saturationModifier(0.6f)
            .build();
    public static final FoodProperties LICHEN_CRISPS = new FoodProperties.Builder().nutrition(2).saturationModifier(0.3f)
            .build();
    public static final FoodProperties SKYBERRIES = new FoodProperties.Builder().nutrition(2).saturationModifier(0.1f)
            .build();
    public static final FoodProperties SHARDWOOD_SYRUP = new FoodProperties.Builder().nutrition(4).saturationModifier(0.3f)
            .effect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 200, 0), 1f)
            .usingConvertsTo(Items.GLASS_BOTTLE).alwaysEdible()
            .build();
    public static final FoodProperties CINDER_CAP_STEW = new FoodProperties.Builder().nutrition(6).saturationModifier(0.6f)
            .effect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 1200, 0), 1f)
            .usingConvertsTo(Items.BOWL)
            .build();
    public static final FoodProperties FROSTFERN_TEA = new FoodProperties.Builder().nutrition(2).saturationModifier(0.4f)
            .usingConvertsTo(Items.GLASS_BOTTLE).alwaysEdible()
            .effect(new MobEffectInstance(ZGEffects.FREEZE_WARD, 1200, 0), 1f)
            .build();
    // Frost Milk also clears all effects first (FrostMilkItem), then applies Surefoot.
    public static final FoodProperties FROST_MILK = new FoodProperties.Builder().nutrition(2).saturationModifier(0.2f)
            .usingConvertsTo(Items.GLASS_BOTTLE).alwaysEdible()
            .effect(new MobEffectInstance(ZGEffects.SUREFOOT, 600, 0), 1f)
            .build();
    public static final FoodProperties PYREFRUIT = new FoodProperties.Builder().nutrition(4).saturationModifier(0.4f)
            .effect(new MobEffectInstance(MobEffects.GLOWING, 200, 0), 1f)
            .build();
    public static final FoodProperties ROASTED_SOLFLOWER_SEEDS = new FoodProperties.Builder().nutrition(2).saturationModifier(0.2f)
            .build();
    public static final FoodProperties ASTRONAUT_RATION = new FoodProperties.Builder().nutrition(10).saturationModifier(1.0f)
            .fast()
            .build();
    public static final FoodProperties ORBIT_BURGER = new FoodProperties.Builder().nutrition(10).saturationModifier(0.9f)
            .build();
    public static final FoodProperties NEBULA_PIE = new FoodProperties.Builder().nutrition(8).saturationModifier(0.5f)
            .effect(new MobEffectInstance(MobEffects.NIGHT_VISION, 1200, 0), 1f)
            .build();
    public static final FoodProperties EMBER_CHILI = new FoodProperties.Builder().nutrition(10).saturationModifier(0.9f)
            .effect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 3600, 0), 1f)
            .effect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 600, 0), 1f)
            .usingConvertsTo(Items.BOWL)
            .build();
    public static final FoodProperties CRYO_CHOWDER = new FoodProperties.Builder().nutrition(10).saturationModifier(0.9f)
            .effect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 600, 0), 1f)
            .usingConvertsTo(Items.BOWL)
            .effect(new MobEffectInstance(ZGEffects.FREEZE_WARD, 3600, 0), 1f)
            .build();
    public static final FoodProperties RATION_PACK = new FoodProperties.Builder().nutrition(6).saturationModifier(0.8f)
            .fast()
            .build();
    public static final FoodProperties STARFALL_FEAST = new FoodProperties.Builder().nutrition(12).saturationModifier(1.2f)
            .effect(new MobEffectInstance(MobEffects.REGENERATION, 200, 1), 1f)
            .effect(new MobEffectInstance(MobEffects.ABSORPTION, 2400, 1), 1f)
            .usingConvertsTo(Items.BOWL)
            .build();
    public static final FoodProperties LOW_G_JELLY = new FoodProperties.Builder().nutrition(3).saturationModifier(0.3f)
            .effect(new MobEffectInstance(MobEffects.SLOW_FALLING, 1200, 0), 1f)
            .effect(new MobEffectInstance(MobEffects.JUMP, 1200, 1), 1f)
            .build();
}
