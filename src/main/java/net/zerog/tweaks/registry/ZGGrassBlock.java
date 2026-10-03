package net.zerog.tweaks.registry;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.GrassBlock;
import net.minecraft.world.level.block.SnowLayerBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.lighting.LightEngine;
import net.neoforged.neoforge.common.ItemAbilities;
import net.neoforged.neoforge.common.ItemAbility;

/** Soil-family grass, preserving the planet soil when suffocated or hoed. */
public final class ZGGrassBlock extends GrassBlock {
    private final Supplier<? extends Block> soil, farmland, shortGrass;
    public ZGGrassBlock(Properties props, Supplier<? extends Block> soil, Supplier<? extends Block> farmland,
            Supplier<? extends Block> shortGrass) { super(props); this.soil = soil; this.farmland = farmland; this.shortGrass = shortGrass; }
    private boolean viable(BlockState state, ServerLevel level, BlockPos pos) {
        var above = pos.above(); var cover = level.getBlockState(above);
        if (cover.is(Blocks.SNOW) && cover.getValue(SnowLayerBlock.LAYERS) == 1) return true;
        if (cover.getFluidState().getAmount() == 8) return false;
        return LightEngine.getLightBlockInto(level, state, pos, cover, above, Direction.UP, cover.getLightBlock(level, above)) < level.getMaxLightLevel();
    }
    @Override protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (!level.isAreaLoaded(pos, 3)) return;
        if (!viable(state, level, pos)) { level.setBlockAndUpdate(pos, soil.get().defaultBlockState()); return; }
        if (level.getMaxLocalRawBrightness(pos.above()) < 9) return;
        for (int i = 0; i < 4; i++) {
            var next = pos.offset(random.nextInt(3) - 1, random.nextInt(5) - 3, random.nextInt(3) - 1);
            if (level.getBlockState(next).is(soil.get()) && viable(defaultBlockState(), level, next)) {
                level.setBlockAndUpdate(next, defaultBlockState().setValue(SNOWY, level.getBlockState(next.above()).is(Blocks.SNOW)));
            }
        }
    }
    @Override public BlockState getToolModifiedState(BlockState state, UseOnContext context, ItemAbility ability, boolean simulate) {
        if (ability == ItemAbilities.HOE_TILL && context.getItemInHand().canPerformAction(ability)
                && context.getClickedFace() != Direction.DOWN && context.getLevel().getBlockState(context.getClickedPos().above()).isAir()) {
            return farmland.get().defaultBlockState();
        }
        return super.getToolModifiedState(state, context, ability, simulate);
    }
    @Override public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state) {
        for (int i = 0; i < 64; i++) {
            var plantPos = pos.offset(random.nextInt(7) - 3, 1, random.nextInt(7) - 3);
            var plant = shortGrass.get().defaultBlockState();
            if (level.getBlockState(plantPos.below()).is(this) && level.isEmptyBlock(plantPos) && plant.canSurvive(level, plantPos)) {
                level.setBlockAndUpdate(plantPos, plant);
            }
        }
    }
}
