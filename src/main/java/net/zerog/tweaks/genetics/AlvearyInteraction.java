package net.zerog.tweaks.genetics;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

@EventBusSubscriber(modid="zerog_tweaks")
public final class AlvearyInteraction {
    @SubscribeEvent public static void open(PlayerInteractEvent.RightClickBlock event){if(event.getHand()!=InteractionHand.MAIN_HAND||!event.getItemStack().isEmpty())return;var be=event.getLevel().getBlockEntity(event.getPos());if(be==null||AlvearyRuntime.tier(be)==0)return;if(event.getEntity() instanceof ServerPlayer player)player.openMenu(new SimpleMenuProvider((id,inv,p)->new AlvearyMenu(id,inv,be),Component.literal("Alveary Controller")),buf->buf.writeBlockPos(event.getPos()));event.setCanceled(true);event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));}
    private AlvearyInteraction(){}
}
