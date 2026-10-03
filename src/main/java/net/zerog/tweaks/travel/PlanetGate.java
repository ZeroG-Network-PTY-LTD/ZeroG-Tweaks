package net.zerog.tweaks.travel;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Block;
import net.zerog.tweaks.registry.BlockInit;

/** T6 testing layout: six frame rings, seven-wide pad, four energy inputs and crown. */
public final class PlanetGate {
    public record Part(BlockPos offset,Block block) {}
    public static List<Part> parts() {
        var parts=new ArrayList<Part>();
        Block[] frames={BlockInit.NULLIFITE_GATE_FRAME.get(),BlockInit.MOONSTEEL_GATE_FRAME.get(),
                BlockInit.CERULITE_GATE_FRAME.get(),BlockInit.SKARNITE_GATE_FRAME.get(),
                BlockInit.EIDOLITE_GATE_FRAME.get(),BlockInit.SOLVANITE_GATE_FRAME.get()};
        for(int r=2;r<=7;r++) for(int x=-r;x<=r;x++) for(int z=-r;z<=r;z++)
            if(Math.max(Math.abs(x),Math.abs(z))==r)
                parts.add(new Part(new BlockPos(x,r<=3?-1:0,z),frames[r-2]));
        for(int x=-3;x<=3;x++) for(int z=-3;z<=3;z++)
            parts.add(new Part(new BlockPos(x,0,z),BlockInit.GATE_PAD_PLATE.get()));
        for(int x:new int[]{-7,7}) for(int z:new int[]{-7,7})
            for(int y=1;y<=4;y++) parts.add(new Part(new BlockPos(x,y,z),BlockInit.GATE_PYLON.get()));
        for(var pos:List.of(new BlockPos(-6,1,7),new BlockPos(6,1,7),new BlockPos(-7,1,0),new BlockPos(7,1,0)))
            parts.add(new Part(pos,BlockInit.GATE_ENERGY_PORT.get()));
        // Standing arch, with the existing lens housing above its centre.
        for(int x:new int[]{-4,4}) for(int y=1;y<=10;y++)
            parts.add(new Part(new BlockPos(x,y,5),BlockInit.SOLVANITE_GATE_FRAME.get()));
        for(int x=-4;x<=4;x++) parts.add(new Part(new BlockPos(x,11,5),BlockInit.SOLVANITE_GATE_FRAME.get()));
        parts.add(new Part(new BlockPos(0,12,5),BlockInit.GATE_LENS_HOUSING.get()));
        parts.add(new Part(new BlockPos(0,1,-7),BlockInit.GATE_CONTROLLER.get()));
        return List.copyOf(parts);
    }
    public static BlockPos controller(BlockPos centre) { return centre.offset(0,1,-7); }
    public static void loadLandingChunks(ServerLevel level,BlockPos centre) {
        for(int x=(centre.getX()-8)>>4;x<=(centre.getX()+8)>>4;x++)
            for(int z=(centre.getZ()-8)>>4;z<=(centre.getZ()+8)>>4;z++)level.getChunk(x,z);
    }
    public static String missing(ServerLevel level,BlockPos centre) {
        for(var part:parts()) {
            var pos=centre.offset(part.offset());
            if(!level.hasChunkAt(pos)) return "Unloaded gate part at "+pos.toShortString();
            if(!level.getBlockState(pos).is(part.block())) return "Missing "+part.block().getName().getString()+" at "+pos.toShortString();
        }
        return null;
    }
    public static void build(ServerLevel level,BlockPos centre) {
        // Only explicitly created test-world/platform locations call this builder.
        for(int x=-8;x<=8;x++) for(int z=-8;z<=8;z++) {
            level.setBlock(centre.offset(x,-2,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
            level.setBlock(centre.offset(x,-1,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
            level.setBlock(centre.offset(x,0,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
        }
        for(var part:parts()) level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),2);
    }
    private PlanetGate() {}
}
