package net.zerog.tweaks.power;

import net.neoforged.neoforge.common.ModConfigSpec;

/** Conservative server-owned balance; no client can choose generation rates. */
public final class PowerConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.IntValue SOLAR_RATE, FUSION_RATE, FUSION_TICKS, BUFFER, TRANSFER;
    public static final ModConfigSpec.DoubleValue MOON, EIDOLON, SOLVANE, RAIN;
    static {
        var b=new ModConfigSpec.Builder();
        SOLAR_RATE=b.defineInRange("solarBaseFEPerTick",20,1,10000);
        FUSION_RATE=b.defineInRange("fusionFEPerTick",1000,1,100000);
        FUSION_TICKS=b.defineInRange("fusionDustTicks",2000,1,1000000);
        BUFFER=b.defineInRange("baseBufferFE",1000000,100000,100000000);
        TRANSFER=b.defineInRange("transferFEPerTick",10000,1,1000000);
        EIDOLON=b.defineInRange("eidolonSolarMultiplier",0.25,0.0,100.0);
        MOON=b.defineInRange("moonSolarMultiplier",2.0,0.0,100.0);
        SOLVANE=b.defineInRange("solvaneSolarMultiplier",8.0,0.0,100.0);
        RAIN=b.defineInRange("rainSolarMultiplier",0.25,0.0,1.0);
        SPEC=b.build();
    }
    private PowerConfig(){}
}
