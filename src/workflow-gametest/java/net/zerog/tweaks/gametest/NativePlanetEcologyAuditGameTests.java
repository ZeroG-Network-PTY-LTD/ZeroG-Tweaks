package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.*;
import net.neoforged.neoforge.gametest.*;

/** Bounded native generation survey, deliberately not a complete ecology certification. */
@GameTestHolder("zerog_native_ecology") @PrefixGameTestTemplate(false)
public final class NativePlanetEcologyAuditGameTests {
    @GameTest(templateNamespace="zerog_native_ecology",template="equipment_empty",timeoutTicks=12000)
    public static void six_planets_generate_native_chunks_and_report_ecology(GameTestHelper h){
        var report=new com.google.gson.JsonObject();report.addProperty("scope","18 naturally generated sampled chunks per Sol planet; not natural-spawn, rarity, all-biome or client approval");
        report.addProperty("seed",h.getLevel().getSeed());var rows=new com.google.gson.JsonArray();report.add("planets",rows);
        report.addProperty("structures_enabled_in_harness",h.getLevel().getServer().getWorldData().worldGenOptions().generateStructures());
        report.addProperty("structure_boundary","Vanilla GameTestServer constructs WorldOptions(0,false,false); this harness cannot certify natural structure placement.");
        var fingerprints=new java.util.HashSet<String>();
        for(String name:net.zerog.tweaks.item.ConcordCodexItem.WORLDS){
            var world=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse("zerog_tweaks:"+name)));
            h.assertTrue(world!=null&&world.getChunkSource().getGenerator() instanceof NoiseBasedChunkGenerator,"Native dimension preset required: "+name);
            var counts=new java.util.TreeMap<String,Integer>();var biomes=new java.util.TreeSet<String>();
            var cache=new java.util.HashMap<net.minecraft.world.level.block.Block,String>();
            var heights=new java.util.ArrayList<Integer>();int chunks=0,starts=0;
            for(int[] site:new int[][]{{64,64},{-80,96}})for(int dx=-1;dx<=1;dx++)for(int dz=-1;dz<=1;dz++){
                var chunk=world.getChunk(site[0]+dx,site[1]+dz);chunks++;
                int x=(site[0]+dx)*16+8,z=(site[1]+dz)*16+8;
                int y=world.getHeight(Heightmap.Types.WORLD_SURFACE,x,z);heights.add(y);
                biomes.add(world.getBiome(new BlockPos(x,y,z)).unwrapKey().map(k->k.location().toString()).orElse("unbound"));
                starts+=(int)chunk.getAllStarts().values().stream().filter(s->s.isValid()).count();
                for(var section:chunk.getSections()){
                    if(section==null||section.hasOnlyAir())continue;
                    for(int sx=0;sx<16;sx++)for(int sy=0;sy<16;sy++)for(int sz=0;sz<16;sz++){
                        var block=section.getBlockState(sx,sy,sz).getBlock();
                        String id=cache.computeIfAbsent(block,b->{var key=BuiltInRegistries.BLOCK.getKey(b);return key.getNamespace().equals("zerog_tweaks")?key.toString():"";});
                        if(!id.isEmpty())counts.merge(id,1,Integer::sum);
                    }
                }
            }
            h.assertTrue(fingerprints.add(heights.toString()),"Duplicate sampled native heightmap: "+name);
            h.assertTrue(counts.keySet().stream().anyMatch(k->k.endsWith("_ore")),"No planetary ore observed in 18 chunks: "+name);
            var row=new com.google.gson.JsonObject();row.addProperty("dimension","zerog_tweaks:"+name);row.addProperty("sampled_full_chunks",chunks);
            row.addProperty("observed_structure_starts",starts);row.add("sampled_surface_biomes",new com.google.gson.Gson().toJsonTree(biomes));
            row.add("surface_heights",new com.google.gson.Gson().toJsonTree(heights));
            var configured=new com.google.gson.JsonArray();
            for(var holder:world.getChunkSource().getGenerator().getBiomeSource().possibleBiomes()){
                var biomeRow=new com.google.gson.JsonObject();
                biomeRow.addProperty("biome",holder.unwrapKey().map(k->k.location().toString()).orElse("unbound"));
                var spawns=new com.google.gson.JsonArray();
                for(var category:net.minecraft.world.entity.MobCategory.values())
                    for(var entry:holder.value().getMobSettings().getMobs(category).unwrap()){
                        var spawn=new com.google.gson.JsonObject();
                        spawn.addProperty("entity",BuiltInRegistries.ENTITY_TYPE.getKey(entry.type).toString());
                        spawn.addProperty("category",category.getName());
                        spawn.addProperty("min",entry.minCount);spawn.addProperty("max",entry.maxCount);
                        spawns.add(spawn);
                    }
                biomeRow.add("loaded_spawn_entries_not_observed_entities",spawns);
                var features=new java.util.TreeSet<String>();
                for(var step:holder.value().getGenerationSettings().features())for(var feature:step)
                    feature.unwrapKey().ifPresent(k->features.add(k.location().toString()));
                biomeRow.add("loaded_placed_features_not_placement_proof",new com.google.gson.Gson().toJsonTree(features));
                configured.add(biomeRow);
            }
            row.add("possible_biome_runtime_configuration",configured);
            row.add("observed_zerog_blocks",new com.google.gson.Gson().toJsonTree(counts));rows.add(row);
        }
        try{java.nio.file.Files.writeString(java.nio.file.Path.of("native-planet-ecology-audit.json"),new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(report));}
        catch(java.io.IOException e){throw new RuntimeException(e);}
        h.succeed();
    }
}
