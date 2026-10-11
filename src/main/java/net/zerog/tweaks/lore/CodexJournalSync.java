package net.zerog.tweaks.lore;

import java.util.List;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.ComponentSerialization;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/** Reader-specific snapshot only. The client cannot grant tasks or request locked lore. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class CodexJournalSync {
    public record Journal(List<Component> pages) implements CustomPacketPayload {
        public Journal { pages=List.copyOf(pages);if(pages.size()>64)throw new IllegalArgumentException("Codex page limit"); }
        public static final Type<Journal> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","codex_journal"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Journal> CODEC=StreamCodec.composite(
                ComponentSerialization.STREAM_CODEC.apply(ByteBufCodecs.list(64)),Journal::pages,Journal::new);
        @Override public Type<Journal> type(){return TYPE;}
    }
    private static volatile Journal pending;
    public static Journal take(){var result=pending;pending=null;return result;}
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){
        event.registrar("1").playToClient(Journal.TYPE,Journal.CODEC,(packet,context)->context.enqueueWork(()->pending=packet));
    }
    private CodexJournalSync(){}
}
