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
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_derelict") @PrefixGameTestTemplate(false)
public final class DerelictWreckGameTests {
    private static ResourceLocation id(String path) {return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path);}

    @GameTest(templateNamespace="zerog_derelict",template="equipment_empty",timeoutTicks=1200)
    public static void wreck_variants_rotate_with_accessible_real_rewards(GameTestHelper h) {
        var level=h.getLevel(); int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()) {
            var template=level.getStructureManager().get(id("derelict_wreck/small_"+variant)).orElseThrow();
            var origin=new BlockPos(22000+index++*64,128,22000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Wreck placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Small wreck requires exactly one reward chest");
            var chest=chests.get(0);
            h.assertTrue(chest.nbt().getString("LootTable").equals(id("chests/derelict_wreck").toString()),"Wrong wreck loot");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Missing real loot container");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Chest lid blocked");
            // Rotation must preserve the continuous central corridor and side entry.
            for(int z=5;z<=19;z++) {
                var at=origin.offset(net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate
                        .transform(new BlockPos(9,2,z),settings.getMirror(),rotation,settings.getRotationPivot()));
                if(z!=16)h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Ship corridor blocked");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Ship corridor lacks floor");
            }
            ((ChestBlockEntity)level.getBlockEntity(chest.pos())).unpackLootTable(null);
        }
        var table=level.getServer().reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,id("chests/derelict_wreck")));
        var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,BlockPos.ZERO.getCenter()).create(LootContextParamSets.CHEST);
        var seen=new java.util.HashSet<String>();
        for(long seed=1;seed<=1024;seed++)for(var stack:table.getRandomItems(params,seed))
            seen.add(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath());
        for(String material:new String[]{"salvium","wraithsteel","palladine","eidolite"})
            h.assertTrue(seen.contains(material+"_upgrade_smithing_template"),"Wreck loot never rolled "+material);
        h.succeed();
    }

    @GameTest(templateNamespace="zerog_derelict",template="equipment_empty",timeoutTicks=2400)
    public static void eidolon_graveyard_can_generate_small_wreck_without_boss_spawns(GameTestHelper h) {
        var level=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,id("eidolon")));
        h.assertTrue(level!=null,"Missing native Eidolon dimension");
        var structure=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(id("derelict_wreck"));
        h.assertTrue(structure!=null,"Wreck structure not loaded");
        var generator=level.getChunkSource().getGenerator();
        var habitat=TagKey.create(Registries.BIOME,id("has_structure/derelict_wreck"));
        boolean found=false;
        for(int sample=0;sample<64&&!found;sample++) {
            var chunk=new ChunkPos((sample%8)*40,(sample/8)*40);
            var start=structure.generate(level.registryAccess(),generator,generator.getBiomeSource(),
                    level.getChunkSource().randomState(),level.getStructureManager(),0L,chunk,0,level,b->b.is(habitat));
            if(!start.isValid())continue;
            found=true;
            h.assertTrue(start.getPieces().size()==1,"Small wreck generated extra encounter pieces");
            var box=start.getPieces().get(0).getBoundingBox();
            h.assertTrue(box.getXSpan()<=27&&box.getZSpan()<=27&&box.getYSpan()==9,"Wreck escaped its authored bounds");
            // Vanilla terrain adaptation expands StructureStart's reference box by12,
            // not the actual template piece. Verify both contracts independently.
            var reference=start.getBoundingBox();
            h.assertTrue(reference.getXSpan()==box.getXSpan()+24&&reference.getYSpan()==33
                    &&reference.getZSpan()==box.getZSpan()+24,"Unexpected vanilla blending margin");
        }
        h.assertTrue(found,"No suitable Frozen Graveyard terrain in bounded samples");
        h.succeed();
    }
}
