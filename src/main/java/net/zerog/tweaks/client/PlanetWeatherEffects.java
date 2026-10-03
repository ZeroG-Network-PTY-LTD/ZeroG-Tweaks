package net.zerog.tweaks.client;

import java.util.Random;
import net.minecraft.client.Minecraft;
import net.minecraft.client.ParticleStatus;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.network.chat.Component;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGWeatherConfig;
import net.zerog.tweaks.worldgen.PlanetEcologyProfile;
import org.joml.Vector3f;

/** Opt-in local atmosphere: never modifies blocks, server RNG or living entities. */
@EventBusSubscriber(modid="zerog_tweaks", value=Dist.CLIENT)
public final class PlanetWeatherEffects {
    private static Level previousLevel;
    private static long lastTick = Long.MIN_VALUE;
    private static int boltId = -1000000;

    @SubscribeEvent public static void menu(ScreenEvent.Init.Post event) {
        if (event.getScreen() instanceof TitleScreen screen) {
            event.addListener(Button.builder(Component.literal("ZeroG Weather"), button ->
                    Minecraft.getInstance().setScreen(new PlanetWeatherScreen(screen)))
                    .bounds(4,4,118,20).build());
        }
    }

    @SubscribeEvent public static void tick(ClientTickEvent.Post event) {
        var client = Minecraft.getInstance(); var level = client.level; var player = client.player;
        if (level != previousLevel) { previousLevel=level; lastTick=Long.MIN_VALUE; }
        if (level==null || player==null || client.isPaused() || ZGWeatherConfig.QUALITY.get()==0) return;
        long time=level.getGameTime(); if(time==lastTick) return; lastTick=time;
        var dimension=level.dimension().location(); String name=dimension.getPath();
        if(!dimension.getNamespace().equals("zerog_tweaks") || !ZGDimensionTerrain.SOILS.containsKey(name)
                || name.equals("moon") || name.endsWith("_moons")) return;
        var origin=player.blockPosition();
        if(!level.canSeeSky(origin) || player.isUnderWater()) return;
        var particles=client.options.particles().get(); if(particles==ParticleStatus.MINIMAL) return;
        // Six-minute cycles, 90-second active windows, reproducible for each dimension.
        long offset=Math.floorMod(name.hashCode(),7200); long phase=Math.floorMod(time+offset,7200);
        if(phase>=1800) return;
        String theme=PlanetEcologyProfile.theme(name);
        var random=new Random(time ^ ((long)name.hashCode()<<32));
        int budget=ZGWeatherConfig.QUALITY.get()==1 ? 4 : 12;
        if(particles==ParticleStatus.DECREASED) budget=Math.max(1,budget/2);
        Vector3f colour=switch(theme) {
            case "mars" -> new Vector3f(0.72f,0.39f,0.23f);
            case "skarn" -> new Vector3f(0.35f,0.28f,0.24f);
            case "eidolon" -> new Vector3f(0.47f,0.77f,0.90f);
            case "solvane" -> new Vector3f(0.93f,0.64f,0.20f);
            default -> new Vector3f(0.35f,0.67f,0.79f);
        };
        boolean largeVortex=Math.floorMod((time+offset)/7200,3)==0;
        for(int i=0;i<budget;i++) {
            double x=player.getX()+random.nextDouble()*30-15;
            double z=player.getZ()+random.nextDouble()*30-15;
            double y=player.getY()+random.nextDouble()*8;
            if(i%2==0 && !theme.equals("eidolon")) {
                // Half the budget forms a moving funnel; no collision or suction.
                double centreX=player.getX()+Math.sin((time+offset)*0.0008)*22;
                double centreZ=player.getZ()+Math.cos((time+offset)*0.0008)*22;
                var base=new BlockPos((int)Math.floor(centreX),0,(int)Math.floor(centreZ));
                if(!level.hasChunkAt(base)) continue;
                double height=largeVortex?18:7;
                double fraction=random.nextDouble();
                double radius=0.5+fraction*(largeVortex?5:2);
                double angle=time*0.24+fraction*9+i;
                x=centreX+Math.cos(angle)*radius;z=centreZ+Math.sin(angle)*radius;
                y=level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,base.getX(),base.getZ())+fraction*height;
                level.addParticle(new DustParticleOptions(colour,largeVortex?1.8f:1.1f),x,y,z,
                        -Math.sin(angle)*0.12,0.045,Math.cos(angle)*0.12);
            } else if(theme.equals("eidolon")) {
                level.addParticle(ParticleTypes.SNOWFLAKE,x,y,z,0.06,-0.035,0.02);
            } else if(theme.equals("cerulon")) {
                level.addParticle(ParticleTypes.SPORE_BLOSSOM_AIR,x,y,z,0.025,-0.008,0);
            } else if(theme.equals("solvane")) {
                level.addParticle(ParticleTypes.ELECTRIC_SPARK,x,y,z,0.10,0.01,0.02);
            } else {
                level.addParticle(new DustParticleOptions(colour,1.3f),x,y,z,0.14,0.006,0.04);
            }
        }
        if((theme.equals("cerulon") || theme.equals("solvane")) && phase%600==120) {
            double angle=random.nextDouble()*Math.PI*2;
            double x=player.getX()+Math.cos(angle)*40,z=player.getZ()+Math.sin(angle)*40;
            var pos=BlockPos.containing(x,0,z); if(!level.hasChunkAt(pos)) return;
            double y=level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,pos.getX(),pos.getZ());
            var bolt=new CosmeticBolt(level); bolt.setPos(x,y,z);
            while(level.getEntity(boltId)!=null) boltId--;
            bolt.setId(boltId--); level.addEntity(bolt);
            if(ZGWeatherConfig.THUNDER.get()) level.playLocalSound(x,y,z,SoundEvents.LIGHTNING_BOLT_THUNDER,
                    SoundSource.WEATHER,2.0f,0.85f+random.nextFloat()*0.2f,true);
        }
    }

    /** Reuses vanilla bolt rendering, but skips native fire/damage/loud sound logic. */
    private static final class CosmeticBolt extends LightningBolt {
        private int age;
        CosmeticBolt(Level level) { super(EntityType.LIGHTNING_BOLT,level); setVisualOnly(true); }
        @Override public void tick() {
            if(++age>=5) discard();
            else if(!ZGWeatherConfig.REDUCED_FLASH.get()) level().setSkyFlashTime(1);
        }
    }
    private PlanetWeatherEffects() {}
}
