package net.zerog.tweaks.client;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.*;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.level.levelgen.Heightmap;

/** Native rain-sheet layout, roof height clipping and scrolling UVs; green vertex tint only.
 * Uses the user's vanilla/resource-pack precipitation texture, never replaces it globally.
 */
public final class PlanetPrecipitation {
    public static boolean tick(ClientLevel level,int ticks,net.minecraft.client.Camera camera) {
        var mode=PlanetWeatherEffects.activeWeather();
        if(mode!=PlanetWeatherEffects.Preview.ACID && mode!=PlanetWeatherEffects.Preview.ELECTRICAL)return true;
        if(PlanetWeatherEffects.strength()<.1F)return true;
        var client=Minecraft.getInstance();var random=new java.util.Random(ticks*312987231L);
        var cameraPos=BlockPos.containing(camera.getPosition());
        BlockPos audible=null;
        int budget=client.options.particles().get()==net.minecraft.client.ParticleStatus.MINIMAL?1:12;
        for(int i=0;i<budget;i++) {
            var column=cameraPos.offset(random.nextInt(21)-10,0,random.nextInt(21)-10);
            if(!level.hasChunkAt(column))continue;
            var surface=level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING,column);
            if(Math.abs(surface.getY()-cameraPos.getY())>10 || !level.canSeeSky(surface))continue;
            audible=surface;
            if(client.options.particles().get()!=net.minecraft.client.ParticleStatus.MINIMAL) {
                var particle=client.particleEngine.createParticle(net.minecraft.core.particles.ParticleTypes.RAIN,
                        surface.getX()+random.nextDouble(),surface.getY()+.02,surface.getZ()+random.nextDouble(),0,0,0);
                if(particle!=null && mode==PlanetWeatherEffects.Preview.ACID)particle.setColor(.42F,1,.18F);
            }
        }
        if(audible!=null && ticks%10==0) {
            boolean roof=level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING,cameraPos).getY()>cameraPos.getY()+1;
            level.playLocalSound(audible,roof?net.minecraft.sounds.SoundEvents.WEATHER_RAIN_ABOVE:net.minecraft.sounds.SoundEvents.WEATHER_RAIN,
                    net.minecraft.sounds.SoundSource.WEATHER,roof?.1F:.2F,roof?.5F:1,false);
        }
        return true;
    }
    public static boolean render(ClientLevel level,int ticks,float partial,LightTexture light,double cx,double cy,double cz) {
        var mode=PlanetWeatherEffects.activeWeather();
        boolean snow=mode==PlanetWeatherEffects.Preview.BLIZZARD;
        if(!snow && mode!=PlanetWeatherEffects.Preview.ACID && mode!=PlanetWeatherEffects.Preview.ELECTRICAL)return true;
        float strength=PlanetWeatherEffects.strength();if(strength<.01F)return true;
        boolean acid=mode==PlanetWeatherEffects.Preview.ACID;
        int radius=Minecraft.useFancyGraphics()?10:5,ix=Mth.floor(cx),iy=Mth.floor(cy),iz=Mth.floor(cz);
        light.turnOnLightLayer();RenderSystem.disableCull();RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();RenderSystem.enableDepthTest();RenderSystem.depthMask(Minecraft.useShaderTransparency());
        RenderSystem.setShader(GameRenderer::getParticleShader);
        RenderSystem.setShaderTexture(0,ResourceLocation.withDefaultNamespace("textures/environment/"+(snow?"snow":"rain")+".png"));
        try {
            var buffer=Tesselator.getInstance().begin(VertexFormat.Mode.QUADS,DefaultVertexFormat.PARTICLE);
            int count=0;
            for(int z=iz-radius;z<=iz+radius;z++)for(int x=ix-radius;x<=ix+radius;x++) {
                var column=new BlockPos(x,0,z);if(!level.hasChunkAt(column))continue;
                int floor=level.getHeight(Heightmap.Types.MOTION_BLOCKING,x,z);
                int low=Math.max(iy-radius,floor),high=Math.max(iy+radius,floor);if(low==high)continue;
                double dx=x+.5-cx,dz=z+.5-cz,distance=Math.sqrt(dx*dx+dz*dz);
                // Tangent to each column faces the viewer, as vanilla's cached rainSize arrays do.
                double length=Math.hypot(x-ix,z-iz);if(length==0)continue;
                float halfX=(float)(-(z-iz)/length*.5),halfZ=(float)((x-ix)/length*.5);
                int seed=x*x*3121+x*45238971+z*z*418711+z*13761;
                var random=new java.util.Random(seed);
                float speed=snow?.06F:(3+random.nextFloat())/32;
                float scroll=-(((ticks&131071)+(seed&255))+partial)*speed;
                float alpha=Mth.clamp((1-(float)(distance*distance)/(radius*radius))*.5F+.5F,0,1)*strength;
                int packed=LevelRenderer.getLightColor(level,new BlockPos(x,Math.max(floor,iy),z));
                float red=acid?.42F:1,green=acid?1:1,blue=acid?.18F:1;
                float left=(float)dx-halfX,right=(float)dx+halfX,front=(float)dz-halfZ,back=(float)dz+halfZ;
                buffer.addVertex(left,(float)(high-cy),front).setUv(0,low*.25F+scroll).setColor(red,green,blue,alpha).setLight(packed);
                buffer.addVertex(right,(float)(high-cy),back).setUv(1,low*.25F+scroll).setColor(red,green,blue,alpha).setLight(packed);
                buffer.addVertex(right,(float)(low-cy),back).setUv(1,high*.25F+scroll).setColor(red,green,blue,alpha).setLight(packed);
                buffer.addVertex(left,(float)(low-cy),front).setUv(0,high*.25F+scroll).setColor(red,green,blue,alpha).setLight(packed);
                count++;
            }
            if(count>0)BufferUploader.drawWithShader(buffer.buildOrThrow());else buffer.build();
        } finally {
            RenderSystem.enableCull();RenderSystem.disableBlend();RenderSystem.depthMask(true);light.turnOffLightLayer();
        }
        return true;
    }
    private PlanetPrecipitation() {}
}
