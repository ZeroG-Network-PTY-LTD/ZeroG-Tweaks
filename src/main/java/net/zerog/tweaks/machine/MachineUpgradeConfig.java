package net.zerog.tweaks.machine;

import net.neoforged.neoforge.common.ModConfigSpec;

/** Conservative server settings bounded by the approved 2.5x / 30% contract. */
public final class MachineUpgradeConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.IntValue SPEED_PERCENT_PER_TIER, ENERGY_SAVING_PER_TIER;
    static {
        var builder=new ModConfigSpec.Builder();
        SPEED_PERCENT_PER_TIER=builder.comment("Acceleration percentage per tier; six tiers, maximum 2.5x speed.").defineInRange("accelerationPercentPerTier",25,0,25);
        ENERGY_SAVING_PER_TIER=builder.comment("Total recipe FE saving percentage per Energy Coil tier; maximum 30%.").defineInRange("energySavingPercentPerTier",5,0,5);
        SPEC=builder.build();
    }
    private MachineUpgradeConfig(){}
}
