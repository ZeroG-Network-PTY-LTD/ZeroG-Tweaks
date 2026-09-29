package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Cinder Cap — vanilla {@code brown_mushroom}: small 6x6 hitbox, faint glow,
 * slowly spreads to nearby spots (max 5 in a 9x3x9 area), pottable.
 * Unlike vanilla it doesn't need darkness — it thrives on hot planet surfaces.
 */
public class ZGMushroomBlock extends ZGPlantBlock {
    protected static final VoxelShape SHAPE = Block.box(5.0, 0.0, 5.0, 11.0, 6.0, 11.0);

    public ZGMushroomBlock(BlockBehaviour.Properties props) {
        super(props);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return SHAPE;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (random.nextInt(25) != 0) return;
        int budget = 5;
        for (BlockPos p : BlockPos.betweenClosed(pos.offset(-4, -1, -4), pos.offset(4, 1, 4))) {
            if (level.getBlockState(p).is(this) && --budget <= 0) return;
        }
        BlockPos target = pos.offset(random.nextInt(3) - 1, random.nextInt(2) - random.nextInt(2), random.nextInt(3) - 1);
        for (int k = 0; k < 4; k++) {
            if (level.isEmptyBlock(target) && state.canSurvive(level, target)) pos = target;
            target = pos.offset(random.nextInt(3) - 1, random.nextInt(2) - random.nextInt(2), random.nextInt(3) - 1);
        }
        if (level.isEmptyBlock(target) && state.canSurvive(level, target)) {
            level.setBlock(target, state, 2);
        }
    }
}
