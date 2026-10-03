package net.zerog.tweaks.worldgen;

import net.zerog.tweaks.event.CometRemnant;

/** Shares the locked galaxy-slot theme mapping with mineral generation. */
public final class PlanetEcologyProfile {
    public static String theme(String dimension) { return CometRemnant.theme(dimension); }
    public static String tree(String dimension) {
        return switch(theme(dimension)) {
            case "mars", "skarn" -> "charwood";
            case "eidolon", "moon" -> "hoarwood";
            case "solvane" -> "gildwood";
            default -> "shardwood";
        };
    }
    private PlanetEcologyProfile() {}
}
