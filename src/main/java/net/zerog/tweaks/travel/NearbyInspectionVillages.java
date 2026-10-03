package net.zerog.tweaks.travel;

import java.util.ArrayList;
import java.util.Comparator;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.levelgen.Heightmap;
import net.zerog.tweaks.worldgen.PlanetSettlementFeature;
import net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity;

/** Opt-in fresh test-hub inspection sites only; natural placement remains unchanged. */
public final class NearbyInspectionVillages {
    public static void prepare(ServerLevel world,GateLedger ledger) {
        if(world==null || !world.getServer().isSameThread())throw new IllegalStateException("Inspection requires server thread");
        String id=world.dimension().location().toString(),name=world.dimension().location().getPath();
        var random=RandomSource.create(world.getSeed()^name.hashCode()^0x5A17E11L);
        int wanted=1+random.nextInt(2);
        var sites=ledger.inspectionVillages.computeIfAbsent(id,k->new ArrayList<>());
        // Rank nearby terrain using noise before loading chunks. The actual site
        // still must pass solid-land, slope, protection and schematic preflight.
        record Candidate(int x,int z,int relief){}
        var candidates=new ArrayList<Candidate>();
        for(int attempt=0;attempt<384;attempt++) {
            double angle=random.nextDouble()*Math.PI*2;
            int radius=96+random.nextInt(289);
            int x=(int)(Math.cos(angle)*radius),z=(int)(Math.sin(angle)*radius);
            int min=Integer.MAX_VALUE,max=Integer.MIN_VALUE;
            for(int dx:new int[]{-18,0,18})for(int dz:new int[]{-18,0,18}) {
                int h=world.getChunkSource().getGenerator().getBaseHeight(x+dx,z+dz,Heightmap.Types.OCEAN_FLOOR_WG,
                        world,world.getChunkSource().randomState());
                min=Math.min(min,h);max=Math.max(max,h);
            }
            // Flat empty space on island/moon generators must not outrank land.
            if(min>=world.getMinBuildHeight()+21 && max<=world.getMaxBuildHeight()-12)
                candidates.add(new Candidate(x,z,max-min));
        }
        candidates.sort(Comparator.comparingInt(Candidate::relief));
        int loaded=0;
        // Ocean worlds use a sealed seabed inspection habitat, not a floating
        // village stamped onto the water surface. Prefer dry terrain first.
        for(int mode=0;mode<2 && sites.size()<wanted;mode++)for(var candidate:candidates) {
            if(sites.size()>=wanted || loaded>=(mode==0?16:32))break;
            if(sites.stream().anyMatch(p->p.distSqr(new BlockPos(candidate.x(),p.getY(),candidate.z()))<80*80))continue;
            // Avoid loading obviously unsuitable steep sites.
            if(candidate.relief()>10)continue;
            for(int cx=(candidate.x()-20)>>4;cx<=(candidate.x()+20)>>4;cx++)
                for(int cz=(candidate.z()-20)>>4;cz<=(candidate.z()+20)>>4;cz++)world.getChunk(cx,cz);
            loaded++;
            var heights=new ArrayList<Integer>();boolean valid=true;
            for(int dx:new int[]{-18,-9,0,9,18})for(int dz:new int[]{-18,-9,0,9,18}) {
                // Non-colliding grass/flowers and tree leaves are not the floor.
                int y=world.getHeight(mode==0?Heightmap.Types.MOTION_BLOCKING_NO_LEAVES:Heightmap.Types.OCEAN_FLOOR,candidate.x()+dx,candidate.z()+dz)-1;
                var at=new BlockPos(candidate.x()+dx,y,candidate.z()+dz);
                if(!world.getFluidState(at).isEmpty() || !world.getBlockState(at).isSolidRender(world,at))valid=false;
                heights.add(y);
            }
            heights.sort(Integer::compare);int y=heights.get(heights.size()/2);
            if(!valid || heights.get(0)<y-4 || heights.get(heights.size()-1)>y+4)continue;
            var centre=new BlockPos(candidate.x(),y,candidate.z());
            if(!PlanetSettlementFeature.build(world,centre,name,random.nextInt(4),random))continue;
            if(mode==1)sealHabitat(world,centre);
            sites.add(centre.immutable());ledger.setDirty();
            if(world.getBlockEntity(centre) instanceof SettlementAnchorBlockEntity anchor)anchor.populate(world);
        }
        var gate=ledger.gates.values().stream().filter(g->g.dimension.equals(id)&&g.target.equals("minecraft:overworld")).findFirst().orElseThrow();
        var signPos=gate.centre.offset(3,1,-8);
        world.setBlock(signPos,Blocks.OAK_SIGN.defaultBlockState(),3);
        if(world.getBlockEntity(signPos) instanceof SignBlockEntity sign) {
            var text=sign.getFrontText().setMessage(0,Component.literal("Village inspections"));
            for(int i=0;i<sites.size();i++)text=text.setMessage(i+1,Component.literal(sites.get(i).toShortString()));
            if(sites.isEmpty())text=text.setMessage(1,Component.literal("No safe land found"));
            sign.setText(text,true);sign.setChanged();
        }
        com.mojang.logging.LogUtils.getLogger().info("ZeroG nearby villages {}: {}/{} sites {} ({} loaded candidates)",id,sites.size(),wanted,sites,loaded);
    }
    private static void sealHabitat(ServerLevel world,BlockPos centre){
        // Complete water-tight stepped canopy with solid floor support on the
        // native seabed. Ordinary glass, never Star Glass. Inspection-only.
        for(int x=-19;x<=19;x++)for(int z=-19;z<=19;z++) {
            var floor=centre.offset(x,0,z);
            if(Math.max(Math.abs(x),Math.abs(z))>=18) {
                for(int dy=0;dy<5;dy++)world.setBlock(floor.below(dy),
                        net.zerog.tweaks.registry.ZGDimensionTerrain.SOILS.get(world.dimension().location().getPath()).get().defaultBlockState(),2);
            }
            int roof=8+(Math.max(Math.abs(x),Math.abs(z))<14?2:0);
            for(int y=1;y<=10;y++) {
                boolean shell=Math.max(Math.abs(x),Math.abs(z))==19 || y>=roof;
                if(shell)world.setBlock(floor.above(y),Blocks.GLASS.defaultBlockState(),2);
                else if(!world.getFluidState(floor.above(y)).isEmpty())world.setBlock(floor.above(y),Blocks.AIR.defaultBlockState(),2);
            }
        }
    }
    private NearbyInspectionVillages(){}
}
