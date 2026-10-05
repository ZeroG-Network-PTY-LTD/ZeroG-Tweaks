package net.zerog.tweaks.worldgen;

import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.WorldGenRegion;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.BlockInit;

/** Small biome-specific geological silhouettes, entirely inside their owning chunk. */
public final class SolBiomeSignatureFeature extends Feature<NoneFeatureConfiguration> {
    public enum Signature { CRATER_ICE, MARE_RUBBLE, HIGHLAND_ROCK, POLAR_SPIRE, OXIDE_BOULDER, RUST_RUBBLE }
    private static final Set<String> NATURAL=Set.of("regolith","lunar_stone","mare_basalt","frozen_regolith","crater_dust","martian_stone","rustsand","oxide_crust","permafrost","polar_frost");
    public SolBiomeSignatureFeature(){super(NoneFeatureConfiguration.CODEC);}
    public static Signature signature(String biome){return switch(biome){case "shadowed_craters"->Signature.CRATER_ICE;case "lunar_mare"->Signature.MARE_RUBBLE;case "lunar_highlands"->Signature.HIGHLAND_ROCK;case "polar_caps"->Signature.POLAR_SPIRE;case "oxide_badlands"->Signature.OXIDE_BOULDER;case "rust_plains"->Signature.RUST_RUBBLE;default->null;};}
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context){
        var key=context.level().getBiome(context.origin()).unwrapKey();
        if(key.isEmpty()||!key.get().location().getNamespace().equals("zerog_tweaks"))return false;
        var signature=signature(key.get().location().getPath());return signature!=null&&placeSignature(context,signature);
    }
    public boolean placeSignature(FeaturePlaceContext<NoneFeatureConfiguration> context,Signature signature){
        var level=context.level();var random=context.random();boolean changed=false;
        int chunkX=context.origin().getX()&~15,chunkZ=context.origin().getZ()&~15;
        for(int attempt=0;attempt<2;attempt++){
            int x=chunkX+3+random.nextInt(10),z=chunkZ+3+random.nextInt(10);
            BlockPos base=new BlockPos(x,level.getHeight(Heightmap.Types.WORLD_SURFACE_WG,x,z)-1,z);
            var manager=level.getLevel().structureManager();if(level instanceof WorldGenRegion region)manager=manager.forWorldGenRegion(region);
            // Any structure reference rejects the whole candidate, not just its visible blocks.
            if(manager.hasAnyStructureAt(base)||!natural(level,base)||!level.isEmptyBlock(base.above()))continue;
            int radius=1+random.nextInt(2),height=signature==Signature.POLAR_SPIRE?2+random.nextInt(4):1+random.nextInt(2);
            Block material=switch(signature){case CRATER_ICE->BlockInit.CRATER_ICE.get();case MARE_RUBBLE->BlockInit.MARE_BASALT.get();case HIGHLAND_ROCK->BlockInit.FROZEN_REGOLITH.get();case POLAR_SPIRE->BlockInit.POLAR_FROST.get();case OXIDE_BOULDER,RUST_RUBBLE->BlockInit.OXIDE_CRUST.get();};
            for(int dx=-radius;dx<=radius;dx++)for(int dz=-radius;dz<=radius;dz++){
                if(dx*dx+dz*dz>radius*radius)continue;
                if(signature==Signature.CRATER_ICE){
                    for(int depth=0;depth<2;depth++){var at=base.offset(dx,-depth,dz);if(natural(level,at)){level.setBlock(at,material.defaultBlockState(),2);changed=true;}}
                }else{
                    var column=base.offset(dx,0,dz);if(!natural(level,column))continue;
                    int columnHeight=signature==Signature.POLAR_SPIRE?Math.max(1,height-Math.abs(dx)-Math.abs(dz)):Math.max(1,height-(Math.abs(dx)+Math.abs(dz))/2);
                    for(int y=1;y<=columnHeight;y++){var at=column.above(y);if(at.getY()>=level.getMaxBuildHeight()||!level.isEmptyBlock(at)||level.getBlockEntity(at)!=null)break;level.setBlock(at,material.defaultBlockState(),2);changed=true;}
                }
            }
        }return changed;
    }
    private static boolean natural(WorldGenLevel level,BlockPos pos){
        if(pos.getY()<=level.getMinBuildHeight()||level.getBlockEntity(pos)!=null)return false;
        var state=level.getBlockState(pos);var id=BuiltInRegistries.BLOCK.getKey(state.getBlock());
        return state.getFluidState().isEmpty()&&id.getNamespace().equals("zerog_tweaks")&&NATURAL.contains(id.getPath());
    }
}
