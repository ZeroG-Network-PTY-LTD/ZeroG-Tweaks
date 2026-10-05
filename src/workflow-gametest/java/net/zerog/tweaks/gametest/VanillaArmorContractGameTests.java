package net.zerog.tweaks.gametest;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ArmorItem;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.item.ZGArmorItem;
import net.zerog.tweaks.registry.ZGArmorMaterials;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class VanillaArmorContractGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void twenty_sets_keep_vanilla_worn_geometry_and_materials(GameTestHelper h) {
        int count=0;
        for(var entry:ZGArmorMaterials.profiles().entrySet()) {
            for(var type:new ArmorItem.Type[]{ArmorItem.Type.HELMET,ArmorItem.Type.CHESTPLATE,ArmorItem.Type.LEGGINGS,ArmorItem.Type.BOOTS}) {
                String suffix=type==ArmorItem.Type.HELMET?"helmet":type==ArmorItem.Type.CHESTPLATE?"chestplate":type==ArmorItem.Type.LEGGINGS?"leggings":"boots";
                var item=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",entry.getKey()+"_"+suffix));
                h.assertTrue(item.getClass()==ZGArmorItem.class,"Custom geometry renderer still active for "+entry.getKey()+"_"+suffix);
                var armor=(ArmorItem)item;
                h.assertTrue(armor.getType()==type&&armor.getMaterial().equals(entry.getValue().material()),"Equipment material/type changed while removing shells");
                count++;
            }
        }
        h.assertTrue(count==80,"Expected all 20 complete equipment sets");h.succeed();
    }
}
