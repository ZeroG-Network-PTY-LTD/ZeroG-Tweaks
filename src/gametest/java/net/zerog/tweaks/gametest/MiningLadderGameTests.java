package net.zerog.tweaks.gametest;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGToolTiers;

/**
 * The ZeroG mining ladder (design doc v1.3, locked): a level-N pickaxe drops every ore whose required level is N or
 * lower and none above it; every ZeroG pick mines its ores at its ladder speed. Ore levels come from
 * data-manifest.json mining_ladder.ore_required_level (vanilla: wood/gold 0, stone 1, iron 2, diamond 3, netherite 4).
 */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class MiningLadderGameTests {
    private static final Map<String, Integer> ORES = new LinkedHashMap<>();
    static {
        ORES.put("coronite_ore", 2);
        ORES.put("cryocite_ore", 2);
        ORES.put("emberite_ore", 2);
        ORES.put("fusion_dust_ore", 2);
        ORES.put("nebulite_ore", 2);
        ORES.put("pulsar_dust_ore", 2);
        ORES.put("regolith_ore", 2);
        ORES.put("spectral_dust_ore", 2);
        ORES.put("tremor_dust_ore", 2);
        ORES.put("deepslate_nullifite_ore", 4);
        ORES.put("ferrox_ore", 5);
        ORES.put("moonsteel_ore", 6);
        ORES.put("olympium_ore", 7);
        ORES.put("selenite_ore", 7);
        ORES.put("aresite_ore", 8);
        ORES.put("cobaltium_ore", 8);
        ORES.put("aurelion_ore", 9);
        ORES.put("cyrrium_ore", 9);
        ORES.put("lumenite_ore", 9);
        ORES.put("starlite_ore", 9);
        ORES.put("cerulite_ore", 10);
        ORES.put("ruskite_ore", 11);
        ORES.put("cinnabrite_ore", 12);
        ORES.put("pyrium_ore", 12);
        ORES.put("rift_opal_ore", 12);
        ORES.put("tectium_ore", 12);
        ORES.put("skarnite_ore", 13);
        ORES.put("salvium_ore", 14);
        ORES.put("palladine_ore", 15);
        ORES.put("remnant_shard_ore", 15);
        ORES.put("rimeglass_ore", 15);
        ORES.put("wraithsteel_ore", 15);
        ORES.put("eidolite_ore", 16);
        ORES.put("photium_ore", 17);
        ORES.put("astrium_ore", 18);
        ORES.put("dawnstone_ore", 18);
        ORES.put("nova_pearl_ore", 18);
        ORES.put("radiantine_ore", 18);
        ORES.put("solvanite_ore", 19);
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void every_pickaxe_mines_exactly_its_ladder_ores(GameTestHelper helper) {
        Map<ItemStack, Integer> picks = new LinkedHashMap<>();
        picks.put(new ItemStack(Items.WOODEN_PICKAXE), 0);
        picks.put(new ItemStack(Items.GOLDEN_PICKAXE), 0);
        picks.put(new ItemStack(Items.STONE_PICKAXE), 1);
        picks.put(new ItemStack(Items.IRON_PICKAXE), 2);
        picks.put(new ItemStack(Items.DIAMOND_PICKAXE), 3);
        picks.put(new ItemStack(Items.NETHERITE_PICKAXE), 4);
        for (var entry : ZGToolTiers.profiles().entrySet()) {
            var item = BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, entry.getKey() + "_pickaxe"));
            picks.put(new ItemStack(item), entry.getValue().level());
        }
        List<String> wrong = new ArrayList<>();
        int checks = 0;
        for (var ore : ORES.entrySet()) {
            var block = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, ore.getKey()));
            helper.assertTrue(block != Blocks.AIR, "Ore block missing: " + ore.getKey());
            var state = block.defaultBlockState();
            for (var pick : picks.entrySet()) {
                boolean expected = pick.getValue() >= ore.getValue();
                boolean actual = pick.getKey().isCorrectToolForDrops(state);
                if (expected != actual) {
                    wrong.add(BuiltInRegistries.ITEM.getKey(pick.getKey().getItem()).getPath() + (expected ? " cannot drop " : " wrongly drops ")
                            + ore.getKey() + " (needs level " + ore.getValue() + ", pick level " + pick.getValue() + ")");
                }
                checks++;
            }
        }
        helper.assertTrue(wrong.isEmpty(), wrong.size() + " ladder violations, e.g. " + wrong.subList(0, Math.min(5, wrong.size())));
        helper.assertTrue(checks == ORES.size() * picks.size(), "Not every pick/ore pair was checked");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void zerog_picks_mine_at_ladder_speed(GameTestHelper helper) {
        var ore = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "deepslate_nullifite_ore")).defaultBlockState();
        for (var entry : ZGToolTiers.profiles().entrySet()) {
            var pick = new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, entry.getKey() + "_pickaxe")));
            float speed = pick.getDestroySpeed(ore);
            helper.assertTrue(speed == entry.getValue().tier().getSpeed(),
                    entry.getKey() + "_pickaxe mines at " + speed + ", ladder says " + entry.getValue().tier().getSpeed());
        }
        helper.succeed();
    }

    private MiningLadderGameTests() {}
}
