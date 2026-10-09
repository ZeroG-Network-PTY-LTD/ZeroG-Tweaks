package net.zerog.tweaks.travel;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.registration.NetworkRegistry;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/** Transient nearby visuals; no entities, saved data or chunk tickets. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class GateHologramSync {
    public record Status(ResourceLocation dimension,BlockPos controller,int tier,String destination,int countdown,int energy,int cost,List<BlockPos> pylons) implements CustomPacketPayload {
        public Status{controller=controller.immutable();pylons=pylons.stream().map(BlockPos::immutable).toList();if(tier<0||tier>6||countdown<0||countdown>100||energy<0||cost<0||destination.length()>128||pylons.size()>32)throw new IllegalArgumentException("Invalid gate display");for(var p:pylons)if(p.distSqr(controller)>24*24)throw new IllegalArgumentException("Pylon outside gate");}
        public static final Type<Status> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gate_hologram"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Status> CODEC=new StreamCodec<>(){
            public Status decode(RegistryFriendlyByteBuf b){var dimension=b.readResourceLocation();var controller=b.readBlockPos();int tier=b.readVarInt();String destination=b.readUtf(128);int countdown=b.readVarInt(),energy=b.readVarInt(),cost=b.readVarInt(),count=b.readVarInt();if(count<0||count>32)throw new IllegalArgumentException("Invalid pylon count");var pylons=new ArrayList<BlockPos>();for(int i=0;i<count;i++)pylons.add(b.readBlockPos());return new Status(dimension,controller,tier,destination,countdown,energy,cost,pylons);}
            public void encode(RegistryFriendlyByteBuf b,Status s){b.writeResourceLocation(s.dimension());b.writeBlockPos(s.controller());b.writeVarInt(s.tier());b.writeUtf(s.destination(),128);b.writeVarInt(s.countdown());b.writeVarInt(s.energy());b.writeVarInt(s.cost());b.writeVarInt(s.pylons().size());for(var p:s.pylons())b.writeBlockPos(p);}
        };
        @Override public Type<Status> type(){return TYPE;}
    }
    private record Entry(Status status,long expires){}
    private static final Map<BlockPos,Entry> CLIENT=new LinkedHashMap<>();
    public static void clear(){CLIENT.clear();}
    public static List<Status> pending(ResourceLocation dimension){
        long now=System.nanoTime();CLIENT.values().removeIf(e->e.expires<now||!e.status.dimension().equals(dimension));
        return CLIENT.values().stream().map(Entry::status).toList();
    }
    public static Status describe(SurvivalGateBlockEntity gate){return new Status(gate.getLevel().dimension().location(),gate.getBlockPos(),gate.formedTier(),gate.selectedDestination(),gate.countdown,gate.stored,gate.cost(1),gate.pylonTops());}
    public static void broadcast(SurvivalGateBlockEntity gate){
        if(!(gate.getLevel() instanceof ServerLevel level))return;
        Status status=null;
        for(var player:level.players())if(player.distanceToSqr(gate.getBlockPos().getCenter())<=32*32&&NetworkRegistry.hasChannel(player.connection,Status.TYPE.id())){
            if(status==null)status=describe(gate);PacketDistributor.sendToPlayer(player,status);
        }
    }
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){event.registrar("2").playToClient(Status.TYPE,Status.CODEC,(s,c)->c.enqueueWork(()->{
        if(CLIENT.size()>=128&&!CLIENT.containsKey(s.controller()))CLIENT.remove(CLIENT.keySet().iterator().next());
        CLIENT.put(s.controller(),new Entry(s,System.nanoTime()+3_000_000_000L));
    }));}
    private GateHologramSync(){}
}
