package net.zerog.tweaks.registry;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.CaveVines;
import net.minecraft.world.level.block.GrowingPlantHeadBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Pyrevine (head) — ZeroG counterpart of vanilla {@code cave_vines}.
 *
 * Same behaviour as CaveVinesBlock: hangs from ceilings and grows downward,
 * 11% chance each new segment bears fruit (BERRIES=true, glows at light 14),
 * right-click picks a Pyrefruit, bone meal ripens it, shift-place / climbable.
 * Vanilla's class can't be reused because it hard-codes glow berries and
 * cave_vines_plant, so this mirrors it with our blocks/items.
 */
public class ZGCaveVinesBlock extends GrowingPlantHeadBlock implements BonemealableBlock {
    public static final MapCodec<ZGCaveVinesBlock> CODEC = simpleCodec(ZGCaveVinesBlock::new);

    public ZGCaveVinesBlock(BlockBehaviour.Properties props) {
        super(props, Direction.DOWN, CaveVines.SHAPE, false, 0.1);
        this.registerDefaultState(this.stateDefinition.any().setValue(AGE, 0).setValue(CaveVines.BERRIES, false));
    }

    @Override
    public MapCodec<ZGCaveVinesBlock> codec() {
        return CODEC;
    }

    @Override
    protected int getBlocksToGrowWhenBonemealed(RandomSource random) {
        return 1;
    }

    @Override
    protected boolean canGrowInto(BlockState state) {
        return state.isAir();
    }

    @Override
    protected Block getBodyBlock() {
        return BlockInit.PYREVINE_PLANT.get();
    }

    @Override
    protected BlockState updateBodyAfterConvertedFromHead(BlockState head, BlockState body) {
        return body.setValue(CaveVines.BERRIES, head.getValue(CaveVines.BERRIES));
    }

    @Override
    protected BlockState getGrowIntoState(BlockState state, RandomSource random) {
        return super.getGrowIntoState(state, random).setValue(CaveVines.BERRIES, random.nextFloat() < 0.11F);
    }

    @Override
    public ItemStack getCloneItemStack(LevelReader level, BlockPos pos, BlockState state) {
        return new ItemStack(ItemInit.PYREFRUIT.get());
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        return ZGCaveVines.use(player, state, level, pos);
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        super.createBlockStateDefinition(builder);
        builder.add(CaveVines.BERRIES);
    }

    @Override
    public boolean isValidBonemealTarget(LevelReader level, BlockPos pos, BlockState state) {
        return !state.getValue(CaveVines.BERRIES);
    }

    @Override
    public boolean isBonemealSuccess(Level level, RandomSource random, BlockPos pos, BlockState state) {
        return true;
    }

    @Override
    public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state) {
        level.setBlock(pos, state.setValue(CaveVines.BERRIES, true), 2);
    }
}
