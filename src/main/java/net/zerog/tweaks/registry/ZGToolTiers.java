package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Tool tiers for the ZeroG mining ladder (design doc v1.3, "Mining ladder" and "Gear stats", locked).
 * Every set out-mines netherite: its tier denies drops from zerog_tweaks:incorrect_for_<set>_tool, which holds the
 * ores of every higher level (see data/zerog_tweaks/tags/block/needs_<pick>_tool). Mining speed is the ladder speed,
 * durability is the doc's multiple of diamond, sword damage is the doc's value (1 base + 3 sword + tier bonus), and
 * precious (gold-style) sets mine faster with enchantability 25.
 */
public final class ZGToolTiers {
    /** baseline only picks the vanilla axe/hoe stat family in ItemInit (gold-style for precious sets). */
    public record Profile(Tier tier, Tiers baseline, int level) {}
    private static final Map<String, Profile> PROFILES = new LinkedHashMap<>();
    private static final int DIAMOND_USES = 1561;

    static {
        //        set            level  speed  x diamond  sword  precious
        register("nullifite",    5,     9.5F,  1.4F,      8.5F,  false);
        register("ferrox",       6,     10F,   1.5F,      9F,    false);
        register("moonsteel",    7,     10.5F, 1.6F,      9.5F,  false);
        register("olympium",     8,     11F,   1.7F,      10F,   false);
        register("cobaltium",    9,     11.5F, 1.8F,      10.5F, false);
        register("aurelion",     9,     15.5F, 1.35F,     10.5F, true);
        register("cyrrium",      10,    12F,   1.9F,      11F,   false);
        register("cerulite",     11,    12.5F, 2.0F,      11.5F, false);
        register("ruskite",      12,    13F,   2.1F,      12F,   false);
        register("pyrium",       12,    17F,   1.6F,      12F,   true);
        register("tectium",      13,    13.5F, 2.2F,      12.5F, false);
        register("skarnite",     14,    14F,   2.3F,      13F,   false);
        register("salvium",      15,    14.5F, 2.4F,      13.5F, false);
        register("palladine",    15,    18.5F, 1.8F,      13.5F, true);
        register("wraithsteel",  16,    15F,   2.5F,      14F,   false);
        register("eidolite",     17,    15.5F, 2.6F,      14.5F, false);
        register("photium",      18,    16F,   2.7F,      15F,   false);
        register("radiantine",   18,    20F,   2.05F,     15F,   true);
        register("astrium",      19,    16.5F, 2.8F,      15.5F, false);
        register("solvanite",    20,    17F,   2.9F,      16F,   false);
    }

    private static void register(String material, int level, float speed, float durabilityVsDiamond, float swordDamage,
                                 boolean precious) {
        int uses = Math.round(DIAMOND_USES * durabilityVsDiamond);
        float damageBonus = swordDamage - 4.0F; // sword = 1 (player) + 3 (sword) + tier bonus
        TagKey<Block> incorrect = TagKey.create(Registries.BLOCK,
                ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "incorrect_for_" + material + "_tool"));
        Tier tier = new Tier() {
            @Override public int getUses() { return uses; }
            @Override public float getSpeed() { return speed; }
            @Override public float getAttackDamageBonus() { return damageBonus; }
            @Override public int getEnchantmentValue() { return precious ? 25 : 15; }
            @Override public TagKey<Block> getIncorrectBlocksForDrops() { return incorrect; }
            @Override public Ingredient getRepairIngredient() {
                return ZGArmorMaterials.profiles().get(material).material().value().repairIngredient().get();
            }
        };
        PROFILES.put(material, new Profile(tier, precious ? Tiers.GOLD : Tiers.NETHERITE, level));
    }

    public static Profile get(String material) {
        var profile = PROFILES.get(material);
        if (profile == null) throw new IllegalArgumentException("Unknown tool material: " + material);
        return profile;
    }

    public static Map<String, Profile> profiles() { return Map.copyOf(PROFILES); }
    private ZGToolTiers() {}
}
