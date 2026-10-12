package net.zerog.tweaks.registry;

import net.neoforged.neoforge.common.ModConfigSpec;

public final class ZGEcologyConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue IMPACTS;
    public static final ModConfigSpec.IntValue RADIUS;
    public static final ModConfigSpec.IntValue TIDEWRAITH_CHANCE, TIDEWRAITH_NEARBY, TIDEWRAITH_RANGE;
    static {
        var builder=new ModConfigSpec.Builder();
        builder.comment("Daily impacts affect natural terrain in loaded ZeroG dimensions, never other dimensions.");
        IMPACTS=builder.define("dailyImpacts",true);
        RADIUS=builder.comment("Crater radius; existing smaller values are clamped to 6 to fit the 10x10x10 remnant. Back up saves.").defineInRange("impactRadius",6,2,6);
        TIDEWRAITH_CHANCE=builder.comment("Natural regular Tidewraith chance: one eligible attempt in this many. Bosses excluded.").defineInRange("tidewraithNaturalChance",8,1,1000);
        TIDEWRAITH_NEARBY=builder.comment("Regular Tidewraith pack cap. Minimum4 permits the approved3-4 member groups; old limit2 is corrected.").defineInRange("tidewraithNearbyLimit",4,4,20);
        TIDEWRAITH_RANGE=builder.defineInRange("tidewraithNearbyRadius",128,32,256);
        SPEC=builder.build();
    }
    private ZGEcologyConfig(){}
}
