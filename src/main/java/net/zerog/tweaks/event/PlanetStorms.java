package net.zerog.tweaks.event;

import java.util.Locale;
import java.util.WeakHashMap;
import com.mojang.brigadier.arguments.StringArgumentType;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.tick.LevelTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.travel.GateLedger;
import net.zerog.tweaks.worldgen.PlanetEcologyProfile;

/** Server-owned storms. No client thread accesses a server level or its RNG. */
@EventBusSubscriber(modid="zerog_tweaks")
public final class PlanetStorms {
    /** Owner-requested build pause. Old configuration and admin tools cannot re-enable it. */
    public static boolean enabled() { return false; }
    public enum Mode {
        AUTO, CLEAR, FOG, BLIZZARD, STEAM, ASH, GEYSER, DUST, VORTEX, ACID, ELECTRICAL;
        public boolean rain() { return this==ACID || this==ELECTRICAL || this==BLIZZARD; }
    }
    private static final WeakHashMap<ServerLevel,Mode> OVERRIDES=new WeakHashMap<>();
    // Receipt is stored without referring to client-only classes on dedicated servers.
    public static volatile State clientState=new State("",Mode.CLEAR.ordinal());
    public record State(String dimension,int mode) implements CustomPacketPayload {
        public static final Type<State> TYPE=new Type<>(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planet_weather"));
        public static final StreamCodec<RegistryFriendlyByteBuf,State> CODEC=StreamCodec.composite(
                ByteBufCodecs.STRING_UTF8,State::dimension,ByteBufCodecs.VAR_INT,State::mode,State::new);
        @Override public Type<State> type() { return TYPE; }
        public Mode value() { return mode>=0 && mode<Mode.values().length?Mode.values()[mode]:Mode.CLEAR; }
    }
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD)
    public static final class Networking {
        @SubscribeEvent public static void register(RegisterPayloadHandlersEvent event) {
            event.registrar("1").playToClient(State.TYPE,State.CODEC,
                    (state,context)->context.enqueueWork(()->clientState=state));
        }
    }
    public static boolean planet(net.minecraft.world.level.Level level) {
        return level.dimension().location().getNamespace().equals("zerog_tweaks")
                && ZGDimensionTerrain.SOILS.containsKey(level.dimension().location().getPath());
    }
    public static Mode automatic(String name,long time,String biome) {
        if(!enabled())return Mode.CLEAR;
        long offset=Math.floorMod(name.hashCode(),7200);
        if(Math.floorMod(time+offset,7200)>=1800 || name.equals("moon") || name.endsWith("_moons"))return Mode.CLEAR;
        if(biome.contains("acid")||biome.contains("toxic")||biome.contains("mud_flats"))return Mode.ACID;
        if(biome.contains("frozen")||biome.contains("glacier")||biome.contains("ice")||biome.contains("polar"))return Mode.BLIZZARD;
        if(biome.contains("lava")||biome.contains("ash")||biome.contains("basalt"))return Mode.ASH;
        return switch(PlanetEcologyProfile.theme(name)) {
            case "eidolon"->((time+offset)/7200)%2==0?Mode.BLIZZARD:Mode.FOG;
            case "mars"->((time+offset)/7200)%2==0?Mode.DUST:Mode.VORTEX;
            case "skarn"->Mode.ASH;
            default->Mode.ELECTRICAL;
        };
    }
    public static void override(ServerLevel level,Mode mode) {
        if(!level.getServer().isSameThread())throw new IllegalStateException("Weather requires server thread");
        if(!enabled())return;
        OVERRIDES.put(level,mode); apply(level,mode==Mode.AUTO?Mode.CLEAR:mode);
    }
    @SubscribeEvent public static void commands(RegisterCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("zgweather").requires(source->source.hasPermission(2)
                || source.getEntity() instanceof net.minecraft.server.level.ServerPlayer player && player.getAbilities().instabuild)
            .then(Commands.argument("mode",StringArgumentType.word()).executes(context->{
                if(!enabled()){
                    context.getSource().sendFailure(net.minecraft.network.chat.Component.literal("Custom ZeroG weather is disabled in this build; vanilla weather is unchanged."));
                    return 0;
                }
                var level=context.getSource().getLevel(); if(!planet(level))return 0;
                Mode mode;try {mode=Mode.valueOf(StringArgumentType.getString(context,"mode").toUpperCase(Locale.ROOT));}
                catch(IllegalArgumentException ex){return 0;}
                override(level,mode);return 1;
            })));
    }
    private static void apply(ServerLevel level,Mode mode) {
        // DerivedLevelData weather setters are no-ops on custom dimensions.
        // Set this level's native strengths, not shared Overworld weather data.
        level.setRainLevel(mode.rain()?1:0);level.setThunderLevel(mode==Mode.ELECTRICAL?1:0);
        if(level.getGameTime()%20==0)PacketDistributor.sendToPlayersInDimension(level,new State(level.dimension().location().toString(),mode.ordinal()));
    }
    @SubscribeEvent public static void tick(LevelTickEvent.Post event) {
        if(!enabled())return;
        if(!(event.getLevel() instanceof ServerLevel level) || !planet(level) || level.players().isEmpty()
                )return;
        String biome=level.getBiome(level.players().getFirst().blockPosition()).unwrapKey().map(k->k.location().getPath()).orElse("");
        Mode mode=OVERRIDES.getOrDefault(level,Mode.AUTO);
        if(mode==Mode.AUTO)mode=automatic(level.dimension().location().getPath(),level.getGameTime(),biome);
        apply(level,mode);
        // One strike attempt per ten seconds per occupied planet, never per player.
        if(mode!=Mode.ELECTRICAL || level.getGameTime()%200!=0)return;
        var player=level.players().get(level.random.nextInt(level.players().size()));
        double angle=level.random.nextDouble()*Math.PI*2,radius=32+level.random.nextInt(65);
        var column=BlockPos.containing(player.getX()+Math.cos(angle)*radius,0,player.getZ()+Math.sin(angle)*radius);
        if(!level.hasChunkAt(column))return;
        BlockPos pos=level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING,column);
        strike(level,pos);
    }
    public static boolean safeStrike(ServerLevel level,BlockPos pos) {
        String dimension=level.dimension().location().toString();
        return GateLedger.get(level.getServer()).gates.values().stream().noneMatch(g->g.testPower && g.dimension.equals(dimension)
                && Math.abs((long)pos.getX()-g.centre.getX())<=24 && Math.abs((long)pos.getZ()-g.centre.getZ())<=24);
    }
    public static boolean strike(ServerLevel level,BlockPos pos) {
        if(!level.getServer().isSameThread())throw new IllegalStateException("Lightning requires server thread");
        if(!enabled())return false;
        if(!planet(level)||!level.hasChunkAt(pos)||!level.canSeeSky(pos)||!safeStrike(level,pos))return false;
        var bolt=EntityType.LIGHTNING_BOLT.create(level);if(bolt==null)return false;
        bolt.moveTo(pos.getX()+.5,pos.getY(),pos.getZ()+.5);bolt.setVisualOnly(false);
        return level.addFreshEntity(bolt);
    }
    @SubscribeEvent public static void protectNativeStrikes(EntityJoinLevelEvent event) {
        if(!enabled())return;
        if(event.getEntity() instanceof LightningBolt && event.getLevel() instanceof ServerLevel level
                && planet(level) && !safeStrike(level,event.getEntity().blockPosition()))event.setCanceled(true);
    }
    private PlanetStorms() {}
}
