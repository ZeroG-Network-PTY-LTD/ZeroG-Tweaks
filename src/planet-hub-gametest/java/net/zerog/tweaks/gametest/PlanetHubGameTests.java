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
        helper.startSequence().thenWaitUntil(()->helper.assertTrue(GateLedger.get(server).prepared==34,"Waiting for all destination chunks"))
            .thenExecute(()-> {
                var ledger=GateLedger.get(server);
                helper.assertTrue(ledger.gates.size()==68,"Expected 34 hub gates and 34 return gates");
                var report=new com.google.gson.JsonObject();
                report.addProperty("seed",server.overworld().getSeed());
                report.addProperty("gate_count",ledger.gates.size());
                var planets=new com.google.gson.JsonArray();report.add("planets",planets);
                var player=helper.makeMockServerPlayerInLevel();
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
                    server.overworld().setBlock(broken,previous,2);
                    var gate=ledger.gates.get(GateLedger.key("minecraft:overworld",centre));
                    ledger.add(new GateLedger.Gate(gate.dimension,gate.centre,gate.target,false));
                    var input=ledger.input(server.overworld(),centre.offset(7,1,0));
                    helper.assertTrue(input!=null&&input.receiveEnergy(123456,true)==123456,"FE simulation failed");
                    helper.assertTrue(input.getEnergyStored()==0,"Simulation changed energy");
                    helper.assertTrue(input.receiveEnergy(123456,false)==123456&&input.getEnergyStored()==123456,"FE input failed");
                    var roundtrip=GateLedger.load(ledger.save(new net.minecraft.nbt.CompoundTag(),server.registryAccess()),server.registryAccess());
                    helper.assertTrue(roundtrip.gates.get(GateLedger.key(gate.dimension,gate.centre)).energy==123456,"Gate energy not persisted");
                    ledger.add(gate);
                    try {
                        java.nio.file.Files.writeString(server.getWorldPath(net.minecraft.world.level.storage.LevelResource.ROOT).resolve("zerog-hub-report.json"),
                                new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(report));
                    } catch(java.io.IOException ex) {throw new IllegalStateException("Cannot save hub evidence",ex);}
                } finally {server.getPlayerList().remove(player);}
            }).thenSucceed();
    }
    private static void click(net.minecraft.server.level.ServerPlayer player,net.minecraft.core.BlockPos controller) {
        var hit=new BlockHitResult(Vec3.atCenterOf(controller),Direction.NORTH,controller,false);
        PlanetTestHub.interact(new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,controller,hit));
    }
}
