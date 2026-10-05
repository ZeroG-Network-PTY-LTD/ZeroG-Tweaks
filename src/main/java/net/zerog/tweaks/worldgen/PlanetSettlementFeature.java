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
    public PlanetSettlementFeature() {super(NoneFeatureConfiguration.CODEC);}
    public static List<BlockPos> homes(int layout) {
        return switch(Math.floorMod(layout,4)) {
            case 1 -> List.of(new BlockPos(-11,0,-10),new BlockPos(11,0,-10),new BlockPos(0,0,12));
            case 2 -> List.of(new BlockPos(-12,0,0),new BlockPos(12,0,0),new BlockPos(0,0,-12));
            case 3 -> List.of(new BlockPos(-10,0,-11),new BlockPos(0,0,12),new BlockPos(10,0,-11));
            default -> List.of(new BlockPos(-10,0,-10),new BlockPos(10,0,-10),new BlockPos(0,0,11));
        };
    }
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        String dimension=context.level().getLevel().dimension().location().getPath();
        if(!ZGDimensionTerrain.SOILS.containsKey(dimension)) return false;
        // One seed-selected candidate per 50x50 chunk region. Candidate offsets
        // 16..33 guarantee at least 33 chunks between neighbouring region sites.
        int cx=context.origin().getX()>>4,cz=context.origin().getZ()>>4;
        int rx=Math.floorDiv(cx,50),rz=Math.floorDiv(cz,50);
        var site=net.minecraft.util.RandomSource.create(context.level().getSeed() ^ ((long)rx*341873128712L)
                ^ ((long)rz*132897987541L) ^ dimension.hashCode());
        if(cx!=rx*50+16+site.nextInt(18) || cz!=rz*50+16+site.nextInt(18)) return false;
        var origin=context.origin().offset(8,0,8);
        int y=context.level().getHeight(Heightmap.Types.WORLD_SURFACE_WG,origin.getX(),origin.getZ())-1;
        // Land only. A sea-surface height is not the solid grass/soil surface.
        for(int x:new int[]{-18,0,18}) for(int z:new int[]{-18,0,18}) {
            int h=context.level().getHeight(Heightmap.Types.WORLD_SURFACE_WG,origin.getX()+x,origin.getZ()+z)-1;
            var ground=new BlockPos(origin.getX()+x,h,origin.getZ()+z);
            if(Math.abs(h-y)>4 || !context.level().getFluidState(ground).isEmpty()
                    || !context.level().getBlockState(ground).isSolidRender(context.level(),ground)) return false;
        }
        return build(context.level(),new BlockPos(origin.getX(),y,origin.getZ()),dimension,context.random().nextInt(4),context.random());
    }
    public static boolean build(WorldGenLevel level,BlockPos centre,String dimension,int layout,RandomSource random) {
        if(!ZGDimensionTerrain.SOILS.containsKey(dimension) || centre.getY()<level.getMinBuildHeight()+20 || centre.getY()>level.getMaxBuildHeight()-12) return false;
        // Never consult server SavedData from a worldgen worker. Only explicit
        // server-side placement needs the registered arrival-region exclusion.
        if(level instanceof net.minecraft.server.level.ServerLevel server
                && net.zerog.tweaks.travel.ArrivalProtection.intersects(server,centre.offset(-20,-18,-20),centre.offset(20,10,20))) return false;
        // Generated footprints may excavate terrain, but never overwrite existing
        // block entities (including neighbouring outposts and player machines).
        for(var pos:BlockPos.betweenClosed(centre.offset(-20,-1,-20),centre.offset(20,9,20))) {
            if(!level.hasChunkAt(pos) || level.getBlockEntity(pos)!=null) return false;
            if(level instanceof net.minecraft.server.level.WorldGenRegion
                    && level.getChunk(pos).getInhabitedTime()>0) return false;
            String block=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos).getBlock()).getPath();
            if(block.equals("landing_platform") || block.contains("gate_") || block.endsWith("_gate_frame")) return false;
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
            if(Math.max(Math.abs(x),Math.abs(z))>17) continue;
            var floor=centre.offset(x,0,z);
            var surfaceMap=level instanceof net.minecraft.server.level.ServerLevel?Heightmap.Types.MOTION_BLOCKING_NO_LEAVES:Heightmap.Types.WORLD_SURFACE_WG;
            int surfaceY=level.getHeight(surfaceMap,floor.getX(),floor.getZ())-1;
            var nativeSurface=level.getBlockState(new BlockPos(floor.getX(),surfaceY,floor.getZ()));
            if(!nativeSurface.getFluidState().isEmpty() || !nativeSurface.isSolidRender(level,floor))
                nativeSurface=ZGDimensionTerrain.SOILS.get(dimension).get().defaultBlockState();
            for(int y=1;y<=9;y++) level.setBlock(floor.above(y),Blocks.AIR.defaultBlockState(),2);
            for(int y=0;y<5;y++) level.setBlock(floor.below(y),ZGDimensionTerrain.SOILS.get(dimension).get().defaultBlockState(),2);
            level.setBlock(floor,nativeSurface,2);
            if(Math.abs(x)<=1 || Math.abs(z)<=1) level.setBlock(floor,hull.defaultBlockState(),2);
        }
        // No raised sea platforms or long pylons: accepted terrain must already
        // be within four blocks of this ground-level footprint.
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
            for(int y=1;y<=2;y++) level.setBlock(at.offset(0,y,4),Blocks.OAK_DOOR.defaultBlockState()
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
