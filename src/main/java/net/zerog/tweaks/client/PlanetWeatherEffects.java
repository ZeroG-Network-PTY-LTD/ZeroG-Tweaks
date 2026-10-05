package net.zerog.tweaks.client;

import java.util.Random;
import net.minecraft.client.Minecraft;
import net.minecraft.client.ParticleStatus;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.network.chat.Component;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.client.event.ViewportEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.level.material.FogType;
import net.minecraft.client.renderer.FogRenderer;
import net.zerog.tweaks.registry.ItemInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGWeatherConfig;
import net.zerog.tweaks.worldgen.PlanetEcologyProfile;
import org.joml.Vector3f;

/** Client atmosphere; real rain/storm state and lightning are owned by the server. */
@EventBusSubscriber(modid="zerog_tweaks", value=Dist.CLIENT)
public final class PlanetWeatherEffects {
    private static Level previousLevel;
    private static long lastTick = Long.MIN_VALUE;
    public enum Preview {
        AUTO("Automatic planet cycle"), CLEAR("Clear / stop preview"), FOG("Cold fog"),
        BLIZZARD("Snow blizzard"), STEAM("Steam vents"), ASH("Volcanic ash"),
        GEYSER("Geyser spray"), DUST("Dust clouds"), VORTEX("Dust devil"),
        ACID("Alien acid rain"), ELECTRICAL("Lightning + thunder");
        public final String label;
        Preview(String label) { this.label=label; }
    }
    private static Preview preview=Preview.AUTO;
    private static Preview active=Preview.CLEAR;
    private static float intensity;
    public static Preview activeWeather() { return active; }
    public static float strength() { return intensity; }
    @SubscribeEvent public static void thunder(net.neoforged.neoforge.client.event.sound.PlaySoundEvent event) {
        if(planet(Minecraft.getInstance().level) && !ZGWeatherConfig.THUNDER.get()
                && event.getOriginalSound().getLocation().equals(net.minecraft.sounds.SoundEvents.LIGHTNING_BOLT_THUNDER.getLocation()))
            event.setSound(null);
    }
    public static void setPreview(Preview mode) {
        var client=Minecraft.getInstance();
        if(client.player==null || !client.player.getAbilities().instabuild || !planet(client.level)) return;
        preview=mode;
        client.player.connection.sendCommand("zgweather "+mode.name().toLowerCase(java.util.Locale.ROOT));
        if(mode!=Preview.AUTO && mode!=Preview.CLEAR && ZGWeatherConfig.QUALITY.get()==0) {
            ZGWeatherConfig.QUALITY.set(1); ZGWeatherConfig.SPEC.save();
        }
    }
    private static boolean planet(Level level) {
        return level!=null && level.dimension().location().getNamespace().equals("zerog_tweaks")
                && ZGDimensionTerrain.SOILS.containsKey(level.dimension().location().getPath());
    }
    @SubscribeEvent public static void tester(PlayerInteractEvent.RightClickItem event) {
        if(!event.getLevel().isClientSide()) return;
        if(!event.getItemStack().is(ItemInit.WEATHER_TESTER.get())) return;
        if(!event.getEntity().getAbilities().instabuild) {
            event.getEntity().displayClientMessage(Component.literal("Weather tester requires Creative mode."),true);
            event.setCanceled(true); event.setCancellationResult(InteractionResult.FAIL); return;
        }
        if(!planet(event.getLevel())) {
            event.getEntity().displayClientMessage(Component.literal("Use the weather tester on a ZeroG planet."),true);
        } else Minecraft.getInstance().setScreen(new WeatherTestScreen());
        event.setCanceled(true); event.setCancellationResult(InteractionResult.SUCCESS);
    }
    @SubscribeEvent public static void fog(ViewportEvent.RenderFog event) {
        if(!planet(Minecraft.getInstance().level) || intensity<=.01F || event.getType()!=FogType.NONE
                || event.getMode()!=FogRenderer.FogMode.FOG_TERRAIN) return;
        float distance=switch(active) {case FOG->50; case BLIZZARD->38; case DUST,VORTEX,ASH->72; case ACID->100; default->0;};
        if(distance==0) return;
        event.setFarPlaneDistance(Math.min(event.getFarPlaneDistance(),distance/intensity));
        event.setNearPlaneDistance(Math.min(event.getNearPlaneDistance(),8));
        event.setCanceled(true);
    }

    @SubscribeEvent public static void menu(ScreenEvent.Init.Post event) {
        if (event.getScreen() instanceof TitleScreen screen) {
            event.addListener(Button.builder(Component.literal("ZeroG Weather"), button ->
                    Minecraft.getInstance().setScreen(new PlanetWeatherScreen(screen)))
                    .bounds(4,4,118,20).build());
        }
    }

    @SubscribeEvent public static void tick(ClientTickEvent.Post event) {
        var client = Minecraft.getInstance(); var level = client.level; var player = client.player;
        if (level != previousLevel) { previousLevel=level; lastTick=Long.MIN_VALUE; preview=Preview.AUTO; active=Preview.CLEAR; intensity=0; }
        if (level==null || player==null || client.isPaused()) return;
        if(planet(level) && ZGWeatherConfig.REDUCED_FLASH.get())level.setSkyFlashTime(0);
        if(!planet(level)) {active=Preview.CLEAR;intensity=0;return;}
        long time=level.getGameTime(); if(time==lastTick) return; lastTick=time;
        var dimension=level.dimension().location(); String name=dimension.getPath();
        if(preview!=Preview.AUTO && !player.getAbilities().instabuild) preview=Preview.AUTO;
        long offset=Math.floorMod(name.hashCode(),7200); long phase=Math.floorMod(time+offset,7200);
        String theme=PlanetEcologyProfile.theme(name);
        if(preview==Preview.AUTO) {
            if(phase>=1800 || name.equals("moon") || name.endsWith("_moons")) active=Preview.CLEAR;
            else {
                String biome=level.getBiome(player.blockPosition()).unwrapKey().map(key->key.location().getPath()).orElse("");
                if(biome.contains("acid") || biome.contains("toxic") || biome.contains("mud_flats"))active=Preview.ACID;
                else if(biome.contains("frozen") || biome.contains("glacier") || biome.contains("ice") || biome.contains("polar"))active=Preview.BLIZZARD;
                else if(biome.contains("lava") || biome.contains("ash") || biome.contains("basalt"))active=Preview.ASH;
                else active=switch(theme) {
                case "eidolon"->((time+offset)/7200)%2==0?Preview.BLIZZARD:Preview.FOG;
                case "mars"->((time+offset)/7200)%2==0?Preview.DUST:Preview.VORTEX;
                case "skarn"->Preview.ASH;
                case "solvane"->Preview.ELECTRICAL;
                default->name.contains("toxic") || name.contains("waste")?Preview.ACID:Preview.ELECTRICAL;
            };
            }
        } else active=preview;
        var received=net.zerog.tweaks.event.PlanetStorms.clientState;
        if(received.dimension().equals(dimension.toString()))active=Preview.valueOf(received.value().name());
        float target=active==Preview.CLEAR?0:1;
        intensity+=(target-intensity)*.08F;
        level.setRainLevel(active==Preview.ACID || active==Preview.ELECTRICAL || active==Preview.BLIZZARD?intensity:0);
        level.setThunderLevel(active==Preview.ELECTRICAL?intensity:0);
        if(active==Preview.CLEAR) return;
        if((active==Preview.DUST || active==Preview.VORTEX) && net.zerog.tweaks.item.ZGArmorSetBonuses.dustProtected(player))return;
        // Native precipitation is not a particle-quality option, and real bolts
        // are synchronized entities. Do not substitute dust/sparks or duplicate bolts.
        if(active==Preview.ACID || active==Preview.ELECTRICAL || ZGWeatherConfig.QUALITY.get()==0)return;
        var origin=player.blockPosition();
        if(!level.canSeeSky(origin) || player.isUnderWater()) return;
        var particles=client.options.particles().get(); if(particles==ParticleStatus.MINIMAL) return;
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
        if(active==Preview.ACID) colour=new Vector3f(.48F,.85F,.22F);
        boolean largeVortex=active==Preview.VORTEX;
        for(int i=0;i<budget;i++) {
            double x=player.getX()+random.nextDouble()*30-15;
            double z=player.getZ()+random.nextDouble()*30-15;
            double y=player.getY()+random.nextDouble()*8;
            if(active==Preview.VORTEX) {
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
            } else if(active==Preview.BLIZZARD) {
                level.addParticle(ParticleTypes.SNOWFLAKE,x,y,z,0.24,-0.12,0.08);
            } else if(active==Preview.STEAM || active==Preview.FOG) {
                level.addParticle(ParticleTypes.CAMPFIRE_COSY_SMOKE,x,y,z,0.025,0.035,0.01);
            } else if(active==Preview.GEYSER) {
                level.addParticle(ParticleTypes.CLOUD,player.getX()+4+random.nextGaussian()*.4,
                        player.getY()+random.nextDouble()*6,player.getZ()+random.nextGaussian()*.4,0,.35,0);
            } else if(active==Preview.ASH) {
                level.addParticle(ParticleTypes.ASH,x,y,z,0.07,-0.025,0.02);
            } else {
                level.addParticle(new DustParticleOptions(colour,1.3f),x,y,z,0.14,0.006,0.04);
            }
        }
    }

    private PlanetWeatherEffects() {}
}
