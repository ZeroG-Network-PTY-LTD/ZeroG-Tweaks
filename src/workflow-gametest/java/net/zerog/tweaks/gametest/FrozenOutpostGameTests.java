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

@GameTestHolder("zerog_frozen_outpost") @PrefixGameTestTemplate(false)
public final class FrozenOutpostGameTests {
    @GameTest(templateNamespace="zerog_frozen_outpost",template="equipment_empty",timeoutTicks=1200)
    public static void shelter_access_and_actual_reward_survive_every_rotation(GameTestHelper h){
        var level=h.getLevel();int index=0;
        for(int v=0;v<2;v++)for(var rotation:Rotation.values()){
            var id=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","frozen_outpost/small_"+v);
            var template=level.getStructureManager().get(id).orElseThrow();
            var origin=new BlockPos(30000+index++*48,128,30000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Outpost placement failed");
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Exactly one outpost chest required");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals("zerog_tweaks:chests/frozen_outpost"),"Wrong reward table");
            h.assertTrue(level.getBlockState(chest.pos().above()).isAir(),"Blocked chest lid");
            for(int z=1;z<13;z++){
                var at=origin.offset(StructureTemplate.transform(new BlockPos(8,2,z),settings.getMirror(),rotation,settings.getRotationPivot()));
                h.assertTrue(level.getBlockState(at).isAir()&&level.getBlockState(at.above()).isAir(),"Blocked entrance corridor");
                h.assertTrue(level.getBlockState(at.below()).isSolidRender(level,at.below()),"Missing approach floor");
            }
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"No physical chest");
            var entity=(ChestBlockEntity)level.getBlockEntity(chest.pos());entity.unpackLootTable(null);
            boolean cryo=false;
            for(int slot=0;slot<entity.getContainerSize();slot++)
                if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(entity.getItem(slot).getItem()).toString().equals("zerog_tweaks:cryo_core"))cryo=true;
            h.assertTrue(cryo,"Guaranteed approved Cryo Core reward missing");
        }
        h.succeed();
    }
}
