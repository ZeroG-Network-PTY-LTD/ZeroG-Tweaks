package net.zerog.tweaks.arena;

import javax.annotation.Nullable;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.zerog.tweaks.registry.BlockEntityInit;
import net.zerog.tweaks.registry.ItemInit;

/**
 * Concord Prism: the altar at the centre of the Prism Sentinel arena (briefs/prism_sentinel_arena.md, section 5).
 * Unbreakable in survival and drops nothing. IDLE -> right-click starts the test (ACTIVE) -> DEFEATED (glowing, inert);
 * a DEFEATED prism re-arms with a Sentinel Prism for a rematch. The fight itself runs in {@link ConcordPrismBlockEntity}.
 */
public class ConcordPrismBlock extends Block implements EntityBlock {
    public enum State implements StringRepresentable {
        IDLE("idle"), ACTIVE("active"), DEFEATED("defeated");

        private final String name;
        State(String name) { this.name = name; }
        @Override public String getSerializedName() { return name; }
    }

    public static final EnumProperty<State> STATE = EnumProperty.create("state", State.class);

    public ConcordPrismBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(STATE, State.IDLE));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(STATE);
    }

    /** Light level per state, for Properties.lightLevel. */
    public static int light(BlockState state) {
        return switch (state.getValue(STATE)) {
            case IDLE -> 10;
            case ACTIVE -> 13;
            case DEFEATED -> 15;
        };
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                              InteractionHand hand, BlockHitResult hit) {
        if (!stack.is(ItemInit.SENTINEL_PRISM.get()) || state.getValue(STATE) != State.DEFEATED) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        if (level instanceof ServerLevel server && level.getBlockEntity(pos) instanceof ConcordPrismBlockEntity prism
                && prism.rearm(server)) {
            stack.consume(1, player);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (level instanceof ServerLevel server && level.getBlockEntity(pos) instanceof ConcordPrismBlockEntity prism) {
            switch (state.getValue(STATE)) {
                case IDLE -> prism.start(server);
                case DEFEATED -> player.displayClientMessage(
                        Component.translatable("chat.zerog_tweaks.prism_sentinel.needs_prism"), true);
                case ACTIVE -> {}
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Nullable
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new ConcordPrismBlockEntity(pos, state);
    }

    @Nullable
    @Override
    @SuppressWarnings("unchecked")
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide || type != BlockEntityInit.CONCORD_PRISM.get()) return null;
        return (BlockEntityTicker<T>) (BlockEntityTicker<ConcordPrismBlockEntity>) ConcordPrismBlockEntity::serverTick;
    }
}
