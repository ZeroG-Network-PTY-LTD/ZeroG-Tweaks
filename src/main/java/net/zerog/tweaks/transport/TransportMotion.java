package net.zerog.tweaks.transport;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.fluids.FluidStack;

/** A bounded representative pulse for a committed transfer, never a second inventory. */
public final class TransportMotion {
    public static void committed(TransportBlockEntity source,ServerLevel level,BlockPos destination,
                                 Direction exit,ItemStack item,FluidStack fluid) {
        committed(source,level,destination,exit,item,fluid,0);
    }
    public static void committed(TransportBlockEntity source,ServerLevel level,BlockPos destination,
                                 Direction exit,ItemStack item,FluidStack fluid,int energy) {
        if(item.isEmpty()&&fluid.isEmpty()&&energy<=0)return;
        var endpoint=destination.relative(exit.getOpposite());
        var previous=new HashMap<BlockPos,BlockPos>();var queue=new ArrayDeque<BlockPos>();
        var start=source.getBlockPos();previous.put(start,start);queue.add(start);
        while(!queue.isEmpty()&&!previous.containsKey(endpoint)) {
            var pos=queue.remove();
            if(!(level.getBlockEntity(pos) instanceof TransportBlockEntity node))continue;
            for(var side:Direction.values()) {
                var nextPos=pos.relative(side);
                if(node.modes[side.ordinal()]==3||previous.containsKey(nextPos)||!level.hasChunkAt(nextPos))continue;
                if(level.getBlockEntity(nextPos) instanceof TransportBlockEntity next
                    &&next.block().family.equals(source.block().family)&&next.enabled()
                    &&next.modes[side.getOpposite().ordinal()]!=3
                    &&(node.colour<0||next.colour<0||node.colour==next.colour)) {
                    previous.put(nextPos,pos);queue.add(nextPos);
                }
            }
        }
        if(!previous.containsKey(endpoint))return;
        var route=new ArrayList<BlockPos>();var pos=endpoint;
        while(true){route.add(pos);if(pos.equals(start))break;pos=previous.get(pos);}
        Collections.reverse(route);
        // Bound visual packets, not the physical route or conserved transfer.
        int stride=Math.max(1,(route.size()+127)/128);
        for(int i=0;i<route.size();i++) {
            if(i%stride!=0&&i!=route.size()-1)continue;
            if(!(level.getBlockEntity(route.get(i)) instanceof TransportBlockEntity node))return;
            // At most one representative packet per node per ten ticks; dense networks stay bounded.
            if(level.getGameTime()-node.motionTick<10)continue;
            Direction outgoing=i==route.size()-1?exit:direction(route.get(i),route.get(i+1));
            Direction incoming=i==0?outgoing.getOpposite():direction(route.get(i),route.get(i-1));
            node.motionItem=item.copyWithCount(item.isEmpty()?0:1);node.motionFluid=fluid.copyWithAmount(fluid.isEmpty()?0:1);
            node.motionFrom=incoming.ordinal();node.motionTo=outgoing.ordinal();node.motionTick=level.getGameTime();
            node.motionEnergy=Math.max(0,energy);
            level.sendBlockUpdated(node.getBlockPos(),node.getBlockState(),node.getBlockState(),2);
        }
    }
    private static Direction direction(BlockPos from,BlockPos to){return Direction.fromDelta(to.getX()-from.getX(),to.getY()-from.getY(),to.getZ()-from.getZ());}
    private TransportMotion(){}
}
