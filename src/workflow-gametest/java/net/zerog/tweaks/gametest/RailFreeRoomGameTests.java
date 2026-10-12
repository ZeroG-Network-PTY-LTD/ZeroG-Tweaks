package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.levelgen.structure.templatesystem.*;
import net.neoforged.neoforge.gametest.*;
@GameTestHolder("zerog_no_rails") @PrefixGameTestTemplate(false)
public final class RailFreeRoomGameTests {
 @GameTest(templateNamespace="zerog_no_rails",template="equipment_empty",timeoutTicks=500)
 public static void authored_mine_rails_removed_in_all_rotations_with_loot_kept(GameTestHelper h){
  var id=ResourceLocation.parse("zerog_tweaks:planet_mines_no_rails");
  var rules=h.getLevel().registryAccess().registryOrThrow(Registries.PROCESSOR_LIST).getHolderOrThrow(ResourceKey.create(Registries.PROCESSOR_LIST,id)).value();
  var base=h.absolutePos(new BlockPos(1,1,1));
  for(var name:java.util.List.of("collapsed_mine","storage_hall")){
  var template=h.getLevel().getStructureManager().get(ResourceLocation.parse("zerog_tweaks:concord_vault/rooms/"+name)).orElseThrow();
  for(var rotation:Rotation.values()){
   var settings=new StructurePlaceSettings().setIgnoreEntities(true).setRotation(rotation).setRotationPivot(new BlockPos(8,0,8)).addProcessor(JigsawReplacementProcessor.INSTANCE);rules.list().forEach(settings::addProcessor);
   h.assertTrue(template.placeInWorld(h.getLevel(),base,base,settings,h.getLevel().random,3),"Mine room placement failed");
   int chests=0;
   for(var pos:BlockPos.betweenClosed(base,base.offset(16,8,16))){
    var state=h.getLevel().getBlockState(pos);h.assertTrue(!state.is(net.minecraft.tags.BlockTags.RAILS),"Authored space mine still has railway blocks");
    if(h.getLevel().getBlockEntity(pos) instanceof net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity chest){if(chest.getLootTable()!=null)chests++;}
   }
   h.assertTrue(chests>0,"Rail removal lost the mine loot");
  }}h.succeed();
 }
}
