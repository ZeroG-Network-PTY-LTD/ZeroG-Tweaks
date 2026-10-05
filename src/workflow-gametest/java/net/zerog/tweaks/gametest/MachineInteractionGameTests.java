package net.zerog.tweaks.gametest;

import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.CombustionMenu;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.transport.TransportInteraction;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class MachineInteractionGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void combustion_both_clicks_open_only_the_real_generator_menu(GameTestHelper h){
        var relative=new BlockPos(1,1,1);h.setBlock(relative,BlockInit.COMBUSTION_GENERATOR.get());
        var pos=h.absolutePos(relative);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(pos.getX()+.5,pos.getY()+1,pos.getZ()+.5);
        var hit=new BlockHitResult(pos.getCenter(),Direction.UP,pos,false);
        for(boolean sneak:new boolean[]{false,true}){
            player.setShiftKeyDown(sneak);
            var event=new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,pos,hit);
            TransportInteraction.open(event);
            h.assertTrue(!event.isCanceled(),"Transport interception overrides dedicated generator GUI for sneak="+sneak);
            var menu=new CombustionMenu(1,player.getInventory(),h.getBlockEntity(relative));
            h.assertTrue(menu.stillValid(player)&&menu.slots.size()==37,"Dedicated generator menu not usable");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void bee_terminals_have_no_sneak_menu_fallthrough(GameTestHelper h){
        var relative=new BlockPos(1,1,1);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        for(String id:new String[]{"geno_station","genetic_splicer","apiary_controller","tier3_controller"}){
            h.setBlock(relative,net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.parse("aeroapiary:"+id)));
            var pos=h.absolutePos(relative);player.setPos(pos.getCenter());
            for(boolean sneak:new boolean[]{false,true}){
                player.setShiftKeyDown(sneak);var hit=new BlockHitResult(pos.getCenter(),Direction.UP,pos,false);
                var event=new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,pos,hit);
                if(id.contains("station")||id.contains("splicer"))net.zerog.tweaks.genetics.GeneticsIntegration.open(event);else net.zerog.tweaks.genetics.AlvearyInteraction.open(event);
                h.assertTrue(event.isCanceled(),"Old addon GUI reachable for "+id+" sneak="+sneak);
            }
        }
        h.succeed();
    }
}
