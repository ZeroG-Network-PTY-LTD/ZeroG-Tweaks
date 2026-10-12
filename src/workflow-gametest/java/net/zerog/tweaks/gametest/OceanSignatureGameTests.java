package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ZGSpawnRules;
import net.zerog.tweaks.registry.ZGDimensionFluids;
@GameTestHolder("zerog_ocean_signature") @PrefixGameTestTemplate(false)
public final class OceanSignatureGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void regular_tidewraith_has_ocean_habitats_but_boss_does_not(GameTestHelper h){
        for(String id:new String[]{"deep_trenches","kelp_jungles","island_chains"}){
            var biome=h.getLevel().registryAccess().registryOrThrow(Registries.BIOME).get(ResourceLocation.parse("zerog_tweaks:wasteland_"+id));
            var entries=biome.getMobSettings().getMobs(MobCategory.MONSTER).unwrap();
            var regular=entries.stream().filter(e->e.type==EntityInit.TIDEWRAITH.get()).toList();
            h.assertTrue(regular.size()==1&&regular.getFirst().getWeight().asInt()==10&&regular.getFirst().minCount==3&&regular.getFirst().maxCount==4,"Missing3-4 member Tidewraith pack in ocean habitat: "+id);
            h.assertTrue(entries.stream().noneMatch(e->e.type==EntityInit.TIDEWRAITH_BOSS.get()),"Boss accidentally added to natural habitat");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void tidewraith_placement_requires_exposed_water_not_dry_land_or_acid(GameTestHelper h){
        var pos=new BlockPos(4,3,4);var actual=h.absolutePos(pos);
        for(int y=3;y<25;y++)h.setBlock(new BlockPos(4,y,4),net.minecraft.world.level.block.Blocks.AIR);
        h.setBlock(pos.below(),net.minecraft.world.level.block.Blocks.STONE);
        h.assertTrue(!ZGSpawnRules.tidewraithHabitat(h.getLevel(),actual),"Ocean mob accepted dry ground");
        h.setBlock(pos.below(),ZGDimensionFluids.ACID.block.get());
        h.assertTrue(!ZGSpawnRules.tidewraithHabitat(h.getLevel(),actual),"Ocean mob accepted acid as water");
        h.setBlock(pos.below(),net.minecraft.world.level.block.Blocks.WATER);
        h.assertTrue(ZGSpawnRules.tidewraithHabitat(h.getLevel(),actual),"Exposed water habitat rejected");
        var random=net.minecraft.util.RandomSource.create(42);boolean accepted=false;
        for(int i=0;i<64;i++)accepted|=net.minecraft.world.entity.SpawnPlacements.checkSpawnRules(EntityInit.TIDEWRAITH.get(),h.getLevel(),net.minecraft.world.entity.MobSpawnType.NATURAL,actual,random);
        h.assertTrue(accepted,"Natural placement not wired to valid water habitat");
        var nearby=new java.util.ArrayList<net.zerog.tweaks.entity.Tidewraith>();
        for(int i=0;i<net.zerog.tweaks.registry.ZGEcologyConfig.TIDEWRAITH_NEARBY.get();i++){
            var mob=EntityInit.TIDEWRAITH.get().create(h.getLevel());mob.setPos(actual.getCenter().add(i,0,2));mob.setNoAi(true);h.getLevel().addFreshEntity(mob);nearby.add(mob);
            if(i==0)for(int attempt=0;attempt<32;attempt++)h.assertTrue(net.minecraft.world.entity.SpawnPlacements.checkSpawnRules(EntityInit.TIDEWRAITH.get(),h.getLevel(),net.minecraft.world.entity.MobSpawnType.NATURAL,actual,random),"Per-member rarity roll prevents a started pack from filling");
        }
        for(int i=0;i<64;i++)h.assertTrue(!net.minecraft.world.entity.SpawnPlacements.checkSpawnRules(EntityInit.TIDEWRAITH.get(),h.getLevel(),net.minecraft.world.entity.MobSpawnType.NATURAL,actual,random),"Nearby population limit was bypassed");
        nearby.forEach(net.minecraft.world.entity.Entity::discard);
        h.setBlock(pos.above(),net.minecraft.world.level.block.Blocks.STONE);
        h.assertTrue(!ZGSpawnRules.tidewraithHabitat(h.getLevel(),actual),"Covered ocean/cave ceiling accepted");
        h.succeed();
    }
}
