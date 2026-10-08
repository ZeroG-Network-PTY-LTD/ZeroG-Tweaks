package net.zerog.tweaks.travel;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.BlockGetter;
import net.zerog.tweaks.registry.BlockInit;

/** Loaded-only, bounded structural discovery. The terminal front is not the gate front. */
public final class SurvivalGateFormation {
    public record Resolution(BlockPos centre,Direction facing,int tier,int coreTier,List<BlockPos> ports,String problem) {
        public Resolution {centre=centre.immutable();ports=List.copyOf(ports);}
        Resolution rejected(String reason){return new Resolution(centre,facing,0,coreTier,ports,reason);}
    }
    private record Shape(int tier,Direction facing){}
    private static final Map<Shape,List<PlanetGate.Part>> CORES=new ConcurrentHashMap<>();
    private static final Map<Shape,List<BlockPos>> SERVICES=new ConcurrentHashMap<>();
    public static int requiredPorts(int tier){return tier>=5?4:tier>=3?2:1;}
    private static boolean service(PlanetGate.Part part){return part.block()==BlockInit.GATE_CONTROLLER.get()||part.block()==BlockInit.GATE_ENERGY_PORT.get();}
    public static List<PlanetGate.Part> structuralParts(int tier,Direction facing){
        return CORES.computeIfAbsent(new Shape(tier,facing),key->SurvivalGateLayout.parts(tier).stream().filter(p->!service(p))
                .map(p->new PlanetGate.Part(SurvivalGateLayout.rotate(p.offset(),facing),p.block())).toList());
    }
    /** Offsets in world orientation; mandatory structure cells are never service sockets. */
    public static List<BlockPos> servicePositions(int tier,Direction facing){
        return SERVICES.computeIfAbsent(new Shape(tier,facing),key->{
            Set<BlockPos> occupied=structuralParts(tier,facing).stream().map(PlanetGate.Part::offset).collect(java.util.stream.Collectors.toSet());
            var result=new ArrayList<BlockPos>();int radius=tier+1;
            for(int x=-radius;x<=radius;x++)for(int z=-radius;z<=radius;z++){
                var local=SurvivalGateLayout.rotate(new BlockPos(x,1,z),facing);
                if(Math.max(Math.abs(x),Math.abs(z))>=2&&!occupied.contains(local))result.add(local);
            }
            return List.copyOf(result);
        });
    }
    private static boolean coreComplete(ServerLevel level,BlockPos centre,int tier,Direction facing){
        for(var part:structuralParts(tier,facing)){
            BlockPos at=centre.offset(part.offset());
            if(!level.hasChunkAt(at)||!level.getBlockState(at).is(part.block()))return false;
        }
        return true;
    }
    private static int anchors(ServerLevel level,BlockPos centre){
        if(!level.hasChunkAt(centre)||!level.getBlockState(centre).is(BlockInit.GATE_PAD_PLATE.get()))return 0;
        int count=0;
        for(int x:new int[]{-2,2})for(int z:new int[]{-2,2}){
            BlockPos at=centre.offset(x,0,z);
            if(level.hasChunkAt(at)&&level.getBlockState(at).is(BlockInit.GATE_PYLON.get()))count++;
        }
        return count;
    }
    private static Resolution services(ServerLevel level,BlockPos centre,BlockPos controller,int tier,Direction facing){
        var slots=servicePositions(tier,facing);var ports=new ArrayList<BlockPos>();int controllers=0;
        int radius=tier+1;
        for(int x=-radius;x<=radius;x++)for(int z=-radius;z<=radius;z++){
            BlockPos at=centre.offset(x,1,z);
            if(level.hasChunkAt(at)&&level.getBlockState(at).is(BlockInit.GATE_CONTROLLER.get()))controllers++;
        }
        for(BlockPos slot:slots){BlockPos at=centre.offset(slot);if(level.hasChunkAt(at)&&level.getBlockState(at).is(BlockInit.GATE_ENERGY_PORT.get()))ports.add(at);}
        String problem=!slots.contains(controller.subtract(centre))?"Controller must occupy a legal service-row position, without replacing structure blocks."
                :controllers!=1?"Service row must contain exactly one controller; found "+controllers+"."
                :ports.size()<requiredPorts(tier)?"Service row needs "+(requiredPorts(tier)-ports.size())+" more energy port(s) for Tier "+tier+".":"";
        return new Resolution(centre,facing,problem.isEmpty()?tier:0,tier,ports,problem);
    }
    /** At most225 candidate centres in a single row; no terrain generation or volumetric search. */
    private static Resolution raw(ServerLevel level,BlockPos controller,Direction preferred){
        Resolution outline=new Resolution(SurvivalGateLayout.centre(controller,preferred),preferred,0,0,List.of(),"Required structure is incomplete.");
        if(!level.hasChunkAt(controller)||!level.getBlockState(controller).is(BlockInit.GATE_CONTROLLER.get()))return outline;
        Resolution formed=null;int bestScore=-1;
        Direction[] directions={preferred,preferred.getClockWise(),preferred.getOpposite(),preferred.getCounterClockWise()};
        for(int x=-7;x<=7;x++)for(int z=-7;z<=7;z++){
            BlockPos centre=controller.offset(x,-1,z);int anchorCount=anchors(level,centre);
            if(anchorCount<2)continue;
            Resolution atCentre=null;
            for(Direction facing:directions){
                // Tier1 is rotationally symmetric; Tier2's surviving inner arch identifies the rear.
                int score=anchorCount*100;
                for(var part:structuralParts(2,facing)){
                    BlockPos at=centre.offset(part.offset());
                    if(level.hasChunkAt(at)&&level.getBlockState(at).is(part.block()))score++;
                }
                if(score>bestScore){bestScore=score;outline=new Resolution(centre,facing,0,0,List.of(),"Required structure is incomplete.");}
                if(anchorCount<4)continue;
                for(int tier=6;tier>=1;tier--){
                    if(atCentre!=null&&tier<=atCentre.tier())break;
                    if(!coreComplete(level,centre,tier,facing))continue;
                    var candidate=services(level,centre,controller,tier,facing);
                    if(candidate.coreTier()>outline.coreTier()||candidate.coreTier()==outline.coreTier()&&score>=bestScore)outline=candidate;
                    if(candidate.tier()>0){atCentre=candidate;break;}
                }
            }
            if(atCentre!=null){
                if(formed!=null&&!formed.centre().equals(atCentre.centre()))return formed.rejected("Controller matches multiple structures; separate the gates and their service blocks.");
                formed=atCentre;
            }
        }
        return formed==null?outline:formed;
    }
    /** Enumerate existing controllers from loaded chunk maps, never force-load a capability query. */
    public static List<SurvivalGateBlockEntity> loadedControllers(ServerLevel level,BlockPos pos,int radius){
        var result=new ArrayList<SurvivalGateBlockEntity>();
        for(int x=(pos.getX()-radius)>>4;x<=(pos.getX()+radius)>>4;x++)for(int z=(pos.getZ()-radius)>>4;z<=(pos.getZ()+radius)>>4;z++){
            var chunk=level.getChunkSource().getChunkNow(x,z);if(chunk==null)continue;
            for(var be:chunk.getBlockEntities().values())if(be instanceof SurvivalGateBlockEntity gate&&!gate.isRemoved()){
                BlockPos at=gate.getBlockPos();
                if(at.getY()==pos.getY()&&Math.abs((long)at.getX()-pos.getX())<=radius&&Math.abs((long)at.getZ()-pos.getZ())<=radius)result.add(gate);
            }
        }
        return result;
    }
    public static Resolution resolve(ServerLevel level,BlockPos controller,Direction preferred){
        Resolution own=raw(level,controller,preferred);
        if(own.tier()==0)return own;
        for(var other:loadedControllers(level,controller,28)){
            if(other.getBlockPos().equals(controller))continue;
            boolean nearPort=own.ports().stream().anyMatch(p->Math.abs((long)p.getX()-other.getBlockPos().getX())<=14&&Math.abs((long)p.getZ()-other.getBlockPos().getZ())<=14);
            if(!nearPort)continue;
            Resolution neighbour=raw(level,other.getBlockPos(),other.facing());
            if(neighbour.tier()>0&&neighbour.ports().stream().anyMatch(own.ports()::contains))
                return own.rejected("An energy port is shared with another complete gate; give each gate separate ports.");
        }
        return own;
    }
    public static BlockPos local(BlockPos offset,Direction facing){
        return SurvivalGateLayout.rotate(offset,switch(facing){case EAST->Direction.WEST;case WEST->Direction.EAST;default->facing;});
    }
    /** An example repair plan uses actual legal service positions, plus recommended sockets for deficits. */
    public static List<PlanetGate.Part> displayPlan(BlockGetter level,BlockPos centre,Direction facing,int tier,BlockPos controller){
        var plan=new LinkedHashMap<BlockPos,net.minecraft.world.level.block.Block>();
        for(var part:SurvivalGateLayout.parts(tier))if(!service(part))plan.put(part.offset(),part.block());
        var legal=servicePositions(tier,facing);BlockPos controllerOffset=controller.subtract(centre);
        BlockPos chosen=legal.contains(controllerOffset)?local(controllerOffset,facing):new BlockPos(0,1,-2);
        plan.put(chosen,BlockInit.GATE_CONTROLLER.get());int ports=0;
        for(BlockPos slot:legal)if(!local(slot,facing).equals(chosen)&&level.getBlockState(centre.offset(slot)).is(BlockInit.GATE_ENERGY_PORT.get())){
            plan.put(local(slot,facing),BlockInit.GATE_ENERGY_PORT.get());ports++;
        }
        var recommended=new ArrayList<BlockPos>();
        for(var part:SurvivalGateLayout.parts(tier))if(part.block()==BlockInit.GATE_ENERGY_PORT.get())recommended.add(SurvivalGateLayout.rotate(part.offset(),facing));
        recommended.addAll(legal);
        for(BlockPos slot:recommended){
            if(ports>=requiredPorts(tier))break;
            BlockPos offset=local(slot,facing);
            if(legal.contains(slot)&&!plan.containsKey(offset)){plan.put(offset,BlockInit.GATE_ENERGY_PORT.get());ports++;}
        }
        return plan.entrySet().stream().map(e->new PlanetGate.Part(e.getKey(),e.getValue())).toList();
    }
    private SurvivalGateFormation(){}
}
