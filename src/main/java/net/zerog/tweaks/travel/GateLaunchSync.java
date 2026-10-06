package net.zerog.tweaks.travel;

import java.util.List;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.zerog.tweaks.event.PlanetGravity;

/** Gate jump client sync: the lift (ticks until launch, 0 = cancelled) and the destination for the transition screen. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class GateLaunchSync {
    // Receipt is stored without referring to client-only classes on dedicated servers; GateLaunchEffects consumes it.
    public static volatile int clientLift=-1;
    public record Lift(int ticks) implements CustomPacketPayload {
        public static final Type<Lift> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gate_lift"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Lift> CODEC=StreamCodec.composite(ByteBufCodecs.VAR_INT,Lift::ticks,Lift::new);
        @Override public Type<Lift> type(){return TYPE;}
    }
    /** Where a gate jump is going, sent just before the teleport so the transition screen never guesses from the id alone. */
    public record Destination(String dimension,int galaxy,String planet,float gravity,boolean echo) implements CustomPacketPayload {
        public static final Type<Destination> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gate_destination"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Destination> CODEC=StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8,Destination::dimension,ByteBufCodecs.VAR_INT,Destination::galaxy,ByteBufCodecs.STRING_UTF8,Destination::planet,
                ByteBufCodecs.FLOAT,Destination::gravity,ByteBufCodecs.BOOL,Destination::echo,Destination::new);
        @Override public Type<Destination> type(){return TYPE;}
    }
    private static final List<String> FIXED=List.of("moon","mars","cerulon","skarn","eidolon","solvane");
    private static volatile Destination clientDestination;
    private static volatile long clientDestinationAt;
    /** Call right before a ZeroG teleport moves {@code player} into {@code target}. */
    public static void sendDestination(ServerPlayer player,ServerLevel target){if(player.level()!=target)PacketDistributor.sendToPlayer(player,describe(player,target));}
    static Destination describe(ServerPlayer player,ServerLevel target){
        var key=target.dimension().location();String id=key.toString(),path=key.getPath(),planet;
        if(id.equals("minecraft:overworld"))planet="earth";
        else if(!key.getNamespace().equals("zerog_tweaks"))planet="unknown";
        else if(FIXED.contains(path))planet=path;
        else if(path.endsWith("_moons"))planet="wasteland_barren";
        else planet=target.getChunkSource().getGenerator() instanceof NoiseBasedChunkGenerator noise
                ?noise.generatorSettings().unwrapKey().map(k->k.location().getPath()).filter(p->p.startsWith("wasteland_")).orElse("unknown"):"unknown";
        // Echo's line for a world unlocks with its Codex advancement.
        String codex=switch(planet){case "earth"->"root";case "moon"->"the_moon";case "unknown"->"";default->planet.startsWith("wasteland_")?"first_gate":planet;};
        var holder=codex.isEmpty()?null:player.server.getAdvancements().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","codex/"+codex));
        boolean echo=holder!=null&&player.getAdvancements().getOrStartProgress(holder).isDone();
        return new Destination(id,Math.max(1,SurvivalGateLayout.galaxy(id)),planet,(float)PlanetGravity.multiplier(id,target.getSeed()),echo);
    }
    /**
     * Client: the destination of the jump now in progress, if one arrived in the last 15 seconds. Not consumed here:
     * vanilla builds the loading screen twice per dimension change (a one-frame screen in Minecraft.setLevel, then the
     * real one in startWaitingForNewLevel), so the real screen clears it when it closes.
     */
    public static Destination pendingDestination(){
        var d=clientDestination;
        return d!=null&&System.currentTimeMillis()-clientDestinationAt<15000?d:null;
    }
    public static void clearDestination(){clientDestination=null;}
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){
        var registrar=event.registrar("1");
        registrar.playToClient(Lift.TYPE,Lift.CODEC,(lift,context)->context.enqueueWork(()->clientLift=Math.max(0,lift.ticks())));
        registrar.playToClient(Destination.TYPE,Destination.CODEC,(d,context)->context.enqueueWork(()->{clientDestination=d;clientDestinationAt=System.currentTimeMillis();}));
    }
    private GateLaunchSync(){}
}
