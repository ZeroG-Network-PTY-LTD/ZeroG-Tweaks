package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.Container;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_sunken_lab") @PrefixGameTestTemplate(false)
public final class SunkenLabGameTests {
    @GameTest(templateNamespace="zerog_sunken_lab",template="equipment_empty",timeoutTicks=1200)
    public static void laboratory_equipment_access_and_neutralizer_survive_rotations(GameTestHelper h){
        var level=h.getLevel();int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()){
            var template=level.getStructureManager().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","sunken_lab/small_"+variant)).orElseThrow();
            var origin=new BlockPos(33000+index++*64,128,33000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Lab placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Exactly one Lab reward chest required");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals("zerog_tweaks:chests/sunken_lab"),"Wrong Lab loot");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Blocked Lab chest lid");
            for(int x=13;x<=15;x++)for(int z=1;z<20;z++){
                var at=at(origin,settings,new BlockPos(x,2,z));
                h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Blocked service spine");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Missing aisle floor");
            }
            var stands=template.filterBlocks(origin,settings,Blocks.BREWING_STAND);
            h.assertTrue(stands.size()==2,"Chemistry bench lacks two brewing stands");
            for(var stand:stands){
                h.assertTrue(level.getBlockEntity(stand.pos()) instanceof Container,"Apparatus has no real container");
                var inventory=(Container)level.getBlockEntity(stand.pos());
                for(int slot=0;slot<inventory.getContainerSize();slot++)h.assertTrue(inventory.getItem(slot).isEmpty(),"Unexpected free chemistry ingredients");
            }
            h.assertTrue(template.filterBlocks(origin,settings,Blocks.CAULDRON).size()==2,"Missing empty cauldrons");
            for(var centre:new int[][]{{19,7},{23,7},{19,14},{23,14}}){
                var base=at(origin,settings,new BlockPos(centre[0],2,centre[1]));
                var cap=at(origin,settings,new BlockPos(centre[0],7,centre[1]));
                h.assertTrue(level.getBlockState(base).isSolidRender(level,base)&&level.getBlockState(cap).isSolidRender(level,cap),"Tube base or cap missing");
            }
            var broken=variant==0?new BlockPos(23,4,6):new BlockPos(19,4,13);
            h.assertTrue(level.getBlockState(at(origin,settings,broken)).isAir()&&level.getBlockState(at(origin,settings,broken.above())).isAir(),"Synthesis tube lacks broken glass opening");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"No real reward chest");
            var reward=(ChestBlockEntity)level.getBlockEntity(chest.pos());reward.unpackLootTable(null);
            boolean neutralizer=false;
            for(int slot=0;slot<reward.getContainerSize();slot++)if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(reward.getItem(slot).getItem()).toString().equals("zerog_tweaks:neutralizer"))neutralizer=true;
            h.assertTrue(neutralizer,"Guaranteed Neutralizer missing");
        }
        h.succeed();
    }
    private static BlockPos at(BlockPos origin,StructurePlaceSettings settings,BlockPos local){
        return origin.offset(StructureTemplate.transform(local,settings.getMirror(),settings.getRotation(),settings.getRotationPivot()));
    }
}
