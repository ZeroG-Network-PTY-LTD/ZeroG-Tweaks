package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.*;

/** Vanilla mock login deliberately runs only without PB's unnegotiated login payload. */
@GameTestHolder("zerog_workflow_optional")
@PrefixGameTestTemplate(false)
public final class GateOptionalTravelGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=300)
    public static void cooperative_return_moves_players_and_charges_once(GameTestHelper helper){
        helper.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("productivebees"),"Use isolated no-PB run for mock-player travel");
        var source=helper.getLevel();var target=source.getServer().getLevel(Level.NETHER);helper.assertTrue(target!=null,"Missing test Nether");
        BlockPos centre=helper.absolutePos(new BlockPos(6,4,6)),home=new BlockPos(1024,90,1024);
        for(var part:SurvivalGateLayout.parts(1)){source.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);target.setBlock(home.offset(part.offset()),part.block().defaultBlockState(),3);}
        var gate=(SurvivalGateBlockEntity)source.getBlockEntity(centre.offset(0,1,-2));
        var homeGate=(SurvivalGateBlockEntity)target.getBlockEntity(home.offset(0,1,-2));
        helper.assertTrue(homeGate.formedTier()==1,"Remote home construction was incomplete before countdown");
        var first=helper.makeMockServerPlayerInLevel();var second=helper.makeMockServerPlayerInLevel();
        first.teleportTo(source,centre.getX()+.3,centre.getY()+1,centre.getZ()+.5,0,0);
        second.teleportTo(source,centre.getX()+.8,centre.getY()+1,centre.getZ()+.5,0,0);
        gate.claim(first);homeGate.claim(first);gate.returnPlatform=true;gate.homeDimension="minecraft:the_nether";gate.homeController=homeGate.getBlockPos();gate.stored=1000000;
        helper.assertTrue(gate.engage(first),"Owner with charged return gate could not engage");
        helper.assertTrue(!gate.mayControl(second),"Non-owner gained control");gate.confirm(second);
        int fee=gate.cost(2);
        helper.runAfterDelay(110,()->{
            helper.assertTrue(first.serverLevel()==target&&second.serverLevel()==target,"Co-op passengers did not reach exact return dimension: countdown="+gate.countdown+", FE="+gate.stored+", tier="+gate.formedTier()+", homeTier="+homeGate.formedTier()+", present="+gate.passengers().size()+", first="+first.serverLevel().dimension().location()+"@"+first.position()+", second="+second.serverLevel().dimension().location()+"@"+second.position());
            helper.assertTrue(gate.stored==1000000-fee,"Launch duplicated/lost FE");
            helper.assertTrue(first.distanceToSqr(home.getX()+.5,home.getY()+1,home.getZ()+.5)<32,"Arrival missed home pad");
            first.discard();second.discard();helper.succeed();
        });
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void clone_keeps_codex_and_controls_reject_nonowner(GameTestHelper helper){
        helper.assertTrue(!net.neoforged.fml.ModList.get().isLoaded("productivebees"),"Use no-PB control test");
        var owner=helper.makeMockServerPlayerInLevel();var stranger=helper.makeMockServerPlayerInLevel();
        var source=helper.getLevel();BlockPos centre=helper.absolutePos(new BlockPos(6,4,6));for(var part:SurvivalGateLayout.parts(1))source.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
        var gate=(SurvivalGateBlockEntity)source.getBlockEntity(centre.offset(0,1,-2));gate.claim(owner);
        owner.moveTo(centre.getX()+.5,centre.getY()+1,centre.getZ()+.5);stranger.moveTo(owner.position());
        var menu=new SurvivalGateMenu(0,stranger.getInventory(),gate);
        helper.assertTrue(!menu.clickMenuButton(stranger,100)&&!menu.clickMenuButton(stranger,102),"Non-owner initiated launch or preview");
        helper.assertTrue(!menu.slots.get(0).mayPickup(stranger),"Non-owner stole upgrade");
        owner.getPersistentData().putBoolean("zerog_codex_moon",true);owner.getPersistentData().putLong("zerog_recall_until",12345);
        net.zerog.tweaks.event.PlanetGravity.cloned(new net.neoforged.neoforge.event.entity.player.PlayerEvent.Clone(stranger,owner,true));
        helper.assertTrue(stranger.getPersistentData().getBoolean("zerog_codex_moon")&&stranger.getPersistentData().getLong("zerog_recall_until")==12345,"Death clone lost Codex or cooldown");
        owner.discard();stranger.discard();helper.succeed();
    }
}
