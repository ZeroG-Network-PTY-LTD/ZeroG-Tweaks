package net.zerog.tweaks.gametest;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ArmorItem;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.item.ZGArmorItem;
import net.zerog.tweaks.item.ZGGeoArmorItem;
import net.zerog.tweaks.registry.ZGArmorMaterials;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class VanillaArmorContractGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void twenty_sets_keep_approved_four_sol_shells_and_sixteen_vanilla_sets(GameTestHelper h) {
        int count=0,shells=0;
        var sol=java.util.Set.of("nullifite","ferrox","moonsteel","olympium");
        for(var entry:ZGArmorMaterials.profiles().entrySet()) {
            for(var type:new ArmorItem.Type[]{ArmorItem.Type.HELMET,ArmorItem.Type.CHESTPLATE,ArmorItem.Type.LEGGINGS,ArmorItem.Type.BOOTS}) {
                String suffix=type==ArmorItem.Type.HELMET?"helmet":type==ArmorItem.Type.CHESTPLATE?"chestplate":type==ArmorItem.Type.LEGGINGS?"leggings":"boots";
                var item=BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",entry.getKey()+"_"+suffix));
                boolean shell=sol.contains(entry.getKey());
                h.assertTrue(item.getClass()==(shell?ZGGeoArmorItem.class:ZGArmorItem.class),"Unexpected geometry class for "+entry.getKey()+"_"+suffix);
                if(shell)shells++;
                var armor=(ArmorItem)item;
                h.assertTrue(armor.getType()==type&&armor.getMaterial().equals(entry.getValue().material()),"Equipment material/type changed");
                count++;
            }
        }
        h.assertTrue(count==80&&shells==16,"Expected four 3D Sol sets and sixteen vanilla-fit sets");h.succeed();
    }
}
