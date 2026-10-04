package net.zerog.tweaks.client;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferUploader;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexFormat;
import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.DimensionSpecialEffects;
import net.minecraft.client.renderer.FogRenderer;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.material.FogType;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterDimensionSpecialEffectsEvent;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;
import org.joml.Matrix4f;

/** Vanilla planet sky and clouds, with a larger coloured star overlay after native rendering. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
public final class PlanetSpaceSky extends DimensionSpecialEffects {
    public static final ResourceLocation EFFECT=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","space");
    private static final float[][] STARS=stars();
    private PlanetSpaceSky() { super(192,true,SkyType.NORMAL,false,false); }
    @SubscribeEvent public static void register(RegisterDimensionSpecialEffectsEvent event) { event.register(EFFECT,new PlanetSpaceSky()); }
    @Override public Vec3 getBrightnessDependentFogColor(Vec3 colour,float daylight) {
        return colour.multiply(daylight*.94+.06,daylight*.94+.06,daylight*.91+.09);
    }
    @Override public boolean isFoggyAt(int x,int y) { return false; }
    @Override public boolean renderSnowAndRain(ClientLevel level,int ticks,float partialTick,LightTexture light,double x,double y,double z) {
        return PlanetPrecipitation.render(level,ticks,partialTick,light,x,y,z);
    }
    @Override public boolean tickRain(ClientLevel level,int ticks,Camera camera) { return PlanetPrecipitation.tick(level,ticks,camera); }
    @Override public boolean renderClouds(ClientLevel level,int ticks,float partialTick,com.mojang.blaze3d.vertex.PoseStack stack,
            double x,double y,double z,Matrix4f view,Matrix4f projection) { return false; }
    @Override public boolean renderSky(ClientLevel level,int ticks,float partialTick,Matrix4f view,
                                      Camera camera,Matrix4f projection,boolean foggy,Runnable setupFog) {
        // Delegate to Minecraft's native sky, sun, moon and sunrise. No galaxy backdrop.
        return false;
    }
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
    public static final class StarOverlay {
        @SubscribeEvent public static void render(RenderLevelStageEvent event) {
            if(event.getStage()!=RenderLevelStageEvent.Stage.AFTER_SKY)return;
            var client=Minecraft.getInstance();var level=client.level;
            if(level==null || !(level.effects() instanceof PlanetSpaceSky))return;
            Camera camera=event.getCamera();
            if(camera.getFluidInCamera()!=FogType.NONE || (camera.getEntity() instanceof LivingEntity living
                    && (living.hasEffect(MobEffects.BLINDNESS)||living.hasEffect(MobEffects.DARKNESS))))return;
            float partialTick=event.getPartialTick().getGameTimeDeltaPartialTick(false);
            float visibility=level.getStarBrightness(partialTick)*(1-level.getRainLevel(partialTick));
            if(visibility<=.001F)return;
            double time=level.getGameTime()+partialTick;
            float offset=(level.dimension().location().hashCode()&65535)/65535F*(float)(Math.PI*2);
            // Native celestial rotation, with a stable different scattering orientation per planet.
            var skyView=new Matrix4f(event.getModelViewMatrix()).rotateY((float)-Math.PI/2)
                    .rotateX(level.getTimeOfDay(partialTick)*(float)(Math.PI*2)).rotateY(offset);
            FogRenderer.setupNoFog();
            RenderSystem.depthMask(false);RenderSystem.disableCull();
            try {
            RenderSystem.enableBlend();RenderSystem.defaultBlendFunc();RenderSystem.setShaderColor(1,1,1,1);RenderSystem.setShader(GameRenderer::getPositionColorShader);
            var starBuffer=Tesselator.getInstance().begin(VertexFormat.Mode.QUADS,DefaultVertexFormat.POSITION_COLOR);
            for(var star:STARS) {
                double shimmer=.5+.5*Math.sin(time*star[10]+star[9]);
                int alpha=(int)((180+75*shimmer)*Math.min(1,visibility*2));
                // Slow independent colour cycles, not synchronized flashes.
                int[] colour=colour(time,star[9]);
                int red=colour[0],green=colour[1],blue=colour[2];
                for(int[] corner:new int[][]{{-1,-1},{1,-1},{1,1},{-1,1}})
                    starBuffer.addVertex(skyView,star[0]+corner[0]*star[3]+corner[1]*star[6],
                            star[1]+corner[0]*star[4]+corner[1]*star[7],star[2]+corner[0]*star[5]+corner[1]*star[8])
                            .setColor(red,green,blue,alpha);
            }
            BufferUploader.drawWithShader(starBuffer.buildOrThrow());
            // Radial translucent halos; no square texture borders around the stars.
            var halos=Tesselator.getInstance().begin(VertexFormat.Mode.TRIANGLES,DefaultVertexFormat.POSITION_COLOR);
            for(var star:STARS) {
                int[] colour=colour(time,star[9]);
                int red=colour[0],green=colour[1],blue=colour[2];
                int alpha=(int)((18+14*(.5+.5*Math.sin(time*star[10]+star[9])))*Math.min(1,visibility*2));
                for(int segment=0;segment<12;segment++) {
                    halos.addVertex(skyView,star[0],star[1],star[2]).setColor(red,green,blue,alpha);
                    for(int end=0;end<2;end++) {
                        double haloAngle=(segment+end)*Math.PI/6;
                        float a=(float)Math.cos(haloAngle)*3,b=(float)Math.sin(haloAngle)*3;
                        halos.addVertex(skyView,star[0]+a*star[3]+b*star[6],star[1]+a*star[4]+b*star[7],
                                star[2]+a*star[5]+b*star[8]).setColor(red,green,blue,0);
                    }
                }
            }
            BufferUploader.drawWithShader(halos.buildOrThrow());

            } finally {
                RenderSystem.disableBlend();RenderSystem.defaultBlendFunc();RenderSystem.setShaderColor(1,1,1,1);
                RenderSystem.enableCull();RenderSystem.depthMask(true);
                FogRenderer.setupFog(camera,FogRenderer.FogMode.FOG_SKY,client.gameRenderer.getRenderDistance(),false,partialTick);
            }
        }
    }
    private static final int[][] PALETTE={{115,240,158},{112,181,255},{255,225,124},{205,139,255}};
    static int[] colour(double time,float phase) {
        double cycle=(time/2400+phase)%PALETTE.length;int index=(int)cycle;
        double mix=cycle-index;mix=mix*mix*(3-2*mix);
        int[] result=new int[3];
        for(int c=0;c<3;c++)result[c]=(int)Math.round(PALETTE[index][c]*(1-mix)+PALETTE[(index+1)%PALETTE.length][c]*mix);
        return result;
    }
    private static float[][] stars() {
        var random=new java.util.Random(729411L);var result=new float[480][11];
        for(var star:result) {
            double phi=Math.acos(2*random.nextDouble()-1),theta=random.nextDouble()*Math.PI*2;
            var normal=new org.joml.Vector3f((float)(Math.sin(phi)*Math.cos(theta)),(float)Math.cos(phi),(float)(Math.sin(phi)*Math.sin(theta)));
            var axis=Math.abs(normal.y)>.99F?new org.joml.Vector3f(1,0,0):new org.joml.Vector3f(0,1,0);
            var tangent=new org.joml.Vector3f(normal).cross(axis).normalize();
            var second=new org.joml.Vector3f(normal).cross(tangent).normalize();
            float size=.35F+random.nextFloat()*.55F;
            star[0]=normal.x*99;star[1]=normal.y*99;star[2]=normal.z*99;
            star[3]=tangent.x*size;star[4]=tangent.y*size;star[5]=tangent.z*size;
            star[6]=second.x*size;star[7]=second.y*size;star[8]=second.z*size;star[9]=random.nextFloat()*4;
            star[10]=.004F+random.nextFloat()*.006F;
        }
        return result;
    }
}
