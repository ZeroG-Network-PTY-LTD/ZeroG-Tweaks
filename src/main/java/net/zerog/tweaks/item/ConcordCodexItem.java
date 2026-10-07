package net.zerog.tweaks.item;

import java.util.List;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundOpenBookPacket;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.network.Filterable;
import net.minecraft.world.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.item.component.WrittenBookContent;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.lore.ConcordPrologue;

/**
 * Opens the GuideME walkthrough (assets/zerog_tweaks/guides/zerog_tweaks/concord_codex); sneaking opens the story
 * pages in the native book viewer. Custom item IDs do not pass vanilla's WRITTEN_BOOK identity check.
 */
public final class ConcordCodexItem extends Item {
    public static final net.minecraft.resources.ResourceLocation GUIDE=net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","concord_codex");
    public ConcordCodexItem(Properties properties) {
        super(properties.stacksTo(1).component(DataComponents.WRITTEN_BOOK_CONTENT,new WrittenBookContent(
            Filterable.passThrough("Concord Codex"),"The Concord",0,List.of(
                page("codex.zerog_tweaks.signal"),page("codex.zerog_tweaks.template"),page("codex.zerog_tweaks.coordinates")),true)));
    }
    private static Filterable<Component> page(String key) {return Filterable.passThrough(Component.translatable(key));}
    public static void recordArrival(ServerPlayer player){
        String id=player.level().dimension().location().toString();
        if(id.equals("zerog_tweaks:moon"))player.getPersistentData().putBoolean("zerog_codex_moon",true);
        if(id.equals("zerog_tweaks:mars"))player.getPersistentData().putBoolean("zerog_codex_mars",true);
    }
    @Override public InteractionResultHolder<ItemStack> use(Level level,Player player,InteractionHand hand) {
        if(player instanceof ServerPlayer server) {
            recordArrival(server);
            var pages=new java.util.ArrayList<Filterable<Component>>();
            pages.add(page("codex.zerog_tweaks.signal"));pages.add(page("codex.zerog_tweaks.template"));pages.add(page("codex.zerog_tweaks.coordinates"));
            if(server.getPersistentData().getBoolean("zerog_codex_moon"))pages.add(page("codex.zerog_tweaks.moon_relay"));
            if(server.getPersistentData().getBoolean("zerog_codex_mars"))pages.add(page("codex.zerog_tweaks.mars_waystation"));
            player.getItemInHand(hand).set(DataComponents.WRITTEN_BOOK_CONTENT,new WrittenBookContent(Filterable.passThrough("Concord Codex"),"The Concord",0,pages,true));
            server.inventoryMenu.broadcastChanges();
            ConcordPrologue.grant(server,"builders_template","read_codex");
            // Right-click: the GuideME walkthrough. Sneak + right-click: Echo's story pages (unlocked per world visited).
            if(player.isShiftKeyDown())server.connection.send(new ClientboundOpenBookPacket(hand));
            else guideme.GuidesCommon.openGuide(server,GUIDE);
        }return InteractionResultHolder.sidedSuccess(player.getItemInHand(hand),level.isClientSide());
    }
}
