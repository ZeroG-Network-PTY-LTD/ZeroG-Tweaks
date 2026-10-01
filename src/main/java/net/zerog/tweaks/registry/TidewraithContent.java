package net.zerog.tweaks.registry;

import java.util.List;
import java.util.stream.Stream;
import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;

/** Admission guard: never expose a spawn egg/renderer while its artwork is still pending. */
public final class TidewraithContent {
    private static final String PREFIX = "assets/zerog_tweaks/";
    public static List<String> missingRuntimeResources() {
        var models = Stream.of("geo/tidewraith.geo.json", "geo/tidewraith_boss.geo.json",
                "animations/tidewraith.animation.json", "animations/tidewraith_boss.animation.json");
        var textures = Stream.of("tidewraith", "tidewraith_boss", "tidewraith_boss_abyssal",
                "tidewraith_boss_pearl", "tidewraith_boss_storm")
                .flatMap(name -> Stream.of("textures/entity/" + name + ".png",
                        "textures/entity/" + name + "_glowmask.png"));
        return Stream.concat(models, textures).filter(path ->
                TidewraithContent.class.getClassLoader().getResource(PREFIX + path) == null).toList();
    }

    public static boolean isReady() { return missingRuntimeResources().isEmpty(); }

    public static void register(IEventBus bus) {
        var missing = missingRuntimeResources();
        if (!missing.isEmpty()) {
            LogUtils.getLogger().warn("Tidewraith artwork admission pending: {} resources missing. "
                    + "Its renderers and boss egg are disabled to avoid broken client models.", missing.size());
            return;
        }
        TidewraithItems.register(bus);
    }

    private TidewraithContent() {}
}
