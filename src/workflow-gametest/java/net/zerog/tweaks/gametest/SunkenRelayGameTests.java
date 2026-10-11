package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("zerog_sunken_relay") @PrefixGameTestTemplate(false)
public final class SunkenRelayGameTests {
    @GameTest(templateNamespace="zerog_sunken_relay",template="equipment_empty",timeoutTicks=1200)
    public static void flooded_relay_access_waterlogging_and_pearl_survive_rotations(GameTestHelper h) {
        var level=h.getLevel();int index=0;
        for(int variant=0;variant<2;variant++)for(var rotation:Rotation.values()) {
            var template=level.getStructureManager().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","sunken_relay/small_"+variant)).orElseThrow();
            var origin=new BlockPos(35000+index++*64,128,35000);
            var settings=new StructurePlaceSettings().setRotation(rotation);
            h.assertTrue(template.placeInWorld(level,origin,origin,settings,level.random,2),"Relay placement failed");
            for(int x=8;x<=10;x++)for(int z=2;z<14;z++)for(int y=2;y<=4;y++) {
                var pos=at(origin,settings,new BlockPos(x,y,z));
                h.assertTrue(level.getBlockState(pos).is(Blocks.WATER),"Swimming aisle obstructed or drained");
            }
            var chests=template.filterBlocks(origin,settings,Blocks.CHEST);
            h.assertTrue(chests.size()==1,"Exactly one relay reward chest required");
            var chest=chests.getFirst();
            h.assertTrue(chest.nbt().getString("LootTable").equals("zerog_tweaks:chests/sunken_relay"),"Wrong relay loot table");
            h.assertTrue(level.getBlockState(chest.pos()).getValue(BlockStateProperties.WATERLOGGED),"Chest not waterlogged");
            h.assertTrue(level.getBlockState(chest.pos().above()).is(Blocks.WATER),"Chest lid blocked or dry");
            for(var bars:template.filterBlocks(origin,settings,Blocks.IRON_BARS))
                h.assertTrue(level.getFluidState(bars.pos()).is(FluidTags.WATER),"Antenna lost waterlogging");
            h.assertTrue(level.getBlockEntity(chest.pos()) instanceof ChestBlockEntity,"No actual relay chest");
            var reward=(ChestBlockEntity)level.getBlockEntity(chest.pos());reward.unpackLootTable(null);
            boolean pearl=false;
            for(int slot=0;slot<reward.getContainerSize();slot++)
                if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(reward.getItem(slot).getItem()).toString().equals("zerog_tweaks:abyssal_pearl"))pearl=true;
            h.assertTrue(pearl,"Guaranteed Abyssal Pearl absent");
        }
        h.succeed();
    }
    private static BlockPos at(BlockPos origin,StructurePlaceSettings settings,BlockPos local) {
        return origin.offset(StructureTemplate.transform(local,settings.getMirror(),settings.getRotation(),settings.getRotationPivot()));
    }
}
