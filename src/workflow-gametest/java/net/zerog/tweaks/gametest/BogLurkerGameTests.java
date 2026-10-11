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
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=140)
    public static void acid_pool_chase_and_idle_surface(GameTestHelper h){
        var level=h.getLevel();
        for(int x=2;x<=15;x++)for(int z=2;z<=6;z++){
            h.setBlock(new BlockPos(x,1,z),net.minecraft.world.level.block.Blocks.STONE);
            h.setBlock(new BlockPos(x,2,z),ZGDimensionFluids.ACID.block.get());
            h.setBlock(new BlockPos(x,3,z),ZGDimensionFluids.ACID.block.get());
            for(int y=4;y<=6;y++)h.setBlock(new BlockPos(x,y,z),net.minecraft.world.level.block.Blocks.AIR);
        }
        var mob=EntityInit.BOG_LURKER.get().create(level);
        mob.setPos(h.absolutePos(new BlockPos(3,3,4)).getCenter());level.addFreshEntity(mob);
        var target=EntityType.COW.create(level);target.setPos(h.absolutePos(new BlockPos(15,4,4)).getCenter());
        target.setNoAi(true);target.setNoGravity(true);target.setInvulnerable(true);level.addFreshEntity(target);
        mob.setTarget(target);double start=mob.getX();
        h.runAfterDelay(60,()->{
            h.assertTrue(mob.getX()>start+.5,"Bog Lurker could not approach a distant target through acid");
            h.assertTrue(mob.getHealth()==28&&!mob.hasEffect(MobEffects.POISON),"Actual acid pool harmed its native mob");
            mob.setTarget(null);target.discard();mob.setNoAi(true);
            mob.setPos(h.absolutePos(new BlockPos(4,3,4)).getCenter());mob.setDeltaMovement(net.minecraft.world.phys.Vec3.ZERO);
        });
        h.runAfterDelay(100,()->{
            double surface=h.absolutePos(new BlockPos(4,4,4)).getY();
            h.assertTrue(Math.abs(mob.getEyeY()-surface)<.35,"Idle bog eyes did not settle at the acid surface");
            h.assertTrue(mob.getHealth()==28,"Idle acid exposure damaged Bog Lurker");
            mob.discard();h.succeed();
        });
    }
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
