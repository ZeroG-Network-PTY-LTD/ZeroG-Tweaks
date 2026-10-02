package net.zerog.tweaks.registry;

import java.util.EnumMap;
import java.util.List;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ArmorMaterials;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/** Vanilla-based first-pass balance; material-specific perks are a separate feature. */
public final class ZGArmorMaterials {
    private static final DeferredRegister<ArmorMaterial> MATERIALS =
            DeferredRegister.create(Registries.ARMOR_MATERIAL, ZeroGTweaks.MODID);
    private static final Map<String, Profile> PROFILES = new LinkedHashMap<>();
    private static final int DIAMOND_ARMOR_DURABILITY = 33;

    public record Profile(DeferredHolder<ArmorMaterial, ArmorMaterial> material, int durabilityFactor) {}

    public static final Profile NULLIFITE = register("nullifite", 4, 8, 6, 3, 3.5F, 0.11F, 1.4F, false, () -> ItemInit.NULLIFITE_INGOT.get());
    public static final Profile OLYMPIUM = register("olympium", 4, 8, 6, 4, 5.0F, 0.14F, 1.7F, false, () -> ItemInit.OLYMPIUM_INGOT.get());
    public static final Profile CERULITE = register("cerulite", 4, 9, 7, 4, 6.5F, 0.17F, 2.0F, false, () -> ItemInit.CERULITE.get());
    public static final Profile SKARNITE = register("skarnite", 5, 9, 7, 4, 8.0F, 0.20F, 2.3F, false, () -> ItemInit.SKARNITE.get());
    public static final Profile EIDOLITE = register("eidolite", 5, 10, 7, 5, 9.5F, 0.23F, 2.6F, false, () -> ItemInit.EIDOLITE.get());
    public static final Profile SOLVANITE = register("solvanite", 6, 10, 8, 6, 11.0F, 0.26F, 2.9F, false, () -> ItemInit.SOLVANITE.get());
    public static final Profile FERROX = register("ferrox", 4, 8, 6, 3, 4.0F, 0.12F, 1.5F, false, () -> ItemInit.FERROX_INGOT.get());
    public static final Profile MOONSTEEL = register("moonsteel", 4, 8, 6, 4, 4.5F, 0.13F, 1.6F, false, () -> ItemInit.MOONSTEEL_INGOT.get());
    public static final Profile COBALTIUM = register("cobaltium", 4, 9, 6, 4, 5.5F, 0.15F, 1.8F, false, () -> ItemInit.COBALTIUM_INGOT.get());
    public static final Profile CYRRIUM = register("cyrrium", 4, 9, 6, 4, 6.0F, 0.16F, 1.9F, false, () -> ItemInit.CYRRIUM_INGOT.get());
    public static final Profile AURELION = register("aurelion", 4, 8, 6, 4, 4.5F, 0.10F, 1.35F, true, () -> ItemInit.AURELION_INGOT.get());
    public static final Profile RUSKITE = register("ruskite", 4, 9, 7, 4, 7.0F, 0.18F, 2.1F, false, () -> ItemInit.RUSKITE_INGOT.get());
    public static final Profile TECTIUM = register("tectium", 5, 9, 7, 4, 7.5F, 0.19F, 2.2F, false, () -> ItemInit.TECTIUM_INGOT.get());
    public static final Profile PYRIUM = register("pyrium", 4, 9, 6, 4, 6.0F, 0.10F, 1.6F, true, () -> ItemInit.PYRIUM_INGOT.get());
    public static final Profile SALVIUM = register("salvium", 5, 9, 7, 5, 8.5F, 0.21F, 2.4F, false, () -> ItemInit.SALVIUM_INGOT.get());
    public static final Profile WRAITHSTEEL = register("wraithsteel", 5, 9, 7, 5, 9.0F, 0.22F, 2.5F, false, () -> ItemInit.WRAITHSTEEL_INGOT.get());
    public static final Profile PALLADINE = register("palladine", 5, 9, 7, 4, 7.5F, 0.10F, 1.8F, true, () -> ItemInit.PALLADINE_INGOT.get());
    public static final Profile PHOTIUM = register("photium", 5, 10, 7, 5, 10.0F, 0.24F, 2.7F, false, () -> ItemInit.PHOTIUM_INGOT.get());
    public static final Profile ASTRIUM = register("astrium", 5, 10, 8, 5, 10.5F, 0.25F, 2.8F, false, () -> ItemInit.ASTRIUM_INGOT.get());
    public static final Profile RADIANTINE = register("radiantine", 5, 9, 7, 5, 9.0F, 0.10F, 2.05F, true, () -> ItemInit.RADIANTINE_INGOT.get());

    /**
     * Design doc v1.3 gear stats: armor points per piece (helmet, chestplate, leggings, boots), toughness, knockback
     * resistance and durability as a multiple of diamond armor (factor 33). Precious (gold-style) sets get
     * enchantability 25 and the gold equip sound; the rest use netherite's enchantability and sound.
     */
    private static Profile register(String name, int helmet, int chestplate, int leggings, int boots, float toughness,
                                    float knockback, float durabilityVsDiamond, boolean precious, Supplier<Item> repair) {
        var feel = (precious ? ArmorMaterials.GOLD : ArmorMaterials.NETHERITE).value();
        var defense = new EnumMap<ArmorItem.Type, Integer>(ArmorItem.Type.class);
        defense.put(ArmorItem.Type.HELMET, helmet);
        defense.put(ArmorItem.Type.CHESTPLATE, chestplate);
        defense.put(ArmorItem.Type.LEGGINGS, leggings);
        defense.put(ArmorItem.Type.BOOTS, boots);
        defense.put(ArmorItem.Type.BODY, chestplate);
        var holder = MATERIALS.register(name, () -> new ArmorMaterial(Map.copyOf(defense), precious ? 25 : feel.enchantmentValue(),
                feel.equipSound(), () -> Ingredient.of(repair.get()),
                List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, name))),
                toughness, knockback));
        var profile = new Profile(holder, Math.round(DIAMOND_ARMOR_DURABILITY * durabilityVsDiamond));
        PROFILES.put(name, profile);
        return profile;
    }

    public static Map<String, Profile> profiles() { return Map.copyOf(PROFILES); }

    public static void register(IEventBus bus) { MATERIALS.register(bus); }

    private ZGArmorMaterials() {}
}
