package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.*;

@GameTestHolder("zerog_hub_tiers") @PrefixGameTestTemplate(false)
public final class HubTieredGateGameTests {
    @GameTest(templateNamespace="zerog_hub_tiers",template="equipment_empty",timeoutTicks=1000)
    public static void six_admin_gate_tiers_form_route_reload_and_preserve_hub(GameTestHelper h){
        var server=h.getLevel().getServer();var level=server.overworld();var ledger=GateLedger.get(server);
        h.assertTrue(PlanetTestHub.isHub(server)&&ledger.tieredHubBuilt,"Tiered hub migration not prepared");
        h.assertTrue(ledger.gates.values().stream().noneMatch(g->g.dimension.equals("minecraft:overworld")),"Old fixed T6 hub routes remain");
        String[] targets={"moon","cerulon","skarn","eidolon","solvane","g5_moons"};
        for(int tier=1;tier<=6;tier++){
            var c=HubTieredGates.centre(tier);var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));
            SurvivalGateLayout.loadFootprint(level,gate.getBlockPos(),net.minecraft.core.Direction.NORTH);
            h.assertTrue(gate!=null&&gate.formedTier()==tier&&gate.adminTest()&&gate.cost(1)==0,"Wrong formed/admin tier "+tier);
            h.assertTrue(gate.canReach("zerog_tweaks:"+targets[tier-1]),"Tier cannot reach its representative destination");
            h.assertTrue(gate.canReach("zerog_tweaks:g5_moons"),"Admin travel remained progression locked");
            var destination=PlanetTestHub.planet(server,"zerog_tweaks:"+targets[tier-1]);h.assertTrue(destination!=null,"Destination missing");
            var arrival=SurvivalGateBlockEntity.prepareArrival(destination,gate);
            h.assertTrue(arrival.formedTier()==1&&arrival.adminTest()&&arrival.cost(1)==0&&arrival.homeController.equals(gate.getBlockPos()),"Return platform not operational for "+tier+": formed="+arrival.formedTier()+", admin="+arrival.adminTest()+", cost="+arrival.cost(1));
            var again=SurvivalGateBlockEntity.prepareArrival(destination,gate);h.assertTrue(again.getBlockPos().equals(arrival.getBlockPos()),"Repeated preparation moved return platform");
            var restored=BlockEntity.loadStatic(gate.getBlockPos(),gate.getBlockState(),gate.saveWithFullMetadata(level.registryAccess()),level.registryAccess());restored.setLevel(level);
            h.assertTrue(((SurvivalGateBlockEntity)restored).adminTest(),"Admin mode lost on reload");
        }
        var edit=PlanetTestHub.hubCentre(33).above(5);level.setBlock(edit,Blocks.STONE.defaultBlockState(),3);HubTieredGates.build(level);
        h.assertTrue(level.getBlockState(edit).is(Blocks.STONE),"Repeated migration destroyed player edits");level.removeBlock(edit,false);
        h.succeed();
    }
}
