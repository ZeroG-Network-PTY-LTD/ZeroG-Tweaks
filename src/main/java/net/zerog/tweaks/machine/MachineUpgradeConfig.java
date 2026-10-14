package net.zerog.tweaks.machine;

import net.neoforged.neoforge.common.ModConfigSpec;

/** T1 settings retained for old server configs; higher tiers double T1 rates. */
public final class MachineUpgradeConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.IntValue SPEED_PERCENT_PER_TIER, ENERGY_SAVING_PER_TIER;
    static {
        var builder=new ModConfigSpec.Builder();
        SPEED_PERCENT_PER_TIER=builder.comment("Legacy key: T1 speed bonus percent. T2-T6 double the previous total speed.").defineInRange("accelerationPercentPerTier",25,0,25);
        ENERGY_SAVING_PER_TIER=builder.comment("Legacy key: T1 recipe FE saving percent. T2-T6 halve the previous cost, minimum 100 FE per powered recipe.").defineInRange("energySavingPercentPerTier",5,0,5);
        SPEC=builder.build();
    }
    private MachineUpgradeConfig(){}
    public static int tierFactor(int tier){return 1<<Math.clamp(tier-1,0,5);}
    public static int speedPercent(int tier){return tier<=0?100:(100+SPEED_PERCENT_PER_TIER.get())*tierFactor(tier);}
    public static int recipeEnergy(long base,int tier){
        if(base<=0)return 100;
        long numerator=base*(tier<=0?100:100-ENERGY_SAVING_PER_TIER.get());
        long divisor=100L*(tier<=0?1:tierFactor(tier));
        return (int)Math.clamp((numerator+divisor-1)/divisor,100,Integer.MAX_VALUE);
    }
}
