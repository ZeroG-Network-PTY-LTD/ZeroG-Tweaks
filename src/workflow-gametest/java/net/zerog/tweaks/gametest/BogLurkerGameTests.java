package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.effect.*;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_bog_lurker") @PrefixGameTestTemplate(false)
public final class BogLurkerGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=120)
    public static void spit_expires_without_leaving_a_hazard(GameTestHelper h){
        var spit=EntityInit.BOG_ACID_SPIT.get().create(h.getLevel());
        spit.setPos(h.absolutePos(new BlockPos(4,3,4)).getCenter());
        spit.setNoGravity(true);
        h.getLevel().addFreshEntity(spit);
        h.runAfterDelay(105,()->{
            h.assertTrue(spit.isRemoved(),"Uncollided acid spit remained as a permanent hazard");
            h.succeed();
        });
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=120)
    public static void collision_spit_and_immunities(GameTestHelper h){
        var level=h.getLevel();var mob=EntityInit.BOG_LURKER.get().create(level);
        mob.setPos(h.absolutePos(new BlockPos(4,3,4)).getCenter());mob.setNoAi(true);mob.setNoGravity(true);level.addFreshEntity(mob);
        h.assertTrue(mob.getMaxHealth()==28&&!mob.addEffect(new MobEffectInstance(MobEffects.POISON,80,1)),"Bog stats/poison immunity mismatch");
        var acid=ResourceKey.create(Registries.DAMAGE_TYPE,ResourceLocation.parse("zerog_tweaks:acid"));
        h.assertTrue(!mob.hurt(new DamageSource(level.registryAccess().registryOrThrow(Registries.DAMAGE_TYPE).getHolderOrThrow(acid)),5),"Bog acid immunity failed");
        var target=EntityType.COW.create(level);target.setPos(mob.position().add(3,0,0));target.setNoAi(true);target.setNoGravity(true);level.addFreshEntity(target);
        mob.performRangedAttack(target,1);
        h.assertTrue(level.getEntitiesOfClass(net.zerog.tweaks.entity.BogAcidSpit.class,mob.getBoundingBox().inflate(10)).size()==1,"Ranged attack did not create a projectile");
        h.runAfterDelay(20,()->{
            h.assertTrue(target.getHealth()<target.getMaxHealth()&&target.hasEffect(MobEffects.POISON)&&target.getEffect(MobEffects.POISON).getAmplifier()==1,"Moving projectile did not collide and apply Poison II");
            mob.discard();target.discard();h.succeed();
        });
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void habitat_egg_and_far_target(GameTestHelper h){
        var level=h.getLevel();var mob=EntityInit.BOG_LURKER.get().create(level);mob.setPos(h.absolutePos(new BlockPos(4,3,4)).getCenter());
        var egg=(ZGSpawnEggItem)net.minecraft.core.registries.BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:bog_lurker_spawn_egg"));
        h.assertTrue(egg.entityType()==mob.getType(),"Bog egg unresolved");
        for(String name:new String[]{"acid_swamps","mud_flats","moss_bogs"}){
            var biome=level.registryAccess().registryOrThrow(Registries.BIOME).get(ResourceLocation.parse("zerog_tweaks:wasteland_"+name));
            var entries=biome.getMobSettings().getMobs(MobCategory.MONSTER).unwrap().stream().filter(s->s.type==mob.getType()).toList();
            h.assertTrue(entries.size()==1&&entries.getFirst().getWeight().asInt()==50&&entries.getFirst().maxCount==2,"Wrong toxic habitat list");
        }
        var target=EntityType.COW.create(level);target.setPos(mob.position().add(15,0,0));mob.performRangedAttack(target,1);
        h.assertTrue(level.getEntitiesOfClass(net.zerog.tweaks.entity.BogAcidSpit.class,new AABB(mob.blockPosition()).inflate(20)).isEmpty(),"Far target received acid spit");h.succeed();
    }
}
