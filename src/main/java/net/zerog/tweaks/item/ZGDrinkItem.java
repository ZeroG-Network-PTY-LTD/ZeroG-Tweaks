package net.zerog.tweaks.item;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;

/** Edible bottled drinks retain their food-defined container after drinking. */
public final class ZGDrinkItem extends Item {
    public ZGDrinkItem(Properties properties) { super(properties); }
    @Override public UseAnim getUseAnimation(ItemStack stack) { return UseAnim.DRINK; }
}
