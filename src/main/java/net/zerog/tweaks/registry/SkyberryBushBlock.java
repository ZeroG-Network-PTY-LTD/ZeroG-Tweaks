package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.item.ItemStack;

/** skyberry_bush: berries by age. */
public class SkyberryBushBlock extends ZGCropBlock {
    public SkyberryBushBlock(Properties props) { super(props); }
    @Override public ItemStack produce() { return new ItemStack(ItemInit.SKYBERRIES.get()); }
}
