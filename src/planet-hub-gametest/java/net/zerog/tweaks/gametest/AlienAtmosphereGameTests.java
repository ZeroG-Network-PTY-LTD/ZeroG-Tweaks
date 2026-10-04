package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CaveVines;
import net.minecraft.world.level.block.VineBlock;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.entity.PlanetVillager;
import net.zerog.tweaks.registry.*;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class AlienAtmosphereGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void alien_vines_support_fruit_and_safe_vents(GameTestHelper helper) {
        var level=helper.getLevel();var pos=helper.absolutePos(new BlockPos(1,130,1));
        helper.assertTrue(ZGAlienVines.VINES.size()==24 && ZGAlienVines.FRUITS.size()==6,"Incomplete vine families");
        for(var entry:ZGAlienVines.VINES.entrySet()) {
            level.setBlock(pos,Blocks.AIR.defaultBlockState(),3);
            level.setBlock(pos.north(),Blocks.STONE.defaultBlockState(),3);
            var block=entry.getValue().get();var state=block.defaultBlockState().setValue(VineBlock.NORTH,true);
            level.setBlock(pos,state,3);
            helper.assertTrue(state.canSurvive(level,pos),"Native wall support failed "+entry.getKey());
            helper.assertTrue(state.is(net.minecraft.tags.BlockTags.CLIMBABLE),"Vine is not climbable "+entry.getKey());
            if(entry.getKey().endsWith("fruit_ivy")) {
                block.performBonemeal(level,net.minecraft.util.RandomSource.create(3),pos,state);
                helper.assertTrue(level.getBlockState(pos).getValue(CaveVines.BERRIES),"Fruit failed to ripen");
                helper.assertTrue(level.getBlockState(pos).getLightEmission(level,pos)==7,"Fruit does not glow");
            }
        }
        for(var fruit:ZGAlienVines.FRUITS.values())helper.assertTrue(new ItemStack(fruit.get()).get(DataComponents.FOOD)!=null,"Vine fruit not edible");
        for(var vent:ZGGasVents.AMBIENT_VENTS.values())helper.assertTrue(!vent.get().defaultBlockState().isRandomlyTicking(),"Ambient vent has gameplay hazard ticks");
        helper.assertTrue(ItemInit.WEATHER_TESTER.get().getDefaultMaxStackSize()==1,"Weather tester stacks incorrectly");
        helper.succeed();
    }

    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void migrate_planet_residents_preserving_trades(GameTestHelper helper) {
        var overworld=helper.getLevel();
        var mars=overworld.getServer().getLevel(ResourceKey.create(Registries.DIMENSION,
                ResourceLocation.fromNamespaceAndPath("zerog_tweaks","mars")));
        helper.assertTrue(mars!=null,"Missing Mars");
        // Remote dimension chunks are not entity-ticking just because getChunk
        // generated them. Pin a disposable fixture chunk, far from hub landings.
        boolean alreadyForced=mars.getForcedChunks().contains(net.minecraft.world.level.ChunkPos.asLong(300,300));
        mars.setChunkForced(300,300,true);mars.getChunk(300,300);
        var resident=EntityType.VILLAGER.create(mars);
        resident.moveTo(4808,210,4808,0,0);resident.setNoGravity(true);resident.setNoAi(true);resident.setPersistenceRequired();
        resident.setCustomName(Component.literal("ZeroG migration check"));
        resident.setVillagerData(resident.getVillagerData().setProfession(VillagerProfession.FARMER).setLevel(3));
        resident.getInventory().addItem(new ItemStack(Items.WHEAT,7));
        resident.getOffers();var before=resident.saveWithoutId(new CompoundTag());var oldUUID=resident.getUUID();
        helper.assertTrue(mars.addFreshEntity(resident),"Could not add migration fixture");
        var vanilla=EntityType.VILLAGER.create(overworld);vanilla.moveTo(helper.absolutePos(new BlockPos(2,130,2)),0,0);
        vanilla.setNoGravity(true);overworld.addFreshEntity(vanilla);
        // Wait for the assertion, not a guessed number of world ticks: the new
        // chunk may spend its first ticks awaiting full entity-ticking status.
        helper.succeedWhen(()->{
            var replacements=mars.getEntitiesOfClass(PlanetVillager.class,new net.minecraft.world.phys.AABB(4804,205,4804,4812,215,4812),
                    entity->Component.literal("ZeroG migration check").equals(entity.getCustomName()));
            helper.assertTrue(replacements.size()==1 && mars.getEntity(oldUUID)==null,
                    "Resident migration missing/duplicated: count="+replacements.size()+", source ticks="+resident.tickCount+", removed="+resident.isRemoved());
            var replacement=replacements.getFirst();var after=replacement.saveWithoutId(new CompoundTag());
            helper.assertTrue(replacement.getType()==ZGPlanetVillagers.TYPES.get("rustborn").get(),"Wrong planetary species");
            helper.assertTrue(before.getCompound("Offers").equals(after.getCompound("Offers")),"Migration lost trades");
            helper.assertTrue(replacement.getInventory().countItem(Items.WHEAT)==7,"Migration lost inventory");
            helper.assertTrue(vanilla.getType()==EntityType.VILLAGER && !vanilla.isRemoved(),"Overworld villagers changed");
            replacement.discard();vanilla.discard();
            if(!alreadyForced)mars.setChunkForced(300,300,false);
        });
    }
}
