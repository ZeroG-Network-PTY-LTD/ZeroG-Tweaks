package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.gametest.*;
import net.neoforged.neoforge.fluids.FluidStack;
import net.zerog.tweaks.registry.ZGGases;
import net.zerog.tweaks.storage.*;
@GameTestHolder("zerog_owner_followup") @PrefixGameTestTemplate(false)
public final class GasCreativeGameTests {
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void dedicated_gas_tab_contains_both_canisters_and_all_twelve_full_tanks(GameTestHelper h){
  var key=ResourceLocation.parse("zerog_tweaks:gases");
  h.assertTrue(BuiltInRegistries.CREATIVE_MODE_TAB.containsKey(key),"Dedicated ZeroG Gases tab missing");
  var tab=BuiltInRegistries.CREATIVE_MODE_TAB.get(key);
  tab.buildContents(new CreativeModeTab.ItemDisplayParameters(h.getLevel().enabledFeatures(),true,h.getLevel().registryAccess()));
  var entries=tab.getDisplayItems();h.assertTrue(entries.size()==15,"Expected empty canister, two full canisters and12 full tanks");
  h.assertTrue(entries.stream().filter(s->s.is(ZGGases.CANISTER.get())).count()==3,"Canister variants missing");
  int[] capacities={5000,20000,100000,500000,2000000,5000000};
  for(var gas:ZGGases.ALL)for(int tier=0;tier<6;tier++){
   int selected=tier;
   long found=entries.stream().filter(s->s.getItem() instanceof BlockItem item&&item.getBlock()==StorageTankRegistry.BLOCKS.get(selected).get())
    .filter(s->{var tag=s.get(DataComponents.BLOCK_ENTITY_DATA);if(tag==null)return false;
      var fluid=FluidStack.parseOptional(h.getLevel().registryAccess(),tag.copyTag().getCompound("fluid").getCompound("Fluid"));
      return fluid.is(gas.fluid().get())&&fluid.getAmount()==capacities[selected];}).count();
   h.assertTrue(found==1,"Missing/duplicate filled tier"+(tier+1)+" "+gas.id());
  }h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void full_gas_tanks_place_reload_and_restore_drops_without_mixing(GameTestHelper h){
  var pos=new BlockPos(1,1,1);var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
  int[] capacities={5000,20000,100000,500000,2000000,5000000};
  for(var gas:ZGGases.ALL)for(int tier=0;tier<6;tier++){
   h.setBlock(pos,net.minecraft.world.level.block.Blocks.AIR);h.setBlock(pos.below(),net.minecraft.world.level.block.Blocks.STONE);
   var stack=StorageTankRegistry.filledGas(tier,gas,h.getLevel().registryAccess());
   player.setPos(h.absolutePos(pos).getCenter().add(0,0,2));player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,stack);
   var hit=new net.minecraft.world.phys.BlockHitResult(h.absolutePos(pos.below()).getCenter().add(0,.5,0),Direction.UP,h.absolutePos(pos.below()),false);
   var result=((BlockItem)stack.getItem()).place(new net.minecraft.world.item.context.BlockPlaceContext(h.getLevel(),player,net.minecraft.world.InteractionHand.MAIN_HAND,stack,hit));
   h.assertTrue(result.consumesAction()&&stack.isEmpty(),"Gas tank placement failed");
   var tank=(StorageTankBlockEntity)h.getBlockEntity(pos);
   h.assertTrue(tank.tank.getFluid().is(gas.fluid().get())&&tank.tank.getFluidAmount()==capacities[tier]&&tank.getBlockState().getValue(StorageTankBlock.LEVEL)==8,"Placed gas identity/amount/gauge lost");
   h.assertTrue(tank.tank.fill(new FluidStack(net.minecraft.world.level.material.Fluids.WATER,1000),net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE)==0,"Water mixed into gas");
   var reload=(StorageTankBlockEntity)net.minecraft.world.level.block.entity.BlockEntity.loadStatic(tank.getBlockPos(),tank.getBlockState(),tank.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
   h.assertTrue(reload.tank.getFluid().is(gas.fluid().get())&&reload.tank.getFluidAmount()==capacities[tier],"Gas lost on reload");
   var drops=tank.getBlockState().getDrops(new net.minecraft.world.level.storage.loot.LootParams.Builder(h.getLevel())
    .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.BLOCK_ENTITY,tank)
    .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.BLOCK_STATE,tank.getBlockState())
    .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.ORIGIN,tank.getBlockPos().getCenter())
    .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.TOOL,ItemStack.EMPTY));
   h.assertTrue(drops.size()==1,"Gas tank drop duplication");
   var saved=FluidStack.parseOptional(h.getLevel().registryAccess(),drops.get(0).get(DataComponents.BLOCK_ENTITY_DATA).copyTag().getCompound("fluid").getCompound("Fluid"));
   h.assertTrue(saved.is(gas.fluid().get())&&saved.getAmount()==capacities[tier],"Gas lost in tank drop");
   var menu=new StorageTankMenu(1,player.getInventory(),tank);
   h.assertTrue(menu.amount()==capacities[tier]&&menu.fluid().is(gas.fluid().get()),"Tank GUI amount/identity truncated");
  }h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void gas_tube_transfers_oxygen_between_existing_tanks(GameTestHelper h){
  h.setBlock(new BlockPos(1,1,1),StorageTankRegistry.BLOCKS.get(0).get());
  h.setBlock(new BlockPos(3,1,1),StorageTankRegistry.BLOCKS.get(0).get());
  var source=(StorageTankBlockEntity)h.getBlockEntity(new BlockPos(1,1,1));var sink=(StorageTankBlockEntity)h.getBlockEntity(new BlockPos(3,1,1));
  source.tank.fill(new FluidStack(ZGGases.OXYGEN.fluid().get(),5000),net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);
  h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_gas_tube")));
  var pipe=(net.zerog.tweaks.transport.TransportBlockEntity)h.getBlockEntity(new BlockPos(2,1,1));pipe.modes[Direction.WEST.ordinal()]=2;pipe.modes[Direction.EAST.ordinal()]=1;
  net.zerog.tweaks.transport.TransportBlockEntity.tick(h.getLevel(),pipe.getBlockPos(),pipe.getBlockState(),pipe);
  h.assertTrue(sink.tank.getFluid().is(ZGGases.OXYGEN.fluid().get())&&sink.tank.getFluidAmount()==250,"Gas tube failed tier throughput");
  h.assertTrue(source.tank.getFluidAmount()+pipe.tank.getFluidAmount()+sink.tank.getFluidAmount()==5000,"Gas transfer lost/duplicated contents");h.succeed();
 }
}
