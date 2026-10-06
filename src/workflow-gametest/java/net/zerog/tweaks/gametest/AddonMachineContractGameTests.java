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
    public static void powered_smelter_preserves_recipe_and_blocked_energy(GameTestHelper h){
        try{
            var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:starmetal_smelter")));
            var be=h.getBlockEntity(pos);var inv=GeneticsRuntime.inventory(be);
            inv.setStackInSlot(0,GeneticsRuntime.product("stardust"));inv.setStackInSlot(2,new ItemStack(net.minecraft.world.item.Items.REDSTONE));
            var tick=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class);
            for(int i=0;i<201;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(3).isEmpty(),"Smelter worked without power");
            var power=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),null);power.receiveEnergy(40000,false);
            inv.setStackInSlot(3,GeneticsRuntime.product("starmetal_nugget").copyWithCount(63));
            for(int i=0;i<220;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(power.getEnergyStored()==40000&&inv.getStackInSlot(0).getCount()==1&&inv.getStackInSlot(2).getCount()==1,"Blocked smelter burned power or materials");
            inv.setStackInSlot(3,ItemStack.EMPTY);
            for(int i=0;i<201;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(0).isEmpty()&&inv.getStackInSlot(2).isEmpty()&&GeneticsRuntime.item(inv.getStackInSlot(3),"starmetal_nugget")&&inv.getStackInSlot(3).getCount()==3,"Smelter changed its existing stardust/redstone recipe");
            h.assertTrue(power.getEnergyStored()==40000-201*net.zerog.tweaks.power.PowerConfig.STARMETAL_COST.get(),"Smelter work cost not conserved");h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void genetics_slots_fit_compact_gui_without_overlap(GameTestHelper h){
        var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:genetic_splicer")));
        var player=net.neoforged.neoforge.common.util.FakePlayerFactory.getMinecraft(h.getLevel());var menu=new net.zerog.tweaks.genetics.GeneticsMenu(1,player.getInventory(),h.getBlockEntity(pos));
        for(int i=0;i<menu.slots.size();i++){
            var a=menu.slots.get(i);h.assertTrue(a.x>=0&&a.y>=0&&a.x+16<=256&&a.y+16<=240,"Slot outside compact machine GUI");
            for(int j=i+1;j<menu.slots.size();j++){var b=menu.slots.get(j);h.assertTrue(a.x+16<=b.x||b.x+16<=a.x||a.y+16<=b.y||b.y+16<=a.y,"Genetics slot overlap");}
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void centrifuge_and_smelter_receive_actual_conduit_power(GameTestHelper h) {
        for(String id:java.util.List.of("centrifuge","starmetal_smelter")) {
            var pos=new BlockPos(1,1,1);
            h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));
            var be=h.getBlockEntity(pos);
            var target=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),net.minecraft.core.Direction.EAST);
            h.assertTrue(target!=null&&target.canReceive(),id+" rejects power cable capability");
            int before=target.getEnergyStored();
            h.setBlock(new BlockPos(2,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_energy_conduit")));
            h.setBlock(new BlockPos(3,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:copper_energy_cell")));
            var cable=(net.zerog.tweaks.transport.TransportBlockEntity)h.getBlockEntity(new BlockPos(2,1,1));
            var source=(net.zerog.tweaks.transport.TransportBlockEntity)h.getBlockEntity(new BlockPos(3,1,1));
            source.stored=10000;java.util.Arrays.fill(source.modes,1);
            cable.modes[net.minecraft.core.Direction.EAST.ordinal()]=2;
            cable.modes[net.minecraft.core.Direction.WEST.ordinal()]=1;
            net.zerog.tweaks.transport.TransportBlockEntity.tick(h.getLevel(),cable.getBlockPos(),cable.getBlockState(),cable);
            int received=target.getEnergyStored()-before;
            h.assertTrue(received>0&&source.stored+received==10000,id+" conduit transfer absent or not conserved");
        }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void silk_weaver_does_not_consume_ignored_pattern(GameTestHelper h) {
        try {
            var pos=new BlockPos(1,1,1);
            h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:silk_weaver")));
            var be=h.getBlockEntity(pos);var inv=GeneticsRuntime.inventory(be);
            inv.setStackInSlot(0,GeneticsRuntime.product("silk_thread"));
            inv.setStackInSlot(2,GeneticsRuntime.product("woven_silk").copyWithCount(3));
            var tick=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class);
            for(int i=0;i<201;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(0).isEmpty(),"Weaver failed to process thread");
            h.assertTrue(inv.getStackInSlot(3).getCount()==1&&GeneticsRuntime.item(inv.getStackInSlot(3),"woven_silk"),"Wrong woven output");
            h.assertTrue(inv.getStackInSlot(2).getCount()==3,"Ignored pattern was consumed by generic processing");
            var filter=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("mayPlaceIn",String.class,int.class,ItemStack.class);
            h.assertTrue(!(Boolean)filter.invoke(null,"silk_weaver",2,GeneticsRuntime.product("woven_silk")),"Ignored pattern advertised as operating input");
            h.succeed();
        } catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
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
            h.assertTrue(!inv.getStackInSlot(0).isEmpty()&&(Integer)be.getClass().getMethod("getProgress").invoke(be)==0,"Unpowered centrifuge processed its comb");
            var power=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),null);
            power.receiveEnergy(40000,false);
            for(int i=0;i<201;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(power.getEnergyStored()==40000-201*net.zerog.tweaks.power.PowerConfig.CENTRIFUGE_COST.get(),"Centrifuge work cost not conserved");
            h.assertTrue(inv.getStackInSlot(0).isEmpty(),"Ordinary centrifuge did not consume its comb after its actual 200-tick process");
            for(var product:expected){int count=0;for(int i=1;i<=6;i++)if(ItemStack.isSameItemSameComponents(product,inv.getStackInSlot(i)))count+=inv.getStackInSlot(i).getCount();h.assertTrue(count==product.getCount(),"Ordinary centrifuge dispatched wrong recipe/output: "+product+" actual="+count);}
            h.succeed();
        } catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void powered_centrifuge_preserves_blocked_energy_and_reload(GameTestHelper h){
        try {
            var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:centrifuge")));
            var be=h.getBlockEntity(pos);var inv=GeneticsRuntime.inventory(be);
            inv.setStackInSlot(0,GeneticsRuntime.product("meteor_comb"));
            for(int i=1;i<=6;i++)inv.setStackInSlot(i,new ItemStack(net.minecraft.world.item.Items.BEDROCK,64));
            var power=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),null);power.receiveEnergy(10000,false);
            var tick=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class);
            for(int i=0;i<220;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(power.getEnergyStored()==10000&&!inv.getStackInSlot(0).isEmpty(),"Blocked outputs consumed power/input");
            for(int i=1;i<=6;i++)inv.setStackInSlot(i,ItemStack.EMPTY);
            for(int i=0;i<40;i++)tick.invoke(null,be,h.getLevel());
            int remaining=10000-40*net.zerog.tweaks.power.PowerConfig.CENTRIFUGE_COST.get();
            var saved=be.saveWithFullMetadata(h.getLevel().registryAccess());
            be.loadWithComponents(saved,h.getLevel().registryAccess());
            h.assertTrue(power.getEnergyStored()==remaining&&(Integer)be.getClass().getMethod("getProgress").invoke(be)==40,"Reload lost paid progress or energy");
            for(int i=0;i<161;i++)tick.invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(0).isEmpty()&&power.getEnergyStored()==10000-201*net.zerog.tweaks.power.PowerConfig.CENTRIFUGE_COST.get(),"Reloaded job duplicated work payment");
            h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
}
