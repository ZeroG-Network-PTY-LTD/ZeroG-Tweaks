package net.zerog.tweaks.client;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.renderer.*;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.*;
import net.zerog.tweaks.machine.MachineDiagnostics;
import net.zerog.tweaks.transport.WrenchModes;

/** Actual capability snapshot: six colour-coded faces, no fictional internals. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class MachineDiagnosticRenderer {
    @SubscribeEvent public static void logout(ClientPlayerNetworkEvent.LoggingOut e){MachineDiagnostics.clear();}
    @SubscribeEvent public static void render(RenderLevelStageEvent e){
        if(e.getStage()!=RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS)return;
        var mc=Minecraft.getInstance();
        if(mc.level==null||mc.player==null||!WrenchModes.isWrench(mc.player.getMainHandItem())||WrenchModes.mode(mc.player.getMainHandItem())!=WrenchModes.CONFIGURE){MachineDiagnostics.clear();return;}
        var s=MachineDiagnostics.pending(mc.level.dimension().location());if(s==null)return;var p=s.position();
        if(mc.player.distanceToSqr(p.getCenter())>16*16||!mc.level.hasChunkAt(p)||!BuiltInRegistries.BLOCK.getKey(mc.level.getBlockState(p).getBlock()).equals(s.block())){MachineDiagnostics.clear();return;}
        var camera=e.getCamera();var at=camera.getPosition();var poses=e.getPoseStack();var buffers=mc.renderBuffers().bufferSource();
        poses.pushPose();
        try{
            poses.translate(p.getX()-at.x,p.getY()-at.y,p.getZ()-at.z);
            var lines=buffers.getBuffer(RenderType.lines());LevelRenderer.renderLineBox(poses,lines,-.02,-.02,-.02,1.02,1.02,1.02,.3F,.8F,1F,.85F);
            for(var side:Direction.values()){
                int mask=s.masks().get(side.ordinal());float r=(mask&4)!=0?1F:(mask&1)!=0?.75F:.18F,g=(mask&2)!=0?.85F:(mask&4)!=0?.7F:.25F,b=(mask&3)!=0?1F:.25F;
                double x=.5+side.getStepX()*.54,y=.5+side.getStepY()*.54,z=.5+side.getStepZ()*.54;
                LevelRenderer.renderLineBox(poses,lines,x-.09,y-.09,z-.09,x+.09,y+.09,z+.09,r,g,b,.95F);
            }
            poses.translate(.5,2.7,.5);poses.mulPose(camera.rotation());poses.scale(-.015F,-.015F,.015F);
            String title=BuiltInRegistries.BLOCK.get(s.block()).getName().getString();
            mc.font.drawInBatch(title,-mc.font.width(title)/2F,0,0xffc8efff,false,poses.last().pose(),buffers,Font.DisplayMode.NORMAL,0x90202a40,15728880);
            for(int i=0;i<6;i++){String label=s.faces().get(i);mc.font.drawInBatch(label,-mc.font.width(label)/2F,12+i*11,0xffb7e7ff,false,poses.last().pose(),buffers,Font.DisplayMode.NORMAL,0x90202a40,15728880);}
            String footer=s.block().getPath().equals("creative_energy_cell")?(s.energy()>0?"Unlimited GFE | 300,000 FE/t shared":"Admin cell inactive"):
                s.energy()+" / "+s.capacity()+" FE | snapshot, click to refresh";
            mc.font.drawInBatch(footer,-mc.font.width(footer)/2F,82,0xffffe0a0,false,poses.last().pose(),buffers,Font.DisplayMode.NORMAL,0x90202a40,15728880);
        }finally{poses.popPose();buffers.endBatch(RenderType.lines());}
    }
    private MachineDiagnosticRenderer(){}
}
