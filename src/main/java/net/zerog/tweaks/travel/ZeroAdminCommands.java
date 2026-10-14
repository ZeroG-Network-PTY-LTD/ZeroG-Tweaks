package net.zerog.tweaks.travel;

import com.mojang.brigadier.arguments.StringArgumentType;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.commands.arguments.coordinates.BlockPosArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.event.RegisterCommandsEvent;

/** Explicit operator tools, not a survival-gate unlock or a world-reset interface. */
public final class ZeroAdminCommands {
    public static final Map<String,String> DESTINATIONS;
    public static final Map<String,String> SHOWCASES=Map.of("water_bio_habitat","cerulon",
            "hot_ring_monolith","skarn","ice_spire_outpost","eidolon");
    private static final Map<java.util.UUID,Long> RANDOM_COOLDOWNS=new java.util.HashMap<>();
    public static final List<String> STRUCTURES=List.of("buried_observatory","collapsed_forge","concord_vault",
            "derelict_wreck","frozen_outpost","impact_site","mars_aresite_shrine","mars_crash_site",
            "prism_sentinel_arena","prism_spire","solar_shrine","sunken_lab","sunken_relay");
    private static final Set<String> HAZARDOUS_FLOORS=Set.of("ember_crust","corona_crust","flare_vent",
            "vent_rock","polar_frost","void_rift","acid");
    static {
        var destinations=new LinkedHashMap<String,String>();
        destinations.put("overworld","minecraft:overworld");
        for(var name:List.of("moon","mars","cerulon","skarn","eidolon","solvane"))
            destinations.put(name,"zerog_tweaks:"+name);
        for(int galaxy=2;galaxy<=5;galaxy++) {
            for(int planet=1;planet<=6;planet++)destinations.put("g"+galaxy+"_p"+planet,"zerog_tweaks:g"+galaxy+"_p"+planet);
            destinations.put("g"+galaxy+"_moons","zerog_tweaks:g"+galaxy+"_moons");
        }
        DESTINATIONS=Collections.unmodifiableMap(destinations);
    }

    public static void commands(RegisterCommandsEvent event) {
        var root=Commands.literal("zero").requires(s->s.hasPermission(2)).executes(c->help(c.getSource()));
        root.then(Commands.literal("help").executes(c->help(c.getSource())));
        root.then(Commands.literal("dimensions").executes(c->{
            DESTINATIONS.forEach((alias,id)->say(c.getSource(),alias+" -> "+id));return DESTINATIONS.size();
        }));
        var travel=Commands.literal("tp");
        for(var destination:DESTINATIONS.entrySet()) {
            String alias=destination.getKey();
            travel.then(Commands.literal(alias).executes(c->travel(c.getSource(),alias,null))
                    .then(Commands.argument("position",BlockPosArgument.blockPos()).executes(c->
                            travel(c.getSource(),alias,BlockPosArgument.getBlockPos(c,"position")))));
        }
        root.then(travel);
        root.then(Commands.literal("random").executes(c->randomTravel(c.getSource())));
        var showcase=Commands.literal("showcase");
        SHOWCASES.forEach((name,planet)->showcase.then(Commands.literal(name)
                .executes(c->showcase(c.getSource(),name,planet))
                .then(Commands.literal("build").executes(c->{var target=destination(c.getSource(),planet);if(target==null)return fail(c.getSource(),"Dimension unavailable.");say(c.getSource(),PlanetShowcaseSites.get(target).build(target,name));return PlanetShowcaseSites.get(target).origin(name)==null?0:1;}))));
        Map.of("ice","ice_spire_outpost","water","water_bio_habitat","hot","hot_ring_monolith").forEach((alias,name)->showcase.then(Commands.literal(alias)
                .executes(c->showcase(c.getSource(),name,SHOWCASES.get(name)))
                .then(Commands.literal("build").executes(c->{var target=destination(c.getSource(),SHOWCASES.get(name));if(target==null)return fail(c.getSource(),"Dimension unavailable.");say(c.getSource(),PlanetShowcaseSites.get(target).build(target,name));return PlanetShowcaseSites.get(target).origin(name)==null?0:1;}))));
        root.then(showcase);
        root.then(Commands.literal("home").executes(c->travel(c.getSource(),"overworld",null)));
        root.then(Commands.literal("structures").executes(c->{
            say(c.getSource(),"Registered ZeroG structures: "+String.join(", ",STRUCTURES));return STRUCTURES.size();
        }));
        var locate=Commands.literal("locate");
        for(String structure:STRUCTURES)locate.then(Commands.literal(structure)
                .executes(c->locate(c.getSource(),structure,null))
                .then(Commands.argument("destination",StringArgumentType.word())
                        .suggests((c,b)->SharedSuggestionProvider.suggest(DESTINATIONS.keySet(),b))
                        .executes(c->locate(c.getSource(),structure,StringArgumentType.getString(c,"destination")))));
        root.then(locate);
        root.then(Commands.literal("status").executes(c->{
            var level=c.getSource().getLevel();
            say(c.getSource(),"Dimension "+level.dimension().location()+"; game time "+level.getGameTime()
                    +"; custom weather paused; admin travel creates no pads or persistent forced chunks.");return 1;
        }));
        root.then(Commands.literal("gate").then(Commands.argument("position",BlockPosArgument.blockPos())
                .executes(c->gate(c.getSource(),BlockPosArgument.getLoadedBlockPos(c,"position")))));
        root.then(Commands.literal("machine").then(Commands.argument("position",BlockPosArgument.blockPos())
                .executes(c->machine(c.getSource(),BlockPosArgument.getLoadedBlockPos(c,"position")))));
        root.then(Commands.literal("hub").then(Commands.literal("status").executes(c->
                c.getSource().getServer().getCommands().getDispatcher().execute("zerog hub status",c.getSource()))));
        event.getDispatcher().register(root);
        // Do not replace another mod's existing /random command.
        if(event.getDispatcher().getRoot().getChild("random")==null)
            event.getDispatcher().register(Commands.literal("random").requires(s->s.hasPermission(2))
                    .executes(c->randomTravel(c.getSource())));
    }

    private static int help(CommandSourceStack source) {
        say(source,"/zero dimensions | tp <planet> [x y z] | home | structures | locate <structure> [planet]");
        say(source,"/zero status | gate <x y z> | machine <x y z> | hub status. Operator level2 required.");
        say(source,"/zero showcase <water_bio_habitat|hot_ring_monolith|ice_spire_outpost> | /zero random (alias /random if available)");
        say(source,"Automatic travel searches dry footing near destination spawn; explicit coordinates are inspection travel, not guaranteed safe.");
        return 1;
    }
    private static int showcase(CommandSourceStack source,String name,String planet) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var target=destination(source,planet);
        if(target==null)return fail(source,"Showcase dimension unavailable.");
        var sites=PlanetShowcaseSites.get(target);var origin=sites.origin(name);
        if(origin==null)return fail(source,"No saved site. Explicitly build with /zero showcase "+name+" build; normal teleport never builds or clears terrain.");
        var feet=sites.arrival(target,name);if(feet==null)return fail(source,"Saved site has no safe entrance footing. Inspect with spectator /zero tp "+planet+" "+origin.toShortString());
        return travel(source,planet,feet);
    }
    private static int randomTravel(CommandSourceStack source) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var player=source.getPlayerOrException();var level=source.getLevel();
        String alias=level.dimension().location().getPath();
        if(!"zerog_tweaks".equals(level.dimension().location().getNamespace())||!DESTINATIONS.containsKey(alias))
            return fail(source,"Random travel is limited to ZeroG planetary dimensions. Use /zero tp <planet> first.");
        long now=System.nanoTime();
        if(now<RANDOM_COOLDOWNS.getOrDefault(player.getUUID(),0L))return fail(source,"Wait 30 seconds between random-travel searches.");
        RANDOM_COOLDOWNS.put(player.getUUID(),now+30_000_000_000L);
        RANDOM_COOLDOWNS.entrySet().removeIf(e->e.getValue()<now);
        // Local RNG avoids shared worldgen random access. At most eight new columns/chunks per invocation.
        var rng=new java.util.Random();var origin=player.blockPosition();
        for(int attempt=0;attempt<8;attempt++) {
            double angle=rng.nextDouble()*Math.PI*2;int radius=128+rng.nextInt(385);
            int x=origin.getX()+(int)(Math.cos(angle)*radius),z=origin.getZ()+(int)(Math.sin(angle)*radius);
            if(!level.getWorldBorder().isWithinBounds(new BlockPos(x,origin.getY(),z)))continue;
            level.getChunk(x>>4,z>>4);
            var feet=new BlockPos(x,level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,x,z),z);
            if(safeFooting(level,feet))return travel(source,alias,feet);
        }
        return fail(source,"No safe dry surface found in eight attempts. Nothing was moved or built; try again after cooldown.");
    }
    private static ServerLevel destination(CommandSourceStack source,String alias) {
        String id=DESTINATIONS.get(alias);
        return id==null?null:source.getServer().getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse(id)));
    }
    public static boolean safeFooting(ServerLevel level,BlockPos feet) {
        if(level.isOutsideBuildHeight(feet)||level.isOutsideBuildHeight(feet.above())||!level.getWorldBorder().isWithinBounds(feet))return false;
        var floor=level.getBlockState(feet.below());
        var id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(floor.getBlock());
        return floor.isFaceSturdy(level,feet.below(),Direction.UP)&&!floor.is(BlockTags.LEAVES)
                &&!floor.is(Blocks.MAGMA_BLOCK)&&!floor.is(Blocks.CACTUS)
                &&!(id.getNamespace().equals("zerog_tweaks")&&HAZARDOUS_FLOORS.contains(id.getPath()))
                &&floor.getFluidState().isEmpty()
                &&level.getBlockState(feet).getCollisionShape(level,feet).isEmpty()
                &&level.getBlockState(feet.above()).getCollisionShape(level,feet.above()).isEmpty()
                &&!unsafeOccupant(level,feet)&&!unsafeOccupant(level,feet.above())
                &&level.getFluidState(feet).isEmpty()&&level.getFluidState(feet.above()).isEmpty();
    }
    private static boolean unsafeOccupant(ServerLevel level,BlockPos pos) {
        var state=level.getBlockState(pos);
        return state.is(Blocks.FIRE)||state.is(Blocks.SOUL_FIRE)||state.is(Blocks.WITHER_ROSE)
                ||state.is(Blocks.SWEET_BERRY_BUSH)||state.is(Blocks.POWDER_SNOW);
    }
    private static int travel(CommandSourceStack source,String alias,BlockPos requested) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var player=source.getPlayerOrException();var target=destination(source,alias);
        if(target==null)return fail(source,"Destination is unavailable: "+alias);
        BlockPos feet=requested;
        if(feet==null) {
            var spawn=target.getSharedSpawnPos();
            // Nine bounded columns in at most nine ordinary chunks. Never make a landing platform or force-load ticket.
            for(int[] offset:new int[][]{{0,0},{16,0},{-16,0},{0,16},{0,-16},{16,16},{-16,16},{16,-16},{-16,-16}}) {
                int x=spawn.getX()+offset[0],z=spawn.getZ()+offset[1];
                if(!target.getWorldBorder().isWithinBounds(new BlockPos(x,spawn.getY(),z)))continue;
                target.getChunk(x>>4,z>>4);
                var candidate=new BlockPos(x,target.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,x,z),z);
                if(safeFooting(target,candidate)){feet=candidate;break;}
            }
            if(feet==null)return fail(source,"No clear dry footing near spawn. Use /zero tp "+alias+" x y z for explicit inspection (may be hazardous).");
        }
        if(target.isOutsideBuildHeight(feet)||target.isOutsideBuildHeight(feet.above())||!target.getWorldBorder().isWithinBounds(feet))
            return fail(source,"Destination is outside the world border or build height.");
        target.getChunkAt(feet);
        if(!player.isSpectator()&&(!target.getBlockState(feet).getCollisionShape(target,feet).isEmpty()
                ||!target.getBlockState(feet.above()).getCollisionShape(target,feet.above()).isEmpty()))
            return fail(source,"Destination is obstructed. Choose clear coordinates or inspect in spectator mode.");
        player.stopRiding();
        if(target!=player.serverLevel())GateLaunchSync.sendDestination(player,target);
        player.teleportTo(target,feet.getX()+.5,feet.getY(),feet.getZ()+.5,player.getYRot(),0);
        player.setDeltaMovement(net.minecraft.world.phys.Vec3.ZERO);player.fallDistance=0;
        if(player.serverLevel()!=target)return fail(source,"Travel was refused; player stayed in the original dimension.");
        say(source,"Admin travel: "+alias+" at "+feet.toShortString()+" (no gate FE spent, pads built or keys granted; normal arrival milestones may unlock).");
        return 1;
    }
    private static int locate(CommandSourceStack source,String structure,String alias) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var target=alias==null?source.getLevel():destination(source,alias);
        if(target==null)return fail(source,"Unknown or unavailable destination. Use /zero dimensions.");
        return source.getServer().getCommands().getDispatcher().execute("locate structure zerog_tweaks:"+structure,source.withLevel(target));
    }
    private static int gate(CommandSourceStack source,BlockPos pos) {
        if(!(source.getLevel().getBlockEntity(pos) instanceof SurvivalGateBlockEntity gate))return fail(source,"This loaded block is not a ZeroG gate controller.");
        var formation=gate.formation();
        say(source,"Gate tier "+formation.tier()+"; energy "+gate.stored+"/"+gate.capacity()+" FE; ports "+formation.ports().size()+"; countdown "+gate.countdown+" ticks.");
        say(source,formation.problem().isEmpty()?"Formation complete.":formation.problem());return 1;
    }
    private static int machine(CommandSourceStack source,BlockPos pos) {
        var level=source.getLevel();say(source,"Block: "+net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos).getBlock()));
        for(var face:Direction.values()) {
            var energy=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos,face);
            var items=level.getCapability(Capabilities.ItemHandler.BLOCK,pos,face);
            var fluid=level.getCapability(Capabilities.FluidHandler.BLOCK,pos,face);
            say(source,face.getName()+": energy "+(energy==null?"none":energy.getEnergyStored()+"/"+energy.getMaxEnergyStored()+" FE")
                    +"; item slots "+(items==null?0:items.getSlots())+"; fluid tanks "+(fluid==null?0:fluid.getTanks()));
        }
        return 1;
    }
    private static int fail(CommandSourceStack source,String message){source.sendFailure(Component.literal(message));return 0;}
    private static void say(CommandSourceStack source,String message){source.sendSuccess(()->Component.literal(message),false);}
    private ZeroAdminCommands() {}
}
