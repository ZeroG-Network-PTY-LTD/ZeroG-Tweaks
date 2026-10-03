package net.zerog.tweaks.arena;

import com.mojang.serialization.MapCodec;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.phys.BlockHitResult;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

/**
 * Concord Lock: sits where the Concord Prism will stand in the unbuilt Sentinel chamber of the Concord Vault. Each
 * Concord Key used on it builds the next stage of the chamber (templates concord_vault/chamber_stage_1..3: the lit
 * floor, then the dais and refractor pylons, then the stands and the crystal dome); the fourth key forms the Concord
 * Prism itself, which runs the fight. The lock faces the chamber's template south, so its facing gives the structure's
 * rotation; stage templates are placed around it with the same rotation (pivot = the lock's spot in the template).
 */
public class ConcordLockBlock extends HorizontalDirectionalBlock {
    public static final MapCodec<ConcordLockBlock> CODEC = simpleCodec(ConcordLockBlock::new);
    public static final int KEYS = 4;
    public static final IntegerProperty STAGE = IntegerProperty.create("stage", 0, KEYS - 1);
    /** The lock's (= the prism's) position inside the 67 x 40 x 67 chamber templates. */
    public static final BlockPos TEMPLATE_PIVOT = new BlockPos(33, 6, 33);

    public ConcordLockBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.SOUTH).setValue(STAGE, 0));
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() { return CODEC; }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, STAGE);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }

    /** The structure rotation that turned the template's south-facing lock to face this way. */
    public static Rotation rotationOf(Direction facing) {
        return switch (facing) {
            case WEST -> Rotation.CLOCKWISE_90;
            case NORTH -> Rotation.CLOCKWISE_180;
            case EAST -> Rotation.COUNTERCLOCKWISE_90;
            default -> Rotation.NONE;
        };
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                              InteractionHand hand, BlockHitResult hit) {
        if (!stack.is(ItemInit.CONCORD_VAULT_KEY.get())) return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        if (level instanceof ServerLevel server) {
            int next = state.getValue(STAGE) + 1;   // keys inserted after this one
            stack.consume(1, player);
            if (next < KEYS) {
                buildStage(server, pos, rotationOf(state.getValue(FACING)), next);
                server.setBlock(pos, state.setValue(STAGE, next), Block.UPDATE_ALL);
            } else {
                server.setBlock(pos, BlockInit.CONCORD_PRISM.get().defaultBlockState(), Block.UPDATE_ALL);
            }
            server.sendParticles(ParticleTypes.END_ROD, pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, 80, 6, 4, 6, 0.08);
            server.playSound(null, pos, next < KEYS ? SoundEvents.BEACON_POWER_SELECT : SoundEvents.BEACON_ACTIVATE,
                    SoundSource.BLOCKS, 4F, 0.6F + next * 0.2F);
            player.displayClientMessage(Component.translatable(next < KEYS ? "block.zerog_tweaks.concord_lock.stage"
                    : "block.zerog_tweaks.concord_lock.complete", next, KEYS).withStyle(ChatFormatting.AQUA), true);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide) {
            player.displayClientMessage(Component.translatable("block.zerog_tweaks.concord_lock.hint", state.getValue(STAGE), KEYS)
                    .withStyle(ChatFormatting.GRAY), true);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    /** Places concord_vault/chamber_stage_{stage} so its pivot lands on the lock. */
    public static boolean buildStage(ServerLevel level, BlockPos lock, Rotation rotation, int stage) {
        var id = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "concord_vault/chamber_stage_" + stage);
        var template = level.getStructureManager().get(id);
        if (template.isEmpty()) return false;
        var settings = new StructurePlaceSettings().setRotation(rotation).setRotationPivot(TEMPLATE_PIVOT);
        BlockPos origin = lock.subtract(TEMPLATE_PIVOT);
        return template.get().placeInWorld(level, origin, origin, settings, level.random, Block.UPDATE_CLIENTS);
    }
}
