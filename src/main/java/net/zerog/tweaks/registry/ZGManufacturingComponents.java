package net.zerog.tweaks.registry;

import java.util.List;

/** Planetary parts plus the owner's explicit Copper manufacturing exception. */
public final class ZGManufacturingComponents {
    public static final List<String> METALS = List.of(
            "moonsteel", "lunarium", "ferrox", "olympium", "aresium",
            "cobaltium", "cyrrium", "aurelion", "azurium",
            "ruskite", "tectium", "pyrium", "basaltine",
            "salvium", "wraithsteel", "palladine", "rime_nickel",
            "photium", "radiantine", "astrium", "helion");
    public static final List<String> ALL_METALS = java.util.stream.Stream.concat(METALS.stream(),java.util.stream.Stream.of("copper")).toList();

    public static void init() {
        for (String metal : ALL_METALS) {
            ItemInit.ITEMS.registerSimpleItem(metal + "_cog");
            ItemInit.ITEMS.registerSimpleItem(metal + "_plate");
        }
    }

    private ZGManufacturingComponents() {}
}
