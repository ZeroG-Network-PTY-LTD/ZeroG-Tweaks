package net.zerog.tweaks.event;

import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

/**
 * Bottle interactions: milk a Frost Yak, tap a Shardwood log for syrup.
 * Shearing (Crystal Stag antlers, Frost Yak wool) lives in the entity classes via IShearable; see the notes at the bottom.
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID)
public final class ZGInteractions {
    private ZGInteractions() {}

    @SubscribeEvent
    public static void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        Player player = event.getEntity();
        ItemStack held = event.getItemStack();
        Level level = event.getLevel();
        BlockPos pos = event.getPos();
        if (held.is(Items.GLASS_BOTTLE) && level.getBlockState(pos).is(BlockInit.SHARDWOOD_LOG.get())
                && !player.getCooldowns().isOnCooldown(Items.GLASS_BOTTLE)) {
            if (!level.isClientSide) {
                ItemStack syrup = new ItemStack(ItemInit.SHARDWOOD_SYRUP.get());
                player.setItemInHand(event.getHand(), ItemUtils.createFilledResult(held, player, syrup));
                level.playSound(null, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, 1.0f, 1.0f);
                player.getCooldowns().addCooldown(Items.GLASS_BOTTLE, 100); // 5 s between taps
            }
            event.setCancellationResult(InteractionResult.sidedSuccess(level.isClientSide));
            event.setCanceled(true);
        }
    }
}

/*
 * Shearing, implemented on the entity (NeoForge IShearable):
 *
 * public class CrystalStag extends Animal implements IShearable {
 *     private static final EntityDataAccessor<Boolean> SHEARED = SynchedEntityData.defineId(CrystalStag.class, EntityDataSerializers.BOOLEAN);
 *     private int regrowTicks;
 *
 *     @Override public boolean isShearable(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
 *         return !isBaby() && !entityData.get(SHEARED);
 *     }
 *     @Override public List<ItemStack> onSheared(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
 *         entityData.set(SHEARED, true); regrowTicks = 6000;              // antlers regrow in 5 minutes
 *         level.playSound(null, this, SoundEvents.AMETHYST_BLOCK_BREAK, SoundSource.NEUTRAL, 1f, 1f);
 *         return List.of(new ItemStack(ZGItems.STARLITE.get(), 1 + random.nextInt(2)));
 *     }
 *     @Override public void aiStep() { super.aiStep(); if (!level().isClientSide && entityData.get(SHEARED) && --regrowTicks <= 0) entityData.set(SHEARED, false); }
 * }
 *
 * FrostYak: same pattern, returning 1-2 Yak Wool; wool regrows after eating (like sheep eating grass) or after a timer.
 */
