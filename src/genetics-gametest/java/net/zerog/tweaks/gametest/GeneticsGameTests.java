package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Bee;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.genetics.*;

@GameTestHolder("zerog_genetics")
@PrefixGameTestTemplate(false)
public final class GeneticsGameTests {
    private static final String PB="cy.jdkdigital.productivebees.";
    private static ItemStack bee(GameTestHelper h) {
        try {
            var type=BuiltInRegistries.ENTITY_TYPE.get(ResourceLocation.parse("productivebees:configurable_bee"));
            var bee=(Bee)type.create(h.getLevel());
            Class<?> attr=Class.forName(PB+"util.GeneAttribute"),value=Class.forName(PB+"util.GeneValue");
            var set=bee.getClass().getMethod("setAttributeValue",attr,value);
            String[] values={"PRODUCTIVITY_HIGH","ENDURANCE_STRONG","TEMPER_PASSIVE","BEHAVIOR_DIURNAL","WEATHER_TOLERANCE_ANY"};
            for(int i=0;i<5;i++)set.invoke(bee,attr.getField(ProductiveBeeGenes.GENES[i].toUpperCase(java.util.Locale.ROOT)).get(null),value.getField(values[i]).get(null));
            var cage=new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("productivebees:bee_cage")));
            Class.forName(PB+"common.item.BeeCage").getMethod("captureEntity",Bee.class,ItemStack.class).invoke(null,bee,cage);
            h.assertTrue(ProductiveBeeGenes.read(cage).size()==5,"Captured cage lost real PB traits");return cage;
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    private static BlockEntity machine(GameTestHelper h,String id) {
        h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("aeroapiary",id)));
        BlockEntity be=h.getBlockEntity(new BlockPos(1,1,1));h.assertTrue(be!=null,"Missing machine BE");return be;
    }
    private static void inputs(BlockEntity be,ItemStack bee,ItemStack second,ItemStack catalyst){var inv=GeneticsRuntime.inventory(be);inv.setStackInSlot(0,bee);inv.setStackInSlot(1,second);inv.setStackInSlot(2,catalyst);}
    private static void start(BlockEntity be,int mode,int gene){var state=GeneticsRuntime.state(be);state.putInt("mode",mode);state.putInt("gene",gene);state.putBoolean("requested",true);state.putInt("progress",0);}
    private static void tick(BlockEntity be,int count){for(int i=0;i<count;i++)GeneticsRuntime.tick(be);}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void analysis_sampling_and_pb_attachment_splicing(GameTestHelper h) {
        var be=machine(h,"geno_station");var specimen=bee(h);var traits=ProductiveBeeGenes.read(specimen);
        inputs(be,specimen,GeneticsRuntime.product("serum_vial"),new ItemStack(Items.HONEY_BOTTLE));
        start(be,1,0);GeneticsRuntime.energy(be).receiveEnergy(10000,false);tick(be,300);
        var inv=GeneticsRuntime.inventory(be);var serum=inv.getStackInSlot(4).copy();var returned=inv.getStackInSlot(3).copy();
        h.assertTrue(traits.equals(ProductiveBeeGenes.read(returned)),"Sampling changed traits");
        h.assertTrue(!GeneticsRuntime.serum(serum).isEmpty(),"No sampled serum");
        h.assertTrue(inv.getStackInSlot(5).is(Items.GLASS_BOTTLE),"Sampling deleted honey bottle container");
        h.assertTrue(GeneticsRuntime.energy(be).getEnergyStored()==4000,"Sampling FE cost wrong");
        var altered=ProductiveBeeGenes.splice(returned,"productivity","productivity.normal");
        h.assertTrue(!altered.isEmpty(),"Valid trait splice refused");
        be=machine(h,"genetic_splicer");inputs(be,altered,serum,GeneticsRuntime.product("cosmic_jelly"));
        start(be,0,0);GeneticsRuntime.energy(be).receiveEnergy(40000,false);tick(be,400);inv=GeneticsRuntime.inventory(be);
        h.assertTrue(ProductiveBeeGenes.read(inv.getStackInSlot(3)).equals(traits),"Spliced trait does not match PB data");
        h.assertTrue(GeneticsRuntime.item(inv.getStackInSlot(4),"serum_vial"),"Splicing did not return vial");
        h.assertTrue(inv.getStackInSlot(1).isEmpty()&&inv.getStackInSlot(2).isEmpty(),"Splicing failed to consume serum/catalyst");
        h.assertTrue(GeneticsRuntime.energy(be).getEnergyStored()==16000,"Splice FE cost wrong");
        h.assertTrue(!ProductiveBeeGenes.valid("type","productivity.high"),"Species mutation accepted");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void output_backpressure_input_replacement_and_unpowered_analysis(GameTestHelper h) {
        var be=machine(h,"geno_station");var inv=GeneticsRuntime.inventory(be);var specimen=bee(h);
        inputs(be,specimen,ItemStack.EMPTY,new ItemStack(Items.HONEY_BOTTLE));inv.setStackInSlot(3,new ItemStack(Items.STONE,64));
        start(be,0,0);GeneticsRuntime.energy(be).receiveEnergy(10000,false);tick(be,150);
        h.assertTrue(GeneticsRuntime.energy(be).getEnergyStored()==10000&&inv.getStackInSlot(0).getCount()==1,"Blocked output consumed resources");
        inv.setStackInSlot(3,ItemStack.EMPTY);tick(be,50);
        inv.setStackInSlot(0,ProductiveBeeGenes.splice(specimen,"productivity","productivity.normal"));tick(be,1);
        h.assertTrue(!GeneticsRuntime.state(be).getBoolean("requested")&&inv.getStackInSlot(3).isEmpty(),"Input swap didn't invalidate job");
        GeneticsRuntime.state(be).putInt("energy",0);start(be,0,0);tick(be,399);
        h.assertTrue(inv.getStackInSlot(3).isEmpty(),"Hand-cranked job completed early");tick(be,1);
        h.assertTrue(!inv.getStackInSlot(3).isEmpty()&&inv.getStackInSlot(4).is(Items.GLASS_BOTTLE),"Unpowered analysis/remainder failed");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void saves_controls_and_automation_filters(GameTestHelper h) {
        var be=machine(h,"genetic_splicer");var specimen=bee(h);var inv=GeneticsRuntime.inventory(be);
        inv.setStackInSlot(0,specimen);inv.setStackInSlot(10,new ItemStack(Items.DIAMOND,7));
        GeneticsRuntime.energy(be).receiveEnergy(32100,false);
        var tag=be.saveWithFullMetadata(h.getLevel().registryAccess());
        var restored=BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),tag,h.getLevel().registryAccess());restored.setLevel(h.getLevel());
        h.assertTrue(GeneticsRuntime.energy(restored).getEnergyStored()==32100,"FE did not survive save/load");
        h.assertTrue(GeneticsRuntime.inventory(restored).getStackInSlot(10).getCount()==7,"Legacy recovery inventory lost");
        var handler=GeneticsRuntime.automation(be);
        h.assertTrue(handler.insertItem(3,new ItemStack(Items.DIAMOND),false).getCount()==1,"Automation inserted into output");
        h.assertTrue(handler.extractItem(0,1,false).isEmpty(),"Automation stole specimen");
        h.assertTrue(handler.extractItem(10,7,true).getCount()==7&&inv.getStackInSlot(10).getCount()==7,"Simulate extraction mutated recovery");
        // No fake network login: PB correctly rejects unnegotiated mock-client packets.
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
        var menu=new GeneticsMenu(1,player.getInventory(),be);
        h.assertTrue(menu.slots.size()==52,"Operational/recovery/player slot count changed");
        h.assertTrue(!menu.clickMenuButton(player,15)&&!menu.clickMenuButton(player,-1),"Invalid control accepted");
        player.setPos(be.getBlockPos().getCenter().add(100,0,0));
        h.assertTrue(!menu.clickMenuButton(player,3),"Distant player could change machine");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void injected_placeholder_suppression_and_power_capability(GameTestHelper h) {
        var be=machine(h,"geno_station");var inv=GeneticsRuntime.inventory(be);
        var comb=GeneticsRuntime.product("stardust_comb");h.assertTrue(!comb.isEmpty(),"Test comb is not registered");inv.setStackInSlot(0,comb);
        try {
            var type=Class.forName("com.zerog.aeroapiary.ZeroGMachines");
            for(int i=0;i<250;i++)type.getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class).invoke(null,be,h.getLevel());
            h.assertTrue(inv.getStackInSlot(0).getCount()==1&&inv.getStackInSlot(1).isEmpty(),"Legacy smelting branch still running");
            var caps=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),null);
            h.assertTrue(caps!=null&&caps.receiveEnergy(500,false)==500,"FE capability absent");
            var items=h.getLevel().getCapability(net.neoforged.neoforge.capabilities.Capabilities.ItemHandler.BLOCK,be.getBlockPos(),null);
            h.assertTrue(items!=null&&!items.isItemValid(3,new ItemStack(Items.DIAMOND)),"Addon capability mixin not applied");h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
}
