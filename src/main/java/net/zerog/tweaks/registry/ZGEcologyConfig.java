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
        RADIUS=builder.comment("Crater radius in blocks; includes excavation. Back up saves before testing.").defineInRange("impactRadius",4,2,6);
        SPEC=builder.build();
    }
    private ZGEcologyConfig(){}
}
