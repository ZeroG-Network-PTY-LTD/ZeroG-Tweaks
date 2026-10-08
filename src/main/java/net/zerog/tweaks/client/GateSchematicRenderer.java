package net.zerog.tweaks.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.RenderType;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;
import net.zerog.tweaks.travel.GateSchematicSync;
import net.zerog.tweaks.travel.SurvivalGateLayout;

/** Temporary wireframe overlay; no chunk tickets, block changes or automatic construction. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class GateSchematicRenderer {
    private static GateSchematicSync.Plan lastPlan;
    private static java.util.List<net.zerog.tweaks.travel.PlanetGate.Part> parts=java.util.List.of();
    private static long planTick=Long.MIN_VALUE;
    @SubscribeEvent public static void logout(net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent.LoggingOut event){
        GateSchematicSync.clear();lastPlan=null;parts=java.util.List.of();
    }
    @SubscribeEvent public static void render(RenderLevelStageEvent event){
        if(event.getStage()!=RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS)return;
        var client=Minecraft.getInstance();var plan=GateSchematicSync.pending();
        if(plan==null)return;
        if(client.level==null||client.player==null||!client.level.dimension().location().equals(plan.dimension())){GateSchematicSync.clear();return;}
        if(client.player.distanceToSqr(plan.controller().getCenter())>48*48){GateSchematicSync.clear();return;}
        long tick=client.level.getGameTime()/10;
        if(!plan.equals(lastPlan)||tick!=planTick){parts=net.zerog.tweaks.travel.SurvivalGateFormation.displayPlan(client.level,plan.centre(),plan.facing(),plan.tier(),plan.controller());lastPlan=plan;planTick=tick;}
        var camera=event.getCamera().getPosition();var stack=event.getPoseStack();
        var buffers=client.renderBuffers().bufferSource();var lines=buffers.getBuffer(RenderType.lines());
        stack.pushPose();
        try {
            stack.translate(-camera.x,-camera.y,-camera.z);
            for(var part:parts){
                var pos=plan.centre().offset(SurvivalGateLayout.rotate(part.offset(),plan.facing()));
                if(!client.level.hasChunkAt(pos))continue;
                var state=client.level.getBlockState(pos);
                boolean complete=state.is(part.block()),empty=state.isAir();
                // Green: correct. Cyan: absent. Red: a different block occupies the slot.
                float r=complete?.25F:empty?.25F:1F,g=complete?1F:empty?.85F:.25F,b=complete?.4F:empty?1F:.25F;
                LevelRenderer.renderLineBox(stack,lines,pos.getX()-.005,pos.getY()-.005,pos.getZ()-.005,
                        pos.getX()+1.005,pos.getY()+1.005,pos.getZ()+1.005,r,g,b,.8F);
            }
        } finally {stack.popPose();buffers.endBatch(RenderType.lines());}
    }
    private GateSchematicRenderer(){}
}
