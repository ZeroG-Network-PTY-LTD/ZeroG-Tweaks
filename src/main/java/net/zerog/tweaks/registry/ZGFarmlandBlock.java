package net.zerog.tweaks.registry;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.gameevent.GameEvent;
import net.neoforged.neoforge.common.CommonHooks;
import net.neoforged.neoforge.common.FarmlandWaterManager;

/** Vanilla farmland height/moisture/crops; reverts to the matching soil, never vanilla dirt. */
public final class ZGFarmlandBlock extends FarmBlock {
    private final Supplier<? extends Block> soil;
    public ZGFarmlandBlock(Properties properties, Supplier<? extends Block> soil) {
        super(properties);
        this.soil = soil;
    }
    private void revert(Entity entity, BlockState state, Level level, BlockPos pos) {
        BlockState dirt = pushEntitiesUp(state, soil.get().defaultBlockState(), level, pos);
        level.setBlockAndUpdate(pos, dirt);
        level.gameEvent(GameEvent.BLOCK_CHANGE, pos, GameEvent.Context.of(entity, dirt));
    }
    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().canSurvive(context.getLevel(), context.getClickedPos())
                ? defaultBlockState() : soil.get().defaultBlockState();
    }
    @Override
    protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (!state.canSurvive(level, pos)) revert(null, state, level, pos);
    }
    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        boolean hydrated = level.isRainingAt(pos.above()) || FarmlandWaterManager.hasBlockWaterTicket(level, pos);
        for (BlockPos water : BlockPos.betweenClosed(pos.offset(-4, 0, -4), pos.offset(4, 1, 4))) {
            if (state.canBeHydrated(level, pos, level.getFluidState(water), water)) {
                hydrated = true;
                break;
            }
        }
        int moisture = state.getValue(MOISTURE);
        if (hydrated && moisture < MAX_MOISTURE) level.setBlock(pos, state.setValue(MOISTURE, MAX_MOISTURE), 2);
        else if (!hydrated && moisture > 0) level.setBlock(pos, state.setValue(MOISTURE, moisture - 1), 2);
        else if (!hydrated && !level.getBlockState(pos.above()).is(BlockTags.MAINTAINS_FARMLAND)) revert(null, state, level, pos);
    }
    @Override
    public void fallOn(Level level, BlockState state, BlockPos pos, Entity entity, float distance) {
        if (!level.isClientSide && CommonHooks.onFarmlandTrample(level, pos, soil.get().defaultBlockState(), distance, entity)) {
            revert(entity, state, level, pos);
        }
        entity.causeFallDamage(distance, 1.0F, entity.damageSources().fall());
    }
}
