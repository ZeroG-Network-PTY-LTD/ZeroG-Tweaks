package net.zerog.tweaks.client;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferUploader;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexFormat;
import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.DimensionSpecialEffects;
import net.minecraft.client.renderer.FogRenderer;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.material.FogType;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterDimensionSpecialEffectsEvent;
import org.joml.Matrix4f;

/** Client-only panoramic sky; never replaces the built-in Overworld effects. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
public final class PlanetSpaceSky extends DimensionSpecialEffects {
    public static final ResourceLocation EFFECT=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","space");
    private static final ResourceLocation TEXTURE=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/environment/universe_v2.png");
    private static final float[] MESH=mesh();
    private static final float[][] STARS=stars();
    private PlanetSpaceSky() { super(Float.NaN,false,SkyType.NORMAL,false,false); }
    @SubscribeEvent public static void register(RegisterDimensionSpecialEffectsEvent event) { event.register(EFFECT,new PlanetSpaceSky()); }
    @Override public Vec3 getBrightnessDependentFogColor(Vec3 colour,float daylight) {
        return colour.multiply(daylight*.94+.06,daylight*.94+.06,daylight*.91+.09);
    }
    @Override public boolean isFoggyAt(int x,int y) { return false; }
    @Override public float[] getSunriseColor(float time,float partialTick) { return null; }
    @Override public boolean renderSky(ClientLevel level,int ticks,float partialTick,Matrix4f view,
                                      Camera camera,Matrix4f projection,boolean foggy,Runnable setupFog) {
        setupFog.run();
        if(foggy || camera.getFluidInCamera()!=FogType.NONE || (camera.getEntity() instanceof LivingEntity living
                && (living.hasEffect(MobEffects.BLINDNESS)||living.hasEffect(MobEffects.DARKNESS)))) return true;
        RenderSystem.depthMask(false);RenderSystem.disableCull();RenderSystem.disableBlend();
        FogRenderer.setupNoFog();RenderSystem.setShader(GameRenderer::getPositionTexShader);
        RenderSystem.setShaderTexture(0,TEXTURE);RenderSystem.setShaderColor(1,1,1,1);
        try {
            // A full slow orbit in two game days, interpolated between ticks.
            // Dimension offsets show different regions of the surrounding universe.
            double time=level.getGameTime()+partialTick;
            float angle=(float)((time%48000)/48000*Math.PI*2
                    +(level.dimension().location().hashCode()&65535)/65535.0*Math.PI*2);
            var skyView=new Matrix4f(view).rotateY(angle).rotateZ(.13F);
            var buffer=Tesselator.getInstance().begin(VertexFormat.Mode.QUADS,DefaultVertexFormat.POSITION_TEX);
            for(int i=0;i<MESH.length;i+=5) buffer.addVertex(skyView,MESH[i],MESH[i+1],MESH[i+2]).setUv(MESH[i+3],MESH[i+4]);
            BufferUploader.drawWithShader(buffer.buildOrThrow());
            RenderSystem.enableBlend();RenderSystem.defaultBlendFunc();RenderSystem.setShader(GameRenderer::getPositionColorShader);
            var starBuffer=Tesselator.getInstance().begin(VertexFormat.Mode.QUADS,DefaultVertexFormat.POSITION_COLOR);
            for(var star:STARS) {
                int alpha=(int)(85+100*(.5+.5*Math.sin(time*.035+star[9])));
                for(int[] corner:new int[][]{{-1,-1},{1,-1},{1,1},{-1,1}})
                    starBuffer.addVertex(skyView,star[0]+corner[0]*star[3]+corner[1]*star[6],
                            star[1]+corner[0]*star[4]+corner[1]*star[7],star[2]+corner[0]*star[5]+corner[1]*star[8])
                            .setColor(200,222,255,alpha);
            }
            BufferUploader.drawWithShader(starBuffer.buildOrThrow());
        } finally {
            RenderSystem.disableBlend();RenderSystem.setShaderColor(1,1,1,1);RenderSystem.enableCull();RenderSystem.depthMask(true);setupFog.run();
        }
        return true;
    }
    private static float[] mesh() {
        int longitude=96,latitude=48,index=0;float[] vertices=new float[longitude*latitude*4*5];
        for(int y=0;y<latitude;y++) for(int x=0;x<longitude;x++) {
            for(int[] corner:new int[][]{{0,0},{1,0},{1,1},{0,1}}) {
                float u=(x+corner[0])/(float)longitude,v=(y+corner[1])/(float)latitude;
                double theta=u*Math.PI*2,phi=v*Math.PI;
                vertices[index++]=(float)(100*Math.sin(phi)*Math.cos(theta));
                vertices[index++]=(float)(100*Math.cos(phi));
                vertices[index++]=(float)(100*Math.sin(phi)*Math.sin(theta));
                vertices[index++]=u;vertices[index++]=v;
            }
        }
        return vertices;
    }
    private static float[][] stars() {
        var random=new java.util.Random(729411L);var result=new float[240][10];
        for(var star:result) {
            double phi=Math.acos(2*random.nextDouble()-1),theta=random.nextDouble()*Math.PI*2;
            var normal=new org.joml.Vector3f((float)(Math.sin(phi)*Math.cos(theta)),(float)Math.cos(phi),(float)(Math.sin(phi)*Math.sin(theta)));
            var tangent=new org.joml.Vector3f(normal).cross(new org.joml.Vector3f(0,1,0)).normalize();
            var second=new org.joml.Vector3f(normal).cross(tangent).normalize();
            float size=.018F+random.nextFloat()*.045F;
            star[0]=normal.x*99;star[1]=normal.y*99;star[2]=normal.z*99;
            star[3]=tangent.x*size;star[4]=tangent.y*size;star[5]=tangent.z*size;
            star[6]=second.x*size;star[7]=second.y*size;star[8]=second.z*size;star[9]=random.nextFloat()*6.28F;
        }
        return result;
    }
}
