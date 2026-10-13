package net.zerog.tweaks.gametest;

import java.nio.file.Files;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.storage.LevelResource;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.PlanetTestHub;

@GameTestHolder("zerog_hub_tiers") @PrefixGameTestTemplate(false)
public final class PlanetStructureShowcaseGameTests {
    @GameTest(templateNamespace="zerog_hub_tiers",template="equipment_empty",timeoutTicks=2000)
    public static void three_planet_templates_have_loot_and_hostile_spawners(GameTestHelper h) {
        var server=h.getLevel().getServer();
        String[] planets={"cerulon","skarn","eidolon"};
        String[] names={"water_bio_habitat","hot_ring_monolith","ice_spire_outpost"};
        var origin=new BlockPos(512,90,512);
        for(int i=0;i<3;i++) {
            var level=PlanetTestHub.planet(server,"zerog_tweaks:"+planets[i]);
            h.assertTrue(level!=null,"Missing showcase dimension");
            for(int x=32;x<=35;x++)for(int z=32;z<=35;z++)level.getChunk(x,z);
            var template=level.getStructureManager().getOrCreate(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planetary_showcase/"+names[i]));
            h.assertTrue(template.getSize().equals(new BlockPos(49,64,49)),"Wrong template extent");
            h.assertTrue(template.placeInWorld(level,origin,origin,new StructurePlaceSettings(),level.random,2),"Template placement failed");
            for(int x:new int[]{14,34}) {
                var chest=level.getBlockEntity(origin.offset(x,4,14));
                h.assertTrue(chest instanceof ChestBlockEntity,"Missing loot room chest");
                var inventory=(ChestBlockEntity)chest;
                boolean loot=false;for(int slot=0;slot<27;slot++)loot|=!inventory.getItem(slot).isEmpty();
                h.assertTrue(loot,"Loot table did not produce supplies");
            }
            h.assertTrue(level.getBlockEntity(origin.offset(18,4,32)) instanceof SpawnerBlockEntity,"Missing hostile spawner");
            h.assertTrue(level.getBlockState(origin.offset(24,5,24)).isAir(),"Central underground route blocked");
        }
        try {
            Files.writeString(server.getWorldPath(LevelResource.ROOT).resolve("zerog-structure-showcase.json"),
                "{\"verified\":true,\"origin\":[512,90,512],\"dimensions\":[\"cerulon\",\"skarn\",\"eidolon\"],\"templates\":3,\"loot_chests\":6,\"spawners\":3,\"natural_generation\":false}");
        }catch(java.io.IOException error){throw new IllegalStateException(error);}
        h.succeed();
    }
}
