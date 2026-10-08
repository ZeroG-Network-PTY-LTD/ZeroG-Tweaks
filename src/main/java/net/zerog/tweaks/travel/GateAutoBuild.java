package net.zerog.tweaks.travel;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;

/** Inventory-funded construction of the exact standing plan; no terrain clearing. */
public final class GateAutoBuild {
    private record Placement(BlockPos pos,BlockState before,BlockState after){}
    public static boolean build(ServerPlayer player,SurvivalGateBlockEntity gate,int tier){
        if(tier<1||tier>6||gate.isRemoved()||player.serverLevel().getBlockEntity(gate.getBlockPos())!=gate||!gate.mayControl(player)||gate.countdown>0||gate.returnPlatform
                ||player.serverLevel()!=gate.getLevel()||player.distanceToSqr(gate.getBlockPos().getCenter())>64)return false;
        var level=player.serverLevel();var plan=GateSchematicSync.plan(gate,tier);
        var changes=new ArrayList<Placement>();var required=new LinkedHashMap<Item,Integer>();
        for(var part:SurvivalGateFormation.displayPlan(level,plan.centre(),plan.facing(),tier,gate.getBlockPos())){
            var pos=plan.centre().offset(SurvivalGateLayout.rotate(part.offset(),plan.facing()));
            if(!level.hasChunkAt(pos)||!level.isInWorldBounds(pos)||!level.getWorldBorder().isWithinBounds(pos))return fail(player,"Build area must be loaded and inside the world border.");
            var old=level.getBlockState(pos);if(old.is(part.block()))continue;
            if(!old.isAir()&&!old.canBeReplaced()||level.getBlockEntity(pos)!=null)return fail(player,"Clear obstructing blocks before building; nothing was consumed.");
            if(!level.mayInteract(player,pos)||!player.mayUseItemAt(pos,net.minecraft.core.Direction.UP,new ItemStack(part.block())))return fail(player,"You cannot build in this area.");
            var state=part.block().defaultBlockState();
            if(state.hasProperty(BlockStateProperties.HORIZONTAL_FACING))state=state.setValue(BlockStateProperties.HORIZONTAL_FACING,gate.facing());
            changes.add(new Placement(pos.immutable(),old,state));required.merge(part.block().asItem(),1,Integer::sum);
        }
        // Creative still checks materials: this is a survival build assistant, not a free admin schematic.
        for(var entry:required.entrySet()){
            int count=0;for(var stack:player.getInventory().items)if(stack.is(entry.getKey()))count+=stack.getCount();
            if(count<entry.getValue())return fail(player,"Missing "+(entry.getValue()-count)+" × "+entry.getKey().getDescription().getString()+"; nothing was consumed.");
        }
        var applied=new ArrayList<Placement>();
        for(var change:changes){
            if(!level.setBlock(change.pos(),change.after(),3)){rollback(level,applied);return fail(player,"Placement failed; nothing was consumed.");}
            applied.add(change);
        }
        if(gate.formedTier()<tier){rollback(level,applied);return fail(player,"The plan conflicts with another controller or shared port; nothing was consumed.");}
        for(var entry:required.entrySet()){
            int remaining=entry.getValue();for(var stack:player.getInventory().items)if(stack.is(entry.getKey())){int used=Math.min(remaining,stack.getCount());stack.shrink(used);remaining-=used;if(remaining==0)break;}
        }
        player.getInventory().setChanged();gate.setChanged();
        player.sendSystemMessage(Component.literal("Tier "+tier+" gate built. Select an allowed world, charge the energy port, then stand on the pad and Engage."));return true;
    }
    private static void rollback(net.minecraft.server.level.ServerLevel level,java.util.List<Placement> changes){for(int i=changes.size()-1;i>=0;i--){var change=changes.get(i);level.setBlock(change.pos(),change.before(),3);}}
    private static boolean fail(ServerPlayer player,String reason){player.sendSystemMessage(Component.literal(reason));return false;}
    private GateAutoBuild(){}
}
