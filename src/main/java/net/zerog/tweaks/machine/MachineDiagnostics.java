package net.zerog.tweaks.machine;

import java.util.*;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.*;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.registration.NetworkRegistry;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.zerog.tweaks.genetics.*;
import net.zerog.tweaks.transport.*;

/** One bounded read-only snapshot, not a chunk scanner or saved hologram entity. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class MachineDiagnostics {
    public record Status(ResourceLocation dimension,BlockPos position,ResourceLocation block,int energy,int capacity,List<Integer> masks,List<String> faces) implements CustomPacketPayload {
        public Status{
            position=position.immutable();masks=List.copyOf(masks);faces=List.copyOf(faces);
            if(energy<0||capacity<energy||masks.size()!=6||faces.size()!=6||masks.stream().anyMatch(m->m<0||m>7)||faces.stream().anyMatch(s->s.length()>128))throw new IllegalArgumentException("Invalid machine diagnostic snapshot");
        }
        public static final Type<Status> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","machine_diagnostic"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Status> CODEC=new StreamCodec<>(){
            public Status decode(RegistryFriendlyByteBuf b){
                var dim=b.readResourceLocation();var pos=b.readBlockPos();var block=b.readResourceLocation();int energy=b.readVarInt(),capacity=b.readVarInt();
                var masks=new ArrayList<Integer>();var faces=new ArrayList<String>();for(int i=0;i<6;i++){masks.add((int)b.readUnsignedByte());faces.add(b.readUtf(128));}
                return new Status(dim,pos,block,energy,capacity,masks,faces);
            }
            public void encode(RegistryFriendlyByteBuf b,Status s){b.writeResourceLocation(s.dimension());b.writeBlockPos(s.position());b.writeResourceLocation(s.block());b.writeVarInt(s.energy());b.writeVarInt(s.capacity());for(int i=0;i<6;i++){b.writeByte(s.masks().get(i));b.writeUtf(s.faces().get(i),128);}}
        };
        @Override public Type<Status> type(){return TYPE;}
    }
    private static Status client;
    private static long expires;
    public static void clear(){client=null;expires=0;}
    public static Status pending(ResourceLocation dimension){if(client!=null&&(System.nanoTime()>expires||!client.dimension().equals(dimension)))clear();return client;}
    public static boolean supports(BlockEntity be){return be instanceof ProcessingBlockEntity||be instanceof CombustionBlockEntity
        ||be instanceof net.zerog.tweaks.power.PowerBlockEntity||be instanceof GasSeparatorBlockEntity||be instanceof TransportBlockEntity||be instanceof CreativeEnergyCell.Cell
        ||be!=null&&(GeneticsRuntime.handles(GeneticsRuntime.id(be))||GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be))||GeneticsRuntime.id(be).equals("stardust_smelter")||AlvearyRuntime.tier(be)>0);}
    public static Status describe(BlockEntity be){
        if(!supports(be)||be.isRemoved()||!(be.getLevel() instanceof ServerLevel level)||!level.hasChunkAt(be.getBlockPos())||level.getBlockEntity(be.getBlockPos())!=be)return null;
        var masks=new ArrayList<Integer>();var labels=new ArrayList<String>();int stored=0,capacity=0;
        for(var side:Direction.values()){
            var items=level.getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),side);
            var fluids=level.getCapability(Capabilities.FluidHandler.BLOCK,be.getBlockPos(),side);
            var power=level.getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),side);
            boolean i=items!=null&&items.getSlots()>0,f=fluids!=null&&fluids.getTanks()>0,e=power!=null&&(power.canReceive()||power.canExtract());
            String item=i?items.getSlots()+" slots":"-";
            String fluid=f?"tank":"-";
            if(be instanceof TransportBlockEntity node){boolean in=node.input(side),out=node.output(side);String role=!in&&!out?"OFF":in?(out?"BOTH":"IN"):"OUT";i&=in||out;f&=in||out;item=i?role:"-";fluid=f?(node.block().family.startsWith("gas")?"gas ":"")+role:"-";}
            else if(be instanceof ProcessingBlockEntity processor&&i)item=switch(processor.itemMode(side)){case 1->"INPUTS";case 2->"CATALYST";case 3->"OUTPUTS";default->"AUTO";};
            else if(LegacyMachineSides.supports(be)){String[] roles={"BOTH","IN","OUT","OFF"};if(i)item=roles[LegacyMachineSides.mode(be,side.ordinal())];if(f)fluid=roles[LegacyMachineSides.mode(be,12+side.ordinal())];}
            if(be instanceof GasSeparatorBlockEntity separator){f=separator.role(side)>0;fluid=switch(separator.role(side)){case 1->"water IN";case 2->"H2 OUT";case 3->"O2 OUT";default->"-";};}
            String energy=!e?"-":power.canReceive()?(power.canExtract()?"BOTH":"IN"):"OUT";
            masks.add((i?1:0)|(f?2:0)|(e?4:0));
            labels.add(side.getName().toUpperCase(java.util.Locale.ROOT)+"  I:"+item+" F:"+fluid+" FE:"+energy);
            if(power!=null){stored=Math.max(stored,Math.max(0,power.getEnergyStored()));capacity=Math.max(capacity,Math.max(0,power.getMaxEnergyStored()));}
        }
        // Closed faces must not make a known machine's real buffer appear empty.
        if(be instanceof ProcessingBlockEntity machine)stored=Math.max(0,machine.stored);
        else if(be instanceof CombustionBlockEntity machine){stored=Math.max(0,machine.stored);capacity=machine.capacity();}
        else if(be instanceof net.zerog.tweaks.power.PowerBlockEntity machine){stored=Math.max(0,machine.stored);capacity=machine.capacity();}
        else if(be instanceof GasSeparatorBlockEntity machine){stored=Math.max(0,machine.stored);capacity=GasSeparatorBlockEntity.ENERGY_CAPACITY;}
        else if(GeneticsRuntime.handles(GeneticsRuntime.id(be))||GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be))){var buffer=GeneticsRuntime.energy(be);stored=buffer.getEnergyStored();capacity=buffer.getMaxEnergyStored();}
        else if(AlvearyRuntime.tier(be)>0){var buffer=AlvearyRuntime.energy(be);stored=buffer.getEnergyStored();capacity=buffer.getMaxEnergyStored();}
        return new Status(level.dimension().location(),be.getBlockPos(),BuiltInRegistries.BLOCK.getKey(be.getBlockState().getBlock()),stored,Math.max(stored,capacity),masks,labels);
    }
    public static boolean show(ServerPlayer player,BlockEntity be){
        if(be==null||player.level()!=be.getLevel()||player.distanceToSqr(be.getBlockPos().getCenter())>64||!WrenchModes.isWrench(player.getMainHandItem())||WrenchModes.mode(player.getMainHandItem())!=WrenchModes.CONFIGURE)return false;
        var status=describe(be);if(status==null)return false;
        if(NetworkRegistry.hasChannel(player.connection,Status.TYPE.id()))PacketDistributor.sendToPlayer(player,status);
        return true;
    }
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent e){e.registrar("1").playToClient(Status.TYPE,Status.CODEC,(s,c)->c.enqueueWork(()->{client=s;expires=System.nanoTime()+15_000_000_000L;}));}
    private MachineDiagnostics(){}
}
