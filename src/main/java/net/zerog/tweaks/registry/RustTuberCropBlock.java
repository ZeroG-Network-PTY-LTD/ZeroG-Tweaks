package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;

/** rust_tuber_crop: drops Rust Tuber. */
public class RustTuberCropBlock extends ZGCropBlock {
    public RustTuberCropBlock(Properties props) { super(props); }
    @Override public ItemStack produce() { return new ItemStack(ItemInit.RUST_TUBER.get()); }
}
