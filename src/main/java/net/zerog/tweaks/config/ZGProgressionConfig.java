package net.zerog.tweaks.config;

import java.util.List;
import net.neoforged.neoforge.common.ModConfigSpec;

/** Common/server progression settings; defaults are the locked design values. */
public final class ZGProgressionConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.DoubleValue ORE_MULTIPLIER;
    public static final List<ModConfigSpec.IntValue> COSTS;
    public static final List<ModConfigSpec.DoubleValue> GRAVITY;
    public static final ModConfigSpec.IntValue RECALL_COOLDOWN;
    static {
        var b=new ModConfigSpec.Builder();
        ORE_MULTIPLIER=b.defineInRange("oreRarityMultiplier",1.0,0.1,10.0);
        COSTS=java.util.stream.IntStream.range(0,6).mapToObj(i->b.defineInRange("tier"+(i+1)+"FE",new int[]{500000,1000000,3000000,8000000,20000000,50000000}[i],1,100000000)).toList();
        String[] ids={"moon","mars","cerulon","skarn","eidolon","solvane"};
        double[] values={0.5,0.7,0.9,1.2,0.8,1.3};
        GRAVITY=java.util.stream.IntStream.range(0,6).mapToObj(i->b.defineInRange(ids[i]+"Gravity",values[i],0.1,3.0)).toList();
        RECALL_COOLDOWN=b.defineInRange("recallCooldownTicks",1200,20,72000);
        SPEC=b.build();
    }
    public static int baseCost(int tier) {return COSTS.get(Math.clamp(tier,1,6)-1).get();}
    private ZGProgressionConfig(){}
}
