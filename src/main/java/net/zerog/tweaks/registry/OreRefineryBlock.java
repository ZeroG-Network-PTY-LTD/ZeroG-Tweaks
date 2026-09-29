package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.items.ItemStackHandler;

import com.mojang.serialization.MapCodec;

/**
 * ZeroG ore refinery: doubles ore output; triples with upgrades (design doc).
 * Cross-mod link: the aeroapiary bee industry's stardust feeds the aresite
 * catalyst recipe — recipes resolve at runtime so aeroapiary stays OPTIONAL:
 * without the Bees jar the refinery still does its vanilla-side work.
 */
public class OreRefineryBlock extends BaseEntityBlock {

    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;
    private final MapCodec<OreRefineryBlock> codec;

    public OreRefineryBlock(Properties props) {
        super(props);
        this.codec = simpleCodec(OreRefineryBlock::new);
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
    }

    @Override
    public MapCodec<? extends OreRefineryBlock> codec() {
        return this.codec;
    }

    @Override
    protected void createBlockStateDefinition(
            StateDefinition.Builder<net.minecraft.world.level.block.Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        return this.defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
    }

    @SuppressWarnings("unchecked")
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(
            net.minecraft.world.level.Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide) {
            return null;
        }
        return (BlockEntityTicker<T>) (BlockEntityTicker<OreRefineryBlockEntity>)
                (lvl, pos, st, be) -> OreRefineryBlockEntity.tick(lvl, pos, st, be);
    }

    @Override
    protected RenderShape getRenderShape(BlockState state) {
        return RenderShape.MODEL;
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        BlockEntityType<OreRefineryBlockEntity> beType = BlockEntityInit.ORE_REFINERY.get();
        if (!beType.isValid(state)) {
            return null;
        }
        return new OreRefineryBlockEntity(beType, pos, state);
    }

    protected void onRemove(BlockState state, net.minecraft.world.level.Level level, BlockPos pos,
            BlockState newState, boolean movedByPiston) {
        if (!state.is(newState.getBlock()) && level.getBlockEntity(pos) instanceof OreRefineryBlockEntity be) {
            ItemStackHandler inv = be.inventory();
            for (int i = 0; i < inv.getSlots(); i++) {
                if (!inv.getStackInSlot(i).isEmpty()) {
                    net.minecraft.world.Containers.dropItemStack(level,
                            pos.getX(), pos.getY(), pos.getZ(), inv.getStackInSlot(i));
                }
            }
        }
        super.onRemove(state, level, pos, newState, movedByPiston);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, net.minecraft.world.level.Level level,
            BlockPos pos, Player player, BlockHitResult hit) {
        if (level.getBlockEntity(pos) instanceof OreRefineryBlockEntity) {
            if (!level.isClientSide) {
                player.openMenu(OreRefineryMenuProvider.of(pos), pos);
            }
            return InteractionResult.SUCCESS;
        }
        return InteractionResult.FAIL;
    }
}