package net.zerog.tweaks.gametest;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.*;
@GameTestHolder("zerog_bog_habitat") @PrefixGameTestTemplate(false)
public final class BogHabitatGameTests {
    @GameTest(templateNamespace="zerog_bog_habitat",template="equipment_empty",timeoutTicks=180)
    public static void submerged_spawn_and_idle_pool_seeking_are_real_gameplay(GameTestHelper h){
        var level=h.getLevel();level.setDayTime(18000); // Full night, not still-bright twilight.
        for(int x=1;x<=10;x++)for(int z=1;z<=8;z++){
            h.setBlock(new BlockPos(x,1,z),Blocks.STONE);
            for(int y=2;y<=8;y++)h.setBlock(new BlockPos(x,y,z),Blocks.AIR);
            if(x>=6&&z>=2&&z<=7)h.setBlock(new BlockPos(x,2,z),ZGDimensionFluids.ACID.block.get());
        }
        var wet=EntityInit.BOG_LURKER.get().create(level);var wetPos=h.absolutePos(new BlockPos(8,2,4));wet.setPos(wetPos.getX()+.5,wetPos.getY()+.1,wetPos.getZ()+.5);
        h.assertTrue(wet.checkSpawnObstruction(level),"Native acid mob cannot spawn immersed in its acid habitat");
        // Only trial spawners ignore vanilla light requirements; ordinary spawners do not.
        h.assertTrue(SpawnPlacements.checkSpawnRules(EntityInit.BOG_LURKER.get(),level,MobSpawnType.TRIAL_SPAWNER,wetPos,net.minecraft.util.RandomSource.create(42)),"Registered Bog placement still rejects acid");
        h.setBlock(new BlockPos(8,2,4),Blocks.WATER);h.assertTrue(!wet.checkSpawnObstruction(level),"Bog acid exception wrongly allows normal water spawning");h.setBlock(new BlockPos(8,2,4),ZGDimensionFluids.ACID.block.get());
        var dry=EntityInit.BOG_LURKER.get().create(level);dry.setPos(h.absolutePos(new BlockPos(3,2,4)).getCenter());level.addFreshEntity(dry);
        h.runAfterDelay(120,()->{
            h.assertTrue(dry.isInFluidType(ZGDimensionFluids.ACID.type.get()),"Idle pool search failed: relative="+dry.position().subtract(h.absolutePos(new BlockPos(3,2,4)).getCenter())+", centreAcid="+(level.getFluidState(dry.blockPosition()).getFluidType()==ZGDimensionFluids.ACID.type.get()));
            h.assertTrue(dry.getHealth()==28&&!dry.hasEffect(net.minecraft.world.effect.MobEffects.POISON),"Seeking its habitat harmed the lurker");
            double surface=h.absolutePos(new BlockPos(6,3,4)).getY();h.assertTrue(Math.abs(dry.getEyeY()-surface)<.35,"AI surface error: eyeDelta="+(dry.getEyeY()-surface)+", centreAcid="+(level.getFluidState(dry.blockPosition()).getFluidType()==ZGDimensionFluids.ACID.type.get())+", velocity="+dry.getDeltaMovement());
            h.assertTrue(SpawnPlacements.checkSpawnRules(EntityInit.BOG_LURKER.get(),level,MobSpawnType.NATURAL,wetPos,net.minecraft.util.RandomSource.create(42)),"Acid placement rejected: time="+level.getDayTime()+", light="+level.getMaxLocalRawBrightness(wetPos)+", fluid="+level.getFluidState(wetPos));
            level.setDayTime(6000);
        });
        h.runAfterDelay(130,()->{
            h.assertTrue(!SpawnPlacements.checkSpawnRules(EntityInit.BOG_LURKER.get(),level,MobSpawnType.NATURAL,wetPos,net.minecraft.util.RandomSource.create(42)),"Exposed daylight acid spawned a hostile ambush mob");
            dry.discard();h.succeed();
        });
    }
}
