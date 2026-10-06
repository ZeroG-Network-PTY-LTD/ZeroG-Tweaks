package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.genetics.GeneticsIntegration;
import net.zerog.tweaks.genetics.GeneticsTank;

@GameTestHolder("zerog_jelly_machine") @PrefixGameTestTemplate(false)
public final class JellyMachineInteractionGameTests {
    @GameTest(templateNamespace="zerog_jelly_machine",template="equipment_empty",timeoutTicks=260)
    public static void spawned_planet_bee_finds_its_hive_without_assigned_coordinates(GameTestHelper h){
        var pos=new BlockPos(3,2,3);
        h.setBlock(pos,net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.get("moon").hive.get());
        var bee=h.spawn(net.zerog.tweaks.registry.ZGGlowbugs.TYPES.get("moon").get(),new BlockPos(3,2,5));
        var nectar=new net.minecraft.nbt.CompoundTag();nectar.putBoolean("HasNectar",true);
        bee.readAdditionalSaveData(nectar);
        var baby=bee.getBreedOffspring(h.getLevel(),bee);
        h.assertTrue(baby!=null&&baby.getType()==bee.getType(),"Breeding changed the planetary bee family");
        baby.readAdditionalSaveData(nectar);baby.setAge(-24000);
        baby.setPos(h.absolutePos(new BlockPos(4,2,5)).getCenter());h.getLevel().addFreshEntity(baby);
        for(var family:net.zerog.tweaks.registry.ZGPlanetApiary.FAMILIES.values())
            for(var state:family.hive.get().getStateDefinition().getPossibleStates()){
                var poi=net.minecraft.world.entity.ai.village.poi.PoiTypes.forState(state);
                h.assertTrue(poi.isPresent()&&poi.get().is(net.minecraft.tags.PoiTypeTags.BEE_HOME),"Hive state missing bee-home POI: "+family.id);
            }
        h.succeedWhen(()->{
            h.assertTrue(h.absolutePos(pos).equals(bee.getHivePos()),"Spawned bee did not discover its planetary hive");
            h.assertTrue(h.absolutePos(pos).equals(baby.getHivePos()),"Breeding offspring did not discover its planetary hive");
        });
    }
    @GameTest(templateNamespace="zerog_jelly_machine",template="equipment_empty",timeoutTicks=100)
    public static void modern_controller_exposes_its_specific_formation_error(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier3_controller")));
        var be=h.getBlockEntity(pos);
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        player.setPos(be.getBlockPos().getCenter());
        var menu=new net.zerog.tweaks.genetics.AlvearyMenu(19,player.getInventory(),be);
        var status=net.zerog.tweaks.guide.ApiaryMachineAccess.read(menu);
        h.assertTrue(status.isPresent(),"Modern menu excluded from status synchronization");
        h.assertTrue(!status.get().formed()&&!status.get().error().isBlank(),"Incomplete structure has no actionable formation reason");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_jelly_machine",template="equipment_empty",timeoutTicks=100)
    public static void held_item_controller_click_cannot_fall_through_to_legacy_menu(GameTestHelper h){
        var pos=new BlockPos(1,1,1);
        h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier3_controller")));
        var be=h.getBlockEntity(pos);
        h.assertTrue(be!=null,"Controller fixture missing");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.STICK));
        var event=new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,be.getBlockPos(),new BlockHitResult(be.getBlockPos().getCenter(),Direction.NORTH,be.getBlockPos(),false));
        net.zerog.tweaks.genetics.AlvearyInteraction.open(event);
        h.assertTrue(event.isCanceled()&&event.getCancellationResult().consumesAction(),"Held item fell through to the old addon menu");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_jelly_machine",template="equipment_empty",timeoutTicks=100)
    public static void filled_bucket_click_fills_splicer_not_old_menu(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:genetic_splicer")));
        var be=h.getBlockEntity(pos);h.assertTrue(be!=null,"Addon splicer fixture missing");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:royal_jelly_bucket"))));
        var event=new PlayerInteractEvent.RightClickBlock(player,InteractionHand.MAIN_HAND,be.getBlockPos(),new BlockHitResult(be.getBlockPos().getCenter(),Direction.NORTH,be.getBlockPos(),false));
        GeneticsIntegration.open(event);
        h.assertTrue(event.isCanceled()&&new GeneticsTank(be).amount()==1000,"Filled bucket click did not transfer jelly into splicer");
        h.assertTrue(player.getMainHandItem().is(Items.BUCKET),"Survival bucket was not returned");h.succeed();
    }
}
