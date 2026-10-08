package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.genetics.*;
import net.zerog.tweaks.machine.*;

@GameTestHolder("zerog_recipe_legacy") @PrefixGameTestTemplate(false)
public final class LegacyRecipePageGameTests {
    private static BlockEntity machine(GameTestHelper h,String id){
        var pos=new BlockPos(2,2,2);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));
        return h.getBlockEntity(pos);
    }
    private static void tick(BlockEntity be){try{Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class).invoke(null,be,be.getLevel());}catch(ReflectiveOperationException ex){throw new IllegalStateException(ex);}}
    @GameTest(templateNamespace="zerog_recipe_legacy",template="equipment_empty",timeoutTicks=200)
    public static void every_combination_matches_actual_processing_and_card_metrics(GameTestHelper h){
        for(String id:new String[]{"centrifuge","starmetal_smelter"}){
            var base=LegacyRecipeCatalogue.basePages(id);h.assertTrue(!base.isEmpty(),"Missing exact recipe pages for "+id);
            var be=machine(h,id);var inv=GeneticsRuntime.inventory(be);
            for(int tier=0;tier<=6;tier++){
                var cards=LegacyMachineCards.inventory(be);
                cards.setStackInSlot(0,tier==0?ItemStack.EMPTY:new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:acceleration_upgrade_card_t"+tier))));
                cards.setStackInSlot(1,tier==0?ItemStack.EMPTY:new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:energy_coil_upgrade_card_t"+tier))));
                var pages=LegacyRecipeCatalogue.adjusted(be,base,ItemStack.EMPTY);h.assertTrue(pages.size()==base.size(),"Card removed a recipe");
                for(var page:pages){
                    for(int i=0;i<inv.getSlots();i++)inv.setStackInSlot(i,ItemStack.EMPTY);
                    LegacyMachineCards.resetJob(be);GeneticsRuntime.state(be).putInt("energy",100000);
                    var input=page.inputs().getFirst();inv.setStackInSlot(0,input.ingredient().getItems()[0].copyWithCount(input.count()));
                    page.catalyst().ifPresent(c->inv.setStackInSlot(2,c.ingredient().getItems()[0].copyWithCount(c.count())));
                    var before=be.getPersistentData().copy();var filtered=LegacyRecipeCatalogue.adjusted(be,base,page.outputs().getFirst().stack());
                    h.assertTrue(filtered.stream().anyMatch(p->p.id().equals(page.id()))&&before.equals(be.getPersistentData()),"Browsing mutated state or omitted output recipe");
                    for(int step=0;step<page.ticks();step++)tick(be);
                    h.assertTrue(inv.getStackInSlot(0).isEmpty(),"Advertised duration did not complete "+id+" tier "+tier);
                    h.assertTrue(100000-GeneticsRuntime.state(be).getInt("energy")==page.energy(),"Advertised FE differs from actual paid job");
                    for(var out:page.outputs()){
                        int count=0;for(int i=id.equals("centrifuge")?1:3;i<= (id.equals("centrifuge")?6:3);i++)if(ItemStack.isSameItemSameComponents(inv.getStackInSlot(i),out.stack()))count+=inv.getStackInSlot(i).getCount();
                        h.assertTrue(count==out.stack().getCount(),"Advertised output quantity differs from actual processing");
                    }
                    if(id.equals("starmetal_smelter"))h.assertTrue(page.catalyst().orElseThrow().consumed()&&inv.getStackInSlot(2).isEmpty(),"Smelter flux consumption not described");
                }
            }
            h.assertTrue(LegacyRecipeCatalogue.adjusted(be,base,new ItemStack(Items.DIRT)).isEmpty(),"Unknown item advertised as recipe");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_recipe_legacy",template="equipment_empty",timeoutTicks=100)
    public static void weaver_page_preserves_recovery_and_uses_no_power(GameTestHelper h){
        var be=machine(h,"silk_weaver");var pages=LegacyRecipeCatalogue.basePages("silk_weaver");h.assertTrue(pages.size()==1,"Missing Weaver recipe");
        var page=pages.getFirst();var inv=GeneticsRuntime.inventory(be);
        inv.setStackInSlot(0,GeneticsRuntime.product("silk_thread"));inv.setStackInSlot(2,new ItemStack(Items.DIRT));
        h.assertTrue(page.energy()==0&&page.ticks()==200&&page.catalyst().isEmpty()&&!LegacyMachineCards.supports(be),"Invented Weaver power, catalyst or upgrades");
        for(int i=0;i<200;i++)tick(be);
        h.assertTrue(inv.getStackInSlot(0).isEmpty()&&GeneticsRuntime.item(inv.getStackInSlot(3),"woven_silk")&&inv.getStackInSlot(3).getCount()==1&&inv.getStackInSlot(2).is(Items.DIRT),"Weaver page differs from actual recipe/recovery contract");h.succeed();
    }
}
