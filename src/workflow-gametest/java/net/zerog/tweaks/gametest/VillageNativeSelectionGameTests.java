package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.worldgen.PlanetSettlementFeature;

/** Exports immutable terrain-selected targets for a separate ordinary-world audit. */
@GameTestHolder("zerog_village_search") @PrefixGameTestTemplate(false)
public final class VillageNativeSelectionGameTests {
    @GameTest(templateNamespace="zerog_village_search",template="equipment_empty",timeoutTicks=1200)
    public static void native_selection_is_repeatable_without_generating_chunks(GameTestHelper helper) {
        var rows=new com.google.gson.JsonArray();long start=System.nanoTime();
        for(String planet:new String[]{"moon","mars","cerulon","skarn","eidolon","solvane"}) {
            var world=helper.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse("zerog_tweaks:"+planet)));
            helper.assertTrue(world!=null&&world.getChunkSource().getGenerator() instanceof net.minecraft.world.level.levelgen.NoiseBasedChunkGenerator,
                    "Native planetary preset required");
            int loadedBefore=world.getChunkSource().getLoadedChunksCount();
            for(int[] region:new int[][]{{0,0},{0,1}}) {
                var selected=PlanetSettlementFeature.terrainCandidate(world,region[0],region[1]);
                helper.assertTrue(selected.equals(PlanetSettlementFeature.terrainCandidate(world,region[0],region[1])),"Terrain selection changed between calls");
                helper.assertTrue(PlanetSettlementFeature.searchCandidates(world.getSeed(),planet,region[0],region[1]).contains(selected),"Unbounded terrain selection");
                var row=new com.google.gson.JsonObject();row.addProperty("dimension","zerog_tweaks:"+planet);row.addProperty("seed",world.getSeed());
                row.addProperty("region_x",region[0]);row.addProperty("region_z",region[1]);
                row.addProperty("chunk_x",selected.x);row.addProperty("chunk_z",selected.z);
                row.addProperty("changed_from_original",!selected.equals(PlanetSettlementFeature.candidate(world.getSeed(),planet,region[0],region[1])));
                rows.add(row);
            }
            helper.assertTrue(world.getChunkSource().getLoadedChunksCount()==loadedBefore,"Candidate search loaded planetary chunks");
        }
        var report=new com.google.gson.JsonObject();report.addProperty("scope","Immutable native terrain selection only; not actual village generation");
        report.addProperty("elapsed_ms",(System.nanoTime()-start)/1000000);report.add("sites",rows);
        try {java.nio.file.Files.writeString(java.nio.file.Path.of("native-village-selection.json"),new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(report));}
        catch(java.io.IOException failure){throw new RuntimeException(failure);}
        helper.succeed();
    }
}
