package net.zerog.tweaks.genetics;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.registration.NetworkRegistry;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/** Server-resolved recipe information for the current menu only; never a job request. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
public final class AlvearyRecipeSync {
    public record Product(ItemStack icon,int min,int max,float chance){
        public Product{icon=icon.copyWithCount(1);if(icon.isEmpty()||min<0||max<min||max>4096||!Float.isFinite(chance)||chance<0||chance>1)throw new IllegalArgumentException("Invalid bee product");}
    }
    public record Snapshot(int menu,BlockPos controller,int tier,int cycle,int feTick,String honey,boolean boosted,boolean truncated,List<Product> products) implements CustomPacketPayload {
        public Snapshot{controller=controller.immutable();products=List.copyOf(products);if(tier<1||tier>7||cycle<80||cycle>10000||feTick<0||feTick>140||honey.length()>128||products.size()>32)throw new IllegalArgumentException("Invalid alveary recipe snapshot");}
        public static final Type<Snapshot> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","alveary_recipe"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Snapshot> CODEC=new StreamCodec<>(){
            public void encode(RegistryFriendlyByteBuf b,Snapshot s){b.writeVarInt(s.menu);b.writeBlockPos(s.controller);b.writeVarInt(s.tier);b.writeVarInt(s.cycle);b.writeVarInt(s.feTick);b.writeUtf(s.honey,128);b.writeBoolean(s.boosted);b.writeBoolean(s.truncated);b.writeVarInt(s.products.size());for(var p:s.products){ItemStack.STREAM_CODEC.encode(b,p.icon);b.writeVarInt(p.min);b.writeVarInt(p.max);b.writeFloat(p.chance);}}
            public Snapshot decode(RegistryFriendlyByteBuf b){int menu=b.readVarInt();var pos=b.readBlockPos();int tier=b.readVarInt(),cycle=b.readVarInt(),fe=b.readVarInt();String honey=b.readUtf(128);boolean boost=b.readBoolean(),truncated=b.readBoolean();int count=b.readVarInt();if(count<0||count>32)throw new IllegalArgumentException("Too many bee products");var products=new ArrayList<Product>();for(int i=0;i<count;i++)products.add(new Product(ItemStack.STREAM_CODEC.decode(b),b.readVarInt(),b.readVarInt(),b.readFloat()));return new Snapshot(menu,pos,tier,cycle,fe,honey,boost,truncated,products);}
        };
        @Override public Type<Snapshot> type(){return TYPE;}
    }
    public static volatile Snapshot clientState;
    public static Snapshot describe(AlvearyMenu menu){
        var be=menu.machine;int tier=AlvearyRuntime.tier(be);var outputs=AlvearyRuntime.products(be);
        var products=outputs.stream().limit(32).map(p->new Product(p.item(),ProductiveBeeProduction.productiveQuantity(p.min(),p.productivity()),ProductiveBeeProduction.productiveQuantity(p.max(),p.productivity()),p.chance())).toList();
        var honey=AlvearyRuntime.cycleHoney(be);
        return new Snapshot(menu.containerId,be.getBlockPos(),tier,AlvearyRuntime.cycle(be),tier>=3?20*tier:0,honey.isEmpty()?"":honey.getHoverName().getString(),new AlvearyFluids(be).getFluidInTank(1).getAmount()>=25,outputs.size()>32,products);
    }
    public static void send(ServerPlayer player){if(player.containerMenu instanceof AlvearyMenu menu&&menu.stillValid(player)&&NetworkRegistry.hasChannel(player.connection,Snapshot.TYPE.id()))PacketDistributor.sendToPlayer(player,describe(menu));}
    @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){event.registrar("1").playToClient(Snapshot.TYPE,Snapshot.CODEC,(s,c)->c.enqueueWork(()->{
        if(c.player().containerMenu instanceof AlvearyMenu menu&&menu.containerId==s.menu&&menu.machine.getBlockPos().equals(s.controller))clientState=s;
    }));}
    private AlvearyRecipeSync(){}
}
