package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.properties.DripstoneThickness;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class AlienCaveCropGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void twenty_crops_and_planet_cave_families(GameTestHelper helper) {
        // Open sky above the flat test terrain, not the underground template.
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(1,130,1));
        helper.assertTrue(ZGAlienAgriculture.HOMES.size()==20,"Expected twenty crop families");
        for(var entry:ZGAlienAgriculture.CROPS.entrySet()) {
            var crop=entry.getValue().get();level.setBlock(pos.below(),ZGDimensionTerrain.FARMLANDS.get(ZGAlienAgriculture.HOMES.get(entry.getKey())).get().defaultBlockState().setValue(FarmBlock.MOISTURE,7),3);
            var immature=crop.getStateForAge(0);level.setBlock(pos,immature,3);
            helper.assertTrue(immature.canSurvive(level,pos),"Crop cannot grow on native farmland "+entry.getKey());
            crop.performBonemeal(level,net.minecraft.util.RandomSource.create(2),pos,immature);
            helper.assertTrue(crop.getAge(level.getBlockState(pos))>0,"Bonemeal failed "+entry.getKey());
            var mature=crop.getStateForAge(3);level.setBlock(pos,mature,3);
            var drops=Block.getDrops(mature,level,pos,null);
            helper.assertTrue(drops.stream().anyMatch(stack->stack.is(crop.produce().getItem())),"Missing produce loot "+entry.getKey());
            helper.assertTrue(crop.produce().get(net.minecraft.core.component.DataComponents.FOOD)!=null,"Produce not edible");
        }
        helper.assertTrue(ZGPlanetCaveVariants.FAMILIES.size()==34,"Missing cave family");
        for(var entry:ZGPlanetCaveVariants.FAMILIES.entrySet()) {
            var family=entry.getValue();level.setBlock(pos.above(),Blocks.STONE.defaultBlockState(),3);
            var bearing=family.head().get().defaultBlockState().setValue(CaveVines.BERRIES,true);level.setBlock(pos,bearing,3);
            helper.assertTrue(bearing.canSurvive(level,pos),"Vine does not hang "+entry.getKey());
            var drops=Block.getDrops(bearing,level,pos,null);
            helper.assertTrue(drops.stream().anyMatch(s->s.is(ZGPlanetCaveVariants.berry(entry.getKey()).getItem())),"Wrong cave berry loot");
            ZGPlanetCaveVariants.pick(entry.getKey(),bearing,level,pos,null);
            helper.assertTrue(!level.getBlockState(pos).getValue(CaveVines.BERRIES),"Berry pick failed");
            helper.assertTrue(ZGPlanetCaveVariants.berry(entry.getKey()).get(net.minecraft.core.component.DataComponents.FOOD)!=null,"Berry not edible");
            var root=pos.below(2);level.setBlock(root.below(),family.rock().get().defaultBlockState(),3);
            var spike=family.point().get().defaultBlockState().setValue(PointedDripstoneBlock.TIP_DIRECTION,Direction.UP);
            level.setBlock(root,spike.setValue(PointedDripstoneBlock.THICKNESS,DripstoneThickness.BASE),3);
            helper.assertTrue(spike.canSurvive(level,root.above()),"Custom stalagmite chain cannot survive");
            level.setBlock(root.above(),spike,3);
        }
        // Native stem progression must produce our fruit and attached stem.
        for(var entry:ZGAlienAgriculture.STEMS.entrySet()) {
            var at=pos.offset(8,0,0);for(int x=-2;x<=2;x++)for(int z=-2;z<=2;z++) {
                level.setBlock(at.offset(x,-1,z),Blocks.FARMLAND.defaultBlockState().setValue(FarmBlock.MOISTURE,7),3);
                level.setBlock(at.offset(x,0,z),Blocks.AIR.defaultBlockState(),3);
                level.setBlock(at.offset(x,1,z),Blocks.AIR.defaultBlockState(),3);
            }
            var stem=entry.getValue().get().defaultBlockState().setValue(StemBlock.AGE,7);level.setBlock(at,stem,3);
            var random=net.minecraft.util.RandomSource.create(99);
            for(int n=0;n<1000 && level.getBlockState(at).is(entry.getValue().get());n++) stem.randomTick(level,at,random);
            boolean found=false;for(var d:Direction.Plane.HORIZONTAL)found|=level.getBlockState(at.relative(d)).is(ZGAlienAgriculture.GOURDS.get(entry.getKey()).get());
            helper.assertTrue(found,"Native stem did not create alien gourd "+entry.getKey());
        }
        helper.succeed();
    }
}
