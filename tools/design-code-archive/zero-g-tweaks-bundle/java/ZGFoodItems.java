package net.zerog.tweaks.item;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
import net.minecraft.world.item.Item;

/** Small item classes for foods with behavior beyond FoodProperties. */
public final class ZGFoodItems {
    private ZGFoodItems() {}

    /** Drinks (Shardwood Syrup, Frostfern Tea, Frost Milk) use the drink animation. */
    public static class DrinkItem extends Item {
        public DrinkItem(Properties props) { super(props); }
        @Override public UseAnim getUseAnimation(ItemStack stack) { return UseAnim.DRINK; }
    }

    /** Frost Milk: clears all effects like milk. */
    public static class FrostMilkItem extends DrinkItem {
        public FrostMilkItem(Properties props) { super(props); }
        @Override public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
            if (!level.isClientSide) entity.removeAllEffects();
            return super.finishUsingItem(stack, level, entity);
        }
    }

    /** Raw Scorch Tail: sets the eater on fire for 2 seconds. */
    public static class ScorchTailItem extends Item {
        public ScorchTailItem(Properties props) { super(props); }
        @Override public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
            if (!level.isClientSide) entity.igniteForSeconds(2.0f);
            return super.finishUsingItem(stack, level, entity);
        }
    }
}
