package net.zerog.tweaks.gametest;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SmithingRecipeInput;
import net.minecraft.world.item.enchantment.Enchantments;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGArmorMaterials;

/**
 * Upgrade chain (design doc v1.3): every set after Nullifite is made at the smithing table from the previous set on
 * the mining ladder (template + previous piece + the new set's ingot or gem), keeping enchantments, and can no longer
 * be crafted at a crafting table.
 */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class UpgradeChainGameTests {
    /** target set -> the set it is upgraded from */
    private static final Map<String, String> FROM = new LinkedHashMap<>();
    static {
        FROM.put("ferrox", "nullifite");
        FROM.put("moonsteel", "ferrox");
        FROM.put("olympium", "moonsteel");
        FROM.put("cobaltium", "olympium");
        FROM.put("aurelion", "olympium");
        FROM.put("cyrrium", "cobaltium");
        FROM.put("cerulite", "cyrrium");
        FROM.put("ruskite", "cerulite");
        FROM.put("pyrium", "cerulite");
        FROM.put("tectium", "ruskite");
        FROM.put("skarnite", "tectium");
        FROM.put("salvium", "skarnite");
        FROM.put("palladine", "skarnite");
        FROM.put("wraithsteel", "salvium");
        FROM.put("eidolite", "wraithsteel");
        FROM.put("photium", "eidolite");
        FROM.put("radiantine", "eidolite");
        FROM.put("astrium", "photium");
        FROM.put("solvanite", "astrium");
    }
    private static final String[] PIECES = {"helmet", "chestplate", "leggings", "boots", "sword", "pickaxe", "axe", "shovel", "hoe"};

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void every_set_upgrades_from_the_previous_one_and_keeps_enchantments(GameTestHelper helper) {
        var level = helper.getLevel();
        var recipes = level.getRecipeManager();
        var unbreaking = level.registryAccess().registryOrThrow(Registries.ENCHANTMENT).getHolderOrThrow(Enchantments.UNBREAKING);
        List<String> wrong = new ArrayList<>();
        int upgrades = 0;
        for (var step : FROM.entrySet()) {
            String set = step.getKey();
            Item template = item(set + "_upgrade_smithing_template");
            Item addition = ZGArmorMaterials.profiles().get(set).material().value().repairIngredient().get().getItems()[0].getItem();
            for (String piece : PIECES) {
                var base = new ItemStack(item(step.getValue() + "_" + piece));
                base.enchant(unbreaking, 3);
                var input = new SmithingRecipeInput(new ItemStack(template), base, new ItemStack(addition));
                var match = recipes.getRecipeFor(RecipeType.SMITHING, input, level);
                if (match.isEmpty()) { wrong.add("no recipe: " + step.getValue() + "_" + piece + " -> " + set); continue; }
                var out = match.get().value().assemble(input, level.registryAccess());
                if (out.getItem() != item(set + "_" + piece)) wrong.add(set + "_" + piece + " recipe gives " + out.getItem());
                else if (out.getEnchantments().getLevel(unbreaking) != 3) wrong.add(set + "_" + piece + " lost its enchantment");
                upgrades++;
            }
        }
        // nothing in the chain may still come from a crafting table
        for (var holder : recipes.getAllRecipesFor(RecipeType.CRAFTING)) {
            var result = holder.value().getResultItem(level.registryAccess()).getItem();
            String id = BuiltInRegistries.ITEM.getKey(result).toString();
            for (String set : FROM.keySet()) {
                for (String piece : PIECES) {
                    if (id.equals(ZeroGTweaks.MODID + ":" + set + "_" + piece)) wrong.add("still craftable: " + id + " via " + holder.id());
                }
            }
        }
        helper.assertTrue(wrong.isEmpty(), wrong.size() + " upgrade-chain problems, e.g. " + wrong.subList(0, Math.min(6, wrong.size())));
        helper.assertTrue(upgrades == FROM.size() * PIECES.length, "Expected 171 upgrades, checked " + upgrades);
        helper.assertTrue(item("nullifite_helmet") != Items.AIR, "Nullifite missing");
        helper.succeed();
    }

    private static Item item(String path) {
        return BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path));
    }

    private UpgradeChainGameTests() {}
}
