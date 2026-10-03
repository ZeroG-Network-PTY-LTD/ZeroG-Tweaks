package net.zerog.tweaks.arena;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;

/**
 * Key Altar: holds one Concord Key in a vault room (placed by KeyAltarPiece). Taking the key wakes the room's guardians,
 * three Prismlings around the altar. An empty altar stays as a marker.
 */
public class VaultKeyAltarBlock extends Block {
    public static final BooleanProperty HAS_KEY = BooleanProperty.create("has_key");
    public static final int GUARDIANS = 3;

    public VaultKeyAltarBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(HAS_KEY, true));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(HAS_KEY);
    }

    public static int light(BlockState state) { return state.getValue(HAS_KEY) ? 12 : 4; }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!state.getValue(HAS_KEY)) return InteractionResult.PASS;
        if (level instanceof ServerLevel server) {
            server.setBlock(pos, state.setValue(HAS_KEY, false), Block.UPDATE_ALL);
            ItemStack key = new ItemStack(ItemInit.CONCORD_VAULT_KEY.get());
            if (!player.getInventory().add(key)) player.drop(key, false);
            server.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.BLOCKS, 2F, 1.2F);
            server.sendParticles(ParticleTypes.END_ROD, pos.getX() + 0.5, pos.getY() + 1.2, pos.getZ() + 0.5, 30, 0.4, 0.6, 0.4, 0.05);
            player.displayClientMessage(Component.translatable("block.zerog_tweaks.vault_key_altar.taken")
                    .withStyle(ChatFormatting.AQUA), true);
            wakeGuardians(server, pos);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    private static void wakeGuardians(ServerLevel level, BlockPos altar) {
        for (int i = 0; i < GUARDIANS; i++) {
            double a = Math.PI * 2 * i / GUARDIANS;
            BlockPos at = altar.offset((int) Math.round(Math.cos(a) * 3), 0, (int) Math.round(Math.sin(a) * 3));
            var guardian = EntityInit.PRISMLING_HOLDER.get().create(level);
            if (guardian == null || !level.getBlockState(at).isAir()) continue;
            guardian.moveTo(at.getX() + 0.5, at.getY(), at.getZ() + 0.5, level.random.nextFloat() * 360, 0);
            guardian.finalizeSpawn(level, level.getCurrentDifficultyAt(at), MobSpawnType.EVENT, null);
            guardian.setPersistenceRequired();
            level.addFreshEntity(guardian);
        }
    }
}
