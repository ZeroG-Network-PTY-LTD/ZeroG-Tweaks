package net.zerog.tweaks.storage;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.Containers;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public abstract class WoodStorageBlock extends BaseEntityBlock {
    protected WoodStorageBlock(Properties p) {
        super(p);
        registerDefaultState(stateDefinition.any().setValue(facingProperty(), Direction.NORTH).setValue(BlockStateProperties.OPEN, false));
    }
    protected abstract DirectionProperty facingProperty();
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) { b.add(facingProperty(), BlockStateProperties.OPEN); }
    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(facingProperty(), this instanceof Barrel ? context.getNearestLookingDirection().getOpposite() : context.getHorizontalDirection().getOpposite());
    }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) { return new WoodStorageBlockEntity(pos, state); }
    @Override protected RenderShape getRenderShape(BlockState state) { return RenderShape.MODEL; }
    @Override protected BlockState rotate(BlockState state, Rotation rotation) { return state.setValue(facingProperty(), rotation.rotate(state.getValue(facingProperty()))); }
    @Override protected BlockState mirror(BlockState state, Mirror mirror) { return rotate(state, mirror.getRotation(state.getValue(facingProperty()))); }
    @Override protected boolean hasAnalogOutputSignal(BlockState state) { return true; }
    @Override protected int getAnalogOutputSignal(BlockState state, Level level, BlockPos pos) { return AbstractContainerMenu.getRedstoneSignalFromBlockEntity(level.getBlockEntity(pos)); }
    @Override protected ItemInteractionResult useItemOn(ItemStack held, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        if (held.is(WoodStorageRegistry.EXPANSION.get()) && level.getBlockEntity(pos) instanceof WoodStorageBlockEntity be) {
            if (level.isClientSide) return ItemInteractionResult.SUCCESS;
            if (be.expand()) { if (!player.getAbilities().instabuild) held.shrink(1); return ItemInteractionResult.CONSUME; }
            player.displayClientMessage(net.minecraft.network.chat.Component.translatable("message.zerog_tweaks.storage_already_expanded"), true);
            return ItemInteractionResult.CONSUME;
        }
        return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
    }
    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide && level.getBlockEntity(pos) instanceof WoodStorageBlockEntity be) {
            if (this instanceof Chest && level.getBlockState(pos.above()).isRedstoneConductor(level, pos.above())) return InteractionResult.CONSUME;
            player.openMenu(be);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
    @Override protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (level.getBlockEntity(pos) instanceof WoodStorageBlockEntity be) be.recheckOpen();
    }
    @Override protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState next, boolean moving) {
        if (!level.isClientSide && !state.is(next.getBlock()) && level.getBlockEntity(pos) instanceof WoodStorageBlockEntity be) {
            Containers.dropContents(level, pos, be);
            if (be.expanded()) Block.popResource(level, pos, new ItemStack(WoodStorageRegistry.EXPANSION.get()));
            level.updateNeighbourForOutputSignal(pos, this);
        }
        super.onRemove(state, level, pos, next, moving);
    }
    public static final class Chest extends WoodStorageBlock {
        public static final MapCodec<Chest> CODEC = simpleCodec(Chest::new);
        public Chest(Properties p) { super(p); }
        @Override public MapCodec<Chest> codec() { return CODEC; }
        @Override protected DirectionProperty facingProperty() { return BlockStateProperties.HORIZONTAL_FACING; }
        @Override protected VoxelShape getShape(BlockState state, net.minecraft.world.level.BlockGetter level, BlockPos pos, CollisionContext context) { return Block.box(1, 0, 1, 15, 14, 15); }
    }
    public static final class Barrel extends WoodStorageBlock {
        public static final MapCodec<Barrel> CODEC = simpleCodec(Barrel::new);
        public Barrel(Properties p) { super(p); }
        @Override public MapCodec<Barrel> codec() { return CODEC; }
        @Override protected DirectionProperty facingProperty() { return BlockStateProperties.FACING; }
    }
}
