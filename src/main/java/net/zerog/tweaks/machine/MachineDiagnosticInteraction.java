package net.zerog.tweaks.machine;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.*;
import net.neoforged.bus.api.*;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.zerog.tweaks.transport.*;
@EventBusSubscriber(modid="zerog_tweaks")
public final class MachineDiagnosticInteraction {
    @SubscribeEvent(priority=EventPriority.HIGHEST)
    public static void read(PlayerInteractEvent.RightClickBlock e){
        if(e.getHand()!=InteractionHand.MAIN_HAND||e.getEntity().isShiftKeyDown()||!WrenchModes.isWrench(e.getItemStack())||WrenchModes.mode(e.getItemStack())!=WrenchModes.CONFIGURE)return;
        var be=e.getLevel().getBlockEntity(e.getPos());if(be instanceof TransportBlockEntity||!MachineDiagnostics.supports(be))return;
        boolean accepted=e.getLevel().isClientSide||e.getEntity() instanceof ServerPlayer p&&MachineDiagnostics.show(p,be);
        if(accepted){e.getEntity().displayClientMessage(net.minecraft.network.chat.Component.literal("Port snapshot: I items, F fluid/gas, FE power. Right-click to refresh."),true);e.setCanceled(true);e.setCancellationResult(InteractionResult.sidedSuccess(e.getLevel().isClientSide));}
    }
    private MachineDiagnosticInteraction(){}
}
