package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.*;

@GameTestHolder("zerog_gate_display") @PrefixGameTestTemplate(false)
public final class GateHologramGameTests {
    @GameTest(templateNamespace="zerog_gate_display",template="equipment_empty",timeoutTicks=100)
    public static void powered_pylons_light_and_display_positions_are_bounded(GameTestHelper h){
        var level=h.getLevel();var c=h.absolutePos(new BlockPos(6,4,6));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));gate.stored=100000;
        h.runAfterDelay(25,()->{
            var status=GateHologramSync.describe(gate);
            h.assertTrue(!status.pylons().isEmpty()&&status.pylons().size()<=32,"Missing bounded pillar display positions");
            for(var top:status.pylons())h.assertTrue(level.getBlockState(top).getValue(GatePylonBlock.LIT),"Powered gate pillar stayed dark");
            var buffer=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),level.registryAccess());
            try{GateHologramSync.Status.CODEC.encode(buffer,status);h.assertTrue(status.equals(GateHologramSync.Status.CODEC.decode(buffer)),"Pillar display codec mismatch");}finally{buffer.release();}
            gate.stored=0;
        });
        h.runAfterDelay(50,()->{for(var top:gate.pylonTops())h.assertTrue(!level.getBlockState(top).getValue(GatePylonBlock.LIT),"Unpowered pillar stayed lit");h.succeed();});
    }
    @GameTest(templateNamespace="zerog_gate_display",template="equipment_empty",timeoutTicks=120)
    public static void inventory_autobuild_and_destination_tiers(GameTestHelper h){
        var level=h.getLevel();var player=ordinaryPlayer(h);var c=h.absolutePos(new BlockPos(8,4,8));
        // The shared GameTest fixture has a barrier ceiling; clear the entire T6 build envelope.
        for(var at:BlockPos.betweenClosed(c.offset(-8,-2,-8),c.offset(8,14,8)))level.setBlock(at,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        var pos=c.offset(0,1,-2);level.setBlock(pos,net.zerog.tweaks.registry.BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(pos);gate.claim(player);player.moveTo(pos.getCenter());
        h.assertTrue(!GateAutoBuild.build(player,gate,1)&&gate.formedTier()==0,"Missing inventory built free gate");
        var needs=new java.util.LinkedHashMap<net.minecraft.world.item.Item,Integer>();
        for(var part:SurvivalGateLayout.parts(1))if(!part.offset().equals(new BlockPos(0,1,-2)))needs.merge(part.block().asItem(),1,Integer::sum);
        needs.forEach((item,count)->player.getInventory().add(new net.minecraft.world.item.ItemStack(item,count)));
        var obstruction=c.offset(2,-1,0);level.setBlock(obstruction,net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),3);
        int inventoryBefore=player.getInventory().items.stream().mapToInt(net.minecraft.world.item.ItemStack::getCount).sum();
        h.assertTrue(!GateAutoBuild.build(player,gate,1)&&level.getBlockState(obstruction).is(net.minecraft.world.level.block.Blocks.STONE)
                &&player.getInventory().items.stream().mapToInt(net.minecraft.world.item.ItemStack::getCount).sum()==inventoryBefore,"Obstructed build changed terrain or consumed inventory");
        level.setBlock(obstruction,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        h.assertTrue(GateAutoBuild.build(player,gate,1)&&gate.formedTier()==1,"Funded Tier1 construction failed");
        h.assertTrue(player.getInventory().items.stream().allMatch(net.minecraft.world.item.ItemStack::isEmpty),"Auto-build failed to consume exact materials");
        h.assertTrue(gate.canReach("zerog_tweaks:moon")&&gate.canReach("zerog_tweaks:mars")&&!gate.canReach("zerog_tweaks:cerulon"),"Tier1 destination restrictions incorrect");
        h.assertTrue(!gate.canReach("zerog_tweaks:g2_moons"),"Non-Tier6 moon cluster unlocked");
        h.assertTrue(GateAutoBuild.build(player,gate,1),"Already complete build should be harmless");
        for(int tier=2;tier<=6;tier++){
            needs.clear();var plan=GateSchematicSync.plan(gate,tier);
            for(var part:SurvivalGateFormation.displayPlan(level,plan.centre(),plan.facing(),tier,pos)){
                var at=plan.centre().offset(SurvivalGateLayout.rotate(part.offset(),plan.facing()));
                if(!level.getBlockState(at).is(part.block()))needs.merge(part.block().asItem(),1,Integer::sum);
            }
            needs.forEach((item,count)->{while(count>0){int amount=Math.min(64,count);player.getInventory().add(new net.minecraft.world.item.ItemStack(item,amount));count-=amount;}});
            h.assertTrue(GateAutoBuild.build(player,gate,tier)&&gate.formedTier()==tier,"Funded construction failed at Tier "+tier);
            h.assertTrue(player.getInventory().items.stream().allMatch(net.minecraft.world.item.ItemStack::isEmpty),"Tier "+tier+" did not consume exact upgrade materials");
            h.assertTrue(gate.canReach("zerog_tweaks:g2_moons"),"Tier2+ must reach Galaxy2 moons, matching the approved Codex");
        }
        player.discard();h.succeed();
    }
    private static net.minecraft.server.level.ServerPlayer ordinaryPlayer(GameTestHelper h){
        var cookie=net.minecraft.server.network.CommonListenerCookie.createInitial(new com.mojang.authlib.GameProfile(java.util.UUID.randomUUID(),"gate-mode-test"),false);
        var player=new net.minecraft.server.level.ServerPlayer(h.getLevel().getServer(),h.getLevel(),cookie.gameProfile(),cookie.clientInformation());
        var connection=new net.minecraft.network.Connection(net.minecraft.network.protocol.PacketFlow.SERVERBOUND);
        new io.netty.channel.embedded.EmbeddedChannel(connection);
        h.getLevel().getServer().getPlayerList().placeNewPlayer(connection,player,cookie);return player;
    }
    @GameTest(templateNamespace="zerog_gate_display",template="equipment_empty",timeoutTicks=100)
    public static void exact_jump_tariff_and_all_six_authorized_plans(GameTestHelper h){
        var level=h.getLevel();var player=h.makeMockServerPlayerInLevel();
        for(int tier=1;tier<=6;tier++){
            BlockPos c=h.absolutePos(new BlockPos(8,4,8));
            for(var p:BlockPos.betweenClosed(c.offset(-8,0,-8),c.offset(8,10,8)))level.setBlock(p,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
            var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));gate.claim(player);
            player.moveTo(gate.getBlockPos().getX()+.5,gate.getBlockPos().getY()+1,gate.getBlockPos().getZ()+.5);
            int expected=100000<<(tier-1);
            h.assertTrue(gate.formedTier()==tier&&gate.cost(1)==expected&&gate.cost(4)==expected,"Wrong exact jump tariff tier "+tier);
            var menu=new SurvivalGateMenu(0,player.getInventory(),gate);
            for(int plan=1;plan<=6;plan++){
                h.assertTrue(menu.clickMenuButton(player,110+plan),"Missing selectable standing Tier "+plan+" plan");
                var packet=GateSchematicSync.plan(gate,plan);
                h.assertTrue(packet.tier()==plan&&packet.controller().equals(gate.getBlockPos()),"Plan lost requested tier or terminal anchor");
                h.assertTrue(SurvivalGateFormation.displayPlan(level,packet.centre(),packet.facing(),plan,packet.controller()).stream()
                    .anyMatch(part->part.block()==net.zerog.tweaks.registry.BlockInit.GATE_CONTROLLER.get()&&packet.centre().offset(SurvivalGateLayout.rotate(part.offset(),packet.facing())).equals(gate.getBlockPos())),"Plan moved the main controller");
            }
            h.assertTrue(!menu.clickMenuButton(player,110)&&!menu.clickMenuButton(player,117),"Invalid plan request accepted");
            gate.stored=expected;gate.cancel();h.assertTrue(gate.stored==expected,"Cancel consumed FE");
            gate.selected=SurvivalGateBlockEntity.destinations().indexOf("zerog_tweaks:moon");gate.countdown=77;
            var visual=GateHologramSync.describe(gate);
            h.assertTrue(visual.destination().equals("zerog_tweaks:moon")&&visual.countdown()==77&&visual.cost()==expected&&visual.energy()==expected,"Hologram does not describe authoritative selected world/countdown/FE");
            var buffer=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),level.registryAccess());
            try{GateHologramSync.Status.CODEC.encode(buffer,visual);h.assertTrue(GateHologramSync.Status.CODEC.decode(buffer).equals(visual),"Hologram packet lost state");}finally{buffer.release();}
            gate.cancel();
            if(tier==6){
                level.setBlock(gate.getBlockPos(),net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
                var moved=c.offset(0,1,-7);level.setBlock(moved,net.zerog.tweaks.registry.BlockInit.GATE_CONTROLLER.get().defaultBlockState(),3);
                var relocated=(SurvivalGateBlockEntity)level.getBlockEntity(moved);var lower=GateSchematicSync.plan(relocated,1);
                h.assertTrue(relocated.formedTier()==6&&lower.centre().equals(SurvivalGateLayout.centre(moved,lower.facing())),"Smaller plan did not re-anchor to relocated Tier6 controller");
            }
        }
        player.discard();h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_display",template="equipment_empty",timeoutTicks=100)
    public static void creative_cell_placement_shared_quota_and_reload(GameTestHelper h){
        var player=ordinaryPlayer(h);var level=h.getLevel();var support=h.absolutePos(new BlockPos(2,2,2));
        level.setBlock(support,net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),3);var position=support.above();
        level.setBlock(position,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
        player.moveTo(support.getX()+3,support.getY()+1,support.getZ()+3);
        var stack=new net.minecraft.world.item.ItemStack(net.zerog.tweaks.transport.TransportRegistry.CREATIVE_CELL.get());
        var item=(net.zerog.tweaks.transport.CreativeEnergyCell.CreativeItem)stack.getItem();
        var hit=new net.minecraft.world.phys.BlockHitResult(net.minecraft.world.phys.Vec3.atCenterOf(support),net.minecraft.core.Direction.UP,support,false);
        player.setGameMode(net.minecraft.world.level.GameType.SURVIVAL);
        var pickup=new net.neoforged.neoforge.event.entity.player.ItemEntityPickupEvent.Pre(player,new net.minecraft.world.entity.item.ItemEntity(level,position.getX(),position.getY(),position.getZ(),stack.copy()));
        net.zerog.tweaks.transport.CreativeEnergyCell.PickupGuard.pickup(pickup);
        h.assertTrue(pickup.canPickup()==net.neoforged.neoforge.common.util.TriState.FALSE,"Survival pickup of creative cell was allowed");
        h.assertTrue(item.place(new net.minecraft.world.item.context.BlockPlaceContext(player,net.minecraft.world.InteractionHand.MAIN_HAND,stack,hit))==net.minecraft.world.InteractionResult.FAIL&&level.getBlockState(position).isAir(),"Survival player placed admin cell");
        player.setGameMode(net.minecraft.world.level.GameType.CREATIVE);
        h.assertTrue(item.place(new net.minecraft.world.item.context.BlockPlaceContext(player,net.minecraft.world.InteractionHand.MAIN_HAND,stack,hit)).consumesAction(),"Creative cell placement failed");
        var cell=(net.zerog.tweaks.transport.CreativeEnergyCell.Cell)level.getBlockEntity(position);
        var a=level.getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,position,net.minecraft.core.Direction.NORTH);
        var b=level.getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,position,net.minecraft.core.Direction.SOUTH);
        h.assertTrue(a!=null&&b!=null&&a.getEnergyStored()==Integer.MAX_VALUE&&!a.canReceive(),"Admin supply not unlimited/extract-only");
        h.assertTrue(a.extractEnergy(999999,true)==300000&&a.extractEnergy(100000,false)==100000&&b.extractEnergy(999999,false)==200000&&a.extractEnergy(1,false)==0,"Faces exceeded shared quota or simulation spent quota");
        var tag=cell.saveWithFullMetadata(level.registryAccess());
        h.runAfterDelay(1,()->{
            h.assertTrue(a.extractEnergy(999999,false)==300000,"Quota did not replenish next tick");
            level.setBlock(position,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
            h.assertTrue(a.extractEnergy(1,false)==0,"Stale removed cell retained power");
            level.setBlock(position,net.zerog.tweaks.transport.TransportRegistry.CREATIVE_CELL.get().defaultBlockState(),3);
            var restored=(net.zerog.tweaks.transport.CreativeEnergyCell.Cell)level.getBlockEntity(position);restored.loadWithComponents(tag,level.registryAccess());
            h.assertTrue(restored.enabled&&restored.energy().extractEnergy(999999,true)==300000,"Reload lost creative authorization/quota");
            player.discard();h.succeed();
        });
    }
    @GameTest(templateNamespace="zerog_gate_display",template="equipment_empty",timeoutTicks=180)
    public static void invalid_destination_never_debits_jump(GameTestHelper h){
        var level=h.getLevel();BlockPos c=h.absolutePos(new BlockPos(8,4,8));
        for(var part:SurvivalGateLayout.parts(1))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));var player=h.makeMockServerPlayerInLevel();
        player.moveTo(c.getX()+.5,c.getY()+1,c.getZ()+.5);gate.claim(player);gate.returnPlatform=true;
        gate.homeDimension="zerog_tweaks:missing_test_dimension";gate.stored=100000;
        h.assertTrue(gate.engage(player),"Failed-launch test could not begin countdown");
        h.runAfterDelay(110,()->{h.assertTrue(gate.stored==100000&&player.serverLevel()==level&&gate.countdown==0,"Invalid destination consumed FE or moved player");player.discard();h.succeed();});
    }
}
