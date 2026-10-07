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
    public static final List<String> WORLDS=List.of("moon","mars","cerulon","skarn","eidolon","solvane");
    public ConcordCodexItem(Properties properties) {
        super(properties.stacksTo(1).component(DataComponents.WRITTEN_BOOK_CONTENT,new WrittenBookContent(
            Filterable.passThrough("Concord Codex"),"The Concord",0,List.of(
                page("codex.zerog_tweaks.signal"),page("codex.zerog_tweaks.template"),page("codex.zerog_tweaks.coordinates")),true)));
    }
    private static Filterable<Component> page(String key) {return Filterable.passThrough(Component.translatable(key));}
    public static void recordArrival(ServerPlayer player){
        String id=player.level().dimension().location().toString();
        for(String world:WORLDS)if(id.equals("zerog_tweaks:"+world))player.getPersistentData().putBoolean("zerog_codex_"+world,true);
    }
    private static boolean complete(ServerPlayer player,String id){
        var holder=player.server.getAdvancements().get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","codex/"+id));
        return holder!=null&&player.getAdvancements().getOrStartProgress(holder).isDone();
    }
    private static boolean visited(ServerPlayer player,String world){return player.getPersistentData().getBoolean("zerog_codex_"+world)||complete(player,world.equals("moon")?"the_moon":world);}
    /** Rebuilt for the reader on every open: another player's book cannot reveal locked lore. */
    public static List<String> pageKeys(ServerPlayer player){
        var keys=new java.util.ArrayList<String>(List.of("signal","template","coordinates"));
        if(complete(player,"root"))keys.add("step_signal");
        if(complete(player,"falling_star"))keys.add("step_courier");
        if(complete(player,"builders_template"))keys.add("step_controller");
        if(complete(player,"first_gate"))keys.add("step_first_gate");
        if(visited(player,"moon")){keys.add("moon_relay");keys.add("step_moon");}
        if(visited(player,"mars")){keys.add("mars_waystation");keys.add("step_mars");if(complete(player,"aresite_core"))keys.add("step_aresite");}
        if(visited(player,"cerulon")){keys.add("act2_arrival");if(complete(player,"prism_sentinel"))keys.add("act2_heir");}
        if(visited(player,"skarn")){keys.add("act3_arrival");if(complete(player,"rift_tyrant"))keys.add("act3_memory");}
        if(visited(player,"eidolon")){keys.add("act4_arrival");if(complete(player,"remnants"))keys.add("act4_fragments");if(complete(player,"captain"))keys.add("act4_key");}
        if(visited(player,"solvane")){keys.add("act5_arrival");if(complete(player,"nova_pearl")){keys.add("act5_revelation");if(complete(player,"heart_of_solvane"))keys.add("act5_heart");}}
        return keys.stream().map(k->"codex.zerog_tweaks."+k).toList();
    }
    @Override public InteractionResultHolder<ItemStack> use(Level level,Player player,InteractionHand hand) {
        if(player instanceof ServerPlayer server) {
            recordArrival(server);
            ConcordPrologue.grant(server,"builders_template","read_codex");
            var pages=pageKeys(server).stream().map(ConcordCodexItem::page).toList();
            player.getItemInHand(hand).set(DataComponents.WRITTEN_BOOK_CONTENT,new WrittenBookContent(Filterable.passThrough("Concord Codex"),"The Concord",0,pages,true));
            server.inventoryMenu.broadcastChanges();
            // Right-click: the GuideME walkthrough. Sneak + right-click: Echo's story pages (unlocked per world visited).
            if(player.isShiftKeyDown())server.connection.send(new ClientboundOpenBookPacket(hand));
            else guideme.GuidesCommon.openGuide(server,GUIDE);
        }return InteractionResultHolder.sidedSuccess(player.getItemInHand(hand),level.isClientSide());
    }
}
