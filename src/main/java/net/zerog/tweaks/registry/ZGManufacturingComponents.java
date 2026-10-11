package net.zerog.tweaks.registry;

import java.util.List;

/** Dimension-origin metal parts. No Overworld metals, gems or implicit machine recipes. */
public final class ZGManufacturingComponents {
    public static final List<String> METALS = List.of(
            "moonsteel", "lunarium", "ferrox", "olympium", "aresium",
            "cobaltium", "cyrrium", "aurelion", "azurium",
            "ruskite", "tectium", "pyrium", "basaltine",
            "salvium", "wraithsteel", "palladine", "rime_nickel",
            "photium", "radiantine", "astrium", "helion");

    public static void init() {
        for (String metal : METALS) {
            ItemInit.ITEMS.registerSimpleItem(metal + "_cog");
            ItemInit.ITEMS.registerSimpleItem(metal + "_plate");
        }
    }

    private ZGManufacturingComponents() {}
}
