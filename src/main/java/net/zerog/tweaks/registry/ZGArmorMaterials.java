package net.zerog.tweaks.registry;

import java.util.List;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.Holder;
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

    public record Profile(DeferredHolder<ArmorMaterial, ArmorMaterial> material, int durabilityFactor) {}

    public static final Profile NULLIFITE = register("nullifite", ArmorMaterials.DIAMOND, 33, 2.0F, 0.00F, () -> ItemInit.NULLIFITE_INGOT.get());
    public static final Profile OLYMPIUM = register("olympium", ArmorMaterials.DIAMOND, 35, 2.5F, 0.05F, () -> ItemInit.OLYMPIUM_INGOT.get());
    public static final Profile CERULITE = register("cerulite", ArmorMaterials.NETHERITE, 37, 3.0F, 0.10F, () -> ItemInit.CERULITE.get());
    public static final Profile SKARNITE = register("skarnite", ArmorMaterials.NETHERITE, 40, 4.0F, 0.10F, () -> ItemInit.SKARNITE.get());
    public static final Profile EIDOLITE = register("eidolite", ArmorMaterials.NETHERITE, 40, 4.0F, 0.10F, () -> ItemInit.EIDOLITE.get());
    public static final Profile SOLVANITE = register("solvanite", ArmorMaterials.NETHERITE, 45, 5.0F, 0.15F, () -> ItemInit.SOLVANITE.get());
    public static final Profile FERROX = register("ferrox", ArmorMaterials.IRON, 18, 0.0F, 0.00F, () -> ItemInit.FERROX_INGOT.get());
    public static final Profile MOONSTEEL = register("moonsteel", ArmorMaterials.IRON, 25, 1.0F, 0.00F, () -> ItemInit.MOONSTEEL_INGOT.get());
    public static final Profile COBALTIUM = register("cobaltium", ArmorMaterials.DIAMOND, 28, 2.0F, 0.00F, () -> ItemInit.COBALTIUM_INGOT.get());
    public static final Profile CYRRIUM = register("cyrrium", ArmorMaterials.DIAMOND, 40, 2.0F, 0.00F, () -> ItemInit.CYRRIUM_INGOT.get());
    public static final Profile AURELION = register("aurelion", ArmorMaterials.GOLD, 12, 0.0F, 0.00F, () -> ItemInit.AURELION_INGOT.get());
    public static final Profile RUSKITE = register("ruskite", ArmorMaterials.DIAMOND, 35, 2.5F, 0.00F, () -> ItemInit.RUSKITE_INGOT.get());
    public static final Profile TECTIUM = register("tectium", ArmorMaterials.NETHERITE, 37, 3.0F, 0.10F, () -> ItemInit.TECTIUM_INGOT.get());
    public static final Profile PYRIUM = register("pyrium", ArmorMaterials.GOLD, 12, 0.0F, 0.00F, () -> ItemInit.PYRIUM_INGOT.get());
    public static final Profile SALVIUM = register("salvium", ArmorMaterials.NETHERITE, 37, 3.0F, 0.10F, () -> ItemInit.SALVIUM_INGOT.get());
    public static final Profile WRAITHSTEEL = register("wraithsteel", ArmorMaterials.NETHERITE, 40, 4.0F, 0.10F, () -> ItemInit.WRAITHSTEEL_INGOT.get());
    public static final Profile PALLADINE = register("palladine", ArmorMaterials.GOLD, 12, 0.0F, 0.00F, () -> ItemInit.PALLADINE_INGOT.get());
    public static final Profile PHOTIUM = register("photium", ArmorMaterials.NETHERITE, 37, 3.0F, 0.10F, () -> ItemInit.PHOTIUM_INGOT.get());
    public static final Profile ASTRIUM = register("astrium", ArmorMaterials.NETHERITE, 40, 4.0F, 0.10F, () -> ItemInit.ASTRIUM_INGOT.get());
    public static final Profile RADIANTINE = register("radiantine", ArmorMaterials.GOLD, 12, 0.0F, 0.00F, () -> ItemInit.RADIANTINE_INGOT.get());

    private static Profile register(String name, Holder<ArmorMaterial> baseline, int durability,
                                    float toughness, float knockback, Supplier<Item> repair) {
        var holder = MATERIALS.register(name, () -> {
            var vanilla = baseline.value();
            return new ArmorMaterial(Map.copyOf(vanilla.defense()), vanilla.enchantmentValue(),
                    vanilla.equipSound(), () -> Ingredient.of(repair.get()),
                    List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(
                            ZeroGTweaks.MODID, name))), toughness, knockback);
        });
        var profile = new Profile(holder, durability);
        PROFILES.put(name, profile);
        return profile;
    }

    public static Map<String, Profile> profiles() { return Map.copyOf(PROFILES); }

    public static void register(IEventBus bus) { MATERIALS.register(bus); }

    private ZGArmorMaterials() {}
}
