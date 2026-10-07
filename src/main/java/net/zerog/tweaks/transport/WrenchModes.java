package net.zerog.tweaks.transport;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

/**
 * Flux Wrench modes, like Mekanism's Configurator. Configure (default): right-click reads a side, shift + right-click
 * cycles it Normal / Push / Pull / None. Wrench: shift + right-click picks the block up with its contents.
 * Shift + scroll while holding the wrench switches mode (client sends {@link Switch}; the server owns the stack).
 */
public final class WrenchModes {
    public static final int CONFIGURE=0,WRENCH=1;
    private static final String KEY="wrench_mode";
    public static final String[] FACE_NAMES={"Normal","Push","Pull","None"};

    public static boolean isWrench(ItemStack stack){return stack.getItem() instanceof TransportToolItem tool&&tool.kind().equals("flux_wrench");}
    public static int mode(ItemStack stack){return stack.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag().getInt(KEY)==WRENCH?WRENCH:CONFIGURE;}
    public static Component modeName(int mode){return Component.literal(mode==WRENCH?"Wrench":"Configure");}
    static void set(ItemStack stack,int mode){CustomData.update(DataComponents.CUSTOM_DATA,stack,tag->tag.putInt(KEY,mode));}

    /** On a pipe, a click on an arm targets that arm's direction (the hit's dominant axis); otherwise the clicked face. */
    public static Direction targetSide(BlockPos pos,Vec3 hit,Direction clicked){
        double x=hit.x-pos.getX()-.5,y=hit.y-pos.getY()-.5,z=hit.z-pos.getZ()-.5;
        double ax=Math.abs(x),ay=Math.abs(y),az=Math.abs(z),max=Math.max(ax,Math.max(ay,az));
        if(max<1e-4)return clicked;
        if(max==ax)return x>0?Direction.EAST:Direction.WEST;
        if(max==ay)return y>0?Direction.UP:Direction.DOWN;
        return z>0?Direction.SOUTH:Direction.NORTH;
    }

    public record Switch() implements CustomPacketPayload {
        public static final Type<Switch> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","wrench_mode"));
        public static final StreamCodec<RegistryFriendlyByteBuf,Switch> CODEC=StreamCodec.unit(new Switch());
        @Override public Type<Switch> type(){return TYPE;}
    }

    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
    public static final class Networking {
        @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event){
            event.registrar("1").playToServer(Switch.TYPE,Switch.CODEC,(value,context)->context.enqueueWork(()->{
                if(!(context.player() instanceof ServerPlayer player))return;
                var stack=player.getItemInHand(InteractionHand.MAIN_HAND);if(!isWrench(stack))return;
                int next=mode(stack)==WRENCH?CONFIGURE:WRENCH;set(stack,next);
                player.displayClientMessage(Component.literal("Flux Wrench: ").append(modeName(next)),true);
            }));
        }
    }

    /** Shift + scroll with the wrench in the main hand switches mode instead of the hotbar slot. */
    @EventBusSubscriber(modid="zerog_tweaks",value=net.neoforged.api.distmarker.Dist.CLIENT)
    public static final class ClientScroll {
        @SubscribeEvent public static void scroll(net.neoforged.neoforge.client.event.InputEvent.MouseScrollingEvent event){
            var mc=net.minecraft.client.Minecraft.getInstance();var player=mc.player;
            if(player==null||mc.screen!=null||!player.isShiftKeyDown()||event.getScrollDeltaY()==0||!isWrench(player.getMainHandItem()))return;
            event.setCanceled(true);
            net.neoforged.neoforge.network.PacketDistributor.sendToServer(new Switch());
        }
    }

    private WrenchModes(){}
}
