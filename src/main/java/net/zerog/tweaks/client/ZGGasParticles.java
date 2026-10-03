package net.zerog.tweaks.client;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.CampfireSmokeParticle;
import net.minecraft.client.particle.SpriteSet;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterParticleProvidersEvent;
import net.zerog.tweaks.registry.ZGGasVents;

/** Vanilla campfire smoke motion and fade, with six tint colours. Vanilla sprites are referenced, not redistributed. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class ZGGasParticles {
    @SubscribeEvent public static void register(RegisterParticleProvidersEvent event) {
        ZGGasVents.SMOKE.forEach((planet,type)->event.registerSpriteSet(type.get(),sprites->
                (particle,level,x,y,z,vx,vy,vz)->new ColouredSmoke(level,x,y,z,vx,vy,vz,sprites,ZGGasVents.COLOURS.get(planet))));
    }
    private static final class ColouredSmoke extends CampfireSmokeParticle {
        ColouredSmoke(ClientLevel level,double x,double y,double z,double vx,double vy,double vz,SpriteSet sprites,int colour) {
            super(level,x,y,z,vx,vy,vz,true);pickSprite(sprites);setAlpha(.8F);
            setColor(((colour>>16)&255)/255F,((colour>>8)&255)/255F,(colour&255)/255F);
        }
    }
}
