package net.zerog.tweaks.worldgen;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.RailBlock;
import net.minecraft.world.level.block.state.properties.RailShape;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Original bounded corridors inspired by vanilla's five-block support sections. */
public final class PlanetMineshaftFeature extends Feature<NoneFeatureConfiguration> {
    public PlanetMineshaftFeature() { super(NoneFeatureConfiguration.CODEC); }
    public record Corridor(BlockPos start, Direction direction, int length, boolean rails) {}

    /** Seed-local plan: one spine and two to four staggered branches, no unbounded recursion. */
    public static List<Corridor> plan(RandomSource random) {
        Direction forward=random.nextBoolean()?Direction.NORTH:Direction.EAST;
        List<Corridor> result=new ArrayList<>();
        result.add(new Corridor(BlockPos.ZERO.relative(forward,-15),forward,30,random.nextInt(3)==0));
        int branches=2+random.nextInt(3);
        for(int n=0;n<branches;n++) {
            Direction side=(n%2==0)?forward.getClockWise():forward.getCounterClockWise();
            int section=-10+n*5+random.nextInt(3);
            result.add(new Corridor(BlockPos.ZERO.relative(forward,section),side,5*(2+random.nextInt(2)),random.nextInt(3)==0));
        }
        return List.copyOf(result);
    }
    @Override public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        var level=context.level();var at=context.origin().offset(8,0,8);
        if(!ZGDimensionTerrain.SOILS.containsKey(level.getLevel().dimension().location().getPath())) return false;
        int y=level.getHeight(Heightmap.Types.OCEAN_FLOOR_WG,at.getX(),at.getZ())-22-context.random().nextInt(28);
        return build(level,new BlockPos(at.getX(),y,at.getZ()),context.random());
    }
    public static boolean build(WorldGenLevel level,BlockPos centre,RandomSource random) {
        if(centre.getY()<level.getMinBuildHeight()+12 || centre.getY()>level.getMaxBuildHeight()-8) return false;
        String dimension=level.getLevel().dimension().location().getPath();
        if(!ZGDimensionTerrain.SOILS.containsKey(dimension)) return false;
        var corridors=plan(random);
        var cells=new LinkedHashSet<BlockPos>();
        for(var corridor:corridors) for(int t=0;t<=corridor.length();t++) for(int w=-1;w<=1;w++)
            cells.add(centre.offset(corridor.start()).relative(corridor.direction(),t).relative(corridor.direction().getClockWise(),w));
        if(level instanceof net.minecraft.server.level.ServerLevel server
                && net.zerog.tweaks.travel.ArrivalProtection.intersects(server,centre.offset(-17,-1,-17),centre.offset(17,4,17))) return false;
        int grounded=0,covered=0;
        for(var base:cells) {
            if(!level.hasChunkAt(base.below()) || !level.hasChunkAt(base.above(4))) return false;
            if(level.getBlockState(base.below()).isSolidRender(level,base.below())) grounded++;
            if(level.getBlockState(base.above(4)).isSolidRender(level,base.above(4))) covered++;
        }
        // Allow occasional cave windows, not a freestanding sky bridge or a
        // mine laid across a cavern with no natural floor/roof.
        if(grounded*4<cells.size()*3 || covered*2<cells.size()) return false;
        // Validate the entire footprint before writes: no fluids, inhabited chunks,
        // existing containers/machines or gate parts. Worldgen never touches SavedData.
        for(var base:cells) for(int y=-1;y<=3;y++) {
            var pos=base.above(y);
            if(!level.hasChunkAt(pos) || level.getBlockEntity(pos)!=null || !level.getFluidState(pos).isEmpty()) return false;
            if(level instanceof net.minecraft.server.level.WorldGenRegion && level.getChunk(pos).getInhabitedTime()>0) return false;
            var id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos).getBlock());
            if(id.getNamespace().equals("zerog_tweaks") && (id.getPath().contains("gate_") || id.getPath().equals("landing_platform"))) return false;
            if(level instanceof net.minecraft.server.level.ServerLevel) {
                var state=level.getBlockState(pos);String path=id.getPath();
                if(state.is(net.minecraft.tags.BlockTags.PLANKS) || state.is(net.minecraft.tags.BlockTags.FENCES)
                        || state.is(net.minecraft.tags.BlockTags.RAILS) || path.contains("glass") || path.contains("plating")
                        || path.contains("hull") || path.endsWith("_bricks") || path.endsWith("_planks")) return false;
            }
        }
        Block planks, fence;
        switch(PlanetEcologyProfile.tree(dimension)) {
            case "charwood" -> {planks=BlockInit.CHARWOOD_PLANKS.get();fence=BlockInit.CHARWOOD_FENCE.get();}
            case "hoarwood" -> {planks=BlockInit.HOARWOOD_PLANKS.get();fence=BlockInit.HOARWOOD_FENCE.get();}
            case "gildwood" -> {planks=BlockInit.GILDWOOD_PLANKS.get();fence=BlockInit.GILDWOOD_FENCE.get();}
            default -> {planks=BlockInit.SHARDWOOD_PLANKS.get();fence=BlockInit.SHARDWOOD_FENCE.get();}
        }
        // Retain surrounding natural ores. Only the actual three-wide tunnel is cut.
        for(var base:cells) {
            level.setBlock(base.below(),planks.defaultBlockState(),2);
            for(int y=0;y<=3;y++) level.setBlock(base.above(y),Blocks.AIR.defaultBlockState(),2);
        }
        for(var corridor:corridors) for(int t=3;t<corridor.length();t+=5) {
            var base=centre.offset(corridor.start()).relative(corridor.direction(),t);
            for(int w:new int[]{-1,1}) for(int y=0;y<3;y++)
                level.setBlock(base.relative(corridor.direction().getClockWise(),w).above(y),fence.defaultBlockState(),2);
            for(int w=-1;w<=1;w++) level.setBlock(base.relative(corridor.direction().getClockWise(),w).above(3),planks.defaultBlockState(),2);
            if(t==3) level.setBlock(base.above(3),Blocks.SEA_LANTERN.defaultBlockState(),2);
        }
        for(var corridor:corridors) if(corridor.rails()) for(int t=0;t<=corridor.length();t++) {
            var base=centre.offset(corridor.start()).relative(corridor.direction(),t);
            level.setBlock(base,Blocks.RAIL.defaultBlockState().setValue(RailBlock.SHAPE,
                    corridor.direction().getAxis()==Direction.Axis.X?RailShape.EAST_WEST:RailShape.NORTH_SOUTH),2);
        }
        var last=corridors.get(corridors.size()-1);
        var chest=centre.offset(last.start()).relative(last.direction(),last.length()-1);
        level.setBlock(chest,Blocks.CHEST.defaultBlockState(),2);
        if(level.getBlockEntity(chest) instanceof RandomizableContainerBlockEntity container)
            container.setLootTable(ResourceKey.create(Registries.LOOT_TABLE,
                    ResourceLocation.fromNamespaceAndPath("zerog_tweaks","chests/buried_observatory")),random.nextLong());
        return true;
    }
}
