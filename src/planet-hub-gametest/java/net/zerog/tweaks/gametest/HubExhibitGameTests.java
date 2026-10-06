package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.LevelReader;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.block.entity.DispenserBlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.*;
import net.zerog.tweaks.guide.MultiblockGuides;

@GameTestHolder("zerog_hub_exhibits")
@PrefixGameTestTemplate(false)
public final class HubExhibitGameTests {
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=100)
    public static void supplied_alveary_kit_contains_real_bees_frames_and_tank_materials(GameTestHelper helper){
        var level=helper.getLevel().getServer().overworld();
        level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack(),"zerog hub workshop");
        var base=HubWorkshop.origin(13);boolean bee=false,frame=false,liquid=false;
        for(int c=0;c<4;c++)if(level.getBlockEntity(base.offset(3+c*2,0,0)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity chest)
            for(int s=0;s<chest.getContainerSize();s++){var stack=chest.getItem(s);
                bee|=net.zerog.tweaks.genetics.ProductiveBeeGenes.read(stack).size()==5||!net.zerog.tweaks.genetics.AlvearyRuntime.species(stack).isEmpty();
                frame|=net.zerog.tweaks.genetics.AlvearyRuntime.isFrame(stack);
                liquid|=BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals("zerog_tweaks:liquid_starlight_bucket");
            }
        helper.assertTrue(bee&&frame&&liquid,"Alveary service kit lacks valid bees, frames or starlight bucket");helper.succeed();
    }
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=5000)
    public static void workshop_forge_crystal_salvage_and_genetics_have_operating_materials(GameTestHelper helper){
        var level=helper.getLevel().getServer().overworld();
        level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack(),"zerog hub workshop");
        var machines=new java.util.ArrayList<net.zerog.tweaks.machine.ProcessingBlockEntity>();
        for(int index=1;index<4;index++){
            var base=HubWorkshop.origin(index);var be=(net.zerog.tweaks.machine.ProcessingBlockEntity)level.getBlockEntity(base);
            helper.assertTrue(be!=null,"Missing workshop machine "+index);
            var output=be.itemsFor(net.minecraft.core.Direction.DOWN);for(int s=0;s<output.getSlots();s++)output.extractItem(s,64,false);
            var recipe=level.getRecipeManager().getAllRecipesFor(net.zerog.tweaks.machine.ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get()).stream()
                .filter(r->r.value().outputs().get(0).chance()==1).sorted(java.util.Comparator.comparing(r->r.id().toString())).findFirst().orElseThrow().value();
            for(int input=0;input<recipe.inputs().size();input++){
                var entry=recipe.inputs().get(input);var supply=findSupply(level,base,entry);
                helper.assertTrue(!supply.isEmpty(),"No recipe material for "+be.kind+" input "+input);
                helper.assertTrue(be.inventory.insertItem(input,supply,false).isEmpty(),"Supplied input rejected by "+be.kind);
            }
            if(recipe.catalyst().isPresent())helper.assertTrue(be.inventory.insertItem(be.kind.catalyst(),findSupply(level,base,recipe.catalyst().get()),false).isEmpty(),"Workshop catalyst rejected");
            for(int t=0;t<=be.duration(recipe);t++)tickInstalledStation(level,base);
            machines.add(be);
        }
        for(int i=7;i<=8;i++){
            var base=HubWorkshop.origin(i);var chest=(net.minecraft.world.level.block.entity.ChestBlockEntity)level.getBlockEntity(base.offset(3,0,0));
            helper.assertTrue(chest!=null&&net.zerog.tweaks.genetics.ProductiveBeeGenes.read(chest.getItem(0)).size()==5,"Genetics sample is an empty/invalid cage");
            String id=HubWorkshop.MACHINES.get(i);
            helper.assertTrue(net.zerog.tweaks.genetics.GeneticsRuntime.mayPlace(id,0,chest.getItem(0)),"Genetics sample rejected");
            if(i==8){boolean serum=false,catalyst=false;for(int s=0;s<chest.getContainerSize();s++){serum|=net.zerog.tweaks.genetics.GeneticsRuntime.mayPlace(id,1,chest.getItem(s));catalyst|=net.zerog.tweaks.genetics.GeneticsRuntime.mayPlace(id,2,chest.getItem(s));}helper.assertTrue(serum&&catalyst,"Splicer lacks valid serum/catalyst");}
        }
        for(var be:machines)helper.assertTrue(!be.inventory.getStackInSlot(be.kind.output()).isEmpty(),"Workshop "+be.kind+" did not complete a supplied recipe through real power");
        helper.succeed();
    }
    @SuppressWarnings("unchecked")
    private static void tickInstalledStation(net.minecraft.server.level.ServerLevel level,BlockPos base){
        // Step the block's actual registered ticker; never inject machine FE or substitute a processing implementation.
        for(int z=-2;z<=0;z++){var pos=base.offset(0,0,z);var be=level.getBlockEntity(pos);var state=level.getBlockState(pos);
            if(be==null)throw new IllegalStateException("Missing powered station part "+pos);
            var type=(net.minecraft.world.level.block.entity.BlockEntityType<net.minecraft.world.level.block.entity.BlockEntity>)(Object)be.getType();
            if(!(state.getBlock() instanceof net.minecraft.world.level.block.EntityBlock block))throw new IllegalStateException("Station part is not an entity block "+pos);
            var ticker=block.getTicker(level,state,type);if(ticker==null)throw new IllegalStateException("Installed machine/cable has no registered ticker "+pos);
            ticker.tick(level,pos,state,be);
        }
    }
    private static net.minecraft.world.item.ItemStack findSupply(net.minecraft.server.level.ServerLevel level,BlockPos base,net.zerog.tweaks.machine.ProcessingRecipe.Counted entry){
        for(int c=0;c<4;c++)if(level.getBlockEntity(base.offset(3+c*2,0,0)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity chest)
            for(int s=0;s<chest.getContainerSize();s++){var stack=chest.getItem(s);if(stack.getCount()>=entry.count()&&entry.ingredient().test(stack))return stack.copyWithCount(entry.count());}
        return net.minecraft.world.item.ItemStack.EMPTY;
    }
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=600)
    public static void supplied_workshop_processes_real_materials_and_preserves_player_edits(GameTestHelper helper) {
        var level=helper.getLevel().getServer().overworld();
        level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack(),"zerog hub workshop");
        var base=new BlockPos(-100,64,-20);
        helper.assertTrue(BuiltInRegistries.BLOCK.getKey(level.getBlockState(base).getBlock()).toString().equals("zerog_tweaks:ore_refinery"),"Supplied workshop refinery absent");
        var chest=(net.minecraft.world.level.block.entity.ChestBlockEntity)level.getBlockEntity(base.offset(3,0,0));
        helper.assertTrue(chest!=null&&!chest.isEmpty(),"Refinery has no working materials");
        var machine=(net.zerog.tweaks.machine.ProcessingBlockEntity)level.getBlockEntity(base);
        helper.assertTrue(machine!=null,"Refinery has no processing backend");
        var products=machine.itemsFor(net.minecraft.core.Direction.DOWN);for(int slot=0;slot<products.getSlots();slot++)products.extractItem(slot,64,false);
        helper.assertTrue(machine.inventory.insertItem(0,chest.getItem(0).copyWithCount(1),false).isEmpty(),"Supplied material rejected by refinery");
        for(int tick=0;tick<300;tick++)tickInstalledStation(level,base);
        var marker=base.offset(5,0,0);level.setBlock(marker,Blocks.DIAMOND_BLOCK.defaultBlockState(),3);
        var original=chest.getItem(0).copy();
        chest.setItem(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.APPLE,7));
        level.getServer().getCommands().performPrefixedCommand(level.getServer().createCommandSourceStack(),"zerog hub workshop");
        helper.assertTrue(chest.getItem(0).is(net.minecraft.world.item.Items.APPLE)&&chest.getItem(0).getCount()==7,"Rebuild refilled or replaced player supplies");
        helper.assertTrue(level.getBlockState(marker).is(Blocks.DIAMOND_BLOCK),"Workshop rebuild overwrote player edit");
        try {
            helper.assertTrue(!machine.inventory.getStackInSlot(machine.kind.output()).isEmpty(),"Powered refinery did not produce output from supplied ore");
        } finally {chest.setItem(0,original);level.setBlock(marker,Blocks.AIR.defaultBlockState(),3);}
        helper.succeed();
    }
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=100)
    public static void smoker_calms_nearby_bees_without_affecting_distant_bees(GameTestHelper helper) {
        var level=helper.getLevel();
        helper.assertTrue(BuiltInRegistries.ITEM.containsKey(ResourceLocation.fromNamespaceAndPath("aeroapiary","bee_smoker")),"Existing handheld smoker missing");
        var centre=helper.absoluteVec(new net.minecraft.world.phys.Vec3(2,2,2));
        var near=net.minecraft.world.entity.EntityType.BEE.create(level);
        var far=net.minecraft.world.entity.EntityType.BEE.create(level);
        var player=helper.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        near.moveTo(centre);far.moveTo(centre.add(9,0,0));
        for(var bee:java.util.List.of(near,far)) {
            bee.setRemainingPersistentAngerTime(400);bee.setPersistentAngerTarget(player.getUUID());bee.setTarget(player);
            level.addFreshEntity(bee);
        }
        helper.assertTrue(net.zerog.tweaks.event.HandheldBeeSmoker.calm(level,centre)>=1,"Smoke reached no bees");
        helper.assertTrue(!near.isAngry()&&near.getTarget()==null&&near.getPersistentAngerTarget()==null,"Nearby bee still attacking");
        helper.assertTrue(far.isAngry()&&far.getTarget()==player,"Smoke incorrectly calmed distant bee");
        near.discard();far.discard();helper.succeed();
    }
    @GameTest(templateNamespace="zerog_hub_exhibits",template="equipment_empty",timeoutTicks=400)
    public static void authored_apiaries_real_formation_and_ten_safe_room_exhibits(GameTestHelper helper) {
        var level=helper.getLevel().getServer().overworld();
        helper.assertTrue(GateLedger.get(level.getServer()).exhibitsBuilt,"Exhibits did not build with installed bee add-on");
        int index=0;
        var displayedTiers=new java.util.HashSet<Integer>();
        for(var layout:MultiblockGuides.layouts()) {
            var base=HubExhibits.designOrigin(index++);
            // Old published hubs used an earlier guide order. Test each actual shell, not today's list position.
            String controller=BuiltInRegistries.BLOCK.getKey(level.getBlockState(base.offset(2,1,4)).getBlock()).toString();
            helper.assertTrue(controller.matches("aeroapiary:tier[1-7]_controller"),"Missing exhibited controller: "+controller);
            int tier=Integer.parseInt(controller.substring("aeroapiary:tier".length(),"aeroapiary:tier".length()+1));displayedTiers.add(tier);
            var formed=net.zerog.tweaks.genetics.AlvearyFormation.locate(level,base.offset(2,1,4),tier);
            helper.assertTrue(formed.formed(),"Rejected ZeroG service ports in hub "+layout.id()+": "+formed.error());
            for(int x=0;x<5;x++)helper.assertTrue(BuiltInRegistries.BLOCK.getKey(level.getBlockState(base.offset(x,0,4)).getBlock()).getNamespace().equals("zerog_tweaks"),"Missing ZeroG service module");
            helper.assertTrue(level.getBlockEntity(base.offset(2,0,8)) instanceof SignBlockEntity,"Missing apiary sign");
        }
        helper.assertTrue(displayedTiers.size()==7,"Exhibits no longer cover all seven tiers");
        index=0;
        for(String tier:HubExhibits.VALIDATED_TIERS) {
            try {
                var base=HubExhibits.formedOrigin(index++);
                level.getChunkAt(base);level.getChunkAt(base.offset(4,0,4));
                var validator=net.zerog.tweaks.genetics.AlvearyFormation.class;
                var result=validator.getMethod("locate",net.minecraft.server.level.ServerLevel.class,BlockPos.class,int.class).invoke(null,level,base.offset(2,1,4),Integer.parseInt(tier.substring(4)));
                helper.assertTrue((boolean)result.getClass().getMethod("formed").invoke(result),"Bee add-on rejected "+tier+": "+result);
                // Accepted alternate service positions, without relaxing roof or air requirements.
                var energy=base.offset(2,0,4);var alternative=base.offset(0,0,4);
                var energyState=level.getBlockState(energy);var casingState=level.getBlockState(alternative);
                level.setBlock(energy,casingState,3);level.setBlock(alternative,energyState,3);
                var frame=base.offset(2,1,4);var alternateFrame=base.offset(0,1,4);
                var frameState=level.getBlockState(frame);var westState=level.getBlockState(alternateFrame);
                level.setBlock(frame,westState,3);level.setBlock(alternateFrame,frameState,3);
                var alternateResult=validator.getMethod("locate",net.minecraft.server.level.ServerLevel.class,BlockPos.class,int.class).invoke(null,level,alternateFrame,Integer.parseInt(tier.substring(4)));
                helper.assertTrue((boolean)alternateResult.getClass().getMethod("formed").invoke(alternateResult),"Alternate ports/frame positions rejected "+tier);
                level.setBlock(energy,energyState,3);level.setBlock(alternative,casingState,3);
                level.setBlock(frame,frameState,3);level.setBlock(alternateFrame,westState,3);
                var roof=base.offset(0,4,0);var roofState=level.getBlockState(roof);level.setBlock(roof,casingState,3);
                var invalid=validator.getMethod("locate",net.minecraft.server.level.ServerLevel.class,BlockPos.class,int.class).invoke(null,level,base.offset(2,1,4),Integer.parseInt(tier.substring(4)));
                helper.assertTrue(!(boolean)invalid.getClass().getMethod("formed").invoke(invalid),"Wrong roof accepted "+tier);
                level.setBlock(roof,roofState,3);
            } catch(ReflectiveOperationException failure) {throw new IllegalStateException(failure);}
        }
        int spawners=0,launchers=0;index=0;
        for(String room:HubExhibits.ROOMS) {
            var base=HubExhibits.roomOrigin(index++);
            helper.assertTrue(!level.getBlockState(base.offset(8,0,8)).isAir(),"Room floor absent "+room);
            helper.assertTrue(level.getBlockEntity(base.offset(8,0,19)) instanceof SignBlockEntity,"Missing room sign "+room);
            for(var pos:BlockPos.betweenClosed(base,base.offset(16,8,16))) {
                helper.assertTrue(!level.getBlockState(pos).is(Blocks.JIGSAW),"Unreplaced jigsaw in "+room);
                if(level.getBlockEntity(pos) instanceof SpawnerBlockEntity spawner) {
                    var tag=spawner.saveWithoutMetadata(level.registryAccess());
                    helper.assertTrue(tag.getShort("SpawnCount")==0 && tag.getShort("RequiredPlayerRange")==0,"Active exhibit spawner");spawners++;
                }
                if(level.getBlockEntity(pos) instanceof DispenserBlockEntity launcher) {helper.assertTrue(launcher.isEmpty(),"Loaded trap launcher");launchers++;}
            }
        }
        helper.assertTrue(spawners>0 && launchers>0,"Spawner/trap inspection fixtures missing");
        var check=HubExhibits.designOrigin(0).offset(0,10,0);level.setBlock(check,Blocks.DIAMOND_BLOCK.defaultBlockState(),3);
        helper.assertTrue(HubExhibits.build(level).contains("already built"),"Exhibits not idempotent");
        helper.assertTrue(level.getBlockState(check).is(Blocks.DIAMOND_BLOCK),"Player modification overwritten");level.setBlock(check,Blocks.AIR.defaultBlockState(),3);
        helper.succeed();
    }
}
