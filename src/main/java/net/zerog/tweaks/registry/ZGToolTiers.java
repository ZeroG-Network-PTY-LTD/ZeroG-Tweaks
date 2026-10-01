package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;

/** Conservative vanilla mining tiers; planet-specific progression gates remain unfinished. */
public final class ZGToolTiers {
    public record Profile(Tier tier, Tiers baseline) {}
    private static final Map<String, Profile> PROFILES = new LinkedHashMap<>();

    static {
        register("nullifite", Tiers.DIAMOND, 1561);
        register("olympium", Tiers.DIAMOND, 1656);
        register("cerulite", Tiers.NETHERITE, 2031);
        register("skarnite", Tiers.NETHERITE, 2196);
        register("eidolite", Tiers.NETHERITE, 2196);
        register("solvanite", Tiers.NETHERITE, 2470);
        register("ferrox", Tiers.IRON, 300);
        register("moonsteel", Tiers.IRON, 417);
        register("cobaltium", Tiers.DIAMOND, 1324);
        register("cyrrium", Tiers.DIAMOND, 1892);
        register("aurelion", Tiers.GOLD, 55);
        register("ruskite", Tiers.DIAMOND, 1656);
        register("tectium", Tiers.NETHERITE, 2031);
        register("pyrium", Tiers.GOLD, 55);
        register("salvium", Tiers.NETHERITE, 2031);
        register("wraithsteel", Tiers.NETHERITE, 2196);
        register("palladine", Tiers.GOLD, 55);
        register("photium", Tiers.NETHERITE, 2031);
        register("astrium", Tiers.NETHERITE, 2196);
        register("radiantine", Tiers.GOLD, 55);
    }

    private static void register(String material, Tiers baseline, int durability) {
        Tier tier = new Tier() {
            @Override public int getUses() { return durability; }
            @Override public float getSpeed() { return baseline.getSpeed(); }
            @Override public float getAttackDamageBonus() { return baseline.getAttackDamageBonus(); }
            @Override public int getEnchantmentValue() { return baseline.getEnchantmentValue(); }
            @Override public TagKey<Block> getIncorrectBlocksForDrops() { return baseline.getIncorrectBlocksForDrops(); }
            @Override public Ingredient getRepairIngredient() {
                return ZGArmorMaterials.profiles().get(material).material().value().repairIngredient().get();
            }
        };
        PROFILES.put(material, new Profile(tier, baseline));
    }

    public static Profile get(String material) {
        var profile = PROFILES.get(material);
        if (profile == null) throw new IllegalArgumentException("Unknown tool material: " + material);
        return profile;
    }

    public static Map<String, Profile> profiles() { return Map.copyOf(PROFILES); }
    private ZGToolTiers() {}
}
