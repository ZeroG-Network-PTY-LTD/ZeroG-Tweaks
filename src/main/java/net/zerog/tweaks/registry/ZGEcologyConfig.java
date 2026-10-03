package net.zerog.tweaks.registry;

import net.neoforged.neoforge.common.ModConfigSpec;

public final class ZGEcologyConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue IMPACTS;
    public static final ModConfigSpec.IntValue RADIUS;
    static {
        var builder=new ModConfigSpec.Builder();
        builder.comment("Daily impacts affect natural terrain in loaded ZeroG dimensions, never other dimensions.");
        IMPACTS=builder.define("dailyImpacts",true);
        RADIUS=builder.comment("Crater radius; existing smaller values are clamped to 6 to fit the 10x10x10 remnant. Back up saves.").defineInRange("impactRadius",6,2,6);
        SPEC=builder.build();
    }
    private ZGEcologyConfig(){}
}
