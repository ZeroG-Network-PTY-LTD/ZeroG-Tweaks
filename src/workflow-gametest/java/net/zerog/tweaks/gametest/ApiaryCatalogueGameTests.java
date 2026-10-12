package net.zerog.tweaks.gametest;
import net.minecraft.gametest.framework.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.GasSeparatorRegistry;
@GameTestHolder("zerog_apiary_catalogue") @PrefixGameTestTemplate(false)
public final class ApiaryCatalogueGameTests {
 @GameTest(templateNamespace="zerog_apiary_catalogue",template="equipment_empty",timeoutTicks=500)
 public static void separator_category_and_retired_crown_are_real_tab_contents(GameTestHelper h){
  var parameters=new CreativeModeTab.ItemDisplayParameters(h.getLevel().enabledFeatures(),true,h.getLevel().registryAccess());
  var separator=GasSeparatorRegistry.ITEM.get();
  for(String tab:new String[]{"functional_blocks","storage_and_transport","ingredients"}){
   var actual=BuiltInRegistries.CREATIVE_MODE_TAB.get(ResourceLocation.parse("zerog_tweaks:"+tab));actual.buildContents(parameters);
   long count=actual.getDisplayItems().stream().filter(s->s.is(separator)).count();h.assertTrue(count==(tab.equals("functional_blocks")?1:0),"Separator category count wrong in "+tab+": "+count);
  }
  var id=ResourceLocation.parse("aeroapiary:tier5_crown");
  var crown=BuiltInRegistries.ITEM.get(id);h.assertTrue(crown instanceof BlockItem,"Run catalogue test with the actual orbital bee addon");
  h.assertTrue(BuiltInRegistries.BLOCK.containsKey(id),"Retired placed-block ID removed from saves");
  var used=new java.util.HashSet<ResourceLocation>();
  var tiers=new java.util.HashSet<String>(net.zerog.tweaks.travel.HubExhibits.VALIDATED_TIERS);
  net.zerog.tweaks.guide.MultiblockGuides.layouts().forEach(layout->tiers.add(layout.id().equals("cosmic_alveary")?"tier5":layout.id().substring(0,5)));
  var base=h.absolutePos(new net.minecraft.core.BlockPos(3,1,3));
  for(var layout:net.zerog.tweaks.guide.MultiblockGuides.layouts()){
   var tier=layout.id().equals("cosmic_alveary")?"tier5":layout.id().substring(0,5);h.assertTrue(layout.cells().size()==107,"Guide still depicts an obsolete shell");
   for(var cell:layout.cells()){
    String part=cell.part();String expected=part.endsWith("item_port")?"zerog_tweaks:item_port":part.endsWith("fluid_port")?"zerog_tweaks:fluid_port":part.equals("energy_port")?"zerog_tweaks:energy_port":"aeroapiary:"+tier+"_"+part;
    h.assertTrue(BuiltInRegistries.BLOCK.getKey(net.zerog.tweaks.travel.HubExhibits.serviceShellState(tier,cell.x(),cell.y(),cell.z()).getBlock()).equals(ResourceLocation.parse(expected)),"Guide cell does not match actual hub: "+part);
   }
  }
  for(var tier:tiers){
   for(int x=0;x<5;x++)for(int y=0;y<5;y++)for(int z=0;z<5;z++)h.getLevel().setBlock(base.offset(x,y,z),net.zerog.tweaks.travel.HubExhibits.serviceShellState(tier,x,y,z),3);
   h.assertTrue(net.zerog.tweaks.genetics.AlvearyFormation.locate(h.getLevel(),base.offset(2,1,4),Integer.parseInt(tier.substring(4))).formed(),"Preserved hub parts no longer form "+tier);
   for(var pos:net.minecraft.core.BlockPos.betweenClosed(base,base.offset(4,4,4))){var key=BuiltInRegistries.BLOCK.getKey(h.getLevel().getBlockState(pos).getBlock());if(key.getNamespace().equals("aeroapiary"))used.add(key);}
  }
  int tabs=0;
  for(var entry:BuiltInRegistries.CREATIVE_MODE_TAB.entrySet())if(entry.getKey().location().getNamespace().equals("aeroapiary")){
   tabs++;entry.getValue().buildContents(parameters);h.assertTrue(entry.getValue().getDisplayItems().stream().noneMatch(s->s.is(crown)),"Retired Tier5 Crown is still in bee catalogue");
   for(var stack:entry.getValue().getDisplayItems()){
    var key=BuiltInRegistries.ITEM.getKey(stack.getItem());if(key.getNamespace().equals("aeroapiary")&&(key.getPath().matches("tier[0-9]+_.*")||key.getPath().equals("apiary_controller")))h.assertTrue(used.contains(key),"Non-hub apiary part still listed: "+key);
   }
   for(var key:used)h.assertTrue(entry.getValue().getDisplayItems().stream().anyMatch(s->BuiltInRegistries.ITEM.getKey(s.getItem()).equals(key)),"Hub-required part was hidden: "+key);
  }
  h.assertTrue(tabs>0,"No real addon creative tab was checked");h.succeed();
 }
}
