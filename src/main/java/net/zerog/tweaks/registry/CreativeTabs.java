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
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> LIQUIDS =
            tab("liquids", "liquid_starlight_bucket", new String[0], SPAWN_EGGS.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> HONEY_LIQUIDS =
            tab("honey_liquids", "flora_bee_honey_bucket", new String[0], LIQUIDS.getId(), false);
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> ADMIN_TOOLS =
            TABS.register("admin_tools", () -> CreativeModeTab.builder()
                    .title(Component.literal("Z-Admintools"))
                    .icon(() -> new ItemStack(ItemInit.WEATHER_TESTER.get()))
                    .withTabsBefore(HONEY_LIQUIDS.getId())
                    .displayItems((params, out) -> out.accept(ItemInit.WEATHER_TESTER.get())).build());
    public static java.util.List<Item> honeyLiquidItems() {
        return liquidItems().stream().filter(it -> ZGPlanetApiary.FAMILIES.values().stream()
                .anyMatch(family -> family.bucket.get() == it)).toList();
    }
    public static java.util.List<Item> planetaryLiquidItems() {
        var honeys = new HashSet<>(honeyLiquidItems());
        return liquidItems().stream().filter(it -> !honeys.contains(it)).toList();
    }
    public static java.util.List<Item> liquidItems() {
        return BuiltInRegistries.ITEM.stream().filter(it -> it instanceof net.minecraft.world.item.BucketItem
                && !(it instanceof net.minecraft.world.item.MobBucketItem)
                && BuiltInRegistries.ITEM.getKey(it).getNamespace().equals(ZeroGTweaks.MODID))
                .sorted(java.util.Comparator.comparing(it -> BuiltInRegistries.ITEM.getKey(it).getPath())).toList();
    }

    private static DeferredHolder<CreativeModeTab, CreativeModeTab> tab(String name, String icon, String[] ids, ResourceLocation after, boolean catchAll) {
        return TABS.register(name, () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup." + ZeroGTweaks.MODID + "." + name))
                .icon(() -> new ItemStack(item(icon)))
                .withTabsBefore(after)
                .displayItems((params, out) -> {
                    String[] visibleIds=name.equals("spawn_eggs")?java.util.stream.Stream.concat(java.util.Arrays.stream(ids),
                            ZGPlanetVillagers.TYPES.keySet().stream().map(id->id+"_spawn_egg")).distinct().sorted().toArray(String[]::new):ids;
                    for (String id : visibleIds) {
                        Item it = item(id);
                        if (it != Items.AIR && (!(it instanceof net.minecraft.world.item.BucketItem) || it instanceof net.minecraft.world.item.MobBucketItem)) out.accept(it);
                    }
                    if (catchAll) {
                        Set<String> listed = new HashSet<>(HIDDEN);
                        listed.add("weather_tester");
                        listed.add("concord_codex");
                        listed.add("recall_anchor");listed.add("group_anchor");
                        for(var tier:net.zerog.tweaks.transport.TransportTier.ALL)
                            for(String suffix:new String[]{"energy_conduit","fluid_pipe","item_tube","energy_cell"})listed.add(tier.name()+"_"+suffix);
                        listed.addAll(java.util.List.of("item_port","fluid_port","energy_port","null_link","flux_wrench","item_filter_card","fluid_filter_card","null_frequency_card"));
                        ZGPlanetAquatic.FAMILIES.keySet().forEach(theme->listed.add(theme+"_kelp"));
                        listed.addAll(ZGPlanetBotany.PLANTS.keySet());listed.addAll(ZGPlanetBotany.BUDS.keySet());
                        listed.addAll(ZGAlienVines.VINES.keySet());
                        ZGGasVents.AMBIENT_VENTS.keySet().forEach(id->listed.add(id+"_ambient_vent"));
                        ZGAlienVines.FRUITS.keySet().forEach(id->listed.add(id+"_vine_fruit"));
                        listed.add("star_glass_blue");listed.add("star_glass_teal");
                        ZGPlanetCrops.CROPS.keySet().forEach(id -> listed.add(id+"_crop"));
                        listed.addAll(ZGPlanetMaterials.BLOCK_ITEMS.keySet());
                        ZGPlanetCrops.PLANET_CROPS.values().forEach(id -> { listed.add(id); listed.add(id+"_seeds"); });
                        listed.add("rust_tuber_seeds");
                        ZGPlanetVillagers.TYPES.keySet().forEach(id->listed.add(id+"_spawn_egg"));
                        ZGAlienAgriculture.HOMES.keySet().forEach(id->{listed.add(id);listed.add(id+"_seeds");listed.add(id+"_slice");});
                        ZGPlanetCaveVariants.FAMILIES.keySet().forEach(id->{listed.add(id+"_cave_berry");listed.add(id+"_pointed_dripstone");listed.add(id+"_dripstone_block");});
                        ZGDimensionTerrain.FLORA.keySet().stream().filter(id -> id.endsWith("_tall_blossom")).forEach(listed::add);
                        for (String[] list : ZGCreativeTabContents.ALL) listed.addAll(java.util.Arrays.asList(list));
                        for (Item it : BuiltInRegistries.ITEM) {
                            ResourceLocation key = BuiltInRegistries.ITEM.getKey(it);
                            if (key.getNamespace().equals(ZeroGTweaks.MODID) && !listed.contains(key.getPath()) && (!(it instanceof net.minecraft.world.item.BucketItem) || it instanceof net.minecraft.world.item.MobBucketItem)) out.accept(it);
                        }
                    }
                    if (name.equals("liquids")) planetaryLiquidItems().forEach(out::accept);
                    if (name.equals("tools_and_utilities")) out.accept(ItemInit.CONCORD_CODEX.get());
                    if (name.equals("honey_liquids")) honeyLiquidItems().forEach(out::accept);
                    if (name.equals("building_blocks")) {
                        out.accept(item("star_glass_blue"));out.accept(item("star_glass_teal"));
                    }
                    if (name.equals("building_blocks") || name.equals("natural_blocks")) {
                        ZGPlanetMaterials.BLOCK_ITEMS.forEach((id, block) -> {
                            if (id.endsWith("_ore") == name.equals("natural_blocks")) out.accept(block.get());
                        });
                    }
                    if (name.equals("food_and_drinks")) ZGPlanetCrops.PLANET_CROPS.values().stream().sorted().forEach(id -> out.accept(item(id)));
                    if(name.equals("functional_blocks")) {
                        for(var tier:net.zerog.tweaks.transport.TransportTier.ALL)
                            for(String suffix:new String[]{"energy_conduit","fluid_pipe","item_tube","energy_cell"})out.accept(item(tier.name()+"_"+suffix));
                        for(String id:new String[]{"item_port","fluid_port","energy_port","null_link"})out.accept(item(id));
                    }
                    if(name.equals("tools_and_utilities"))
                        for(String id:new String[]{"flux_wrench","item_filter_card","fluid_filter_card","null_frequency_card","recall_anchor","group_anchor"})out.accept(item(id));
                    if(name.equals("food_and_drinks")) {
                        ZGPlanetBotany.BUDS.keySet().forEach(id->out.accept(item(id)));
                        ZGAlienVines.FRUITS.values().forEach(fruit->out.accept(fruit.get()));
                        ZGAlienAgriculture.HOMES.keySet().forEach(id->out.accept(item(ZGAlienAgriculture.GOURDS.containsKey(id)?id+"_slice":id)));
                        ZGPlanetCaveVariants.FAMILIES.keySet().forEach(id->out.accept(item(id+"_cave_berry")));
                    }
                    if (name.equals("natural_blocks")) {
                        ZGPlanetAquatic.FAMILIES.values().forEach(family->out.accept(item(net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(family.head().get()).getPath())));
                        ZGPlanetBotany.PLANTS.values().forEach(plant->out.accept(plant.get()));
                        ZGPlanetBotany.BUDS.keySet().forEach(id->out.accept(item(id)));
                        ZGAlienVines.VINES.values().forEach(vine->out.accept(vine.get()));
                        ZGGasVents.AMBIENT_VENTS.values().forEach(vent->out.accept(vent.get()));
                        ZGAlienAgriculture.HOMES.keySet().forEach(id->out.accept(item(id+"_seeds")));
                        ZGAlienAgriculture.GOURDS.values().forEach(block->out.accept(block.get()));
                        ZGPlanetCaveVariants.FAMILIES.forEach((id,family)->{out.accept(family.point().get());out.accept(family.rock().get());});
                        ZGPlanetCrops.PLANET_CROPS.values().stream().sorted().forEach(id -> out.accept(item(id+"_seeds")));
                        out.accept(ItemInit.RUST_TUBER_SEEDS.get());
                        ZGDimensionTerrain.FLORA.forEach((id, block) -> { if(id.endsWith("_tall_blossom")) out.accept(block.get()); });
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
