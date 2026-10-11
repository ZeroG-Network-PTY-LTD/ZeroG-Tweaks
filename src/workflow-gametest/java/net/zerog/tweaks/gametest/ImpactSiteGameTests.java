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

@GameTestHolder("zerog_impact_site") @PrefixGameTestTemplate(false)
public final class ImpactSiteGameTests {
    @GameTest(templateNamespace="zerog_impact_site",template="equipment_empty",timeoutTicks=1200)
    public static void crater_access_and_stardust_survive_every_rotation(GameTestHelper h){
        var level=h.getLevel(); int index=0;
        for(int variant=0;variant<2;variant++) for(var rotation:Rotation.values()){
            var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","impact_site/small_"+variant);
            var template=level.getStructureManager().get(id).orElseThrow();
            var origin=new BlockPos(31000+index++*48,128,31000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Impact placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Exactly one Impact chest required");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals("zerog_tweaks:chests/impact_site"),"Wrong Impact loot");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Blocked chest lid");
            for(int z=1;z<14;z++){
                var at=origin.offset(StructureTemplate.transform(new BlockPos(10,1,z),settings.getMirror(),rotation,settings.getRotationPivot()));
                h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Blocked approach");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Missing crater floor");
            }
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"Missing physical chest");
            var entity=(ChestBlockEntity)level.getBlockEntity(chest.pos()); entity.unpackLootTable(null);
            boolean stardust=false;
            for(int slot=0;slot<entity.getContainerSize();slot++)
                if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(entity.getItem(slot).getItem()).toString().equals("zerog_tweaks:stardust")) stardust=true;
            h.assertTrue(stardust,"Guaranteed Stardust missing");
        }
        h.succeed();
    }
}
