package net.zerog.tweaks.gametest;

import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.GateLedger;
import net.zerog.tweaks.travel.PlanetGate;
import net.zerog.tweaks.travel.PlanetTestHub;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

@GameTestHolder("zerog_planet_hub")
@PrefixGameTestTemplate(false)
public final class PlanetHubGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=20000)
    public static void all_34_planets_generate_and_gates_travel_both_ways(GameTestHelper helper) {
        var server=helper.getLevel().getServer();
        helper.assertTrue(PlanetTestHub.isHub(server),"Hub preset did not load");
        var failure=new java.util.concurrent.atomic.AtomicReference<RuntimeException>();
        helper.startSequence().thenWaitUntil(()->helper.assertTrue(GateLedger.get(server).prepared==34
                && GateLedger.get(server).inspectionPrepared==34,"Waiting for destinations and nearby inspection villages"))
            .thenExecute(()-> {
                try {
                var ledger=GateLedger.get(server);
                helper.assertTrue(ledger.gates.size()==68,"Expected 34 hub gates and 34 return gates");
                var report=new com.google.gson.JsonObject();
                report.addProperty("seed",server.overworld().getSeed());
                report.addProperty("gate_count",ledger.gates.size());
                var planets=new com.google.gson.JsonArray();report.add("planets",planets);
                var player=helper.makeMockServerPlayerInLevel();
                var terrainFingerprints=new java.util.HashSet<String>();
                boolean cleanShowcase=Boolean.getBoolean("zerog.cleanShowcase");
                report.addProperty("demonstration_colonies",!cleanShowcase);
                report.addProperty("nearby_inspection_villages",true);
                try {
                    int index=0;
                    for(String name:ZGDimensionTerrain.dimensions()) {
                        String id="zerog_tweaks:"+name;
                        var world=PlanetTestHub.planet(server,id);
                        helper.assertTrue(world!=null,"Missing dimension "+id);
                        var home=PlanetTestHub.hubCentre(index++);
                        PlanetGate.loadLandingChunks(server.overworld(),home);
                        helper.assertTrue(PlanetGate.missing(server.overworld(),home)==null,"Broken outgoing gate "+id+": "+PlanetGate.missing(server.overworld(),home));
                        var arrival=ledger.gates.values().stream().filter(g->g.dimension.equals(id)).findFirst().orElseThrow();
                        PlanetGate.loadLandingChunks(world,arrival.centre);
                        helper.assertTrue(PlanetGate.missing(world,arrival.centre)==null,"Broken return gate "+id+": "+PlanetGate.missing(world,arrival.centre));
                        player.teleportTo(server.overworld(),home.getX()+.5,home.getY()+1,home.getZ()-3,0,0);
                        click(player,PlanetGate.controller(home));
                        helper.assertTrue(player.serverLevel()==world,"Outgoing gateway failed "+id);
                        player.teleportTo(world,arrival.centre.getX()+.5,arrival.centre.getY()+1,arrival.centre.getZ()-3,0,0);
                        click(player,PlanetGate.controller(arrival.centre));
                        helper.assertTrue(player.serverLevel()==server.overworld(),"Return gateway failed "+id);
                        var entry=new com.google.gson.JsonObject();entry.addProperty("dimension",id);
                        var sites=ledger.inspectionVillages.get(id);
                        helper.assertTrue(sites!=null && sites.size()>=1 && sites.size()<=2,"Expected 1–2 safe nearby villages "+id);
                        entry.add("inspection_village_positions",new com.google.gson.Gson().toJsonTree(sites.stream().map(net.minecraft.core.BlockPos::toShortString).toList()));
                        for(var site:sites) {
                            for(int cx=(site.getX()-20)>>4;cx<=(site.getX()+20)>>4;cx++)
                                for(int cz=(site.getZ()-20)>>4;cz<=(site.getZ()+20)>>4;cz++)world.getChunk(cx,cz);
                            var anchor=(net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity)world.getBlockEntity(site);
                            helper.assertTrue(anchor!=null,"Missing inspection anchor "+id);anchor.populate(world);
                            helper.assertTrue(anchor.residentsCreated()==6 && anchor.speciesResidentsCreated()==2,"Expected eight designed planetary villagers "+id);
                            helper.assertTrue(site.distSqr(new net.minecraft.core.BlockPos(0,site.getY(),0))<=385*385,"Village not near gate "+id);
                        }
                        // Native noise generator, not colour/block-ID fingerprints.
                        var heights=new java.util.ArrayList<Integer>();
                        for(int sx=-3;sx<=3;sx++) for(int sz=-3;sz<=3;sz++) {
                            int sample=world.getChunkSource().getGenerator().getBaseHeight(sx*173+512,sz*173-1024,
                                    net.minecraft.world.level.levelgen.Heightmap.Types.OCEAN_FLOOR_WG,world,world.getChunkSource().randomState());
                            heights.add(sample);
                            int repeat=world.getChunkSource().getGenerator().getBaseHeight(sx*173+512,sz*173-1024,
                                    net.minecraft.world.level.levelgen.Heightmap.Types.OCEAN_FLOOR_WG,world,world.getChunkSource().randomState());
                            helper.assertTrue(sample==repeat,"Terrain is not deterministic "+id);
                        }
                        helper.assertTrue(terrainFingerprints.add(heights.toString()),"Mirrored terrain heightmap "+id);
                        helper.assertTrue(new java.util.HashSet<>(heights).size()>3,"Flat/unvaried terrain "+id);
                        entry.add("terrain_height_samples",new com.google.gson.Gson().toJsonTree(heights));
                        var protectedBreak=new net.neoforged.neoforge.event.level.BlockEvent.BreakEvent(world,
                                PlanetGate.controller(arrival.centre),world.getBlockState(PlanetGate.controller(arrival.centre)),player);
                        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.post(protectedBreak);
                        helper.assertTrue(protectedBreak.isCanceled(),"Arrival gate can be broken "+id);
                        helper.assertTrue(!net.zerog.tweaks.event.DailyPlanetImpacts.impact(world,arrival.centre,6,name),"Impact entered arrival region "+id);
                        if(!cleanShowcase) {
                        // Actual generated schematic, populated through the same server
                        // method as the ticking anchor. GameTest disables natural features.
                        for(int cx=6;cx<=10;cx++) for(int cz=6;cz<=10;cz++)world.getChunk(cx,cz);
                        int settlementY=Math.max(world.getSeaLevel()+2,world.getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.WORLD_SURFACE,136,136));
                        var outpost=new net.minecraft.core.BlockPos(136,settlementY,136);
                        helper.assertTrue(net.zerog.tweaks.worldgen.PlanetSettlementFeature.build(world,outpost,name,index%4,
                                net.minecraft.util.RandomSource.create(1000+index)),"Settlement failed "+id);
                        var anchor=(net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity)world.getBlockEntity(outpost);
                        helper.assertTrue(anchor!=null,"No settlement anchor "+id);anchor.populate(world);
                        helper.assertTrue(anchor.residentsCreated()==6,"Settlement has no inhabitants "+id);
                        long count=world.getEntitiesOfClass(net.minecraft.world.entity.npc.Villager.class,
                                new net.minecraft.world.phys.AABB(Vec3.atLowerCornerOf(outpost.offset(-20,0,-20)),Vec3.atLowerCornerOf(outpost.offset(20,8,20)))).size();
                        helper.assertTrue(count==8,"Expected eight designed planetary villagers, found "+count+" in "+id);
                        anchor.populate(world);helper.assertTrue(anchor.residentsCreated()==6,"Resident duplication "+id);
                        entry.addProperty("settlement_residents",count);
                        entry.addProperty("settlement_position",outpost.toShortString());
                        helper.assertTrue(world.getEntitiesOfClass(net.minecraft.world.entity.npc.Villager.class,
                                new net.minecraft.world.phys.AABB(Vec3.atLowerCornerOf(outpost.offset(-20,0,-20)),Vec3.atLowerCornerOf(outpost.offset(20,8,20))))
                                .stream().allMatch(v->v instanceof net.zerog.tweaks.entity.PlanetVillager),
                                "Outpost still contains old vanilla planetary residents "+id);
                        }
                        entry.addProperty("tree_species",net.zerog.tweaks.worldgen.PlanetEcologyProfile.tree(name));
                        entry.addProperty("landing",arrival.centre.toShortString());
                        int ores=0,logs=0,vines=0,mushrooms=0;
                        for(int x=16;x<32;x++) for(int z=16;z<32;z++) for(int y=world.getMinBuildHeight();y<world.getMaxBuildHeight();y++) {
                            var state=world.getBlockState(new net.minecraft.core.BlockPos(x,y,z));
                            if(state.isAir())continue;
                            String block=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath();
                            if(block.endsWith("_ore"))ores++;
                            if(block.endsWith("_log"))logs++;
                            if(block.contains("vine"))vines++;
                            if(block.contains("mushroom"))mushrooms++;
                        }
                        entry.addProperty("sampled_ore_blocks",ores);entry.addProperty("sampled_tree_logs",logs);
                        entry.addProperty("sampled_vine_blocks",vines);entry.addProperty("sampled_mushrooms",mushrooms);
                        planets.add(entry);
                    }
                    // Damage disables travel; test power must never bypass structural validation.
                    var centre=PlanetTestHub.hubCentre(0);var broken=centre.offset(7,0,1);
                    var previous=server.overworld().getBlockState(broken);
                    server.overworld().setBlock(broken,Blocks.AIR.defaultBlockState(),2);
                    helper.assertTrue(PlanetGate.missing(server.overworld(),centre)!=null,"Broken frame was accepted");
                    net.zerog.tweaks.travel.ArrivalProtection.repairLoaded(server);
                    helper.assertTrue(server.overworld().getBlockState(broken).equals(previous),"Arrival gate repair failed");
                    var gate=ledger.gates.get(GateLedger.key("minecraft:overworld",centre));
                    ledger.add(new GateLedger.Gate(gate.dimension,gate.centre,gate.target,false));
                    var input=ledger.input(server.overworld(),centre.offset(7,1,0));
                    helper.assertTrue(input!=null&&input.receiveEnergy(123456,true)==123456,"FE simulation failed");
                    helper.assertTrue(input.getEnergyStored()==0,"Simulation changed energy");
                    helper.assertTrue(input.receiveEnergy(123456,false)==123456&&input.getEnergyStored()==123456,"FE input failed");
                    var roundtrip=GateLedger.load(ledger.save(new net.minecraft.nbt.CompoundTag(),server.registryAccess()),server.registryAccess());
                    helper.assertTrue(roundtrip.gates.get(GateLedger.key(gate.dimension,gate.centre)).energy==123456,"Gate energy not persisted");
                    ledger.add(gate);
                    if(!cleanShowcase) {
                    // Actual natural feature placement, not the authored demos above.
                    var mars=PlanetTestHub.planet(server,"zerog_tweaks:mars");
                    int naturalSettlements=0;
                    var naturalAnchors=new java.util.ArrayList<net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity>();
                    for(int cx=24;cx<36;cx++) for(int cz=24;cz<36;cz++) {
                        var chunk=mars.getChunk(cx,cz);
                        for(var be:chunk.getBlockEntities().values()) if(be instanceof net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity colony) {
                            naturalSettlements++;naturalAnchors.add(colony);
                        }
                    }
                    helper.assertTrue(naturalSettlements<=1,"Rare villages clustered within 144 Mars chunks");
                    for(var colony:naturalAnchors) {
                        var pos=colony.getBlockPos();
                        for(int cx=(pos.getX()-20)>>4;cx<=(pos.getX()+20)>>4;cx++)
                            for(int cz=(pos.getZ()-20)>>4;cz<=(pos.getZ()+20)>>4;cz++) mars.getChunk(cx,cz);
                        colony.populate(mars);helper.assertTrue(colony.residentsCreated()==6,"Natural outpost residents never spawn");
                    }
                    report.addProperty("naturally_generated_mars_settlements",naturalSettlements);
                    // Build a real supported mine fixture through dry native stone.
                    var mine=new net.minecraft.core.BlockPos(680,0,680);
                    for(int cx=40;cx<=44;cx++) for(int cz=40;cz<=44;cz++)mars.getChunk(cx,cz);
                    for(var pos:net.minecraft.core.BlockPos.betweenClosed(mine.offset(-19,-1,-19),mine.offset(19,4,19)))
                        mars.setBlock(pos,net.zerog.tweaks.registry.BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
                    helper.assertTrue(net.zerog.tweaks.worldgen.PlanetMineshaftFeature.build(mars,mine,net.minecraft.util.RandomSource.create(10)),"Mineshaft build failed");
                    helper.assertTrue(mars.getBlockState(mine.offset(6,0,0)).is(Blocks.RAIL),"Mine rails missing");
                    helper.assertTrue(mars.getBlockState(mine.offset(6,2,1)).is(net.zerog.tweaks.registry.BlockInit.HULL_PLATING.get()),"Mine supports missing");
                    helper.assertTrue(mars.getBlockEntity(mine.offset(0,0,2)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity,"Mine loot chest missing");
                    for(String colour:new String[]{"blue","teal"}) {
                        var item=net.minecraft.core.registries.BuiltInRegistries.ITEM.get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","star_glass_"+colour));
                        var component=item.getDefaultInstance().get(net.minecraft.core.component.DataComponents.BLOCK_STATE);
                        helper.assertTrue(component!=null && component.properties().get("nebula").equals(colour),"Glass variant places wrong colour");
                    }
                    helper.assertTrue(net.zerog.tweaks.registry.ZGCrystalGrowth.STAR_GLASS.get().asItem()==net.minecraft.core.registries.BuiltInRegistries.ITEM.get(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","star_glass")),"Canonical glass item overwritten");
                    report.addProperty("supported_mineshaft_fixture",true);report.addProperty("star_glass_variant_items",true);
                    var impact=new net.minecraft.core.BlockPos(744,64,680);
                    for(int cx=45;cx<=47;cx++) for(int cz=41;cz<=43;cz++)mars.getChunk(cx,cz);
                    for(var pos:net.minecraft.core.BlockPos.betweenClosed(impact.offset(-8,-7,-8),impact.offset(8,9,8)))
                        mars.setBlock(pos,net.zerog.tweaks.registry.BlockInit.MARTIAN_STONE.get().defaultBlockState(),2);
                    helper.assertTrue(net.zerog.tweaks.event.DailyPlanetImpacts.impact(mars,impact,6,"mars"),"Comet cannot create its remnant");
                    var core=mars.getBlockState(impact.above());
                    helper.assertTrue(core.is(net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks","redshift_garnet_ore"))),"Comet rare centre missing");
                    report.addProperty("comet_remnant_fixture",true);
                    }
                    try {
                        java.nio.file.Files.writeString(server.getWorldPath(net.minecraft.world.level.storage.LevelResource.ROOT).resolve("zerog-hub-report.json"),
                                new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(report));
                    } catch(java.io.IOException ex) {throw new IllegalStateException("Cannot save hub evidence",ex);}
                } finally {server.getPlayerList().remove(player);}
                } catch(RuntimeException ex){failure.set(ex);}
            // Do not stop the test server in the same tick as cross-dimension
            // portal tickets and neighbouring generation tasks were created.
            }).thenIdle(400).thenExecute(()->{if(failure.get()!=null)throw failure.get();}).thenSucceed();
    }
    private static void click(net.minecraft.server.level.ServerPlayer player,net.minecraft.core.BlockPos controller) {
        var hit=new BlockHitResult(Vec3.atCenterOf(controller),Direction.NORTH,controller,false);
        PlanetTestHub.interact(new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,controller,hit));
    }
}
