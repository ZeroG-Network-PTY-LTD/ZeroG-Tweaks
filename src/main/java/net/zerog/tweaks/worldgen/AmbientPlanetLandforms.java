package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.zerog.tweaks.registry.ZGGasVents;

/** Small natural steam/geyser fields and extinct hot-world cones. No lava or damage. */
public final class AmbientPlanetLandforms {
    public static void place(WorldGenLevel level,RandomSource random,BlockPos centre,String theme,Block surface) {
        if(!ZGGasVents.AMBIENT_VENTS.containsKey(theme))return;
        var vent=ZGGasVents.AMBIENT_VENTS.get(theme).get().defaultBlockState();
        boolean hot=theme.equals("skarn") || theme.equals("solvane");
        int count=3+random.nextInt(4);
        if(hot && random.nextInt(4)==0) {
            // Preflight the entire footprint before editing. Never flatten structures,
            // trees, hive entities or gates. Feature-local RNG only on worldgen workers.
            var tops=new java.util.ArrayList<BlockPos>();
            var columns=new java.util.ArrayList<BlockPos>();
            for(int dx=-4;dx<=4;dx++)for(int dz=-4;dz<=4;dz++) {
                if(dx*dx+dz*dz>16)continue;
                if(!level.hasChunkAt(centre.offset(dx,0,dz)))return;
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,centre.offset(dx,0,dz)).below();
                if(!level.hasChunkAt(pos) || Math.abs(pos.getY()-centre.getY())>2
                        || !level.getBlockState(pos).is(surface) || level.getBlockEntity(pos)!=null)return;
                for(int y=1;y<=4;y++)if(!level.isEmptyBlock(pos.above(y)))return;
                columns.add(pos);
                double radius=Math.sqrt(dx*dx+dz*dz);
                if(radius<1.5)tops.add(pos.above(Math.max(0,(int)Math.round(4-radius))));
            }
            shuffle(tops,random);
            if(tops.size()<count)return;
            for(var ground:columns) {
                double radius=Math.hypot(ground.getX()-centre.getX(),ground.getZ()-centre.getZ());
                int height=Math.max(0,(int)Math.round(4-radius));
                for(int y=0;y<=height;y++) level.setBlock(ground.above(y),
                        (radius<1.5?Blocks.OBSIDIAN:Blocks.BASALT).defaultBlockState(),2);
            }
            for(int i=0;i<count;i++)level.setBlock(tops.get(i),vent,2);
        } else {
            var candidates=new java.util.ArrayList<BlockPos>();
            for(int dx=-3;dx<=3;dx++)for(int dz=-3;dz<=3;dz++) {
                if(!level.hasChunkAt(centre.offset(dx,0,dz)))continue;
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,centre.offset(dx,0,dz)).below();
                if(Math.abs(pos.getY()-centre.getY())<=2 && level.getBlockState(pos).is(surface)
                        && level.isEmptyBlock(pos.above()) && level.getBlockEntity(pos)==null)candidates.add(pos);
            }
            if(candidates.size()<count)return;
            shuffle(candidates,random);
            for(int i=0;i<count;i++)level.setBlock(candidates.get(i),vent,2);
        }
    }
    private static void shuffle(java.util.List<BlockPos> sites,RandomSource random) {
        for(int i=sites.size()-1;i>0;i--)java.util.Collections.swap(sites,i,random.nextInt(i+1));
    }
    private AmbientPlanetLandforms() {}
}
