package net.zerog.tweaks.registry;

import net.neoforged.neoforge.common.ModConfigSpec;

/** Local ambient quality/audio/accessibility; native storms are server-owned. */
public final class ZGWeatherConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.IntValue QUALITY;
    public static final ModConfigSpec.BooleanValue THUNDER;
    public static final ModConfigSpec.BooleanValue REDUCED_FLASH;
    static {
        var builder = new ModConfigSpec.Builder();
        builder.push("alienWeather");
        QUALITY = builder.comment("0=ambient particles off, 1=low (4/tick), 2=high (12/tick). Native rain and real lightning are independent.")
                .defineInRange("quality", 0, 0, 2);
        THUNDER = builder.comment("Local thunder audio during electrical storms, respecting Weather volume.")
                .define("thunder", true);
        REDUCED_FLASH = builder.comment("Disable additional sky flashes. Not a photosensitivity safety guarantee.")
                .define("reducedFlash", true);
        builder.pop(); SPEC = builder.build();
    }
    private ZGWeatherConfig() {}
}
