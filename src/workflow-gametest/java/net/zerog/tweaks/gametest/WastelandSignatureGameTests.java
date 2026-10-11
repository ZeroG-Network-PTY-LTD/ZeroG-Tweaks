package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_wasteland_signatures")
@PrefixGameTestTemplate(false)
public final class WastelandSignatureGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void ash_mount_food_lava_and_reload(GameTestHelper h){
        var level=h.getLevel();var mob=EntityInit.ASH_STRIDER.get().create(level);
        mob.setPos(h.absolutePos(new BlockPos(4,3,4)).getCenter());level.addFreshEntity(mob);
        h.assertTrue(mob.fireImmune()&&mob.canStandOnFluid(net.minecraft.world.level.material.Fluids.LAVA.defaultFluidState()),"Ash mount lost lava/fire immunity");
        h.assertTrue(mob.getMaxHealth()==30&&mob.getAttributeValue(Attributes.ATTACK_DAMAGE)==6,"Ash mount stats differ from approved design");
        h.assertTrue(mob.isFood(new ItemStack(ItemInit.CINDER_CAP_ITEM.get()))&&!mob.isFood(new ItemStack(net.minecraft.world.item.Items.WARPED_FUNGUS)),"Incorrect breeding food");
        h.assertTrue(mob.getBreedOffspring(level,mob).getType()==mob.getType(),"Breeding creates a vanilla Strider");
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.CREATIVE);
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(net.minecraft.world.item.Items.SADDLE));
        mob.mobInteract(player,net.minecraft.world.InteractionHand.MAIN_HAND);
        h.assertTrue(mob.isSaddled(),"Real saddle interaction failed");
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,ItemStack.EMPTY);
        mob.mobInteract(player,net.minecraft.world.InteractionHand.MAIN_HAND);
        h.assertTrue(player.getVehicle()==mob,"Saddled mount did not accept player");player.stopRiding();
        var tag=new net.minecraft.nbt.CompoundTag();mob.saveWithoutId(tag);
        var restored=EntityInit.ASH_STRIDER.get().create(level);restored.load(tag);
        h.assertTrue(restored.isSaddled()&&restored.getTarget()==null,"Reload lost saddle or introduced aggression");
        mob.discard();h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void actual_eggs_attributes_and_frozen_bite(GameTestHelper h){
        var level=h.getLevel();var floor=h.absolutePos(new BlockPos(3,1,3));level.setBlock(floor,Blocks.STONE.defaultBlockState(),3);
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.CREATIVE);
        var egg=(ZGSpawnEggItem)BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:rime_stalker_spawn_egg"));
        h.assertTrue(egg.entityType()==EntityInit.RIME_STALKER.get(),"Existing frozen egg did not resolve registered entity");
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(egg));
        egg.useOn(new UseOnContext(player,net.minecraft.world.InteractionHand.MAIN_HAND,new BlockHitResult(Vec3.atCenterOf(floor),net.minecraft.core.Direction.UP,floor,false)));
        var stalkers=level.getEntitiesOfClass(net.zerog.tweaks.entity.RimeStalker.class,new AABB(floor).inflate(3));
        h.assertTrue(stalkers.size()==1,"Real spawn egg did not create Rime Stalker");var mob=stalkers.getFirst();
        h.assertTrue(mob.getMaxHealth()==24&&mob.getAttributeValue(Attributes.ATTACK_DAMAGE)==5&&!mob.canFreeze(),"Frozen predator differs from approved stats/immunity");
        var target=EntityType.ZOMBIE.create(level);target.setPos(mob.position().add(0,0,1));target.setTicksFrozen(0);level.addFreshEntity(target);
        h.assertTrue(mob.doHurtTarget(target)&&target.getTicksFrozen()==100,"Successful bite did not add exactly100 frozen ticks");
        target.discard();mob.discard();h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void drifter_neutral_floating_fragment_and_reload(GameTestHelper h){
        var level=h.getLevel();var mob=EntityInit.CRATER_DRIFTER.get().create(level);mob.setPos(h.absolutePos(new BlockPos(6,3,6)).getCenter());level.addFreshEntity(mob);
        h.assertTrue(mob.isNoGravity()&&mob.getTarget()==null&&mob.getMaxHealth()==20&&mob.getAttributeValue(Attributes.ATTACK_DAMAGE)==4,"Drifter is not neutral/weightless with approved stats");
        var egg=(ZGSpawnEggItem)BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:crater_drifter_spawn_egg"));h.assertTrue(egg.entityType()==mob.getType(),"Existing barren egg unresolved");
        var tag=new net.minecraft.nbt.CompoundTag();mob.saveWithoutId(tag);tag.putInt("FragmentTicks",1);
        mob.load(tag);mob.aiStep();var after=new net.minecraft.nbt.CompoundTag();mob.saveWithoutId(after);
        var drops=level.getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,mob.getBoundingBox().inflate(2));
        h.assertTrue(drops.size()==1&&drops.getFirst().getItem().is(ItemInit.METEORITE_FRAGMENT_ITEM.get())&&drops.getFirst().getItem().getCount()==1,"Timed fragment drop missing/duplicated");
        h.assertTrue(after.getInt("FragmentTicks")==6000,"Fragment cooldown did not reset to approved6000ticks");
        var restored=EntityInit.CRATER_DRIFTER.get().create(level);restored.load(after);var restoredTag=new net.minecraft.nbt.CompoundTag();restored.saveWithoutId(restoredTag);
        h.assertTrue(restored.isNoGravity()&&restoredTag.getInt("FragmentTicks")==6000,"Reload lost gravity/cooldown");
        mob.discard();drops.forEach(Entity::discard);h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void loaded_habitat_lists_are_precise(GameTestHelper h){
        var biomes=h.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        String[] frozen={"wasteland_glaciers","wasteland_ice_spike_forest","wasteland_frozen_canyons"};
        String[] barren={"wasteland_cratered_plains","wasteland_dust_badlands","wasteland_canyon_scars"};
        String[] volcanic={"wasteland_basalt_fields","wasteland_ash_plains","wasteland_lava_lakes"};
        for(String name:volcanic)assertEntry(h,biomes.get(ResourceLocation.parse("zerog_tweaks:"+name)),EntityInit.ASH_STRIDER.get(),50,1,3);
        for(String name:frozen)assertEntry(h,biomes.get(ResourceLocation.parse("zerog_tweaks:"+name)),EntityInit.RIME_STALKER.get(),50,1,2);
        for(String name:barren)assertEntry(h,biomes.get(ResourceLocation.parse("zerog_tweaks:"+name)),EntityInit.CRATER_DRIFTER.get(),50,1,3);
        for(var biome:biomes){for(var category:MobCategory.values())for(var entry:biome.getMobSettings().getMobs(category).unwrap()){
            if(entry.type==EntityInit.RIME_STALKER.get())h.assertTrue(java.util.Arrays.asList(frozen).contains(biomes.getKey(biome).getPath()),"Rime Stalker in wrong habitat");
            if(entry.type==EntityInit.CRATER_DRIFTER.get())h.assertTrue(java.util.Arrays.asList(barren).contains(biomes.getKey(biome).getPath()),"Crater Drifter in wrong habitat");
            if(entry.type==EntityInit.ASH_STRIDER.get())h.assertTrue(java.util.Arrays.asList(volcanic).contains(biomes.getKey(biome).getPath()),"Ash Strider in wrong habitat");
        }}h.succeed();
    }
    private static void assertEntry(GameTestHelper h,net.minecraft.world.level.biome.Biome biome,EntityType<?> type,int weight,int min,int max){
        h.assertTrue(biome!=null,"Required habitat missing");var entries=biome.getMobSettings().getMobs(type.getCategory()).unwrap().stream().filter(e->e.type==type).toList();
        h.assertTrue(entries.size()==1&&entries.getFirst().getWeight().asInt()==weight&&entries.getFirst().minCount==min&&entries.getFirst().maxCount==max,"Habitat spawn contract wrong for "+type);
    }
}
