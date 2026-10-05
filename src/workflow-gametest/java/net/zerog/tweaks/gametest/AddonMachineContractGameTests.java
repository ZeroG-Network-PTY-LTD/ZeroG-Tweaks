package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.genetics.GeneticsRuntime;

/** Exercises the installed addon dispatch, not a replacement recipe invented by the test. */
@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class AddonMachineContractGameTests {
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void unused_machine_input_slots_are_not_misleading_inputs(GameTestHelper h) {
        try {
            var filter=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("mayPlaceIn",String.class,int.class,ItemStack.class);
            h.assertTrue(!(Boolean)filter.invoke(null,"starmetal_smelter",1,new ItemStack(net.minecraft.world.item.Items.IRON_INGOT)),"Starmetal slot1 accepts alloy input but installed recipe reads only slots0/2");
            h.assertTrue(!(Boolean)filter.invoke(null,"silk_weaver",1,GeneticsRuntime.product("silk_thread")),"Silk slot1 accepts fiber but installed recipe reads only slot0");
            h.assertTrue(!(Boolean)filter.invoke(null,"frame_infusion_altar",2,new ItemStack(net.minecraft.world.item.Items.AMETHYST_SHARD)),"Frame infusion slot2 accepts reagent but installed recipe reads only slots0/1");
            for(var id:java.util.List.of("starmetal_smelter","silk_weaver","frame_infusion_altar")){
                var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));
                var be=h.getBlockEntity(pos);int unused=id.equals("frame_infusion_altar")?2:1;
                var handler=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.ItemHandler.BLOCK,be.getBlockPos(),null);
                h.assertTrue(handler!=null&&!handler.isItemValid(unused,new ItemStack(net.minecraft.world.item.Items.IRON_INGOT)),"Pipes bypass unused-input filter: "+id);
                h.assertTrue(handler.insertItem(unused,new ItemStack(net.minecraft.world.item.Items.IRON_INGOT),false).getCount()==1,"Automation swallowed rejected input");
                GeneticsRuntime.inventory(be).setStackInSlot(unused,new ItemStack(net.minecraft.world.item.Items.DIAMOND,3));
                h.assertTrue(handler.extractItem(unused,3,false).getCount()==3,"Legacy recovery lost old inputs");
            }
            h.succeed();
        } catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void ordinary_centrifuge_dispatches_actual_comb_products(GameTestHelper h) {
        try {
            var pos=new BlockPos(1,1,1);
            h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:centrifuge")));
            var be=h.getBlockEntity(pos);
            h.assertTrue(be!=null&&GeneticsRuntime.id(be).equals("centrifuge"),"Installed ordinary centrifuge block/entity missing");
            var comb=GeneticsRuntime.product("meteor_comb");
            h.assertTrue(!comb.isEmpty(),"Installed meteor comb missing");
            var productsMethod=Class.forName("com.zerog.aeroapiary.ZeroGSlotFamilies").getDeclaredMethod("centrifugeProducts",ItemStack.class);
            productsMethod.setAccessible(true);
            @SuppressWarnings("unchecked") var expected=(java.util.List<ItemStack>)productsMethod.invoke(null,comb.copy());
            h.assertTrue(!expected.isEmpty(),"Installed comb has no authoritative centrifuge products");
            var inv=GeneticsRuntime.inventory(be);inv.setStackInSlot(0,comb.copy());
            var tick=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class);
            for(int i=0;i<201;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(0).isEmpty(),"Ordinary centrifuge did not consume its comb after its actual 200-tick process");
            for(var product:expected){int count=0;for(int i=1;i<=6;i++)if(ItemStack.isSameItemSameComponents(product,inv.getStackInSlot(i)))count+=inv.getStackInSlot(i).getCount();h.assertTrue(count==product.getCount(),"Ordinary centrifuge dispatched wrong recipe/output: "+product+" actual="+count);}
            h.succeed();
        } catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
}
