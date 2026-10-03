package net.zerog.tweaks.event;

import java.util.HashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.saveddata.SavedData;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGEcologyConfig;

/** One persisted impact per active dimension/day; unloaded dimensions are not force-loaded. */
public final class DailyPlanetImpacts {
    public static final class Ledger extends SavedData {
        public final Map<String,Long> days=new HashMap<>();
        public static Ledger load(CompoundTag tag,HolderLookup.Provider registries){
            var ledger=new Ledger(); for(String key:tag.getAllKeys()) ledger.days.put(key,tag.getLong(key)); return ledger;
        }
        @Override public CompoundTag save(CompoundTag tag,HolderLookup.Provider registries){ days.forEach(tag::putLong);return tag; }
    }
    public static void tick(ServerTickEvent.Post event) {
        if(!ZGEcologyConfig.IMPACTS.get()||event.getServer().getTickCount()%200!=0) return;
        var ledger=event.getServer().overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(Ledger::new,Ledger::load),"zerog_daily_impacts");
        for(var level:event.getServer().getAllLevels()) {
            String dim=level.dimension().location().getPath();
            if(!level.dimension().location().getNamespace().equals("zerog_tweaks")||!ZGDimensionTerrain.SOILS.containsKey(dim)||level.players().isEmpty()) continue;
            long day=Math.floorDiv(level.getDayTime(),24000L);
            if(Math.floorMod(level.getDayTime(),24000L)<18000 || ledger.days.getOrDefault(dim,-1L)>=day) continue;
            var player=level.players().get(level.random.nextInt(level.players().size()));
            for(int attempt=0;attempt<6;attempt++) {
                double angle=level.random.nextDouble()*Math.PI*2;int distance=80+level.random.nextInt(65);
                int x=player.blockPosition().getX()+(int)(Math.cos(angle)*distance),z=player.blockPosition().getZ()+(int)(Math.sin(angle)*distance);
                int radius=ZGEcologyConfig.RADIUS.get();
                if(!level.hasChunkAt(new BlockPos(x-radius-2,64,z-radius-2))||!level.hasChunkAt(new BlockPos(x+radius+2,64,z+radius+2))) continue;
                var centre=new BlockPos(x,level.getHeight(Heightmap.Types.WORLD_SURFACE,x,z)-1,z);
                if(level.players().stream().anyMatch(p->p.distanceToSqr(centre.getX(),centre.getY(),centre.getZ())<64*64)) continue;
                if(impact(level,centre,radius,dim)) {
                    ledger.days.put(dim,day);ledger.setDirty();
                    for(var nearby:level.players()) nearby.displayClientMessage(Component.literal("A "+(day%2==0?"comet":"asteroid")+" struck "+dim+" at "+x+", "+z+"."),false);
                    break;
                }
            }
        }
    }
    /** Validate the entire volume before changing anything. Does not explode or drop arbitrary terrain items. */
    public static boolean impact(ServerLevel level,BlockPos centre,int radius,String dim) {
        if(centre.getY()<level.getMinBuildHeight()+radius+2 || centre.getY()>level.getMaxBuildHeight()-radius-2) return false;
        for(BlockPos pos:BlockPos.betweenClosed(centre.offset(-radius-2,-radius-1,-radius-2),centre.offset(radius+2,radius+3,radius+2))) {
            if(!level.hasChunkAt(pos) || level.getBlockEntity(pos)!=null || !natural(level,pos)) return false;
        }
        if(!level.getBlockState(centre).isSolidRender(level,centre)) return false;
        for(int x=-radius;x<=radius;x++) for(int z=-radius;z<=radius;z++) {
            int squared=x*x+z*z; if(squared>radius*radius) continue;
            int depth=Math.max(1,(int)Math.sqrt(radius*radius-squared)/2);
            for(int y=-depth;y<=radius;y++) {
                var pos=centre.offset(x,y,z); if(!level.getBlockState(pos).isAir()) level.setBlockAndUpdate(pos,Blocks.AIR.defaultBlockState());
            }
        }
        var core=centre.below(Math.max(1,radius/2));
        level.setBlockAndUpdate(core,BlockInit.METEORITE_FRAGMENT.get().defaultBlockState());
        for(int i=0;i<9;i++) {
            var pos=core.offset(level.random.nextInt(5)-2,0,level.random.nextInt(5)-2);
            if(pos.distSqr(core)<=5) level.setBlockAndUpdate(pos,BlockInit.METEORITE_FRAGMENT.get().defaultBlockState());
        }
        // Small gated ore nodes, never entire storage blocks; normal mining gates/loot remain authoritative.
        String rare=switch(dim){case "moon"->"moonsteel_ore";case "mars"->"olympium_ore";case "cerulon"->"lumenite_ore";case "skarn"->"cinnabrite_ore";case "eidolon"->"rimeglass_ore";case "solvane"->"dawnstone_ore";default->"selenite_ore";};
        Block ore=net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",rare));
        if(ore!=Blocks.AIR) for(int i=0;i<2;i++) level.setBlockAndUpdate(core.offset(i==0?-1:1,0,0),ore.defaultBlockState());
        level.sendParticles(ParticleTypes.EXPLOSION_EMITTER,centre.getX()+.5,centre.getY()+1,centre.getZ()+.5,1,0,0,0,0);
        level.sendParticles(ParticleTypes.CAMPFIRE_SIGNAL_SMOKE,centre.getX()+.5,centre.getY()+1,centre.getZ()+.5,20,2,.5,2,.02);
        level.playSound(null,centre,net.minecraft.sounds.SoundEvents.GENERIC_EXPLODE.value(),net.minecraft.sounds.SoundSource.BLOCKS,3,.7F);
        return true;
    }
    private static boolean natural(ServerLevel level,BlockPos pos) {
        var state=level.getBlockState(pos); if(state.isAir()) return true;
        if(!state.getFluidState().isEmpty()||state.getDestroySpeed(level,pos)<0) return false;
        if(state.is(BlockTags.BASE_STONE_OVERWORLD)||state.is(BlockTags.BASE_STONE_NETHER)||state.is(BlockTags.DIRT)||state.is(BlockTags.SAND)||state.is(BlockTags.ICE)) return true;
        var id=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getKey(state.getBlock());
        if(!id.getNamespace().equals("zerog_tweaks")) return state.is(Blocks.SHORT_GRASS)||state.is(Blocks.TALL_GRASS)||state.is(Blocks.SNOW);
        String path=id.getPath();return path.endsWith("_soil")||path.endsWith("_grass_block")||path.endsWith("_short_grass")||path.endsWith("_tall_grass")||path.endsWith("_ore")||path.contains("glow_")
                ||java.util.Set.of("regolith","rustsand","oxide_crust","lunar_stone","martian_stone","cerulean_stone","skarn_rock","solar_stone","permafrost","polar_frost","prismstone","sludgestone","frostrock","sunspot_rock","crystal_sand","slag","azure_moss","cerulean_soil","shimmer_sand","tidesand","dunesand","blightmoss","toxic_mud").contains(path);
    }
    private DailyPlanetImpacts(){}
}
