package net.zerog.tweaks.registry;

import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * ZeroG creative tabs, split and ordered like the vanilla tabs (Building Blocks, Natural Blocks,
 * Functional Blocks, Tools & Utilities, Combat, Food & Drinks, Ingredients, Spawn Eggs). They sit after the
 * vanilla tabs, in that order. Contents come from {@link ZGCreativeTabContents}, which is generated.
 * Any ZeroG item missing from every list is appended to Ingredients, so nothing is ever hidden by accident
 * (except crop blocks, which vanilla also keeps out of the tabs).
 */
public final class CreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ZeroGTweaks.MODID);

    /** Blocks that vanilla would not show (crop stages are placed by their seed item). */
    private static final Set<String> HIDDEN = Set.of("rust_tuber_crop", "skyberry_bush");

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> BUILDING_BLOCKS =
            tab("building_blocks", "cerulean_stone_bricks", ZGCreativeTabContents.BUILDING_BLOCKS, CreativeModeTabs.SPAWN_EGGS.location(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> NATURAL_BLOCKS =
            tab("natural_blocks", "cerulite_ore", ZGCreativeTabContents.NATURAL_BLOCKS, BUILDING_BLOCKS.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> FUNCTIONAL_BLOCKS =
            tab("functional_blocks", "gate_controller", ZGCreativeTabContents.FUNCTIONAL_BLOCKS, NATURAL_BLOCKS.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TOOLS_AND_UTILITIES =
            tab("tools_and_utilities", "nullifite_pickaxe", ZGCreativeTabContents.TOOLS_AND_UTILITIES, FUNCTIONAL_BLOCKS.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> COMBAT =
            tab("combat", "solvanite_sword", ZGCreativeTabContents.COMBAT, TOOLS_AND_UTILITIES.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> FOOD_AND_DRINKS =
            tab("food_and_drinks", "orbit_burger", ZGCreativeTabContents.FOOD_AND_DRINKS, COMBAT.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> INGREDIENTS =
            tab("ingredients", "nullifite_ingot", ZGCreativeTabContents.INGREDIENTS, FOOD_AND_DRINKS.getId(), true);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> SPAWN_EGGS =
            tab("spawn_eggs", "mossback_spawn_egg", ZGCreativeTabContents.SPAWN_EGGS, INGREDIENTS.getId(), false);

    private static DeferredHolder<CreativeModeTab, CreativeModeTab> tab(String name, String icon, String[] ids, ResourceLocation after, boolean catchAll) {
        return TABS.register(name, () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup." + ZeroGTweaks.MODID + "." + name))
                .icon(() -> new ItemStack(item(icon)))
                .withTabsBefore(after)
                .displayItems((params, out) -> {
                    for (String id : ids) {
                        Item it = item(id);
                        if (it != Items.AIR) out.accept(it);
                    }
                    if (catchAll) {
                        Set<String> listed = new HashSet<>(HIDDEN);
                        for (String[] list : ZGCreativeTabContents.ALL) listed.addAll(java.util.Arrays.asList(list));
                        for (Item it : BuiltInRegistries.ITEM) {
                            ResourceLocation key = BuiltInRegistries.ITEM.getKey(it);
                            if (key.getNamespace().equals(ZeroGTweaks.MODID) && !listed.contains(key.getPath())) out.accept(it);
                        }
                    }
                })
                .build());
    }

    private static Item item(String path) {
        return BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path));
    }

    public static void register(IEventBus bus) {
        TABS.register(bus);
    }

    private CreativeTabs() {}
}
