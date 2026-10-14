package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.*;
@GameTestHolder("zerog_owner_followup") @PrefixGameTestTemplate(false)
public final class CompressorGameTests {
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void pressing_has_no_bench_routes_and_visual_sync_cannot_change_inventory(GameTestHelper h){
  for(var recipe:h.getLevel().getRecipeManager().getRecipes()){
   if(recipe.value().getType()!=net.minecraft.world.item.crafting.RecipeType.CRAFTING)continue;
   var result=recipe.value().getResultItem(h.getLevel().registryAccess());
   for(String metal:ZGManufacturingComponents.ALL_METALS)for(String kind:new String[]{"plate","cog"})
    h.assertTrue(!result.is(item(metal+"_"+kind,1).getItem()),"Crafting-table component route remains: "+recipe.id());
  }
  var b=machine(h);b.inventory.setStackInSlot(0,item("moonsteel_ingot",4));b.inventory.setStackInSlot(1,item("cog_press",1));b.stored=10000;
  ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);
  var tag=b.getUpdateTag(h.getLevel().registryAccess());
  h.assertTrue(tag.getBoolean("PressVisual")&&!tag.contains("Inventory")&&!tag.contains("VoidFilters"),"Visual packet leaks full machine state");
  var visual=new ProcessingBlockEntity(b.getBlockPos(),b.getBlockState());
  visual.loadWithComponents(tag,h.getLevel().registryAccess());
  h.assertTrue(visual.displayProgress==1&&visual.displayDuration==160&&visual.displayInput.is(item("moonsteel_ingot",1).getItem())&&visual.displayDie.is(item("cog_press",1).getItem())&&visual.displayResult.is(item("moonsteel_cog",1).getItem()),"Press visual state did not round-trip");
  h.assertTrue(visual.inventory.getStackInSlot(0).isEmpty()&&b.inventory.getStackInSlot(0).getCount()==4,"Visual decode mutated inventory");h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void every_nonfront_face_accepts_inputs_dies_power_and_extracts_output(GameTestHelper h){
  var b=machine(h);var level=h.getLevel();var pos=b.getBlockPos();
  for(Direction front:Direction.Plane.HORIZONTAL){
   level.setBlock(pos,b.getBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,front),3);
   for(Direction side:Direction.values()){
    var items=level.getCapability(Capabilities.ItemHandler.BLOCK,pos,side);
    var power=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos,side);
    if(side==front){h.assertTrue(items==null&&power==null,"Front terminal has ports");continue;}
    h.assertTrue(items!=null&&power!=null&&items.getSlots()==3,"Missing combined Auto face");
    b.inventory.setStackInSlot(0,ItemStack.EMPTY);b.inventory.setStackInSlot(b.kind.catalyst(),ItemStack.EMPTY);b.stored=0;
    h.assertTrue(items.insertItem(0,item("moonsteel_ingot",4),false).isEmpty(),"Face rejected ingots");
    h.assertTrue(items.insertItem(1,item("cog_press",1),false).isEmpty(),"Face rejected reusable die");
    h.assertTrue(items.extractItem(0,4,false).isEmpty()&&items.extractItem(1,1,false).isEmpty(),"Face extracted ingredients/die");
    b.inventory.setStackInSlot(b.kind.output(),item("moonsteel_cog",1));
    h.assertTrue(items.extractItem(2,1,false).is(item("moonsteel_cog",1).getItem()),"Face failed output extraction");
    h.assertTrue(power.receiveEnergy(100,false)==100&&b.stored==100,"Face rejected FE");
   }
  }h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void actual_conduits_and_item_tubes_feed_and_extract_without_front_access(GameTestHelper h){
  var b=machine(h);var level=h.getLevel();var pos=b.getBlockPos();
  java.util.function.BiFunction<BlockPos,String,net.zerog.tweaks.transport.TransportBlockEntity> place=(at,id)->{
   level.setBlock(at,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+id)).defaultBlockState(),3);
   var node=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(at);java.util.Arrays.fill(node.modes,3);return node;
  };
  var power=place.apply(pos.east(),"copper_energy_conduit");power.stored=1000;power.modes[Direction.WEST.ordinal()]=1;
  var intake=place.apply(pos.above(),"copper_item_tube");intake.items.setStackInSlot(0,item("moonsteel_ingot",2));intake.modes[Direction.DOWN.ordinal()]=1;
  b.setItemMode(Direction.UP,1);
  var output=place.apply(pos.below(),"copper_item_tube");output.modes[Direction.UP.ordinal()]=2;b.setItemMode(Direction.DOWN,3);
  b.inventory.setStackInSlot(b.kind.output(),item("moonsteel_plate",1));
  h.runAfterDelay(25,()->{
   h.assertTrue(b.stored==1000&&power.stored==0,"Real conduit did not conservatively charge compressor");
   h.assertTrue(b.inventory.getStackInSlot(0).getCount()==2&&intake.items.getStackInSlot(0).isEmpty(),"Real item tube failed input delivery");
   h.assertTrue(b.inventory.getStackInSlot(b.kind.output()).isEmpty()&&output.items.getStackInSlot(0).is(item("moonsteel_plate",1).getItem()),"Real item tube failed output extraction");
   level.setBlock(pos,b.getBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.EAST),3);b.stored=0;power.stored=1000;
   h.runAfterDelay(25,()->{h.assertTrue(b.stored==0&&power.stored==1000,"Conduit charged rotated front terminal");h.succeed();});
  });
 }
 private static ItemStack item(String id,int count){return new ItemStack(id.equals("copper_ingot")?Items.COPPER_INGOT:BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)),count);}
 private static ProcessingBlockEntity machine(GameTestHelper h){
  var pos=h.absolutePos(new BlockPos(2,2,2));h.getLevel().setBlock(pos,BlockInit.INDUSTRIAL_COMPRESSOR.get().defaultBlockState(),3);
  return (ProcessingBlockEntity)h.getLevel().getBlockEntity(pos);
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void pressing_loaded_recipes_and_reusable_tooling(GameTestHelper h){
  var b=machine(h);var pages=ProcessingRecipeCatalogue.pages(b,ItemStack.EMPTY);
  h.assertTrue(pages.size()==ZGManufacturingComponents.ALL_METALS.size()*2,"Incomplete material recipe catalogue");
  for(String metal:ZGManufacturingComponents.ALL_METALS){
   for(String mode:new String[]{"plate","cog"}){
    String source=metal+"_ingot";int count=mode.equals("plate")?2:4;
    b.inventory.setStackInSlot(0,item(source,count));b.inventory.setStackInSlot(b.kind.catalyst(),item(mode+"_press",1));b.inventory.setStackInSlot(b.kind.output(),ItemStack.EMPTY);b.stored=10000;
    var recipe=h.getLevel().getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(b.kind).get(),b.input(),h.getLevel());
    h.assertTrue(recipe.isPresent(),"Missing actual recipe: "+metal+"/"+mode);
    int cost=b.energyCost(recipe.get().value());
    for(int t=0;t<b.duration(recipe.get().value());t++)ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);
    h.assertTrue(b.inventory.getStackInSlot(0).isEmpty()&&b.inventory.getStackInSlot(b.kind.output()).is(item(metal+"_"+mode,1).getItem()),"Incorrect pressing output");
    h.assertTrue(b.inventory.getStackInSlot(b.kind.catalyst()).getCount()==1&&b.stored==10000-cost,"Press consumed or incorrect FE debit");
   }
  }h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void pressing_pauses_filters_and_reload(GameTestHelper h){
  var b=machine(h);b.inventory.insertItem(0,item("moonsteel_ingot",2),false);
  h.assertTrue(!b.inventory.isItemValid(b.kind.catalyst(),new ItemStack(Items.DIRT)),"Invalid die accepted");
  b.inventory.insertItem(b.kind.catalyst(),new ItemStack(ItemInit.COG_PRESS.get()),false);b.stored=10000;
  ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);h.assertTrue(b.progress==0&&b.stored==10000,"Wrong die started a job");
  b.inventory.setStackInSlot(b.kind.catalyst(),new ItemStack(ItemInit.PLATE_PRESS.get()));
  b.inventory.setStackInSlot(b.kind.output(),item("moonsteel_plate",64));
  ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);h.assertTrue(b.progress==0&&b.stored==10000,"Full output spent power");
  b.inventory.setStackInSlot(b.kind.output(),ItemStack.EMPTY);b.stored=0;
  ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);h.assertTrue(b.progress==0,"Unpowered job progressed");
  b.stored=10000;ProcessingBlockEntity.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);
  int stored=b.stored,progress=b.progress;var tag=b.saveWithFullMetadata(h.getLevel().registryAccess());var pos=b.getBlockPos();
  h.getLevel().removeBlock(pos,false);h.getLevel().setBlock(pos,BlockInit.INDUSTRIAL_COMPRESSOR.get().defaultBlockState(),3);
  var loaded=(ProcessingBlockEntity)h.getLevel().getBlockEntity(pos);loaded.loadWithComponents(tag,h.getLevel().registryAccess());
  h.assertTrue(loaded.stored==stored&&loaded.progress==progress&&loaded.inventory.getStackInSlot(0).getCount()==2,"Reload lost inputs/paid job");h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void terminal_faces_refuse_connections_and_revoke_cached_access(GameTestHelper h){
  var b=machine(h);var pos=b.getBlockPos();
  h.assertTrue(h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,pos,Direction.NORTH)==null&&h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,pos,Direction.NORTH)==null,"Compressor front exposed an automation port");
  var cached=b.energyInput(Direction.EAST);h.assertTrue(cached.receiveEnergy(100,true)==100&&b.stored==0,"FE simulation mutated buffer");
  h.assertTrue(b.itemsFor(Direction.UP).insertItem(0,item("moonsteel_ingot",2),false).isEmpty(),"Top input rejected metal");
  b.setItemMode(Direction.DOWN,3);h.assertTrue(b.itemsFor(Direction.DOWN)!=null,"Output face missing");
  h.getLevel().setBlock(pos,b.getBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.EAST),3);
  h.assertTrue(cached.receiveEnergy(100,false)==0&&b.energyInput(Direction.EAST)==null,"Rotation left cached front power active");
  var separatorPos=pos.offset(3,0,0);h.getLevel().setBlock(separatorPos,GasSeparatorRegistry.BLOCK.get().defaultBlockState(),3);
  var separator=(GasSeparatorBlockEntity)h.getLevel().getBlockEntity(separatorPos);
  h.assertTrue(h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,separatorPos,Direction.NORTH)==null&&h.getLevel().getCapability(Capabilities.FluidHandler.BLOCK,separatorPos,Direction.NORTH)==null&&h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,separatorPos,Direction.NORTH)==null,"Separator front exposed pipes/power/items");
  var cardItems=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,separatorPos,Direction.SOUTH);
  h.assertTrue(cardItems!=null&&!cardItems.isItemValid(0,new ItemStack(Items.DIRT)),"Separator accepts arbitrary item ingredients");
  h.assertTrue(cardItems.insertItem(0,new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("acceleration_upgrade_card_t1").get()),false).isEmpty(),"Separator card automation rejected valid upgrade");
  h.assertTrue(separator.energy(Direction.SOUTH).receiveEnergy(100,false)==100&&separator.fluid(Direction.UP)!=null,"Separator functional ports missing");h.succeed();
 }
}
