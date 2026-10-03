package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Excavated crossing mine tunnels, support arches, rails and a planetary loot chest. */
public final class PlanetMineshaftFeature extends Feature<NoneFeatureConfiguration> {
    public PlanetMineshaftFeature() {super(NoneFeatureConfiguration.CODEC);}
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        var level=context.level();var at=context.origin().offset(8,0,8);
        if(!ZGDimensionTerrain.SOILS.containsKey(level.getLevel().dimension().location().getPath())) return false;
        int y=level.getHeight(Heightmap.Types.OCEAN_FLOOR_WG,at.getX(),at.getZ())-22-context.random().nextInt(28);
        return build(level,new BlockPos(at.getX(),y,at.getZ()),context.random());
    }
    public static boolean build(WorldGenLevel level,BlockPos centre,net.minecraft.util.RandomSource random) {
        if(centre.getY()<level.getMinBuildHeight()+12 || centre.getY()>level.getMaxBuildHeight()-8) return false;
        if(level instanceof net.minecraft.server.level.ServerLevel server
                && net.zerog.tweaks.travel.ArrivalProtection.intersects(server,centre.offset(-18,-1,-18),centre.offset(18,4,18))) return false;
        // Only solid, dry terrain. Never drain an ocean or cut through a machine.
        for(int axis=0;axis<2;axis++) for(int t=-18;t<=18;t++) for(int w=-1;w<=1;w++) for(int y=-1;y<=3;y++) {
            var pos=centre.offset(axis==0?t:w,y,axis==0?w:t);
            if(!level.hasChunkAt(pos) || level.getBlockEntity(pos)!=null || !level.getFluidState(pos).isEmpty()) return false;
        }
        for(int axis=0;axis<2;axis++) for(int t=-18;t<=18;t++) for(int w=-1;w<=1;w++) {
            var base=centre.offset(axis==0?t:w,0,axis==0?w:t);
            level.setBlock(base.below(),BlockInit.CORRODED_HULL.get().defaultBlockState(),2);
            for(int y=0;y<=3;y++) level.setBlock(base.above(y),Blocks.AIR.defaultBlockState(),2);
            if(t%6==0) {
                if(Math.abs(w)==1) for(int y=0;y<=2;y++) level.setBlock(base.above(y),BlockInit.HULL_PLATING.get().defaultBlockState(),2);
                level.setBlock(base.above(3),BlockInit.HULL_PLATING.get().defaultBlockState(),2);
            }
            if(w==0 && axis==0) level.setBlock(base,Blocks.RAIL.defaultBlockState(),2);
            if(w==0 && t%12==0) level.setBlock(base.above(3),Blocks.SEA_LANTERN.defaultBlockState(),2);
        }
        var chest=centre.offset(0,0,2);level.setBlock(chest,Blocks.CHEST.defaultBlockState(),2);
        if(level.getBlockEntity(chest) instanceof RandomizableContainerBlockEntity container)
            container.setLootTable(ResourceKey.create(Registries.LOOT_TABLE,
                    ResourceLocation.fromNamespaceAndPath("zerog_tweaks","chests/buried_observatory")),random.nextLong());
        return true;
    }
}
