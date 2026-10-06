package net.zerog.tweaks.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.ReceivingLevelScreen;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.ComputeFovModifierEvent;
import net.neoforged.neoforge.client.event.RenderGuiEvent;
import net.zerog.tweaks.travel.GateLaunchSync;

/** Gate lift: the view stretches, whites out in the last moments, holds white until the new dimension loads, then fades. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class GateLaunchEffects {
    private static final int WHITE_IN=8,HOLD=100,FADE=25;
    private static ResourceLocation launchedFrom;
    private static int lift,liftTotal,hold,fade;
    @SubscribeEvent public static void tick(ClientTickEvent.Post event){
        var mc=Minecraft.getInstance();
        if(mc.level==null||mc.player==null){lift=hold=fade=0;return;}
        var current=mc.level.dimension().location();
        int received=GateLaunchSync.clientLift;
        if(received>=0){GateLaunchSync.clientLift=-1;fade=0;if(received==0){lift=hold=0;}else{lift=liftTotal=received;hold=0;launchedFrom=current;}}
        if(lift>0){if(--lift==0)hold=HOLD;}
        // Hold the white-out until we have arrived and the loading/transition screen has closed; never longer than HOLD
        // if the launch fails silently. GateTransitionScreen draws its own white-outs while it is open.
        else if(hold>0){if(!(mc.screen instanceof ReceivingLevelScreen)&&(!current.equals(launchedFrom)||--hold==0)){hold=0;fade=FADE;}}
        else if(fade>0)fade--;
    }
    private static float stretch(){return lift>0&&liftTotal>0?1F-lift/(float)liftTotal:hold>0?1F:0F;}
    @SubscribeEvent public static void fov(ComputeFovModifierEvent event){
        float p=stretch();if(p>0)event.setNewFovModifier(event.getNewFovModifier()*(1F+.35F*p*p));
    }
    @SubscribeEvent public static void render(RenderGuiEvent.Post event){
        float white=lift>0?Math.max(0F,(WHITE_IN-lift)/(float)WHITE_IN):hold>0?1F:fade/(float)FADE;
        if(white<=0)return;
        var g=event.getGuiGraphics();int alpha=Math.min(255,(int)(white*255));
        g.fill(0,0,g.guiWidth(),g.guiHeight(),(alpha<<24)|0xFFFFFF);
    }
    private GateLaunchEffects(){}
}
