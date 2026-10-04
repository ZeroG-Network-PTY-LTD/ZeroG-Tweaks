package net.zerog.tweaks.worldgen;

import net.zerog.tweaks.event.CometRemnant;

/** Shares the locked galaxy-slot theme mapping with mineral generation. */
public final class PlanetEcologyProfile {
    /** Bounded density: fertile biomes are richer, exposed planets keep sparse silhouettes. */
    public record Habitat(int treeChance,int flowerChance,int shortGrassChance,int tallGrassChance,
                          int caveColumns,int hangingChance,int floorChance) {}
    public static Habitat habitat(String dimension,String biome) {
        boolean lush=java.util.List.of("oasis","jungle","island","moss_bog","taiga").stream().anyMatch(biome::contains);
        if(lush)return new Habitat(1,8,3,10,56,9,9);
        return switch(theme(dimension)) {
            case "cerulon" -> new Habitat(2,9,4,12,48,10,10);
            case "eidolon" -> new Habitat(3,12,5,18,44,12,10);
            case "solvane" -> new Habitat(2,10,4,14,48,10,10);
            default -> new Habitat(4,14,5,22,40,12,10);
        };
    }
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
