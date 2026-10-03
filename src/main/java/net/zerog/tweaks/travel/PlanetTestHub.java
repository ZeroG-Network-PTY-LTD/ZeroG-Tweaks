package net.zerog.tweaks.travel;

import com.mojang.brigadier.arguments.StringArgumentType;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.coordinates.BlockPosArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Explicit test-world preset only: never automatically edits ordinary saves. */
public final class PlanetTestHub {
    public static final ResourceLocation BIOME=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planet_test_hub");
    public static boolean isHub(MinecraftServer server) {
        return server.overworld().getChunkSource().getGenerator().getBiomeSource().possibleBiomes().stream()
                .anyMatch(b->b.unwrapKey().map(k->k.location().equals(BIOME)).orElse(false));
    }
    public static BlockPos hubCentre(int index) {return new BlockPos((index%6)*25,64,25+(index/6)*25);}
    public static ServerLevel planet(MinecraftServer server,String id) {
        return server.getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse(id)));
    }
    public static void started(ServerStartedEvent event) {
        var server=event.getServer();if(!isHub(server))return;
        var ledger=GateLedger.get(server);if(ledger.hubBuilt)return;
        var level=server.overworld();
        for(int x=-12;x<=137;x++) for(int z=-12;z<=162;z++)
            level.setBlock(new BlockPos(x,63,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
        var dimensions=ZGDimensionTerrain.dimensions();
        for(int i=0;i<dimensions.size();i++) {
            var centre=hubCentre(i);PlanetGate.build(level,centre);
            String destination="zerog_tweaks:"+dimensions.get(i);
            ledger.add(new GateLedger.Gate("minecraft:overworld",centre,destination,true));
            label(level,centre,dimensions.get(i),"TEST POWER","Right-click gate","Stand on pad");
        }
        level.setDefaultSpawnPos(new BlockPos(62,65,0),0);
        ledger.hubBuilt=true;ledger.setDirty();
    }
    public static void tick(ServerTickEvent.Post event) {
        var server=event.getServer();
        if(!isHub(server)||server.getTickCount()%20!=0)return;
        var ledger=GateLedger.get(server);if(!ledger.hubBuilt)return;
        var ids=ZGDimensionTerrain.dimensions();
        if(ledger.prepared>=ids.size())return;
        String id="zerog_tweaks:"+ids.get(ledger.prepared);
        var level=planet(server,id);if(level==null)throw new IllegalStateException("Missing test-hub dimension "+id);
        prepareLanding(level,hubCentre(ledger.prepared),ledger);
        ledger.prepared++;ledger.setDirty();
        com.mojang.logging.LogUtils.getLogger().info("ZeroG planet test hub: {}/{} destinations prepared ({})",ledger.prepared,ids.size(),id);
    }
    public static GateLedger.Gate prepareLanding(ServerLevel level,BlockPos home,GateLedger ledger) {
        var existing=ledger.gates.values().stream().filter(g->g.dimension.equals(level.dimension().location().toString())
                &&g.target.equals("minecraft:overworld")).findFirst().orElse(null);
        if(existing!=null)return existing;
        // Only nine chunks around the landing site, not a forced planet-wide load.
        for(int x=-1;x<=1;x++) for(int z=-1;z<=1;z++) level.getChunk(x,z);
        int y=Math.min(level.getMaxBuildHeight()-16,Math.max(level.getSeaLevel()+5,level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,0,0)+5));
        var centre=new BlockPos(0,y,0);
        // Clear only the explicitly constructed landing volume above natural terrain.
        for(var pos:BlockPos.betweenClosed(centre.offset(-8,1,-8),centre.offset(8,13,8)))
            level.setBlock(pos,Blocks.AIR.defaultBlockState(),2);
        PlanetGate.build(level,centre);
        var gate=new GateLedger.Gate(level.dimension().location().toString(),centre,"minecraft:overworld",true);
        ledger.add(gate);
        label(level,centre,"RETURN TO HUB",level.dimension().location().getPath(),"TEST POWER","Stand on pad");
        return gate;
    }
    private static void label(ServerLevel level,BlockPos centre,String a,String b,String c,String d) {
        var pos=centre.offset(0,1,-8);level.setBlock(pos,Blocks.OAK_SIGN.defaultBlockState(),3);
        if(level.getBlockEntity(pos) instanceof SignBlockEntity sign) {
            var text=sign.getFrontText();String[] lines={a,b,c,d};
            for(int i=0;i<4;i++)text=text.setMessage(i,Component.literal(lines[i]));
            sign.setText(text,true);sign.setChanged();
        }
    }
    public static void interact(PlayerInteractEvent.RightClickBlock event) {
        if(!(event.getEntity() instanceof ServerPlayer player)||!(event.getLevel() instanceof ServerLevel level)
                ||!level.getBlockState(event.getPos()).is(BlockInit.GATE_CONTROLLER.get()))return;
        var ledger=GateLedger.get(level.getServer());var gate=ledger.controller(level,event.getPos());
        if(gate==null)return;event.setCanceled(true);event.setCancellationResult(InteractionResult.SUCCESS);
        String problem=PlanetGate.missing(level,gate.centre);
        if(problem!=null){player.displayClientMessage(Component.literal(problem),false);return;}
        if(Math.abs(player.getX()-(gate.centre.getX()+.5))>3.6||Math.abs(player.getZ()-(gate.centre.getZ()+.5))>3.6
                ||Math.abs(player.getY()-(gate.centre.getY()+1))>2) {
            player.displayClientMessage(Component.literal("Stand on the central pad, then right-click the controller."),false);return;
        }
        if(!gate.testPower&&gate.energy<GateLedger.TRAVEL_COST) {
            player.displayClientMessage(Component.literal("Gate needs "+GateLedger.TRAVEL_COST+" FE; stored "+gate.energy+" FE."),false);return;
        }
        var target=planet(level.getServer(),gate.target);
        if(target==null){player.displayClientMessage(Component.literal("Destination is unavailable: "+gate.target),false);return;}
        GateLedger.Gate arrival;
        if(gate.target.equals("minecraft:overworld")) {
            arrival=ledger.gates.values().stream().filter(g->g.dimension.equals(gate.target)&&g.target.equals(gate.dimension)).findFirst().orElse(null);
        } else {
            arrival=ledger.gates.values().stream().filter(g->g.dimension.equals(gate.target)&&g.target.equals(gate.dimension)).findFirst().orElse(null);
            if(arrival==null&&gate.testPower&&isHub(level.getServer()))arrival=prepareLanding(target,gate.centre,ledger);
        }
        if(arrival!=null)PlanetGate.loadLandingChunks(target,arrival.centre);
        if(arrival==null||PlanetGate.missing(target,arrival.centre)!=null) {
            player.displayClientMessage(Component.literal("No complete return gate exists at the destination."),false);return;
        }
        var position=arrival.centre;
        var result=player.changeDimension(new DimensionTransition(target,new Vec3(position.getX()+.5,position.getY()+1,position.getZ()+.5),
                Vec3.ZERO,180,0,DimensionTransition.PLAY_PORTAL_SOUND.then(DimensionTransition.PLACE_PORTAL_TICKET)));
        if(result!=null&&!gate.testPower){gate.energy-=GateLedger.TRAVEL_COST;ledger.setDirty();}
    }
    public static void commands(RegisterCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("zerog").requires(s->s.hasPermission(2))
            .then(Commands.literal("hub").then(Commands.literal("status").executes(c-> {
                var ledger=GateLedger.get(c.getSource().getServer());
                c.getSource().sendSuccess(()->Component.literal("Hub destinations: "+ledger.prepared+"/34; gates: "+ledger.gates.size()),false);return ledger.prepared;
            })))
            .then(Commands.literal("gate").then(Commands.literal("bind")
                .then(Commands.argument("destination",StringArgumentType.word())
                .then(Commands.argument("centre",BlockPosArgument.blockPos()).executes(c-> {
                    var level=c.getSource().getLevel();var centre=BlockPosArgument.getLoadedBlockPos(c,"centre");
                    String destination=StringArgumentType.getString(c,"destination");
                    if(planet(level.getServer(),destination)==null||PlanetGate.missing(level,centre)!=null) {
                        c.getSource().sendFailure(Component.literal("Build the complete T6 gate and use an existing destination ID."));return 0;
                    }
                    GateLedger.get(level.getServer()).add(new GateLedger.Gate(level.dimension().location().toString(),centre,destination,false));
                    c.getSource().sendSuccess(()->Component.literal("Energy-fed gate bound to "+destination+". Bind its return gate separately."),true);return 1;
                }))))));
    }
    private PlanetTestHub() {}
}
