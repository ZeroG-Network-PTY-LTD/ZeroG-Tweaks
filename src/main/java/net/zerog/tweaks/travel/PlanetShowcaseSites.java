package net.zerog.tweaks.travel;

import java.util.*;
import net.minecraft.core.*;
import net.minecraft.nbt.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.saveddata.SavedData;

/** Explicit operator-built inspection sites; never natural worldgen or a startup sweep. */
public final class PlanetShowcaseSites extends SavedData {
    public static int width(String name){return name.equals("ice_spire_outpost")?54:48;}
    public static int height(String name){return name.equals("ice_spire_outpost")?50:name.equals("hot_ring_monolith")?56:52;}
    public static int surface(String name){return name.equals("ice_spire_outpost")?14:name.equals("hot_ring_monolith")?20:16;}
    public static BlockPos entrance(String name){int c=width(name)/2,d=surface(name);return new BlockPos(c,d+1,c+d+1);}
    private final Map<String,BlockPos> sites=new HashMap<>();
    public static PlanetShowcaseSites get(ServerLevel level){return level.getDataStorage().computeIfAbsent(new SavedData.Factory<>(PlanetShowcaseSites::new,PlanetShowcaseSites::load),"zerog_showcase_sites");}
    private static PlanetShowcaseSites load(CompoundTag tag,HolderLookup.Provider lookup){var data=new PlanetShowcaseSites();for(String name:ZeroAdminCommands.SHOWCASES.keySet())if(tag.contains(name,Tag.TAG_LONG))data.sites.put(name,BlockPos.of(tag.getLong(name)));return data;}
    @Override public CompoundTag save(CompoundTag tag,HolderLookup.Provider lookup){sites.forEach((name,pos)->tag.putLong(name,pos.asLong()));return tag;}
    public BlockPos origin(String name){return sites.get(name);}
    public BlockPos arrival(ServerLevel level,String name){var origin=sites.get(name);if(origin==null)return null;
        var entry=entrance(name);
        for(int[] offset:new int[][]{{0,0},{-1,0},{1,0},{0,1},{0,-1}}){int x=origin.getX()+entry.getX()+offset[0],z=origin.getZ()+entry.getZ()+offset[1];level.getChunk(x>>4,z>>4);
            // Fixed local surface anchor, not tower-top heightmap arrival.
            for(int y=origin.getY()+entry.getY();y<=origin.getY()+entry.getY()+2;y++){var feet=new BlockPos(x,y,z);if(ZeroAdminCommands.safeFooting(level,feet))return feet;}}
        return null;
    }
    public String build(ServerLevel level,String name){
        if(!ZeroAdminCommands.SHOWCASES.containsKey(name)||!level.dimension().location().equals(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",ZeroAdminCommands.SHOWCASES.get(name))))return "Wrong showcase dimension.";
        if(sites.containsKey(name))return "Existing site preserved.";
        var template=level.getStructureManager().getOrCreate(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planetary_showcase/"+name));
        int width=width(name),height=height(name),surface=surface(name);
        if(!template.getSize().equals(new BlockPos(width,height,width)))return "Unexpected template size; no blocks changed.";
        var source=template.save(new CompoundTag());var blocks=source.getList("blocks",Tag.TAG_COMPOUND);var palette=source.getList("palette",Tag.TAG_COMPOUND);
        boolean waterSite=name.equals("water_bio_habitat");
        int foundationDepth=waterSite?32:16;
        var footprint=new HashSet<Integer>();
        for(var raw:blocks){var block=(CompoundTag)raw;var local=block.getList("pos",Tag.TAG_INT);if(!palette.getCompound(block.getInt("state")).getString("Name").equals("minecraft:air"))footprint.add(local.getInt(0)*width+local.getInt(2));}
        int noiseRejected=0,surfaceRejected=0,protectedRejected=0;
        for(int candidate=0;candidate<25;candidate++){
            int bx=4160+(candidate%5)*1024,bz=4160+(candidate/5)*1024;
            int min=Integer.MAX_VALUE,max=Integer.MIN_VALUE;boolean valid=true;
            // Noise-only gradient/waterline preflight avoids generating every rejected candidate.
            for(int dx:new int[]{12,24,36})for(int dz:new int[]{12,24,36}){int y=level.getChunkSource().getGenerator().getBaseHeight(bx+dx,bz+dz,Heightmap.Types.WORLD_SURFACE_WG,level,level.getChunkSource().randomState());min=Math.min(min,y);max=Math.max(max,y);}
            if(max-min>12){noiseRejected++;continue;}
            min=Integer.MAX_VALUE;max=Integer.MIN_VALUE;
            for(int x=0;x<width&&valid;x++)for(int z=0;z<width;z++){
                if(!footprint.contains(x*width+z))continue;
                var column=new BlockPos(bx+x,0,bz+z);if(!level.getWorldBorder().isWithinBounds(column)){valid=false;break;}
                level.getChunk((bx+x)>>4,(bz+z)>>4);int y=level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,bx+x,bz+z)-1;var floor=level.getBlockState(new BlockPos(bx+x,y,bz+z));
                if(waterSite&&!floor.getFluidState().isEmpty()){y=level.getHeight(Heightmap.Types.OCEAN_FLOOR,bx+x,bz+z)-1;floor=level.getBlockState(new BlockPos(bx+x,y,bz+z));}
                for(int tree=0;tree<32&&(floor.is(BlockTags.LOGS)||floor.is(BlockTags.LEAVES));tree++){y--;floor=level.getBlockState(new BlockPos(bx+x,y,bz+z));}
                if(!floor.getFluidState().isEmpty()||floor.is(BlockTags.LOGS)||floor.is(BlockTags.LEAVES)||!floor.isFaceSturdy(level,new BlockPos(bx+x,y,bz+z),Direction.UP)){valid=false;break;}
                min=Math.min(min,y);max=Math.max(max,y);
            }
            if(!valid||max-min>12){surfaceRejected++;continue;}
            var origin=new BlockPos(bx,(waterSite?Math.max(max,level.getSeaLevel()):max)-surface,bz);if(origin.getY()<level.getMinBuildHeight()+32||origin.getY()+height>=level.getMaxBuildHeight())continue;
            // Protect actual authored writes, including carved air. Unused bounding-box
            // corners/ponds are neither cleared nor grounds for a false rejection.
            for(var raw:blocks){var block=(CompoundTag)raw;var local=block.getList("pos",Tag.TAG_INT);var p=origin.offset(local.getInt(0),local.getInt(1),local.getInt(2));var state=level.getBlockState(p);if(state.hasBlockEntity()||state.is(Blocks.BEDROCK)||!state.getFluidState().isEmpty()&&(!waterSite||!state.is(Blocks.WATER))){valid=false;break;}}
            if(!valid){protectedRejected++;continue;}
            var foundations=new ArrayList<BlockPos>();var bottoms=new HashMap<Integer,Integer>();var authored=new HashSet<BlockPos>();
            for(var raw:blocks){var block=(CompoundTag)raw;var local=block.getList("pos",Tag.TAG_INT);int y=local.getInt(1);String id=palette.getCompound(block.getInt("state")).getString("Name");
                authored.add(origin.offset(local.getInt(0),y,local.getInt(2)));
                if(y>surface||id.equals("minecraft:air"))continue;
                bottoms.merge(local.getInt(0)*width+local.getInt(2),y,Math::min);
            }
            for(var bottom:bottoms.entrySet()){
                var floor=origin.offset(bottom.getKey()/width,bottom.getValue(),bottom.getKey()%width);
                boolean supported=false;
                for(int depth=1;depth<=foundationDepth;depth++){var below=floor.below(depth);if(authored.contains(below))continue;var state=level.getBlockState(below);if(state.hasBlockEntity()||state.is(Blocks.BEDROCK)){valid=false;break;}if(!state.getFluidState().isEmpty()&&(!waterSite||!state.is(Blocks.WATER))){valid=false;break;}if(!state.isAir()&&(!waterSite||!state.is(Blocks.WATER))){supported=true;break;}foundations.add(below);}
                if(!valid||!supported){valid=false;break;}
            }
            if(!valid){protectedRejected++;continue;}
            if(!template.placeInWorld(level,origin,origin,new StructurePlaceSettings(),net.minecraft.util.RandomSource.create(0),2))return "Template placement failed.";
            var soil=net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",ZeroAdminCommands.SHOWCASES.get(name)+"_soil")).defaultBlockState();
            for(var p:foundations)if(level.getBlockState(p).isAir()||waterSite&&level.getBlockState(p).is(Blocks.WATER))level.setBlock(p,soil,2);
            sites.put(name,origin);setDirty();return "Built grounded site.";
        }
        return "No dry gentle protected site among25 bounded candidates; no blocks placed (noise="+noiseRejected+", surface="+surfaceRejected+", protected="+protectedRejected+").";
    }
}
