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
        var edit=HubTieredGates.centre(6).above(10);level.setBlock(edit,Blocks.STONE.defaultBlockState(),3);HubTieredGates.build(level);
        h.assertTrue(level.getBlockState(edit).is(Blocks.STONE),"Repeated migration destroyed player edits");level.removeBlock(edit,false);
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_hub_tiers",template="equipment_empty",timeoutTicks=1000)
    public static void compact_hub_is_supplied_unforced_and_does_not_sweep_planets(GameTestHelper h){
        var server=h.getLevel().getServer();var level=server.overworld();var ledger=GateLedger.get(server);
        h.assertTrue(ledger.compactHub&&ledger.exhibitsBuilt&&ledger.workshopBuilt,"Compact hub or supplied districts not completed");
        for(long packed:level.getForcedChunks()){
            var chunk=new net.minecraft.world.level.ChunkPos(packed);
            // The test runner forces its distant test templates; only inspect the hub.
            h.assertTrue(chunk.x < -8 || chunk.x > 8 || chunk.z < -5 || chunk.z > 6,"Showcase permanently forces hub chunks");
        }
        int landing=0;
        for(int x=-112;x<=120;x++)for(int z=-100;z<=94;z++){
            var pos=new net.minecraft.core.BlockPos(x,63,z);
            if(!level.getBlockState(pos).is(net.zerog.tweaks.registry.BlockInit.LANDING_PLATFORM.get()))continue;
            landing++;boolean gateFloor=false;
            for(int tier=1;tier<=6;tier++)for(var c:java.util.List.of(HubTieredGates.centre(tier),HubTieredGates.playerCentre(tier))){int r=tier+1;if(Math.abs(x-c.getX())<=r&&Math.abs(z-c.getZ())<=r)gateFloor=true;}
            h.assertTrue(gateFloor,"Landing pad outside a gate footprint at "+pos);
        }
        h.assertTrue(landing>0&&landing<=1340,"Unexpected landing-pad count "+landing);
        for(int i=0;i<HubWorkshop.MACHINES.size();i++)h.assertTrue(level.getBlockEntity(HubWorkshop.origin(i))!=null,"Missing workshop machine "+i);
        h.runAfterDelay(100,()->{h.assertTrue(ledger.prepared==0&&ledger.inspectionPrepared==0&&!ledger.inspectionEnabled,"Background world/village generation resumed");h.succeed();});
    }
    @GameTest(templateNamespace="zerog_hub_tiers",template="equipment_empty",timeoutTicks=1000)
    public static void six_player_gates_charge_through_ports_and_show_exact_menu_energy(GameTestHelper h){
        var level=h.getLevel().getServer().overworld();
        h.assertTrue(GateLedger.get(level.getServer()).playerHubBuilt,"Player gate set missing");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.CREATIVE);
        for(int tier=1;tier<=6;tier++){
            var c=HubTieredGates.playerCentre(tier);SurvivalGateLayout.loadFootprint(level,c.offset(0,1,-2),net.minecraft.core.Direction.NORTH);
            var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));
            h.assertTrue(gate!=null&&gate.formedTier()==tier&&!gate.adminTest(),"Player/admin separation failed at "+tier);
            var wirePos=c.offset(3,1,0);var cellPos=c.offset(3,2,0);var genPos=c.offset(4,1,0);
            var wire=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(wirePos);
            var cell=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(cellPos);
            var gen=(net.zerog.tweaks.machine.CombustionBlockEntity)level.getBlockEntity(genPos);
            int total=gate.stored+wire.stored+cell.stored+gen.stored;
            java.util.Arrays.fill(cell.modes,3);
            gate.stored=0;wire.stored=0;cell.stored=0;gen.stored=0;gen.burn=0;gen.fuel.setStackInSlot(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.CHARCOAL,2));
            for(int i=0;i<10;i++){
                net.zerog.tweaks.machine.CombustionBlockEntity.tick(level,genPos,gen.getBlockState(),gen);
                net.zerog.tweaks.transport.TransportBlockEntity.tick(level,wirePos,wire.getBlockState(),wire);
            }
            h.assertTrue(gate.stored+wire.stored+cell.stored+gen.stored==500,"FE not conserved at tier "+tier);
            h.assertTrue(gate.cost(1)>0,"Player gate has free admin travel");
        }
        var mark=HubTieredGates.playerCentre(1).above(10);level.setBlock(mark,Blocks.STONE.defaultBlockState(),3);HubTieredGates.build(level);
        h.assertTrue(level.getBlockState(mark).is(Blocks.STONE),"Rebuild replaced player edits");level.removeBlock(mark,false);
        // Let the real world advance its per-tick receiving budget, rather than resetting private counters.
        h.runAfterDelay(2,()->{
            for(int tier=1;tier<=6;tier++){
                var c=HubTieredGates.playerCentre(tier);var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));
                var wirePos=c.offset(3,1,0);var wire=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(wirePos);
                var cell=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(c.offset(3,2,0));
                var gen=(net.zerog.tweaks.machine.CombustionBlockEntity)level.getBlockEntity(c.offset(4,1,0));
                net.zerog.tweaks.transport.TransportBlockEntity.tick(level,wirePos,wire.getBlockState(),wire);
                h.assertTrue(gate.stored>0&&gate.stored+wire.stored+cell.stored+gen.stored==(1600-gen.burn)*50,"Actual port charge or conservation failed tier "+tier);
                var menu=new SurvivalGateMenu(7,player.getInventory(),gate);h.assertTrue(menu.energy()==gate.stored&&menu.energyCapacity()==gate.capacity(),"Menu hid actual charge tier "+tier);
                cell.stored=Math.min(cell.capacity(),gate.capacity());cell.modes[net.minecraft.core.Direction.DOWN.ordinal()]=1;cell.setChanged();
                gen.fuel.setStackInSlot(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.COAL,64));gen.setChanged();gate.setChanged();
            }
            player.discard();h.succeed();
        });
    }
}
