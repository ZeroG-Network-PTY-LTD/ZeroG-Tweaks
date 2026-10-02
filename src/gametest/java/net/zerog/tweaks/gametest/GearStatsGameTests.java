package net.zerog.tweaks.gametest;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * Gear stats (design doc v1.3, data-manifest.json gear_stats): every set's armor points per piece, toughness,
 * knockback resistance, armor durability (multiple of diamond, factor 33) and sword damage, read from the real items.
 */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class GearStatsGameTests {
    /** helmet, chestplate, leggings, boots, toughness, knockback resistance, durability x diamond, sword damage */
    private static final Map<String, float[]> STATS = new LinkedHashMap<>();
    static {
        STATS.put("nullifite", new float[]{4, 8, 6, 3, 3.5F, 0.11F, 1.4F, 8.5F});
        STATS.put("olympium", new float[]{4, 8, 6, 4, 5.0F, 0.14F, 1.7F, 10.0F});
        STATS.put("cerulite", new float[]{4, 9, 7, 4, 6.5F, 0.17F, 2.0F, 11.5F});
        STATS.put("skarnite", new float[]{5, 9, 7, 4, 8.0F, 0.20F, 2.3F, 13.0F});
        STATS.put("eidolite", new float[]{5, 10, 7, 5, 9.5F, 0.23F, 2.6F, 14.5F});
        STATS.put("solvanite", new float[]{6, 10, 8, 6, 11.0F, 0.26F, 2.9F, 16.0F});
        STATS.put("ferrox", new float[]{4, 8, 6, 3, 4.0F, 0.12F, 1.5F, 9.0F});
        STATS.put("moonsteel", new float[]{4, 8, 6, 4, 4.5F, 0.13F, 1.6F, 9.5F});
        STATS.put("cobaltium", new float[]{4, 9, 6, 4, 5.5F, 0.15F, 1.8F, 10.5F});
        STATS.put("cyrrium", new float[]{4, 9, 6, 4, 6.0F, 0.16F, 1.9F, 11.0F});
        STATS.put("aurelion", new float[]{4, 8, 6, 4, 4.5F, 0.10F, 1.35F, 10.5F});
        STATS.put("ruskite", new float[]{4, 9, 7, 4, 7.0F, 0.18F, 2.1F, 12.0F});
        STATS.put("tectium", new float[]{5, 9, 7, 4, 7.5F, 0.19F, 2.2F, 12.5F});
        STATS.put("pyrium", new float[]{4, 9, 6, 4, 6.0F, 0.10F, 1.6F, 12.0F});
        STATS.put("salvium", new float[]{5, 9, 7, 5, 8.5F, 0.21F, 2.4F, 13.5F});
        STATS.put("wraithsteel", new float[]{5, 9, 7, 5, 9.0F, 0.22F, 2.5F, 14.0F});
        STATS.put("palladine", new float[]{5, 9, 7, 4, 7.5F, 0.10F, 1.8F, 13.5F});
        STATS.put("photium", new float[]{5, 10, 7, 5, 10.0F, 0.24F, 2.7F, 15.0F});
        STATS.put("astrium", new float[]{5, 10, 8, 5, 10.5F, 0.25F, 2.8F, 15.5F});
        STATS.put("radiantine", new float[]{5, 9, 7, 5, 9.0F, 0.10F, 2.05F, 15.0F});
    }
    private static final String[] PIECES = {"helmet", "chestplate", "leggings", "boots"};

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void armor_and_swords_match_the_design_doc(GameTestHelper helper) {
        List<String> wrong = new ArrayList<>();
        for (var set : STATS.entrySet()) {
            float[] s = set.getValue();
            for (int i = 0; i < PIECES.length; i++) {
                var item = BuiltInRegistries.ITEM.get(id(set.getKey() + "_" + PIECES[i]));
                if (!(item instanceof ArmorItem armor)) { wrong.add(set.getKey() + "_" + PIECES[i] + " is not armor"); continue; }
                var material = armor.getMaterial().value();
                if (armor.getDefense() != (int) s[i]) wrong.add(set.getKey() + "_" + PIECES[i] + " armor " + armor.getDefense() + " != " + (int) s[i]);
                if (material.toughness() != s[4]) wrong.add(set.getKey() + " toughness " + material.toughness() + " != " + s[4]);
                if (Math.abs(material.knockbackResistance() - s[5]) > 1e-4) wrong.add(set.getKey() + " knockback " + material.knockbackResistance() + " != " + s[5]);
                int uses = armor.getType().getDurability(Math.round(33 * s[6]));
                if (new ItemStack(item).getMaxDamage() != uses) wrong.add(set.getKey() + "_" + PIECES[i] + " durability " + new ItemStack(item).getMaxDamage() + " != " + uses);
            }
            var sword = new ItemStack(BuiltInRegistries.ITEM.get(id(set.getKey() + "_sword")));
            double damage = 1.0 + sword.getOrDefault(net.minecraft.core.component.DataComponents.ATTRIBUTE_MODIFIERS, ItemAttributeModifiers.EMPTY)
                    .modifiers().stream().filter(m -> m.attribute().is(Attributes.ATTACK_DAMAGE) && m.slot() == EquipmentSlotGroup.MAINHAND)
                    .mapToDouble(m -> m.modifier().amount()).sum();
            if (Math.abs(damage - s[7]) > 1e-4) wrong.add(set.getKey() + "_sword damage " + damage + " != " + s[7]);
        }
        helper.assertTrue(wrong.isEmpty(), wrong.size() + " gear-stat mismatches, e.g. " + wrong.subList(0, Math.min(6, wrong.size())));
        helper.succeed();
    }

    private static ResourceLocation id(String path) { return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path); }
    private GearStatsGameTests() {}
}
