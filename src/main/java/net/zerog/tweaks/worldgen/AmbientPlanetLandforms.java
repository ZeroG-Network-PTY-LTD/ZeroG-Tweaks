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
        var vent=ZGGasVents.AMBIENT_VENTS.get(theme).get().defaultBlockState();
        boolean hot=theme.equals("skarn") || theme.equals("solvane");
        if(hot && random.nextInt(4)==0) {
            // Preflight the entire footprint before editing. Never flatten structures,
            // trees, hive entities or gates. Feature-local RNG only on worldgen workers.
            for(int dx=-4;dx<=4;dx++)for(int dz=-4;dz<=4;dz++) {
                if(dx*dx+dz*dz>16)continue;
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,centre.offset(dx,0,dz)).below();
                if(!level.hasChunkAt(pos) || Math.abs(pos.getY()-centre.getY())>2
                        || !level.getBlockState(pos).is(surface) || level.getBlockEntity(pos)!=null)return;
                for(int y=1;y<=4;y++)if(!level.isEmptyBlock(pos.above(y)))return;
            }
            for(int dx=-4;dx<=4;dx++)for(int dz=-4;dz<=4;dz++) {
                double radius=Math.sqrt(dx*dx+dz*dz);if(radius>4)continue;
                var ground=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,centre.offset(dx,0,dz)).below();
                int height=Math.max(0,(int)Math.round(4-radius));
                for(int y=0;y<=height;y++) level.setBlock(ground.above(y),
                        (radius<1.5?Blocks.OBSIDIAN:Blocks.BASALT).defaultBlockState(),2);
                if(radius<1.5)level.setBlock(ground.above(height),vent,2);
            }
        } else {
            for(int n=0;n<3+random.nextInt(4);n++) {
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,
                        centre.offset(random.nextInt(7)-3,0,random.nextInt(7)-3)).below();
                if(level.hasChunkAt(pos) && level.getBlockState(pos).is(surface)
                        && level.isEmptyBlock(pos.above()) && level.getBlockEntity(pos)==null)
                    level.setBlock(pos,vent,2);
            }
        }
    }
    private AmbientPlanetLandforms() {}
}
