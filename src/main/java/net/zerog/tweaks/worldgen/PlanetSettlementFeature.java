package net.zerog.tweaks.worldgen;

import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BedBlock;
import net.minecraft.world.level.block.DoorBlock;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.state.properties.BedPart;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGPlanetCrops;

/** Randomized 3-D colonies. No Star Glass or entity creation on worldgen workers. */
public final class PlanetSettlementFeature extends Feature<NoneFeatureConfiguration> {
    private static final int MAX_GRADE = 6;
    public PlanetSettlementFeature() {super(NoneFeatureConfiguration.CODEC);}
    public static net.minecraft.world.level.ChunkPos candidate(long seed,String dimension,int regionX,int regionZ) {
        var site=RandomSource.create(seed ^ ((long)regionX*341873128712L)
                ^ ((long)regionZ*132897987541L) ^ dimension.hashCode());
        return new net.minecraft.world.level.ChunkPos(regionX*50+16+site.nextInt(18),regionZ*50+16+site.nextInt(18));
    }
    public static List<net.minecraft.world.level.ChunkPos> searchCandidates(long seed,String dimension,int rx,int rz) {
        var base=candidate(seed,dimension,rx,rz);
        var sites=new java.util.LinkedHashSet<net.minecraft.world.level.ChunkPos>();
        sites.add(base);
        for(int[] delta:new int[][]{{6,0},{-6,0},{0,6},{0,-6},{4,4},{-4,-4}}) {
            int x=Math.max(rx*50+16,Math.min(rx*50+33,base.x+delta[0]));
            int z=Math.max(rz*50+16,Math.min(rz*50+33,base.z+delta[1]));
            sites.add(new net.minecraft.world.level.ChunkPos(x,z));
        }
        return List.copyOf(sites);
    }
    /** Selection depends only on immutable base terrain, never generated neighbour chunks. */
    public static net.minecraft.world.level.ChunkPos terrainCandidate(long seed,String dimension,int rx,int rz,
            java.util.function.ToIntFunction<net.minecraft.world.level.ChunkPos> score) {
        for(var site:searchCandidates(seed,dimension,rx,rz))if(score.applyAsInt(site)==0)return site;
        return candidate(seed,dimension,rx,rz);
    }
    private static int terrainScore(FeaturePlaceContext<NoneFeatureConfiguration> context,net.minecraft.world.level.ChunkPos site) {
        return terrainScore(context.chunkGenerator(),context.level(),context.level().getLevel().getChunkSource().randomState(),site);
    }
    public static net.minecraft.world.level.ChunkPos terrainCandidate(net.minecraft.server.level.ServerLevel level,int rx,int rz) {
        return terrainCandidate(level.getSeed(),level.dimension().location().getPath(),rx,rz,
                site->terrainScore(level.getChunkSource().getGenerator(),level,level.getChunkSource().randomState(),site));
    }
    private static int terrainScore(net.minecraft.world.level.chunk.ChunkGenerator generator,
            net.minecraft.world.level.LevelHeightAccessor heights,net.minecraft.world.level.levelgen.RandomState randomState,
            net.minecraft.world.level.ChunkPos site) {
        int x=site.getMinBlockX()+8,z=site.getMinBlockZ()+8;
        int centreY=generator.getFirstFreeHeight(x,z,Heightmap.Types.OCEAN_FLOOR_WG,heights,randomState)-1;
        for(int dx:new int[]{-18,0,18})for(int dz:new int[]{-18,0,18}) {
            int surface=generator.getFirstFreeHeight(x+dx,z+dz,Heightmap.Types.WORLD_SURFACE_WG,heights,randomState);
            int floor=generator.getFirstFreeHeight(x+dx,z+dz,Heightmap.Types.OCEAN_FLOOR_WG,heights,randomState);
            if(surface!=floor || Math.abs(floor-1-centreY)>MAX_GRADE)return 1;
        }
        return 0;
    }
    public static List<BlockPos> homes(int layout) {
        return switch(Math.floorMod(layout,4)) {
            case 1 -> List.of(new BlockPos(-11,0,-10),new BlockPos(11,0,-10),new BlockPos(0,0,12));
            case 2 -> List.of(new BlockPos(-12,0,0),new BlockPos(12,0,0),new BlockPos(0,0,-12));
            case 3 -> List.of(new BlockPos(-10,0,-11),new BlockPos(0,0,12),new BlockPos(10,0,-11));
            default -> List.of(new BlockPos(-10,0,-10),new BlockPos(10,0,-10),new BlockPos(0,0,11));
        };
    }
    public static boolean usedColumn(int x,int z,int layout,String dimension) {
        return usedColumn(x,z,homes(layout),PlanetEcologyProfile.theme(dimension).equals("mars"));
    }
    private static boolean usedColumn(int x,int z,List<BlockPos> homes,boolean shrine) {
        if(Math.max(Math.abs(x),Math.abs(z))>17)return false;
        if(Math.abs(x)<=1 || Math.abs(z)<=1)return true;
        for(var home:homes) {
            if(Math.abs(x-home.getX())<=4 && Math.abs(z-home.getZ())<=4)return true;
            if(z==home.getZ()+5 && x>=Math.min(0,home.getX()) && x<=Math.max(0,home.getX()))return true;
        }
        if(Math.abs(Math.abs(x)-12)<=3 && Math.abs(z-12)<=2)return true;
        if(shrine && x>=4 && x<=6 && z>=2 && z<=4)return true;
        return x==-16 && z==5 || x==-14 && z>=3 && z<=7;
    }
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        String dimension=context.level().getLevel().dimension().location().getPath();
        if(!ZGDimensionTerrain.SOILS.containsKey(dimension)) return false;
        // One seed-selected candidate per 50x50 chunk region. Candidate offsets
        // 16..33 guarantee at least 33 chunks between neighbouring region sites.
        int cx=context.origin().getX()>>4,cz=context.origin().getZ()>>4;
        int rx=Math.floorDiv(cx,50),rz=Math.floorDiv(cz,50);
        if(!searchCandidates(context.level().getSeed(),dimension,rx,rz)
                .contains(new net.minecraft.world.level.ChunkPos(cx,cz)))return false;
        var site=terrainCandidate(context.level().getSeed(),dimension,rx,rz,pos->terrainScore(context,pos));
        if(cx!=site.x || cz!=site.z) return false;
        var origin=context.origin().offset(8,0,8);
        int y=groundY(context.level(),origin.getX(),origin.getZ());
        // The actual layout's used columns are validated by build. Unused corner
        // ponds are not permission to reject every house, or drain a square lawn.
        return tryLayouts(context.level(),new BlockPos(origin.getX(),y,origin.getZ()),dimension,context.random().nextInt(4),context.random());
    }
    private static int groundY(WorldGenLevel level,int x,int z) {
        int y=level.getHeight(level instanceof net.minecraft.server.level.ServerLevel
                ?Heightmap.Types.MOTION_BLOCKING_NO_LEAVES:Heightmap.Types.WORLD_SURFACE_WG,x,z)-1;
        // WORLD_SURFACE_WG includes crowns and vines: descend through vegetation,
        // not water, rather than placing the whole settlement on a tree canopy.
        while(y>level.getMinBuildHeight()) {
            var pos=new BlockPos(x,y,z);var state=level.getBlockState(pos);
            if(state.getFluidState().isEmpty() && (state.is(net.minecraft.tags.BlockTags.LEAVES)
                    || state.is(net.minecraft.tags.BlockTags.LOGS) || !state.isSolidRender(level,pos))) y--;
            else break;
        }
        return y;
    }
    public static boolean tryLayouts(WorldGenLevel level,BlockPos centre,String dimension,int preferred,RandomSource random) {
        for(int offset=0;offset<4;offset++) {
            if(build(level,centre,dimension,Math.floorMod(preferred+offset,4),random)) return true;
        }
        return false;
    }
    public static boolean build(WorldGenLevel level,BlockPos centre,String dimension,int layout,RandomSource random) {
        if(!ZGDimensionTerrain.SOILS.containsKey(dimension) || centre.getY()<level.getMinBuildHeight()+20 || centre.getY()>level.getMaxBuildHeight()-12) return false;
        // Never consult server SavedData from a worldgen worker. Only explicit
        // server-side placement needs the registered arrival-region exclusion.
        if(level instanceof net.minecraft.server.level.ServerLevel server
                && net.zerog.tweaks.travel.ArrivalProtection.intersects(server,centre.offset(-20,-18,-20),centre.offset(20,10,20))) return false;
        var used=new boolean[35][35];var housePositions=homes(layout);
        boolean hasShrine=PlanetEcologyProfile.theme(dimension).equals("mars");
        for(int x=-17;x<=17;x++)for(int z=-17;z<=17;z++)used[x+17][z+17]=usedColumn(x,z,housePositions,hasShrine);
        // Protect every actual write, without rejecting unrelated edge beehives.
        for(var pos:BlockPos.betweenClosed(centre.offset(-20,-MAX_GRADE,-20),centre.offset(20,11,20))) {
            int x=pos.getX()-centre.getX(),z=pos.getZ()-centre.getZ();
            if(Math.max(Math.abs(x),Math.abs(z))>17 || !used[x+17][z+17])continue;
            if(!level.hasChunkAt(pos) || level.getBlockEntity(pos)!=null)return false;
            if(level instanceof net.minecraft.server.level.WorldGenRegion
                    && level.getChunk(pos).getInhabitedTime()>0) return false;
            String block=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos).getBlock()).getPath();
            if(block.equals("landing_platform") || block.contains("gate_") || block.endsWith("_gate_frame")) return false;
        }
        // Check every graded column, not just nine survey samples: a ravine,
        // pond or narrow ridge inside the homes/farms must reject the whole
        // colony before any blocks are cleared or foundations are placed.
        int[][] heights=new int[35][35];
        for(int x=-17;x<=17;x++)for(int z=-17;z<=17;z++) {
            if(!used[x+17][z+17])continue;
            int y=groundY(level,centre.getX()+x,centre.getZ()+z);
            heights[x+17][z+17]=y;
            var ground=new BlockPos(centre.getX()+x,y,centre.getZ()+z);
            if(Math.abs(y-centre.getY())>MAX_GRADE || !level.getFluidState(ground).isEmpty()
                    || !level.getBlockState(ground).isSolidRender(level,ground))return false;
        }
        // Grading a continuous gentle slope is not permission to fill a ravine
        // or bulldoze a cliff. Check adjacent columns before any terrain writes.
        for(int x=0;x<35;x++)for(int z=0;z<35;z++) {
            if(!used[x][z])continue;
            if(x>0 && used[x-1][z] && Math.abs(heights[x][z]-heights[x-1][z])>4)return false;
            if(z>0 && used[x][z-1] && Math.abs(heights[x][z]-heights[x][z-1])>4)return false;
        }
        var hull=switch(PlanetEcologyProfile.theme(dimension)) {
            case "mars" -> BlockInit.MARTIAN_STONE_BRICKS.get();
            case "skarn" -> BlockInit.SKARN_ROCK_BRICKS.get();
            case "solvane" -> BlockInit.SOLAR_STONE_BRICKS.get();
            case "eidolon" -> BlockInit.FROSTROCK.get();
            case "moon" -> BlockInit.LUNAR_STONE_BRICKS.get();
            default -> BlockInit.CERULEAN_STONE_BRICKS.get();
        };
        var wood=switch(PlanetEcologyProfile.tree(dimension)) {
            case "charwood" -> BlockInit.CHARWOOD_PLANKS.get();
            case "hoarwood" -> BlockInit.HOARWOOD_PLANKS.get();
            case "gildwood" -> BlockInit.GILDWOOD_PLANKS.get();
            default -> BlockInit.SHARDWOOD_PLANKS.get();
        };
        var door=switch(PlanetEcologyProfile.tree(dimension)) {
            case "charwood" -> BlockInit.CHARWOOD_DOOR.get();
            case "hoarwood" -> BlockInit.HOARWOOD_DOOR.get();
            case "gildwood" -> BlockInit.GILDWOOD_DOOR.get();
            default -> BlockInit.SHARDWOOD_DOOR.get();
        };
        Block glass=random.nextBoolean()?Blocks.GLASS:switch(PlanetEcologyProfile.theme(dimension)) {
            case "mars" -> BlockInit.RUST_GLASS.get();
            case "eidolon", "moon" -> BlockInit.FROST_GLASS.get();
            case "skarn" -> BlockInit.SLAG_GLASS.get();
            case "solvane" -> BlockInit.SHIMMER_GLASS.get();
            default -> BlockInit.CRYSTAL_GLASS.get();
        };
        for(int x=-19;x<=19;x++) for(int z=-19;z<=19;z++) {
            // Leave the outer transition band untouched, rather than stamping
            // a sharp rectangular green/brown lawn onto unrelated terrain.
            if(Math.max(Math.abs(x),Math.abs(z))>17 || !used[x+17][z+17]) continue;
            var floor=centre.offset(x,0,z);
            int surfaceY=groundY(level,floor.getX(),floor.getZ());
            var nativeSurface=level.getBlockState(new BlockPos(floor.getX(),surfaceY,floor.getZ()));
            if(!nativeSurface.getFluidState().isEmpty() || !nativeSurface.isSolidRender(level,floor))
                nativeSurface=ZGDimensionTerrain.SOILS.get(dimension).get().defaultBlockState();
            for(int y=1;y<=11;y++) level.setBlock(floor.above(y),Blocks.AIR.defaultBlockState(),2);
            for(int y=0;y<=MAX_GRADE;y++) level.setBlock(floor.below(y),ZGDimensionTerrain.SOILS.get(dimension).get().defaultBlockState(),2);
            level.setBlock(floor,nativeSurface,2);
            if(Math.abs(x)<=1 || Math.abs(z)<=1) level.setBlock(floor,hull.defaultBlockState(),2);
        }
        // No raised sea platforms or long pylons: accepted terrain must already
        // be within six blocks with no sharp cliff/ravine steps.
        int index=0;
        for(var home:homes(layout)) {
            var at=centre.offset(home);
            for(int x=-4;x<=4;x++) for(int z=-4;z<=4;z++) for(int y=0;y<=6;y++) {
                var pos=at.offset(x,y,z);
                if(y==0 || y==1 && (Math.abs(x)==4 || Math.abs(z)==4)) level.setBlock(pos,wood.defaultBlockState(),2);
                else if(y>=2 && (Math.abs(x)==4 || Math.abs(z)==4 || y==6)) {
                    boolean rib=Math.abs(x)==4 && Math.abs(z)==4 || y==6 && (x%4==0 || z%4==0);
                    // Alternate roof heights create stepped dome/greenhouse ribs.
                    if((layout&1)==0 && y==6 && Math.abs(x)<=2 && Math.abs(z)<=2) {
                        level.setBlock(pos,Blocks.AIR.defaultBlockState(),2);
                        level.setBlock(pos.above(),glass.defaultBlockState(),2);
                    } else level.setBlock(pos,(rib?hull:glass).defaultBlockState(),2);
                }
            }
            for(int y=1;y<=2;y++) level.setBlock(at.offset(0,y,4),door.defaultBlockState()
                    .setValue(DoorBlock.FACING,Direction.SOUTH).setValue(DoorBlock.HALF,y==1?DoubleBlockHalf.LOWER:DoubleBlockHalf.UPPER),2);
            for(int x:new int[]{-2,2}) {
                level.setBlock(at.offset(x,1,-2),Blocks.WHITE_BED.defaultBlockState().setValue(BedBlock.FACING,Direction.NORTH).setValue(BedBlock.PART,BedPart.FOOT),2);
                level.setBlock(at.offset(x,1,-3),Blocks.WHITE_BED.defaultBlockState().setValue(BedBlock.FACING,Direction.NORTH).setValue(BedBlock.PART,BedPart.HEAD),2);
            }
            // Two additional beds for the specialists; every resident is planetary.
            if(index<2) {
                level.setBlock(at.offset(-2,1,1),Blocks.WHITE_BED.defaultBlockState().setValue(BedBlock.FACING,Direction.NORTH).setValue(BedBlock.PART,BedPart.FOOT),2);
                level.setBlock(at.offset(-2,1,0),Blocks.WHITE_BED.defaultBlockState().setValue(BedBlock.FACING,Direction.NORTH).setValue(BedBlock.PART,BedPart.HEAD),2);
            }
            level.setBlock(at.offset(3,1,0),switch(index++) {
                case 0 -> Blocks.COMPOSTER.defaultBlockState();
                case 1 -> Blocks.BLAST_FURNACE.defaultBlockState();
                default -> Blocks.LECTERN.defaultBlockState();
            },2);
            level.setBlock(at.offset(0,5,0),Blocks.SEA_LANTERN.defaultBlockState(),2);
            for(int x=Math.min(0,home.getX());x<=Math.max(0,home.getX());x++)
                level.setBlock(centre.offset(x,0,home.getZ()+5),hull.defaultBlockState(),2);
            for(int z=Math.min(0,home.getZ()+5);z<=Math.max(0,home.getZ()+5);z++)
                level.setBlock(centre.offset(0,0,z),hull.defaultBlockState(),2);
        }
        for(int side:new int[]{-1,1}) for(int x=-3;x<=3;x++) for(int z=-2;z<=2;z++) {
            var pos=centre.offset(side*12+x,0,12+z);
            if(x==0) level.setBlock(pos,Blocks.WATER.defaultBlockState(),2);
            else {
                level.setBlock(pos,ZGDimensionTerrain.FARMLANDS.get(dimension).get().defaultBlockState().setValue(FarmBlock.MOISTURE,7),2);
                var vegetables=net.zerog.tweaks.registry.ZGAlienAgriculture.vegetables(PlanetEcologyProfile.theme(dimension));
                var crop=vegetables.isEmpty()?ZGPlanetCrops.CROPS.get(ZGPlanetCrops.PLANET_CROPS.get(PlanetEcologyProfile.theme(dimension))).get():
                        net.zerog.tweaks.registry.ZGAlienAgriculture.CROPS.get(vegetables.get(Math.floorMod(x+z,vegetables.size()))).get();
                level.setBlock(pos.above(),crop.getStateForAge(crop.getMaxAge()),2);
            }
        }
        level.setBlock(centre,BlockInit.SETTLEMENT_ANCHOR.get().defaultBlockState(),2);
        if(level.getBlockEntity(centre) instanceof SettlementAnchorBlockEntity anchor) anchor.configure(layout);
        String theme=PlanetEcologyProfile.theme(dimension);
        // Every Rustborn layout keeps one hand-cut Aresite core, away from
        // homes, farms and the central resident anchor. No standalone shrine loot.
        if(theme.equals("mars")) {
            var shrine=centre.offset(5,0,3);
            for(int x=-1;x<=1;x++)for(int z=-1;z<=1;z++)
                level.setBlock(shrine.offset(x,0,z),BlockInit.MARTIAN_STONE_BRICKS.get().defaultBlockState(),2);
            level.setBlock(shrine.above(),BlockInit.MARTIAN_STONE_BRICKS.get().defaultBlockState(),2);
            level.setBlock(shrine.above(2),BlockInit.ARESITE_BLOCK.get().defaultBlockState(),2);
        }
        var garden=centre.offset(-16,1,5);
        var flower=ZGDimensionTerrain.FLORA.get(theme+"_glow_flower");
        if(flower!=null) for(int z=-2;z<=2;z++) level.setBlock(garden.offset(2,0,z),flower.get().defaultBlockState(),2);
        var variants=net.zerog.tweaks.registry.ZGGlowbugs.HOMES.entrySet().stream().filter(e -> e.getValue().equals(theme)).map(java.util.Map.Entry::getKey).toList();
        if(!variants.isEmpty()) {
            String variant=variants.get(random.nextInt(variants.size()));
            var hive=net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.get(variant).hive.get();
            level.setBlock(garden,hive.defaultBlockState(),2);
            if(level.getBlockEntity(garden) instanceof net.minecraft.world.level.block.entity.BeehiveBlockEntity storage) for(int n=0;n<2;n++) {
                var data=new net.minecraft.nbt.CompoundTag();
                data.putString("id",net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(net.zerog.tweaks.registry.ZGGlowbugs.TYPES.get(variant).get()).toString());
                storage.storeBee(new net.minecraft.world.level.block.entity.BeehiveBlockEntity.Occupant(net.minecraft.world.item.component.CustomData.of(data),0,600));
            }
        }
        return true;
    }
}
