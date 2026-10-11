package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_observatory") @PrefixGameTestTemplate(false)
public final class BuriedObservatoryGameTests {
    @GameTest(templateNamespace="zerog_observatory",template="equipment_empty",timeoutTicks=1200)
    public static void room_access_and_fragments_survive_every_rotation(GameTestHelper h){
        var level=h.getLevel();int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()){
            var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","buried_observatory/small_"+variant);
            var template=level.getStructureManager().get(id).orElseThrow();
            var origin=new BlockPos(32000+index++*48,128,32000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Observatory placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Exactly one Observatory chest required");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals("zerog_tweaks:chests/buried_observatory"),"Wrong Observatory loot");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Blocked chest lid");
            for(int z=1;z<15;z++){
                var at=origin.offset(StructureTemplate.transform(new BlockPos(10,2,z),settings.getMirror(),rotation,settings.getRotationPivot()));
                h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Blocked approach");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Missing approach floor");
            }
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Missing physical chest");
            var entity=(ChestBlockEntity)level.getBlockEntity(chest.pos());entity.unpackLootTable(null);
            boolean fragment=false;
            for(int slot=0;slot<entity.getContainerSize();slot++)
                if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(entity.getItem(slot).getItem()).toString().equals("zerog_tweaks:star_map_fragment"))fragment=true;
            h.assertTrue(fragment,"Guaranteed Star Map Fragment missing");
        }
        h.succeed();
    }
}
