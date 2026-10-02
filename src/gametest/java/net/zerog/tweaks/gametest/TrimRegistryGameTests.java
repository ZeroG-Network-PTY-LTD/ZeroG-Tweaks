package net.zerog.tweaks.gametest;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.armortrim.TrimPatterns;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGTrimKeys;
import net.zerog.tweaks.registry.ZGTrims;

/** Every ZeroG trim key resolves in the game, and each trim template applies its own pattern. */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class TrimRegistryGameTests {
    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void every_zerog_trim_is_registered_and_has_its_template(GameTestHelper helper) {
        var access = helper.getLevel().registryAccess();
        var patterns = access.registryOrThrow(Registries.TRIM_PATTERN);
        var materials = access.registryOrThrow(Registries.TRIM_MATERIAL);
        List<String> wrong = new ArrayList<>();
        for (var key : ZGTrimKeys.ALL_PATTERNS) if (patterns.getHolder(key).isEmpty()) wrong.add("pattern missing: " + key.location());
        for (var key : ZGTrimKeys.ALL_MATERIALS) if (materials.getHolder(key).isEmpty()) wrong.add("material missing: " + key.location());
        for (var template : ZGTrims.ALL) {
            var stack = new ItemStack(template.get());
            var pattern = TrimPatterns.getFromTemplate(access, stack);
            String expected = template.getId().getPath().replace("_armor_trim_smithing_template", "");
            if (pattern.isEmpty() || !pattern.get().is(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, expected)))
                wrong.add(template.getId() + " does not apply pattern " + expected);
        }
        helper.assertTrue(ZGTrimKeys.ALL_PATTERNS.size() == 10 && ZGTrimKeys.ALL_MATERIALS.size() == 20 && ZGTrims.ALL.size() == 10,
                "Expected 10 patterns, 20 materials, 10 templates");
        helper.assertTrue(wrong.isEmpty(), wrong.size() + " trim registry problems: " + wrong);
        helper.succeed();
    }

    private TrimRegistryGameTests() {}
}
