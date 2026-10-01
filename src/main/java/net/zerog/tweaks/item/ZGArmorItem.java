package net.zerog.tweaks.item;

import java.util.List;
import java.util.Set;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** Only advertises abilities actually implemented in this local gameplay pass. */
public final class ZGArmorItem extends ArmorItem {
    private static final Set<String> IMPLEMENTED = Set.of("nullifite", "moonsteel", "ruskite",
            "skarnite", "eidolite", "cobaltium", "ferrox", "astrium");
    private final String materialName;

    public ZGArmorItem(String materialName, Holder<ArmorMaterial> material, Type type, Properties properties) {
        super(material, type, properties);
        this.materialName = materialName;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltip, flag);
        if (IMPLEMENTED.contains(materialName)) {
            tooltip.add(Component.translatable("tooltip.zerog_tweaks.armor_set." + materialName)
                    .withStyle(ChatFormatting.AQUA));
            tooltip.add(Component.translatable("tooltip.zerog_tweaks.full_set_required")
                    .withStyle(ChatFormatting.GRAY));
        }
    }
}
