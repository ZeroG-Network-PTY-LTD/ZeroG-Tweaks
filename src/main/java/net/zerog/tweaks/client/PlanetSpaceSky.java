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
    private static final ResourceLocation TEXTURE=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/environment/universe_v1.png");
    private static final float[] MESH=mesh();
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
            var buffer=Tesselator.getInstance().begin(VertexFormat.Mode.QUADS,DefaultVertexFormat.POSITION_TEX);
            for(int i=0;i<MESH.length;i+=5) buffer.addVertex(view,MESH[i],MESH[i+1],MESH[i+2]).setUv(MESH[i+3],MESH[i+4]);
            BufferUploader.drawWithShader(buffer.buildOrThrow());
        } finally {
            RenderSystem.setShaderColor(1,1,1,1);RenderSystem.enableCull();RenderSystem.depthMask(true);setupFog.run();
        }
        return true;
    }
    private static float[] mesh() {
        int longitude=48,latitude=24,index=0;float[] vertices=new float[longitude*latitude*4*5];
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
}
