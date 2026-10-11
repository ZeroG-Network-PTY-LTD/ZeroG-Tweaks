package net.zerog.tweaks.machine;
import net.neoforged.neoforge.common.ModConfigSpec;
/** Server-controlled gameplay volumes; not a physical pressure simulation. */
public final class GasProductionConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.IntValue WATER,ENERGY,TICKS,LEAK;
    static {var b=new ModConfigSpec.Builder();
        WATER=b.defineInRange("waterMBPerCycle",10,1,8000);
        ENERGY=b.defineInRange("FEPerCycle",2000,1,200000);
        TICKS=b.defineInRange("ticksPerCycle",100,1,12000);
        LEAK=b.defineInRange("wrongLiquidPipeLeakMBPerSecond",10,0,100);
        SPEC=b.build();}
    private GasProductionConfig(){}
}
