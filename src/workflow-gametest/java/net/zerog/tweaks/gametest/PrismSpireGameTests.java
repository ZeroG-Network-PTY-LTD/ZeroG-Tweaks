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
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Loaded template/reward and bounded terrain checks; not client or natural-placement approval. */
@GameTestHolder("zerog_galaxy_access") @PrefixGameTestTemplate(false)
public final class PrismSpireGameTests {
    private static ResourceLocation id(String path) { return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path); }

    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=1200)
    public static void spire_rotations_preserve_access_and_real_chest_rewards(GameTestHelper h) {
        var level=h.getLevel();
        var template=level.getStructureManager().get(id("prism_spire/tower")).orElseThrow();
        int index=0;
        for(var rotation:Rotation.values()) {
            var origin=new BlockPos(20000+index++*64,128,20000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Spire template placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Spire must contain exactly one authored reward chest");
            var chest=chests.get(0);
            h.assertTrue(chest.nbt()!=null&&chest.nbt().getString("LootTable").equals(id("chests/prism_spire").toString()),"Wrong spire reward binding");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Placed reward is not a real chest");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Spire chest lid is obstructed");
            var placed=(ChestBlockEntity)level.getBlockEntity(chest.pos());
            placed.unpackLootTable(null);
            boolean lens=false;
            for(int slot=0;slot<placed.getContainerSize();slot++)
                if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(placed.getItem(slot).getItem()).equals(id("refracting_lens")))lens=true;
            h.assertTrue(lens,"Actual placed chest did not generate the guaranteed lens");
            var ladder=template.filterBlocks(origin,settings,Blocks.LADDER);
            h.assertTrue(ladder.size()==15,"Continuous authored ladder was lost");
            for(var rung:ladder) {
                var facing=level.getBlockState(rung.pos()).getValue(net.minecraft.world.level.block.LadderBlock.FACING);
                h.assertTrue(level.getBlockState(rung.pos().relative(facing.getOpposite())).isSolidRender(level,rung.pos().relative(facing.getOpposite())),"Ladder has no backing wall");
                int height=rung.pos().getY()-origin.getY();
                var landing=rung.pos().relative(facing);
                if(height==1||height==7||height==13)
                    h.assertTrue(level.getBlockState(landing.above()).isAir(),"Floor exit above ladder is blocked");
                else h.assertTrue(level.getBlockState(landing).isAir(),"Ladder climbing space is blocked");
            }
        }
        var table=level.getServer().reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,id("chests/prism_spire")));
        h.assertTrue(table!=LootTable.EMPTY,"Spire loot table did not load");
        var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,BlockPos.ZERO.getCenter()).create(LootContextParamSets.CHEST);
        var seen=new java.util.HashSet<String>();
        for(long seed=1;seed<=1024;seed++)for(var stack:table.getRandomItems(params,seed))
            seen.add(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).getPath());
        for(var metal:new String[]{"cobaltium","cyrrium","aurelion"})
            h.assertTrue(seen.contains(metal+"_upgrade_smithing_template"),"Spire never rolled ladder template "+metal);
        h.succeed();
    }

    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=2400)
    public static void native_crystal_terrain_can_generate_a_bounded_spire(GameTestHelper h) {
        var level=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,id("g2_p6")));
        h.assertTrue(level!=null,"Native crystal dimension fixture is required");
        var structure=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(id("prism_spire"));
        h.assertTrue(structure!=null,"Spire structure is not registered");
        var habitat=TagKey.create(Registries.BIOME,id("has_structure/prism_spire"));
        var generator=level.getChunkSource().getGenerator();
        boolean found=false;
        for(int sample=0;sample<64&&!found;sample++) {
            var chunk=new ChunkPos((sample%8)*40,(sample/8)*40);
            var start=structure.generate(level.registryAccess(),generator,generator.getBiomeSource(),
                    level.getChunkSource().randomState(),level.getStructureManager(),0L,chunk,0,level,b->b.is(habitat));
            if(!start.isValid())continue;
            found=true;
            h.assertTrue(start.getPieces().size()==1,"Standalone spire generated unexpected pieces");
            var box=start.getBoundingBox();
            h.assertTrue((box.minX()>>4)>=chunk.x-8&&(box.maxX()>>4)<=chunk.x+8
                    &&(box.minZ()>>4)>=chunk.z-8&&(box.maxZ()>>4)<=chunk.z+8,"Spire escapes reference window");
        }
        h.assertTrue(found,"No acceptable dry crystal terrain found in64 bounded samples");
        h.succeed();
    }
}
