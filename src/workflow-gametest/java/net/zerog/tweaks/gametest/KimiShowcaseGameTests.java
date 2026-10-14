package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.*;

@GameTestHolder("zerog_kimi_sites") @PrefixGameTestTemplate(false)
public final class KimiShowcaseGameTests {
 @GameTest(templateNamespace="zerog_kimi_sites",template="equipment_empty",timeoutTicks=4000)
 public static void grounded_kimi_templates_loot_entrance_saved_positions(GameTestHelper h) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
  var server=h.getLevel().getServer();var sites=new java.util.LinkedHashMap<String,BlockPos>();
  for(var entry:ZeroAdminCommands.SHOWCASES.entrySet()){
   var level=PlanetTestHub.planet(server,"zerog_tweaks:"+entry.getValue());h.assertTrue(level!=null,"Missing planet");var data=PlanetShowcaseSites.get(level);
   String result=data.build(level,entry.getKey());var origin=data.origin(entry.getKey());h.assertTrue(origin!=null,entry.getKey()+": "+result);
   var feet=data.arrival(level,entry.getKey());h.assertTrue(feet!=null&&ZeroAdminCommands.safeFooting(level,feet),"Unsafe/unreachable entrance "+entry.getKey());
   var player=h.makeMockServerPlayerInLevel();var command="zero showcase "+entry.getKey();h.assertTrue(server.getCommands().getDispatcher().execute(command,player.createCommandSourceStack().withPermission(2))==1,"Structure travel refused");h.assertTrue(player.serverLevel()==level&&player.blockPosition().equals(feet),"Wrong planet/entrance arrival");player.discard();
   int width=PlanetShowcaseSites.width(entry.getKey()),depth=PlanetShowcaseSites.surface(entry.getKey()),c=width/2;
   for(int x:new int[]{8,width-9})for(int z:new int[]{8,width-9}){var pos=origin.offset(x,2,z);h.assertTrue(level.getBlockEntity(pos) instanceof ChestBlockEntity,"Missing loot chest");var chest=(ChestBlockEntity)level.getBlockEntity(pos);boolean loot=false;for(int slot=0;slot<27;slot++)loot|=!chest.getItem(slot).isEmpty();h.assertTrue(loot,"Empty generated loot");}
   h.assertTrue(level.getBlockEntity(origin.offset(c-4,2,c-4)) instanceof SpawnerBlockEntity,"Missing hostile spawner");
   for(int step=0;step<depth-1;step++)for(int x=c-1;x<=c+1;x++)for(int dy=0;dy<3;dy++){var p=origin.offset(x,2+step+dy,c+2+step);h.assertTrue(level.getBlockState(p).getCollisionShape(level,p).isEmpty(),"Blocked stairs "+entry.getKey()+" step="+step+" block="+level.getBlockState(p));}
   var edit=origin.offset(24,5,24);level.setBlock(edit,Blocks.GOLD_BLOCK.defaultBlockState(),2);data.build(level,entry.getKey());h.assertTrue(level.getBlockState(edit).is(Blocks.GOLD_BLOCK),"Repeated build overwrote player edit");level.setBlock(edit,Blocks.AIR.defaultBlockState(),2);
   sites.put(entry.getKey(),origin);
  }
  try{var text=new StringBuilder("{\"version\":1,\"natural_generation\":false,\"sites\":[");int i=0;for(var entry:sites.entrySet()){if(i++>0)text.append(',');var p=entry.getValue();text.append("{\"name\":\"").append(entry.getKey()).append("\",\"planet\":\"").append(ZeroAdminCommands.SHOWCASES.get(entry.getKey())).append("\",\"origin\":[").append(p.getX()).append(',').append(p.getY()).append(',').append(p.getZ()).append("]}");}text.append("]}");java.nio.file.Files.writeString(server.getWorldPath(net.minecraft.world.level.storage.LevelResource.ROOT).resolve("zerog-kimi-sites.json"),text);}catch(java.io.IOException ex){throw new RuntimeException(ex);}
  h.succeed();
 }
}
