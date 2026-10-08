package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.*;

/** Real outbound planets use the opt-in workflowPlanetPreset, without Productive Bees mock login. */
@GameTestHolder("zerog_gate_outbound") @PrefixGameTestTemplate(false)
public final class GateOutboundGameTests {
    @GameTest(templateNamespace="zerog_gate_outbound",template="equipment_empty",timeoutTicks=800)
    public static void tier_one_reaches_moon(GameTestHelper h){outbound(h,"moon");}
    @GameTest(templateNamespace="zerog_gate_outbound",template="equipment_empty",timeoutTicks=800)
    public static void tier_one_reaches_mars(GameTestHelper h){outbound(h,"mars");}
    private static void outbound(GameTestHelper h,String planet){
        var source=h.getLevel();var target=PlanetTestHub.planet(source.getServer(),"zerog_tweaks:"+planet);
        h.assertTrue(target!=null,"Use workflowPlanetPreset for actual outbound planets");
        var c=h.absolutePos(new BlockPos(6,4,6));
        for(var part:SurvivalGateLayout.parts(1))source.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)source.getBlockEntity(c.offset(0,1,-2));var player=h.makeMockServerPlayerInLevel();
        gate.claim(player);gate.stored=100000;gate.selected=SurvivalGateBlockEntity.destinations().indexOf("zerog_tweaks:"+planet);
        player.moveTo(c.getX()+.5,c.getY()+1,c.getZ()+.5);
        h.assertTrue(gate.engage(player),"Valid funded Tier1 could not engage toward "+planet);
        h.runAfterDelay(115,()->{
            h.assertTrue(player.serverLevel()==target,"Tier1 failed to reach "+planet);
            h.assertTrue(gate.stored==0,"Successful Tier1 jump did not charge exactly100000FE");
            var landing=SurvivalGateBlockEntity.prepareArrival(target,gate);
            h.assertTrue(landing!=null&&landing.formedTier()==1&&landing.returnPlatform&&landing.homeController.equals(gate.getBlockPos()),"Missing correctly bound return gate");
            var packet=new GateLaunchSync.Destination(target.dimension().location().toString(),1,planet,1.0F,false);
            var buffer=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),source.registryAccess());
            try{GateLaunchSync.Destination.CODEC.encode(buffer,packet);h.assertTrue(GateLaunchSync.Destination.CODEC.decode(buffer).equals(packet),"Transition payload lost destination");}finally{buffer.release();}
            player.discard();h.succeed();
        });
    }
}
