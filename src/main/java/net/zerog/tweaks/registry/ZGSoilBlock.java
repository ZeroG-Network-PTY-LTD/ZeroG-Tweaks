package net.zerog.tweaks.registry;

import java.util.function.Supplier;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.common.ItemAbilities;
import net.neoforged.neoforge.common.ItemAbility;

/** Planet dirt that hoes into its own farmland, without changing vanilla tool behavior. */
public final class ZGSoilBlock extends Block {
    private final Supplier<Block> farmland;
    public ZGSoilBlock(Properties properties, Supplier<Block> farmland) {
        super(properties);
        this.farmland = farmland;
    }
    @Override
    public BlockState getToolModifiedState(BlockState state, UseOnContext context, ItemAbility ability, boolean simulate) {
        if (ability == ItemAbilities.HOE_TILL && context.getItemInHand().canPerformAction(ability)
                && context.getClickedFace() != Direction.DOWN
                && context.getLevel().getBlockState(context.getClickedPos().above()).isAir()) {
            return farmland.get().defaultBlockState();
        }
        return super.getToolModifiedState(state, context, ability, simulate);
    }
}
