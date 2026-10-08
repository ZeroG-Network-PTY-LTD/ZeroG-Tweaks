package net.zerog.tweaks.travel;

import java.util.LinkedHashMap;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Block;
import net.zerog.tweaks.registry.BlockInit;

/** Survival geometry, separate from the historical T6 test-hub layout. */
public final class SurvivalGateLayout {
    private static final java.util.Map<Integer,List<PlanetGate.Part>> PARTS=new java.util.concurrent.ConcurrentHashMap<>();
    public static int padRadius(int tier){return tier>=5?3:tier>=3?2:1;}
    public static int passengers(int tier){return tier>=5?8:tier>=3?4:2;}
    public static BlockPos rotate(BlockPos local,Direction facing){return switch(facing){case EAST->new BlockPos(-local.getZ(),local.getY(),local.getX());case SOUTH->new BlockPos(-local.getX(),local.getY(),-local.getZ());case WEST->new BlockPos(local.getZ(),local.getY(),-local.getX());default->local;};}
    public static BlockPos centre(BlockPos controller,Direction facing){return controller.subtract(rotate(new BlockPos(0,1,-2),facing));}
    public static List<PlanetGate.Part> parts(int tier){
        if(tier<1||tier>6)throw new IllegalArgumentException("Gate tier outside 1..6");
        return PARTS.computeIfAbsent(tier,SurvivalGateLayout::buildParts);
    }
    private static List<PlanetGate.Part> buildParts(int tier){
        var p=new LinkedHashMap<BlockPos,Block>();
        Block[] frames={BlockInit.NULLIFITE_GATE_FRAME.get(),BlockInit.MOONSTEEL_GATE_FRAME.get(),BlockInit.CERULITE_GATE_FRAME.get(),BlockInit.SKARNITE_GATE_FRAME.get(),BlockInit.EIDOLITE_GATE_FRAME.get(),BlockInit.SOLVANITE_GATE_FRAME.get()};
        for(int t=1;t<=tier;t++){
            int r=t+1;
            for(int x=-r;x<=r;x++)for(int z=-r;z<=r;z++)if(Math.max(Math.abs(x),Math.abs(z))==r)p.put(new BlockPos(x,-1,z),frames[t-1]);
        }
        int pad=padRadius(tier);
        for(int x=-pad;x<=pad;x++)for(int z=-pad;z<=pad;z++)if(!(Math.abs(x)==2&&Math.abs(z)==2))p.put(new BlockPos(x,0,z),BlockInit.GATE_PAD_PLATE.get());
        // Inner pylons remain when upgrading; each ring adds a taller outer set.
        for(int t=1;t<=tier;t++){
            int r=t+1,height=tier+1;
            if(t==1||t==3||t==5)for(int x:new int[]{-r,r})for(int z:new int[]{-r,r})for(int y=0;y<=height;y++)p.put(new BlockPos(x,y,z),BlockInit.GATE_PYLON.get());
            if(t>=2){
                int h=t*2;
                for(int x:new int[]{-r+1,r-1})for(int y=1;y<h;y++)p.put(new BlockPos(x,y,r),frames[t-1]);
                for(int x=-r+1;x<=r-1;x++)p.put(new BlockPos(x,h,r),frames[t-1]);
                p.put(new BlockPos(0,h+1,r),BlockInit.GATE_LENS_HOUSING.get());
            }
        }
        if(tier>=2){p.put(new BlockPos(0,6,3),BlockInit.SELENITE_BLOCK.get());p.put(new BlockPos(0,-2,0),BlockInit.ARESITE_BLOCK.get());}
        p.put(new BlockPos(2,1,0),BlockInit.GATE_ENERGY_PORT.get());
        if(tier>=3)p.put(new BlockPos(-2,1,0),BlockInit.GATE_ENERGY_PORT.get());
        if(tier>=5){p.put(new BlockPos(0,1,3),BlockInit.GATE_ENERGY_PORT.get());p.put(new BlockPos(0,1,-3),BlockInit.GATE_ENERGY_PORT.get());}
        p.put(new BlockPos(0,1,-2),BlockInit.GATE_CONTROLLER.get());
        return p.entrySet().stream().map(e->new PlanetGate.Part(e.getKey(),e.getValue())).toList();
    }
    public static int formedTier(ServerLevel level,BlockPos controller,Direction facing){
        return SurvivalGateFormation.resolve(level,controller,facing).tier();
    }
    public record MissingPart(BlockPos pos,Block expected){}
    public record MissingRequirement(String section,Block expected,int count){}
    /** Group construction faults by local structure section, never by world coordinates. */
    public static List<MissingRequirement> missingRequirements(ServerLevel level,BlockPos controller,Direction facing,int tier){
        record Key(String section,Block expected){}
        var counts=new LinkedHashMap<Key,Integer>();
        var resolved=SurvivalGateFormation.resolve(level,controller,facing);BlockPos origin=resolved.centre();
        for(var part:SurvivalGateFormation.displayPlan(level,origin,resolved.facing(),tier,controller)){
            BlockPos at=origin.offset(rotate(part.offset(),resolved.facing()));
            if(level.hasChunkAt(at)&&level.getBlockState(at).is(part.block()))continue;
            counts.merge(new Key(section(part.offset(),part.block()),part.block()),1,Integer::sum);
        }
        return counts.entrySet().stream().map(e->new MissingRequirement(e.getKey().section(),e.getKey().expected(),e.getValue())).toList();
    }
    private static String section(BlockPos local,Block block){
        if(block==BlockInit.GATE_CONTROLLER.get())return "Service row — controller";
        if(block==BlockInit.GATE_ENERGY_PORT.get())return "Service row — energy ports";
        if(block==BlockInit.GATE_PAD_PLATE.get())return "Landing pad — floor";
        if(local.getY()==-1)return "Base frame — tier "+(Math.max(Math.abs(local.getX()),Math.abs(local.getZ()))-1)+" ring";
        if(block==BlockInit.GATE_PYLON.get())return "Pylons — "+(local.getZ()<0?"front":"rear")+" "+(local.getX()<0?"left":"right")+" column";
        if(block==BlockInit.GATE_LENS_HOUSING.get())return "Rear arch — tier "+(local.getZ()-1)+" lens";
        if(local.getY()< -1)return "Foundation — buried core";
        if(block==BlockInit.SELENITE_BLOCK.get())return "Rear arch — Selenite focus";
        return "Rear arch — tier "+(local.getZ()-1)+" "+(local.getY()==2*(local.getZ()-1)?"crossbeam":local.getX()<0?"left column":"right column");
    }
    public static List<MissingPart> missingParts(ServerLevel level,BlockPos controller,Direction facing,int tier){
        var resolved=SurvivalGateFormation.resolve(level,controller,facing);BlockPos origin=resolved.centre();
        return SurvivalGateFormation.displayPlan(level,origin,resolved.facing(),tier,controller).stream().map(p->new MissingPart(origin.offset(rotate(p.offset(),resolved.facing())),p.block()))
            .filter(p->!level.hasChunkAt(p.pos())||!level.getBlockState(p.pos()).is(p.expected())).toList();
    }
    /** Prefer the current facing on ties; hints never relax required blocks. */
    public static Direction closestFacing(ServerLevel level,BlockPos controller,Direction current){
        return SurvivalGateFormation.resolve(level,controller,current).facing();
    }
    /** Load only the maximum gate footprint before validating a remote, unloaded home. */
    public static void loadFootprint(ServerLevel level,BlockPos controller,Direction facing){
        for(int x=(controller.getX()-14)>>4;x<=(controller.getX()+14)>>4;x++)
            for(int z=(controller.getZ()-14)>>4;z<=(controller.getZ()+14)>>4;z++)level.getChunk(x,z);
    }
    public static int galaxy(String id){if(id.equals("minecraft:overworld")||id.endsWith(":moon")||id.endsWith(":mars"))return 1;return switch(id){case "zerog_tweaks:cerulon"->2;case "zerog_tweaks:skarn"->3;case "zerog_tweaks:eidolon"->4;case "zerog_tweaks:solvane"->5;default->id.matches("zerog_tweaks:g[2-5]_.*")?id.charAt(14)-'0':0;};}
    public static int cost(int base,String source,String target,int players,boolean lens){long numerator=(long)base*(galaxy(source)==galaxy(target)?25:100)*(100+10L*Math.max(0,players-1))*(lens?80:100);return (int)Math.min(Integer.MAX_VALUE,(numerator+999999)/1000000);}
    /** Owner-approved fixed gate tariff; recall-item pricing remains separate. */
    public static int jumpCost(int tier){return 100000 << (Math.clamp(tier,1,6)-1);}
    private SurvivalGateLayout(){}
}
