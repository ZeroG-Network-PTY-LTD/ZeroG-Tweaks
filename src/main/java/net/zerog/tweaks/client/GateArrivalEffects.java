package net.zerog.tweaks.client;

import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RenderGuiEvent;

/** A short, transparent arrival vignette driven by the server's actual dimension change. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class GateArrivalEffects {
    private static ResourceLocation previous;
    private static int remaining;
    @SubscribeEvent public static void tick(ClientTickEvent.Post event){
        var mc=Minecraft.getInstance();
        if(mc.level==null||mc.player==null){remaining=0;return;}
        var current=mc.level.dimension().location();
        if(previous!=null&&!previous.equals(current)&&(previous.getNamespace().equals("zerog_tweaks")||current.getNamespace().equals("zerog_tweaks")))remaining=30;
        previous=current;if(remaining>0)remaining--;
    }
    @SubscribeEvent public static void render(RenderGuiEvent.Post event){
        var mc=Minecraft.getInstance();if(remaining<=0||mc.level==null||mc.player==null||mc.options.hideGui)return;
        var g=event.getGuiGraphics();int w=g.guiWidth(),h=g.guiHeight(),edge=Math.max(8,Math.min(w,h)/8),alpha=remaining*64/30;
        int colour=(alpha<<24)|0x8e63c9;
        g.fillGradient(0,0,w,edge,colour,0);g.fillGradient(0,h-edge,w,h,0,colour);
        // Side strips never cover the aiming reticle or remove control during arrival.
        for(int x=0;x<edge;x++){int a=alpha*(edge-x)/edge,c=(a<<24)|0x8e63c9;g.fill(x,edge,x+1,h-edge,c);g.fill(w-x-1,edge,w-x,h-edge,c);}
    }
    private GateArrivalEffects(){}
}
