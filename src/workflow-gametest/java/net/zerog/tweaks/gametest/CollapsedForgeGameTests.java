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

@GameTestHolder("zerog_forge_ruin") @PrefixGameTestTemplate(false)
public final class CollapsedForgeGameTests {
    private static ResourceLocation id(String path){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path);}

    @GameTest(templateNamespace="zerog_forge_ruin",template="equipment_empty",timeoutTicks=1200)
    public static void forge_rotations_keep_workshop_access_and_real_template_rewards(GameTestHelper h){
        var level=h.getLevel();int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()){
            var template=level.getStructureManager().get(id("collapsed_forge/small_"+variant)).orElseThrow();
            var origin=new BlockPos(24000+index++*64,128,24000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Forge placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Forge must contain exactly one chest");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals(id("chests/collapsed_forge").toString()),"Wrong forge rewards");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Forge chest has no block entity");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Forge chest lid blocked");
            for(int z=2;z<=16;z++)assertWalkable(h,origin,settings,new BlockPos(8,2,z));
            for(int x=8;x<=11;x++)assertWalkable(h,origin,settings,new BlockPos(x,2,14));
            h.assertTrue(template.filterBlocks(origin,settings,Blocks.BLAST_FURNACE).size()==1,"Cold forge furnace missing");
            h.assertTrue(template.filterBlocks(origin,settings,Blocks.ANVIL).size()==1,"Smithy anvil missing");
            ((ChestBlockEntity)level.getBlockEntity(chest.pos())).unpackLootTable(null);
        }
        var table=level.getServer().reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,id("chests/collapsed_forge")));
        var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,BlockPos.ZERO.getCenter()).create(LootContextParamSets.CHEST);
        var seen=new java.util.HashSet<String>();
        for(long seed=1;seed<=1024;seed++)for(var stack:table.getRandomItems(params,seed))
            seen.add(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath());
        for(String material:new String[]{"ruskite","pyrium","tectium","skarnite"})
            h.assertTrue(seen.contains(material+"_upgrade_smithing_template"),"Forge loot never rolled "+material);
        h.assertTrue(seen.contains("heatproof_plating"),"Approved forge salvage missing");
        h.succeed();
    }

    private static void assertWalkable(GameTestHelper h,BlockPos origin,StructurePlaceSettings settings,BlockPos local){
        var at=origin.offset(StructureTemplate.transform(local,settings.getMirror(),settings.getRotation(),settings.getRotationPivot()));
        h.assertTrue(h.getLevel().getBlockState(at).isAir()&&h.getLevel().getBlockState(at.above()).isAir(),"Forge route blocked");
        h.assertTrue(h.getLevel().getBlockState(at.below()).isSolidRender(h.getLevel(),at.below()),"Forge route lacks floor");
    }

    @GameTest(templateNamespace="zerog_forge_ruin",template="equipment_empty",timeoutTicks=2400)
    public static void native_skarn_can_generate_bounded_forge_and_tags_exclude_lava_lakes(GameTestHelper h){
        var level=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,id("skarn")));
        h.assertTrue(level!=null,"Missing native Skarn");
        var habitat=TagKey.create(Registries.BIOME,id("has_structure/collapsed_forge"));
        var biomes=level.registryAccess().registryOrThrow(Registries.BIOME);
        for(String biome:new String[]{"ember_fields","marble_contact_zone","charwood_barrens","wasteland_ash_plains","wasteland_basalt_fields"})
            h.assertTrue(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME,id(biome))).is(habitat),"Missing forge habitat "+biome);
        h.assertTrue(!biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME,id("wasteland_lava_lakes"))).is(habitat),"Forge enabled in lava lake biome");
        var structure=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(id("collapsed_forge"));
        h.assertTrue(structure!=null,"Forge structure not registered");
        var generator=level.getChunkSource().getGenerator();boolean found=false;
        for(int sample=0;sample<64&&!found;sample++){
            var start=structure.generate(level.registryAccess(),generator,generator.getBiomeSource(),level.getChunkSource().randomState(),
                    level.getStructureManager(),0L,new ChunkPos((sample%8)*40,(sample/8)*40),0,level,b->b.is(habitat));
            if(!start.isValid())continue;
            found=true;
            h.assertTrue(start.getPieces().size()==1,"Unexpected forge encounter pieces");
            var box=start.getPieces().getFirst().getBoundingBox();
            h.assertTrue(box.getXSpan()<=19&&box.getZSpan()<=19&&box.getYSpan()==8,"Forge exceeds authored bounds");
        }
        h.assertTrue(found,"No suitable native Skarn terrain in bounded sample");h.succeed();
    }
}
