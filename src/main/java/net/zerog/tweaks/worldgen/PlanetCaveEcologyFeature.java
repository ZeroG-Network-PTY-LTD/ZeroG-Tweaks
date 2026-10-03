package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CaveVines;
import net.minecraft.world.level.block.MultifaceBlock;
import net.minecraft.world.level.block.PointedDripstoneBlock;
import net.minecraft.world.level.block.VineBlock;
import net.minecraft.world.level.block.state.properties.DripstoneThickness;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Worldgen uses only its context random: no entities, server random or forced chunks. */
public final class PlanetCaveEcologyFeature extends Feature<NoneFeatureConfiguration> {
    public PlanetCaveEcologyFeature() { super(NoneFeatureConfiguration.CODEC); }
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        var level=context.level();
        String dim=level.getLevel().dimension().location().getPath();
        if(!ZGDimensionTerrain.SOILS.containsKey(dim)) return false;
        var random=context.random(); String theme=PlanetEcologyProfile.theme(dim);
        int chunkX=context.origin().getX()&~15,chunkZ=context.origin().getZ()&~15;
        boolean changed=false;
        for(int column=0;column<32;column++) {
            int x=chunkX+1+random.nextInt(14),z=chunkZ+1+random.nextInt(14);
            int surface=level.getHeight(Heightmap.Types.WORLD_SURFACE_WG,x,z);
            for(int y=level.getMinBuildHeight()+8;y<Math.min(surface-8,level.getMaxBuildHeight()-8);y++) {
                var pos=new BlockPos(x,y,z);
                if(level.isEmptyBlock(pos)) {
                    if(natural(level,pos.above()) && random.nextInt(14)==0) {
                        if(random.nextBoolean()) changed|=hang(level,random,pos,theme,2+random.nextInt(5));
                        else changed|=spike(level,pos,Direction.DOWN,1+random.nextInt(3));
                    }
                    if(natural(level,pos.below()) && random.nextInt(12)==0) {
                        if(random.nextBoolean()) changed|=spike(level,pos,Direction.UP,1+random.nextInt(3));
                        else {
                            // A small fertile pocket supports the existing glowing alien mushroom.
                            level.setBlock(pos.below(),ZGDimensionTerrain.SOILS.get(dim).get().defaultBlockState(),2);
                            var mushroom=ZGDimensionTerrain.FLORA.get(theme+"_glow_mushroom").get().defaultBlockState();
                            if(mushroom.canSurvive(level,pos)) { level.setBlock(pos,mushroom,2);changed=true; }
                        }
                    }
                    if(random.nextInt(24)==0) for(var face:Direction.Plane.HORIZONTAL) {
                        if(!natural(level,pos.relative(face))) continue;
                        var lichen=(theme.equals("mars")?BlockInit.RUST_LICHEN.get():BlockInit.LUNAR_LICHEN.get())
                                .defaultBlockState().setValue(MultifaceBlock.getFaceProperty(face),true);
                        if(lichen.canSurvive(level,pos)) {level.setBlock(pos,lichen,2);changed=true;}
                        break;
                    }
                } else if(level.getFluidState(pos).is(FluidTags.WATER) && natural(level,pos.below()) && random.nextInt(10)==0) {
                    var kelp=BlockInit.GLOWKELP.get().defaultBlockState();
                    if(kelp.canSurvive(level,pos)) {
                        int height=1+random.nextInt(4);
                        for(int n=0;n<height;n++) {
                            var p=pos.above(n);
                            if(!level.getBlockState(p).is(Blocks.WATER)) break;
                            var next=n+1<height&&level.getBlockState(p.above()).is(Blocks.WATER)?
                                    BlockInit.GLOWKELP_PLANT.get().defaultBlockState():kelp;
                            level.setBlock(p,next,2);changed=true;
                        }
                    }
                }
            }
        }
        return changed;
    }
    public static void decorateCanopy(WorldGenLevel level,RandomSource random,BlockPos trunk,String theme) {
        for(int x=-3;x<=3;x++) for(int z=-3;z<=3;z++) for(int y=3;y<=9;y++) {
            var leaf=trunk.offset(x,y,z);
            if(!level.getBlockState(leaf).is(BlockTags.LEAVES)) continue;
            if(level.isEmptyBlock(leaf.below()) && random.nextInt(10)==0)
                hang(level,random,leaf.below(),theme,2+random.nextInt(4));
            for(var face:Direction.Plane.HORIZONTAL) {
                var pos=leaf.relative(face);
                if(!level.isEmptyBlock(pos)||random.nextInt(20)!=0) continue;
                var vine=Blocks.VINE.defaultBlockState().setValue(VineBlock.getPropertyForFace(face.getOpposite()),true);
                if(vine.canSurvive(level,pos)) level.setBlock(pos,vine,2);
            }
        }
    }
    public static boolean hang(WorldGenLevel level,RandomSource random,BlockPos start,String theme,int maximum) {
        boolean hot=theme.equals("skarn")||theme.equals("solvane")||theme.equals("mars");
        int length=0;
        while(length<maximum && level.isEmptyBlock(start.below(length))) length++;
        if(length==0) return false;
        var plant=hot?BlockInit.PYREVINE_PLANT.get():Blocks.CAVE_VINES_PLANT;
        var head=hot?BlockInit.PYREVINE.get():Blocks.CAVE_VINES;
        for(int n=0;n<length;n++) {
            var state=(n==length-1?head:plant).defaultBlockState().setValue(CaveVines.BERRIES,random.nextInt(4)==0);
            var pos=start.below(n);
            if(!state.canSurvive(level,pos)) return n>0;
            level.setBlock(pos,state,2);
        }
        return true;
    }
    public static boolean spike(WorldGenLevel level,BlockPos start,Direction direction,int maximum) {
        int length=0;
        while(length<maximum&&level.isEmptyBlock(start.relative(direction,length))) length++;
        for(int n=0;n<length;n++) {
            var thickness=n==length-1?DripstoneThickness.TIP:n==length-2?DripstoneThickness.FRUSTUM:n==0?DripstoneThickness.BASE:DripstoneThickness.MIDDLE;
            var state=Blocks.POINTED_DRIPSTONE.defaultBlockState()
                    .setValue(PointedDripstoneBlock.TIP_DIRECTION,direction).setValue(PointedDripstoneBlock.THICKNESS,thickness);
            var pos=start.relative(direction,n);
            if(!state.canSurvive(level,pos)) return n>0;
            level.setBlock(pos,state,2);
        }
        return length>0;
    }
    private static boolean natural(WorldGenLevel level,BlockPos pos) {
        var state=level.getBlockState(pos);
        if(!state.getFluidState().isEmpty()||state.hasBlockEntity()) return false;
        var id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(state.getBlock());
        return state.is(BlockTags.BASE_STONE_OVERWORLD)||state.is(BlockTags.DIRT)
                ||(id.getNamespace().equals("zerog_tweaks")&&java.util.Set.of("lunar_stone","martian_stone","cerulean_stone",
                "skarn_rock","solar_stone","permafrost","frostrock","sludgestone","prismstone","ruinstone").contains(id.getPath()));
    }
}
