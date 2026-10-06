package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.worldgen.PlanetSettlementFeature;

@GameTestHolder("zerog_lore") @PrefixGameTestTemplate(false)
public final class SolLoreGameTests {
    @GameTest(templateNamespace="zerog_lore",template="equipment_empty",timeoutTicks=200)
    public static void every_rustborn_layout_contains_a_ground_level_aresite_shrine(GameTestHelper h){
        var level=h.getLevel();var centre=h.absolutePos(new BlockPos(96,24,96));
        for(int x=(centre.getX()-24)>>4;x<=(centre.getX()+24)>>4;x++)for(int z=(centre.getZ()-24)>>4;z<=(centre.getZ()+24)>>4;z++)level.getChunk(x,z);
        for(int layout=0;layout<4;layout++){
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,10,22)))level.setBlock(at,Blocks.AIR.defaultBlockState(),2);
            for(var at:BlockPos.betweenClosed(centre.offset(-22,-1,-22),centre.offset(22,0,22)))level.setBlock(at,ZGDimensionTerrain.SOILS.get("mars").get().defaultBlockState(),2);
            h.assertTrue(PlanetSettlementFeature.build(level,centre,"mars",layout,RandomSource.create(23)),"Rustborn layout rejected");
            int cores=0;
            for(var at:BlockPos.betweenClosed(centre.offset(-17,1,-17),centre.offset(17,5,17)))if(level.getBlockState(at).is(BlockInit.ARESITE_BLOCK.get())){
                cores++;h.assertTrue(level.getBlockState(at.below()).is(BlockInit.MARTIAN_STONE_BRICKS.get()),"Aresite core has no Mars pedestal");
            }
            h.assertTrue(cores==1,"Rustborn village must contain exactly one Aresite shrine, layout "+layout);
            h.assertTrue(level.getBlockState(centre).is(BlockInit.SETTLEMENT_ANCHOR.get()),"Shrine replaced settlement anchor");
        }h.succeed();
    }
}
