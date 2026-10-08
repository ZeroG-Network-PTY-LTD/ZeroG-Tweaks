package net.zerog.tweaks.travel;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.NetworkRegistry;

/** A bounded, server-selected construction plan; never an instruction to place blocks. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class GateSchematicSync {
    public record Plan(ResourceLocation dimension,BlockPos controller,BlockPos centre,int direction,int tier) implements CustomPacketPayload {
        public Plan {
            controller=controller.immutable();centre=centre.immutable();
            if(tier<1||tier>6||direction<0||direction>3||Math.abs((long)controller.getX()-centre.getX())>7
                    ||Math.abs((long)controller.getZ()-centre.getZ())>7||controller.getY()!=centre.getY()+1)
                throw new IllegalArgumentException("Invalid gate schematic bounds");
        }
        public static final Type<Plan> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gate_schematic"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Plan> CODEC=new StreamCodec<>() {
            public Plan decode(RegistryFriendlyByteBuf buf){return new Plan(buf.readResourceLocation(),buf.readBlockPos(),buf.readBlockPos(),buf.readVarInt(),buf.readVarInt());}
            public void encode(RegistryFriendlyByteBuf buf,Plan plan){buf.writeResourceLocation(plan.dimension());buf.writeBlockPos(plan.controller());buf.writeBlockPos(plan.centre());buf.writeVarInt(plan.direction());buf.writeVarInt(plan.tier());}
        };
        public Direction facing(){return Direction.from2DDataValue(direction);}
        @Override public Type<Plan> type(){return TYPE;}
    }
    private static volatile Plan clientPlan;
    private static volatile long expires;
    public static Plan pending(){if(System.nanoTime()>expires){clear();return null;}return clientPlan;}
    public static void clear(){clientPlan=null;expires=0;}
    private static void receive(Plan plan){
        Plan current=pending();
        if(plan.equals(current)){clear();return;}
        clientPlan=plan;expires=System.nanoTime()+60_000_000_000L;
    }
    public static void send(ServerPlayer player,SurvivalGateBlockEntity gate){
        if(!(gate.getLevel() instanceof ServerLevel level)||!gate.mayControl(player)||player.serverLevel()!=level
                ||player.distanceToSqr(gate.getBlockPos().getCenter())>64)return;
        int formed=gate.formedTier(),tier=Math.max(1,formed);
        Direction facing=formed==0?SurvivalGateLayout.closestFacing(level,gate.getBlockPos(),gate.facing()):gate.facing();
        if(NetworkRegistry.hasChannel(player.connection,Plan.TYPE.id()))
            PacketDistributor.sendToPlayer(player,new Plan(level.dimension().location(),gate.getBlockPos(),SurvivalGateLayout.centre(gate.getBlockPos(),facing),facing.get2DDataValue(),tier));
    }
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){
        event.registrar("1").playToClient(Plan.TYPE,Plan.CODEC,(plan,context)->context.enqueueWork(()->receive(plan)));
    }
    private GateSchematicSync(){}
}
