package net.zerog.tweaks.event;

import java.util.ArrayList;
import java.util.Comparator;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.zerog.tweaks.guide.AlvearyLayout;
import net.zerog.tweaks.guide.ApiaryMachineAccess;

/** Read-only live status and a permission-checked sort; no invented bee/tank values. */
@EventBusSubscriber(modid="zerog_tweaks")
public final class AlvearyMenuSync {
    public static volatile State clientState=new State(-1,0,false,"");
    public record State(int menu,int progress,boolean formed,String error) implements CustomPacketPayload {
        public static final Type<State> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","alveary_status"));
        public static final StreamCodec<RegistryFriendlyByteBuf,State> CODEC=StreamCodec.of(
            (buf,value)->{buf.writeVarInt(value.menu);buf.writeVarInt(value.progress);buf.writeBoolean(value.formed);buf.writeUtf(value.error,1024);},
            buf->new State(buf.readVarInt(),buf.readVarInt(),buf.readBoolean(),buf.readUtf(1024)));
        @Override public Type<State> type(){return TYPE;}
    }
    public record Sort(int menu) implements CustomPacketPayload {
        public static final Type<Sort> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","alveary_sort"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Sort> CODEC=StreamCodec.of((buf,v)->buf.writeVarInt(v.menu),buf->new Sort(buf.readVarInt()));
        @Override public Type<Sort> type(){return TYPE;}
    }
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
    public static final class Networking {
        @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event) {
            var registrar=event.registrar("1");
            registrar.playToClient(State.TYPE,State.CODEC,(value,context)->context.enqueueWork(()->clientState=value));
            registrar.playToServer(Sort.TYPE,Sort.CODEC,(value,context)->context.enqueueWork(()->{
                if(context.player() instanceof ServerPlayer player)sort(player,value.menu);
            }));
        }
    }
    @SubscribeEvent public static void tick(PlayerTickEvent.Post event) {
        if(!(event.getEntity() instanceof ServerPlayer player)||player.tickCount%20!=0)return;
        ApiaryMachineAccess.read(player.containerMenu).ifPresent(machine->{
            // All verified addon machine menus can receive the same read-only cycle status.
            String error=machine.error();if(error.length()>1024)error=error.substring(0,1024);
            PacketDistributor.sendToPlayer(player,new State(player.containerMenu.containerId,machine.progress(),machine.formed(),error));
        });
    }
    static void sort(ServerPlayer player,int id) {
        var menu=player.containerMenu;if(menu.containerId!=id)return;
        ApiaryMachineAccess.read(menu).ifPresent(machine->{
            int tier=AlvearyLayout.tier(machine.id());
            if(tier==0 || !menu.stillValid(player) || player.distanceToSqr(machine.entity().getBlockPos().getCenter())>64
                    || menu.slots.size()!=AlvearyLayout.machineSlots(tier)+36)return;
            int start=2+AlvearyLayout.frames(tier),end=AlvearyLayout.machineSlots(tier);
            // Only reorder copies of output stacks; no deletion, recipe or input changes.
            var stacks=new ArrayList<ItemStack>();
            for(int i=start;i<end;i++)if(menu.slots.get(i).hasItem())stacks.add(menu.slots.get(i).getItem().copy());
            stacks.sort(Comparator.comparing(stack->BuiltInRegistries.ITEM.getKey(stack.getItem()).toString()));
            for(int i=start;i<end;i++)menu.slots.get(i).set(i-start<stacks.size()?stacks.get(i-start):ItemStack.EMPTY);
            menu.broadcastChanges();
        });
    }
    private AlvearyMenuSync() {}
}
