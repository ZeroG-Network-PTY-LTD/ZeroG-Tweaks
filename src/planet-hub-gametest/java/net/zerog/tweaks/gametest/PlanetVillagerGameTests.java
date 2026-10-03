package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.item.SpawnEggItem;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.registry.ZGPlanetVillagers;
import net.zerog.tweaks.travel.GateLedger;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class PlanetVillagerGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=200)
    public static void planetary_species_preserve_villagers_and_saved_styles(GameTestHelper helper){
        var level=helper.getLevel();
        helper.assertTrue(ZGPlanetVillagers.TYPES.size()==6,"Missing planetary species");
        for(var entry:ZGPlanetVillagers.TYPES.entrySet()){
            var type=entry.getValue().get();var mob=type.create(level);
            helper.assertTrue(mob!=null && mob.getBrain()!=null,"Missing villager brain "+entry.getKey());
            mob.setStyle(2);mob.setVillagerData(mob.getVillagerData().setProfession(VillagerProfession.FARMER).setLevel(2));
            helper.assertTrue(!mob.getOffers().isEmpty(),"Native farmer trades unavailable "+entry.getKey());
            var tag=new CompoundTag();mob.saveWithoutId(tag);
            var restored=type.create(level);restored.load(tag);
            helper.assertTrue(restored.style()==2 && restored.getVillagerData().getProfession()==VillagerProfession.FARMER,
                    "Style/profession lost during save "+entry.getKey());
            var child=mob.getBreedOffspring(level,mob);
            helper.assertTrue(child!=null && child.getType()==type,"Breeding replaced planetary species "+entry.getKey());
            var egg=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",entry.getKey()+"_spawn_egg"));
            helper.assertTrue(egg instanceof SpawnEggItem && SpawnEggItem.byId(type)==egg,"Wrong spawn egg type "+entry.getKey());
            helper.assertTrue(EntityType.VILLAGER.create(level).getType()==EntityType.VILLAGER,"Vanilla villager replaced");
        }
        var old=new CompoundTag();old.putBoolean("hubBuilt",true);old.putInt("prepared",34);
        var ledger=GateLedger.load(old,level.registryAccess());
        helper.assertTrue(!ledger.inspectionEnabled,"Older hub would be retroactively edited");
        ledger.inspectionEnabled=true;ledger.inspectionPrepared=1;
        ledger.inspectionVillages.put("zerog_tweaks:moon",new java.util.ArrayList<>(java.util.List.of(new BlockPos(120,64,80))));
        var copy=GateLedger.load(ledger.save(new CompoundTag(),level.registryAccess()),level.registryAccess());
        helper.assertTrue(copy.inspectionEnabled && copy.inspectionPrepared==1 && copy.inspectionVillages.equals(ledger.inspectionVillages),
                "Inspection persistence would rebuild villages");
        helper.succeed();
    }
}
