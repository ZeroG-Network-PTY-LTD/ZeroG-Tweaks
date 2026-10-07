package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.storage.loot.*;
import net.minecraft.world.level.storage.loot.parameters.*;
import net.neoforged.neoforge.gametest.*;

@GameTestHolder("zerog_galaxy_access") @PrefixGameTestTemplate(false)
public final class VaultTemplateSourceGameTests {
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=200)
    public static void vault_uncommon_chests_roll_three_ladder_templates(GameTestHelper h){
        var level=h.getLevel();String loot="zerog_tweaks:chests/concord_vault/uncommon";
        var table=level.getServer().reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE,ResourceLocation.parse(loot)));
        h.assertTrue(table!=LootTable.EMPTY,"Vault source is missing from loaded loot registry");
        for(String room:new String[]{"forge","star_library"}){
            var template=level.getStructureManager().get(ResourceLocation.parse("zerog_tweaks:concord_vault/rooms/"+room)).orElseThrow();
            var chests=template.filterBlocks(BlockPos.ZERO,new StructurePlaceSettings(),Blocks.CHEST);
            h.assertTrue(chests.stream().anyMatch(c->c.nbt()!=null&&loot.equals(c.nbt().getString("LootTable"))),"Vault room no longer binds uncommon loot: "+room);
        }
        var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,h.absolutePos(BlockPos.ZERO).getCenter()).create(LootContextParamSets.CHEST);
        var seen=new java.util.HashSet<String>();
        for(long seed=1;seed<=2048;seed++)for(var stack:table.getRandomItems(params,seed)){
            String id=BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
            if(id.endsWith("_upgrade_smithing_template")){
                h.assertTrue(stack.getCount()==1,"Progression fallback changed template quantities");seen.add(id);
            }
        }
        for(String metal:new String[]{"cobaltium","cyrrium","aurelion"})
            h.assertTrue(seen.contains("zerog_tweaks:"+metal+"_upgrade_smithing_template"),"Loaded chest never rolled "+metal);
        h.succeed();
    }
}
