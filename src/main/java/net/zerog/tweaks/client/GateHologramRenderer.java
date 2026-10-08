package net.zerog.tweaks.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.*;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;
import net.zerog.tweaks.travel.*;

/** Emissive wire galaxy and a camera-facing live terminal label, anchored above the real controller. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class GateHologramRenderer {
    @SubscribeEvent public static void logout(net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent.LoggingOut e){GateHologramSync.clear();}
    @SubscribeEvent public static void render(RenderLevelStageEvent e){
        if(e.getStage()!=RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS)return;
        var mc=Minecraft.getInstance();if(mc.level==null||mc.player==null){GateHologramSync.clear();return;}
        var camera=e.getCamera();var position=camera.getPosition();var poses=e.getPoseStack();var buffers=mc.renderBuffers().bufferSource();
        for(var s:GateHologramSync.pending(mc.level.dimension().location())){
            var p=s.controller();if(mc.player.distanceToSqr(p.getCenter())>32*32||!mc.level.hasChunkAt(p)||!mc.level.getBlockState(p).is(net.zerog.tweaks.registry.BlockInit.GATE_CONTROLLER.get()))continue;
            poses.pushPose();
            try{
                poses.translate(p.getX()+.5-position.x,p.getY()+2.1-position.y,p.getZ()+.5-position.z);
                var lines=buffers.getBuffer(RenderType.lines());double phase=(mc.level.getGameTime()+e.getPartialTick().getGameTimeDeltaPartialTick(false))*.025;
                for(int i=0;i<48;i++){double t=i/47.0,a=t*Math.PI*6+phase,r=.08+.65*t;double x=Math.cos(a)*r,z=Math.sin(a)*r;
                    LevelRenderer.renderLineBox(poses,lines,x-.014,0,z-.014,x+.014,.028,z+.014,.35F,.75F,1F,.8F);}
                LevelRenderer.renderLineBox(poses,lines,-.07,-.07,-.07,.07,.07,.07,1F,.8F,.25F,1F);
                // Highlight selected planet on its orbit; no invented texture or world entity.
                double a=phase*.5+s.destination().hashCode();double x=Math.cos(a)*.8,z=Math.sin(a)*.8;
                LevelRenderer.renderLineBox(poses,lines,x-.06,-.06,z-.06,x+.06,.06,z+.06,.7F,.35F,1F,1F);
                poses.translate(0,.65,0);poses.mulPose(camera.rotation());poses.scale(-.02F,-.02F,.02F);
                String dest=s.destination().isEmpty()?"Select planet in controller":s.destination().substring(s.destination().indexOf(':')+1).replace('_',' ');
                String[] labels={"GALAXY "+Math.max(1,SurvivalGateLayout.galaxy(s.destination()))+" / TIER "+s.tier(),dest,s.countdown()>0?"CHARGING  "+((s.countdown()+19)/20)+"s":s.energy()+" FE / JUMP "+s.cost()+" FE"};
                for(int row=0;row<labels.length;row++)mc.font.drawInBatch(labels[row],-mc.font.width(labels[row])/2F,row*11,0xffb3edff,false,poses.last().pose(),buffers,Font.DisplayMode.NORMAL,0x80202a40,15728880);
            }finally{poses.popPose();}
        }
        buffers.endBatch(RenderType.lines());
    }
    private GateHologramRenderer(){}
}
