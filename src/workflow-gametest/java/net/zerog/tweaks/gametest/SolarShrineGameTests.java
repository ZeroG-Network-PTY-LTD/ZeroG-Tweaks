package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_solar_shrine") @PrefixGameTestTemplate(false)
public final class SolarShrineGameTests {
    private static ResourceLocation id(String path){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path);}

    @GameTest(templateNamespace="zerog_solar_shrine",template="equipment_empty",timeoutTicks=1200)
    public static void shrine_rotations_preserve_access_lamps_and_approved_rewards(GameTestHelper h){
        var level=h.getLevel();int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()){
            var template=level.getStructureManager().get(id("solar_shrine/small_"+variant)).orElseThrow();
            var origin=new BlockPos(26000+index++*64,128,26000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Shrine placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Shrine requires exactly one reward chest");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals(id("chests/solar_shrine").toString()),"Wrong shrine rewards");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Missing actual shrine chest");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Shrine chest lid blocked");
            for(int z=1;z<=13;z++){
                var at=origin.offset(StructureTemplate.transform(new BlockPos(9,2,z),settings.getMirror(),rotation,settings.getRotationPivot()));
                h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Shrine approach blocked");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Shrine approach lacks a floor");
            }
            var lamps=template.filterBlocks(origin,settings,net.zerog.tweaks.registry.BlockInit.FUSION_LAMP.get());
            h.assertTrue(lamps.size()==9,"Shrine pillar/panel lighting missing");
            ((ChestBlockEntity)level.getBlockEntity(chest.pos())).unpackLootTable(null);
        }
        var table=level.getServer().reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,id("chests/solar_shrine")));
        var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,BlockPos.ZERO.getCenter()).create(LootContextParamSets.CHEST);
        var seen=new java.util.HashSet<String>();
        for(long seed=1;seed<=1024;seed++)for(var stack:table.getRandomItems(params,seed))
            seen.add(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath());
        for(String material:new String[]{"photium","radiantine","astrium","solvanite"})
            h.assertTrue(seen.contains(material+"_upgrade_smithing_template"),"Shrine loot never rolled "+material);
        h.assertTrue(!seen.contains("heart_of_solvane"),"Shrine bypassed final boss Heart reward");h.succeed();
    }

    @GameTest(templateNamespace="zerog_solar_shrine",template="equipment_empty",timeoutTicks=2400)
    public static void native_solvane_generates_bounded_shrine_without_other_planet_habitats(GameTestHelper h){
        var level=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,id("solvane")));
        h.assertTrue(level!=null,"Missing native Solvane");
        var habitat=TagKey.create(Registries.BIOME,id("has_structure/solar_shrine"));
        var biomes=level.registryAccess().registryOrThrow(Registries.BIOME);
        for(String biome:new String[]{"corona_flats","sunspot_plateaus","gildwood_oasis"})
            h.assertTrue(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME,id(biome))).is(habitat),"Missing shrine habitat "+biome);
        h.assertTrue(!biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME,id("ember_fields"))).is(habitat),"Shrine incorrectly targets Skarn");
        var structure=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(id("solar_shrine"));
        h.assertTrue(structure!=null,"Shrine structure not loaded");
        var generator=level.getChunkSource().getGenerator();boolean found=false;
        for(int sample=0;sample<64&&!found;sample++){
            var start=structure.generate(level.registryAccess(),generator,generator.getBiomeSource(),level.getChunkSource().randomState(),
                    level.getStructureManager(),0L,new ChunkPos((sample%8)*40,(sample/8)*40),0,level,b->b.is(habitat));
            if(!start.isValid())continue;
            found=true;h.assertTrue(start.getPieces().size()==1,"Unexpected shrine encounter pieces");
            var box=start.getPieces().getFirst().getBoundingBox();
            h.assertTrue(box.getXSpan()==19&&box.getZSpan()==19&&box.getYSpan()==9,"Shrine exceeds authored bounds");
        }
        h.assertTrue(found,"No suitable native Solvane terrain in bounded sample");h.succeed();
    }
}
