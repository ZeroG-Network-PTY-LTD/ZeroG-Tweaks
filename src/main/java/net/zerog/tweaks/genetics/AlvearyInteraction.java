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
    @SubscribeEvent public static void open(PlayerInteractEvent.RightClickBlock event){
        if(event.getHand()!=InteractionHand.MAIN_HAND)return;
        var be=event.getLevel().getBlockEntity(event.getPos());
        if(be==null||AlvearyRuntime.tier(be)==0)return;
        // Ordinary held items must not fall through to the addon's legacy menu.
        // Keep deliberate wrench use and sneak-placement available.
        var stack=event.getItemStack();
        if((event.getEntity().isShiftKeyDown()&&stack.getItem() instanceof net.minecraft.world.item.BlockItem)
                ||net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath().endsWith("wrench"))return;
        if(event.getEntity() instanceof ServerPlayer player)player.openMenu(new SimpleMenuProvider((id,inv,p)->new AlvearyMenu(id,inv,be),Component.literal("Alveary Controller")),buf->buf.writeBlockPos(event.getPos()));
        event.setCanceled(true);
        event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));
    }
    private AlvearyInteraction(){}
}
