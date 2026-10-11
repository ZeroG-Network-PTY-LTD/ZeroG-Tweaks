package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.ZeroAdminCommands;

@GameTestHolder("zerog_admin_commands") @PrefixGameTestTemplate(false)
public final class ZeroAdminCommandGameTests {
    @GameTest(templateNamespace="zerog_admin_commands",template="equipment_empty",timeoutTicks=500)
    public static void fixed_destinations_and_permissions(GameTestHelper h) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var server=h.getLevel().getServer();var commands=server.getCommands().getDispatcher();
        var admin=server.createCommandSourceStack().withPermission(2);
        var ordinary=admin.withPermission(0);
        h.assertTrue(ZeroAdminCommands.DESTINATIONS.size()==35,"Expected34 planets and Overworld");
        h.assertTrue(commands.getRoot().getChild("zero")!=null,"Missing /zero registration");
        h.assertTrue(!commands.getRoot().getChild("zero").canUse(ordinary),"Non-op can use admin root");
        h.assertTrue(commands.getRoot().getChild("zero").canUse(admin),"Op2 cannot use admin root");
        for(var name:ZeroAdminCommands.DESTINATIONS.keySet())
            h.assertTrue(commands.getRoot().getChild("zero").getChild("tp").getChild(name)!=null,"Missing literal travel shortcut "+name);
        h.assertTrue(commands.execute("zero dimensions",admin)==35,"Dimension catalogue failed");
        h.assertTrue(commands.execute("zero structures",admin)==13,"Structure catalogue failed");
        h.assertTrue(commands.execute("zero locate sunken_relay invalid_planet",admin)==0,"Unknown destination accepted");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_admin_commands",template="equipment_empty",timeoutTicks=500)
    public static void explicit_travel_and_collision_refusal(GameTestHelper h) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var level=h.getLevel();var player=h.makeMockServerPlayerInLevel();var source=player.createCommandSourceStack().withPermission(2);
        var feet=h.absolutePos(new BlockPos(3,3,3));
        level.setBlock(feet.below(),Blocks.STONE.defaultBlockState(),3);
        level.setBlock(feet,Blocks.AIR.defaultBlockState(),3);level.setBlock(feet.above(),Blocks.AIR.defaultBlockState(),3);
        h.assertTrue(ZeroAdminCommands.safeFooting(level,feet),"Clear stone footing refused");
        var command="zero tp overworld "+feet.getX()+" "+feet.getY()+" "+feet.getZ();
        h.assertTrue(level.getServer().getCommands().getDispatcher().execute(command,source)==1,"Explicit admin travel failed");
        h.assertTrue(player.blockPosition().equals(feet),"Admin arrived at wrong position");
        level.setBlock(feet,Blocks.STONE.defaultBlockState(),3);
        h.assertTrue(level.getServer().getCommands().getDispatcher().execute(command,source)==0,"Obstructed destination accepted");
        level.setBlock(feet,Blocks.WATER.defaultBlockState(),3);
        h.assertTrue(!ZeroAdminCommands.safeFooting(level,feet),"Automatic travel allows flooded footing");
        level.setBlock(feet,Blocks.FIRE.defaultBlockState(),3);
        h.assertTrue(!ZeroAdminCommands.safeFooting(level,feet),"Automatic travel allows fire");
        level.setBlock(feet,Blocks.AIR.defaultBlockState(),3);level.setBlock(feet.below(),Blocks.MAGMA_BLOCK.defaultBlockState(),3);
        h.assertTrue(!ZeroAdminCommands.safeFooting(level,feet),"Automatic travel allows magma footing");
        player.discard();h.succeed();
    }
    @GameTest(templateNamespace="zerog_admin_commands",template="equipment_empty",timeoutTicks=500)
    public static void moon_travel(GameTestHelper h) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var server=h.getLevel().getServer();
        var moon=net.zerog.tweaks.travel.PlanetTestHub.planet(server,"zerog_tweaks:moon");
        h.assertTrue(moon!=null,"Run with workflowPlanetPreset to load the Moon");
        var feet=new BlockPos(0,120,0);
        moon.setBlock(feet,Blocks.AIR.defaultBlockState(),3);
        moon.setBlock(feet.above(),Blocks.AIR.defaultBlockState(),3);
        var player=h.makeMockServerPlayerInLevel();
        var source=player.createCommandSourceStack().withPermission(2);
        h.assertTrue(server.getCommands().getDispatcher().execute("zero tp moon 0 120 0",source)==1,"Moon command failed");
        h.assertTrue(player.serverLevel()==moon&&player.blockPosition().equals(feet),"Wrong Moon arrival");
        h.assertTrue(server.getCommands().getDispatcher().execute("zero tp overworld 0 120 0",player.createCommandSourceStack().withPermission(2))==1,"Return command failed");
        h.assertTrue(player.serverLevel()==h.getLevel(),"Wrong return dimension");
        player.discard();h.succeed();
    }
}
