package net.zerog.tweaks.registry;

import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.item.ItemStack;

/** Base crop: age 0..3 (shipped blockstates). Subclasses bind their produce item. */
public abstract class ZGCropBlock extends CropBlock {
    public static final IntegerProperty AGE = IntegerProperty.create("age", 0, 3);
    public ZGCropBlock(Properties props) { super(props); }
    @Override public int getMaxAge() { return 3; }
    @Override public IntegerProperty getAgeProperty() { return AGE; }
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) { b.add(AGE); }
    public abstract ItemStack produce();
}