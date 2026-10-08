package net.zerog.tweaks.gametest;

import java.nio.file.Files;
import java.util.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.storage.LevelResource;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.travel.*;

/** Explicit isolated export preparation; never included in production and never runs in a player's save. */
@GameTestHolder("zerog_hub_pregen") @PrefixGameTestTemplate(false)
public final class HubPregenGameTests {
    @GameTest(templateNamespace="zerog_hub_tiers",template="equipment_empty",timeoutTicks=240000)
    public static void fifty_full_chunks_per_planet_and_twelve_distinct_return_gates(GameTestHelper h){
        var server=h.getLevel().getServer();
        h.assertTrue(PlanetTestHub.isHub(server)&&GateLedger.get(server).playerHubBuilt,"Not the prepared dual hub");
        var worlds=ZGDimensionTerrain.dimensions();h.assertTrue(worlds.size()==34,"Unexpected dimension count");
        var results=new ArrayList<Map<String,Object>>();
        class Work implements Runnable {
            int dimension,index;
            public void run(){
                if(dimension>=worlds.size()){
                    try {
                        var report=new LinkedHashMap<String,Object>();report.put("chunks_per_dimension",50);report.put("total_requested_chunks",1700);report.put("dimensions",results);report.put("permanent_forced_chunks",false);report.put("generation_margin_note","Vanilla feature dependencies may save neighboring chunks outside the requested rectangle.");
                        Files.writeString(server.getWorldPath(LevelResource.ROOT).resolve("zerog-pregen50.json"),new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(report));
                    }catch(java.io.IOException ex){throw new IllegalStateException("Cannot save pre-generation receipt",ex);}
                    h.succeed();return;
                }
                var name=worlds.get(dimension);ServerLevel level=PlanetTestHub.planet(server,"zerog_tweaks:"+name);
                h.assertTrue(level!=null,"Missing dimension "+name);
                // Exactly 10 by 5 requested chunks encompass the compact twelve-platform cluster.
                int cx=29+index%10,cz=32+index/10;
                var chunk=level.getChunk(cx,cz);
                h.assertTrue(chunk.getPos().x==cx&&chunk.getPos().z==cz,"Wrong fully generated chunk");
                if(++index==50){
                    var positions=new HashSet<BlockPos>();
                    for(int set=0;set<2;set++)for(int tier=1;tier<=6;tier++){
                        var c=set==0?HubTieredGates.centre(tier):HubTieredGates.playerCentre(tier);
                        var home=(SurvivalGateBlockEntity)server.overworld().getBlockEntity(c.offset(0,1,-2));
                        var landing=SurvivalGateBlockEntity.prepareArrival(level,home);
                        // Finite, one-time workshop supply; ordinary survival return gates are unchanged.
                        if(set==1){landing.stored=landing.capacity();landing.setChanged();}
                        h.assertTrue(landing.formedTier()==1&&landing.adminTest()==(set==0)&&positions.add(landing.getBlockPos()),"Missing/colliding/wrong-mode return gate "+name+" "+set+" "+tier);
                        h.assertTrue(landing.getBlockPos().getX()>>4>=29&&landing.getBlockPos().getX()>>4<=38&&landing.getBlockPos().getZ()>>4>=32&&landing.getBlockPos().getZ()>>4<=36,"Landing outside pre-generation rectangle");
                    }
                    h.assertTrue(level.getForcedChunks().isEmpty(),"Permanent tickets left in "+name);
                    level.getChunkSource().save(true);
                    results.add(Map.of("id","zerog_tweaks:"+name,"chunks",50,"min_chunk_x",29,"max_chunk_x",38,"min_chunk_z",32,"max_chunk_z",36,"return_gates",12));
                    com.mojang.logging.LogUtils.getLogger().info("ZeroG pregen50: {}/34 {} — 50 FULL chunks, 12 return gates, no forced chunks",dimension+1,name);
                    index=0;dimension++;
                }
                // GameTest removes the executing Runnable after it returns: use a new callback identity.
                h.runAfterDelay(1,()->run());
            }
        }
        h.runAfterDelay(1,new Work());
    }
}
