package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.item.*;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.*;
import net.minecraft.world.phys.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.*;
@GameTestHolder("zerog_owner_followup") @PrefixGameTestTemplate(false)
public final class OwnerFollowupGameTests {
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void planetary_mine_plans_never_request_rails(GameTestHelper h){
  for(int seed=0;seed<128;seed++)for(var corridor:net.zerog.tweaks.worldgen.PlanetMineshaftFeature.plan(net.minecraft.util.RandomSource.create(seed)))h.assertTrue(!corridor.rails(),"Planetary mine plan still has rails: seed "+seed);
  h.succeed();
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=140)
 public static void tidewraith_flies_up_to_visible_prey(GameTestHelper h){
  for(int x=1;x<10;x++)for(int z=1;z<10;z++)for(int y=2;y<30;y++)h.setBlock(new BlockPos(x,y,z),Blocks.AIR);
  var start=h.absolutePos(new BlockPos(4,3,4)).getCenter();
  var mob=EntityInit.TIDEWRAITH.get().create(h.getLevel());mob.setPos(start);h.getLevel().addFreshEntity(mob);
  var prey=net.minecraft.world.entity.EntityType.COW.create(h.getLevel());prey.setNoAi(true);prey.setNoGravity(true);prey.setInvulnerable(true);prey.setPos(start.add(0,16,0));h.getLevel().addFreshEntity(prey);mob.setTarget(prey);
  h.runAfterDelay(100,()->{h.assertTrue(mob.getY()>start.y+5,"Visible high prey was not pursued in flight: "+(mob.getY()-start.y));h.assertTrue(mob.getMaxSpawnClusterSize()==4,"Pack size contract lost");mob.discard();prey.discard();h.succeed();});
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void water_immersion(GameTestHelper h){immersion(h,Blocks.WATER,false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void acid_immersion(GameTestHelper h){immersion(h,ZGDimensionFluids.ACID.block.get(),false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void cryo_immersion(GameTestHelper h){immersion(h,ZGDimensionFluids.CRYO.block.get(),false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void plasma_immersion(GameTestHelper h){immersion(h,ZGDimensionFluids.SOLAR.block.get(),false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void null_immersion(GameTestHelper h){immersion(h,ZGDimensionFluids.NULL.block.get(),false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void starlight_immersion(GameTestHelper h){immersion(h,BlockInit.LIQUID_STARLIGHT.get(),false);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void lava_immersion(GameTestHelper h){immersion(h,Blocks.LAVA,true);}
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=120) public static void magma_immersion(GameTestHelper h){immersion(h,ZGDimensionFluids.MAGMA.block.get(),true);}
 private static void immersion(GameTestHelper h,Block liquid,boolean hot){
  for(int x=1;x<=5;x++)for(int z=1;z<=5;z++)for(int y=1;y<=6;y++)h.setBlock(new BlockPos(x,y,z),x==1||x==5||z==1||z==5||y==1||y==6?Blocks.STONE:liquid);
  var mob=EntityInit.TIDEWRAITH.get().create(h.getLevel());mob.setNoAi(true);mob.setAirSupply(10);mob.setPos(h.absolutePos(new BlockPos(3,2,3)).getCenter());h.getLevel().addFreshEntity(mob);
  // Exercise actual block-contact callbacks as well as breathing. Stationary
  // NoAI fixtures need explicit movement to cross that gameplay boundary.
  for(int t=1;t<=70;t++)h.runAfterDelay(t,()->mob.move(net.minecraft.world.entity.MoverType.SELF,new Vec3(.003,0,0)));
  h.runAfterDelay(80,()->{
   if(hot)h.assertTrue(mob.getHealth()<30,"Hot immersion caused no damage: "+liquid+", health="+mob.getHealth()+", contact="+mob.getPersistentData().contains("ZeroGFluidContact_magma_slag")+", fluid="+h.getLevel().getFluidState(mob.blockPosition()));
   else{h.assertTrue(mob.getHealth()==30,"Immersion damage in "+liquid+": "+mob.getHealth());h.assertTrue(!mob.hasEffect(net.minecraft.world.effect.MobEffects.POISON)&&!mob.isOnFire(),"Non-magma hazard remained");}
   mob.discard();h.succeed();
  });
 }
 @GameTest(templateNamespace="zerog_owner_followup",template="equipment_empty",timeoutTicks=100)
 public static void separator_placement_rotation_preserves_world_ports(GameTestHelper h){
  var block=GasSeparatorRegistry.BLOCK.get();
  h.assertTrue(block.defaultBlockState().hasProperty(BlockStateProperties.HORIZONTAL_FACING),"Separator has no rotatable front");
  var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
  var pos=h.absolutePos(new BlockPos(3,2,3));
  for(var facing:new Direction[]{Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST}){
   player.setYRot(facing.toYRot());
   var context=new BlockPlaceContext(player,InteractionHand.MAIN_HAND,new ItemStack(GasSeparatorRegistry.ITEM.get()),new BlockHitResult(pos.getCenter(),Direction.UP,pos.below(),false));
   var state=block.getStateForPlacement(context);
   h.assertTrue(state.getValue(BlockStateProperties.HORIZONTAL_FACING)==facing.getOpposite(),"Placement front not toward player");
   h.assertTrue(state.rotate(Rotation.CLOCKWISE_90).getValue(BlockStateProperties.HORIZONTAL_FACING)==facing.getOpposite().getClockWise(),"Quarter rotation failed");
   h.getLevel().setBlock(pos,state,3);var be=(GasSeparatorBlockEntity)h.getLevel().getBlockEntity(pos);
   be.water.setFluid(new net.neoforged.neoforge.fluids.FluidStack(net.minecraft.world.level.material.Fluids.WATER,500));be.stored=600;
   var before=be.saveWithoutMetadata(h.getLevel().registryAccess());h.getLevel().setBlock(pos,state.rotate(Rotation.CLOCKWISE_90),3);
   h.assertTrue(h.getLevel().getBlockEntity(pos)==be&&before.equals(be.saveWithoutMetadata(h.getLevel().registryAccess())),"Rotation replaced separator or remapped stored world-face modes");
  }h.succeed();
 }
}
