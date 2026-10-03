package net.zerog.tweaks.registry;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.AmethystBlock;
import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BuddingAmethystBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluids;

/** Vanilla budding-amethyst growth, with this family's four crystal stages. */
public class ZGBuddingCrystalBlock extends AmethystBlock {
    private final Supplier<Block[]> stages;

    public ZGBuddingCrystalBlock(Properties properties, Supplier<Block[]> stages) {
        super(properties.randomTicks());
        this.stages = stages;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (random.nextInt(BuddingAmethystBlock.GROWTH_CHANCE) != 0) return;
        Direction direction = Direction.values()[random.nextInt(Direction.values().length)];
        BlockPos target = pos.relative(direction);
        BlockState current = level.getBlockState(target);
        Block[] family = stages.get();
        Block next = null;
        if (BuddingAmethystBlock.canClusterGrowAtState(current)) next = family[0];
        else {
            for (int i = 0; i < family.length - 1; i++) {
                if (current.is(family[i]) && current.getValue(AmethystClusterBlock.FACING) == direction) {
                    next = family[i + 1];
                    break;
                }
            }
        }
        if (next != null) level.setBlockAndUpdate(target, next.defaultBlockState()
                .setValue(AmethystClusterBlock.FACING, direction)
                .setValue(AmethystClusterBlock.WATERLOGGED, current.getFluidState().getType() == Fluids.WATER));
    }
}
