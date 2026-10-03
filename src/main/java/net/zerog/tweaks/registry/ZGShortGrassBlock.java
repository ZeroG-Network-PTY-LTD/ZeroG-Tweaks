package net.zerog.tweaks.registry;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.DoublePlantBlock;
import net.minecraft.world.level.block.TallGrassBlock;
import net.minecraft.world.level.block.state.BlockState;

public final class ZGShortGrassBlock extends TallGrassBlock {
    private final Supplier<DoublePlantBlock> tall;
    public ZGShortGrassBlock(Properties props, Supplier<DoublePlantBlock> tall) { super(props); this.tall = tall; }
    @Override public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state) {
        var plant = tall.get();
        if (plant.defaultBlockState().canSurvive(level, pos) && level.isEmptyBlock(pos.above())) {
            DoublePlantBlock.placeAt(level, plant.defaultBlockState(), pos, 2);
        }
    }
}
