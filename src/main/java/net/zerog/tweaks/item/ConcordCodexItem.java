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

/** Native book component/viewer; custom item IDs do not pass vanilla's WRITTEN_BOOK identity check. */
public final class ConcordCodexItem extends Item {
    public ConcordCodexItem(Properties properties) {
        super(properties.stacksTo(1).component(DataComponents.WRITTEN_BOOK_CONTENT,new WrittenBookContent(
            Filterable.passThrough("Concord Codex"),"The Concord",0,List.of(
                page("codex.zerog_tweaks.signal"),page("codex.zerog_tweaks.template"),page("codex.zerog_tweaks.coordinates")),true)));
    }
    private static Filterable<Component> page(String key) {return Filterable.passThrough(Component.translatable(key));}
    @Override public InteractionResultHolder<ItemStack> use(Level level,Player player,InteractionHand hand) {
        if(player instanceof ServerPlayer server) {
            ConcordPrologue.grant(server,"builders_template","read_codex");
            server.connection.send(new ClientboundOpenBookPacket(hand));
        }return InteractionResultHolder.sidedSuccess(player.getItemInHand(hand),level.isClientSide());
    }
}
