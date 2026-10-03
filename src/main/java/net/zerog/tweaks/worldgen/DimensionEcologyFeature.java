package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Small fertile patches, not replacement of the planetary terrain/ore/cave system. */
public final class DimensionEcologyFeature extends Feature<NoneFeatureConfiguration> {
    public DimensionEcologyFeature() { super(NoneFeatureConfiguration.CODEC); }
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        var level=context.level(); var random=context.random(); var dim=level.getLevel().dimension().location().getPath();
        if (!ZGDimensionTerrain.SOILS.containsKey(dim)) return false;
        var theme=PlanetEcologyProfile.theme(dim);
        var origin=context.origin(); var soil=ZGDimensionTerrain.SOILS.get(dim).get(); var grass=ZGDimensionTerrain.GRASS.get(dim).get();
        int radius=3+random.nextInt(3); boolean changed=false;
        for (int x=-radius;x<=radius;x++) for (int z=-radius;z<=radius;z++) {
            if (x*x+z*z>radius*radius) continue;
            int y=level.getHeight(Heightmap.Types.WORLD_SURFACE_WG,origin.getX()+x,origin.getZ()+z)-1;
            var pos=new BlockPos(origin.getX()+x,y,origin.getZ()+z); var previous=level.getBlockState(pos);
            if (!previous.getFluidState().isEmpty() || !previous.isSolidRender(level,pos) || !level.isEmptyBlock(pos.above())) continue;
            var key=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(previous.getBlock());
            // Only naturally themed surface materials, not ores, machines, structures or player blocks.
            if (!key.getNamespace().equals("zerog_tweaks") || !isSurface(key.getPath())) continue;
            level.setBlock(pos,grass.defaultBlockState(),2);
            if (level.getBlockState(pos.below()).is(previous.getBlock())) level.setBlock(pos.below(),soil.defaultBlockState(),2);
            changed=true;
            if (random.nextInt(5)==0) {
                var plant=ZGDimensionTerrain.SHORT_GRASS.get(dim).get().defaultBlockState();
                if (plant.canSurvive(level,pos.above())) level.setBlock(pos.above(),plant,2);
            }
            if (random.nextInt(18)==0 && level.isEmptyBlock(pos.above()) && level.isEmptyBlock(pos.above(2))) {
                var plant=ZGDimensionTerrain.TALL_GRASS.get(dim).get().defaultBlockState();
                if(plant.canSurvive(level,pos.above())) net.minecraft.world.level.block.DoublePlantBlock.placeAt(level,plant,pos.above(),2);
            }
            if (random.nextInt(80)==0 && ZGDimensionTerrain.FLORA.containsKey(theme+"_tall_blossom")
                    && level.isEmptyBlock(pos.above()) && level.isEmptyBlock(pos.above(2))) {
                var plant=ZGDimensionTerrain.FLORA.get(theme+"_tall_blossom").get().defaultBlockState();
                if(plant.canSurvive(level,pos.above())) net.minecraft.world.level.block.DoublePlantBlock.placeAt(level,plant,pos.above(),2);
            }
            if (random.nextInt(40)==0 && level.isEmptyBlock(pos.above()) && ZGDimensionTerrain.FLORA.containsKey(theme+"_glow_flower")) {
                var plant=ZGDimensionTerrain.FLORA.get(theme+"_glow_flower").get().defaultBlockState();
                if (plant.canSurvive(level,pos.above())) level.setBlock(pos.above(),plant,2);
            }
        }
        if (changed && random.nextInt(3)==0) {
            String tree=PlanetEcologyProfile.tree(dim);
            var key=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",tree+"_tree");
            var configured=level.registryAccess().registryOrThrow(Registries.CONFIGURED_FEATURE).get(key);
            if(configured!=null) {
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,origin);
                if(level.getBlockState(pos.below()).is(grass) && configured.place(level,context.chunkGenerator(),random,pos))
                    PlanetCaveEcologyFeature.decorateCanopy(level,random,pos,theme);
            }
        }
        if(changed && random.nextInt(12)==0 && net.zerog.tweaks.registry.ZGGasVents.VENTS.containsKey(dim)) {
            var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,origin).below();
            if(level.getBlockState(pos).is(grass)) level.setBlock(pos,net.zerog.tweaks.registry.ZGGasVents.VENTS.get(dim).get().defaultBlockState(),2);
        }
        if(changed && random.nextInt(8)==0) {
            var variants=net.zerog.tweaks.registry.ZGGlowbugs.HOMES.entrySet().stream().filter(e->e.getValue().equals(theme)).map(java.util.Map.Entry::getKey).toList();
            if(!variants.isEmpty()) {
                String variant=variants.get(random.nextInt(variants.size()));
                var pos=level.getHeightmapPos(Heightmap.Types.WORLD_SURFACE_WG,origin);
                if(level.isEmptyBlock(pos)&&level.getBlockState(pos.below()).is(grass)) {
                    var hive=net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.get(variant).hive.get();
                    level.setBlock(pos,hive.defaultBlockState(),2);
                    if(level.getBlockEntity(pos) instanceof net.minecraft.world.level.block.entity.BeehiveBlockEntity storage) {
                        for(int n=0;n<2;n++) {
                            // Like vanilla BeehiveDecorator, store data only on the
                            // worldgen worker. Bee construction initializes goals using
                            // ServerLevel.random and must wait for server-thread release.
                            var data=new net.minecraft.nbt.CompoundTag();
                            var type=net.zerog.tweaks.registry.ZGGlowbugs.TYPES.get(variant).get();
                            data.putString("id",net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(type).toString());
                            storage.storeBee(new net.minecraft.world.level.block.entity.BeehiveBlockEntity.Occupant(
                                    net.minecraft.world.item.component.CustomData.of(data),0,600));
                        }
                    }
                }
            }
        }
        return changed;
    }
    private boolean isSurface(String name) {
        return name.endsWith("_soil") || name.endsWith("_grass_block") || java.util.Set.of("regolith","rustsand","crystal_sand","azure_moss","cerulean_soil",
                "slag","oxide_crust","permafrost","polar_frost","shimmer_sand","dunesand","toxic_mud","blightmoss","tidesand","sludgestone","prismstone",
                "frostrock","sunspot_rock","lunar_stone","martian_stone","skarn_rock","solar_stone","cerulean_stone",
                "frozen_regolith","crater_dust","mare_basalt","ember_crust","corona_crust","craterstone","snowpack",
                "vent_rock","scoria","scorched_marble","sunbaked_stone","salt_crust","glacial_ice","crater_ice","phantom_ice").contains(name);
    }
}
