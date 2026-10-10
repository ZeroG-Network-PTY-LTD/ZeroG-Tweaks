package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.*;
import net.neoforged.neoforge.fluids.*;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;
import net.zerog.tweaks.genetics.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class AlvearyRecipeGameTests {
    private static ItemStack specimen(GameTestHelper h){try{
        String pb="cy.jdkdigital.productivebees.";var bee=(net.minecraft.world.entity.animal.Bee)BuiltInRegistries.ENTITY_TYPE.get(ResourceLocation.parse("productivebees:configurable_bee")).create(h.getLevel());bee.getClass().getMethod("setBeeType",String.class).invoke(bee,"productivebees:iron");
        Class<?> attr=Class.forName(pb+"util.GeneAttribute"),value=Class.forName(pb+"util.GeneValue");var set=bee.getClass().getMethod("setAttributeValue",attr,value);String[] values={"PRODUCTIVITY_HIGH","ENDURANCE_STRONG","TEMPER_PASSIVE","BEHAVIOR_DIURNAL","WEATHER_TOLERANCE_ANY"};for(int i=0;i<5;i++)set.invoke(bee,attr.getField(ProductiveBeeGenes.GENES[i].toUpperCase(java.util.Locale.ROOT)).get(null),value.getField(values[i]).get(null));
        var cage=new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("productivebees:bee_cage")));Class.forName(pb+"common.item.BeeCage").getMethod("captureEntity",net.minecraft.world.entity.animal.Bee.class,ItemStack.class).invoke(null,bee,cage);return cage;
    }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}}
    @GameTest(templateNamespace="zerog_recipe_alveary",template="equipment_empty",timeoutTicks=100)
    public static void all_tiers_snapshot_frames_catalyst_and_no_inventory_mutation(GameTestHelper h){
        var bee=specimen(h);var expected=ProductiveBeeProduction.outputs(bee,h.getLevel());h.assertTrue(!expected.isEmpty(),"Real specimen has no loaded recipe");
        var pos=new BlockPos(1,1,1);
        for(int tier=1;tier<=7;tier++){
            h.setBlock(pos,Blocks.AIR);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier"+tier+"_controller")));var be=h.getBlockEntity(pos);
            GeneticsRuntime.inventory(be).setStackInSlot(0,bee.copy());var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=new AlvearyMenu(7,player.getInventory(),be);
            var before=be.saveWithFullMetadata(h.getLevel().registryAccess());var s=AlvearyRecipeSync.describe(menu);
            h.assertTrue(s.tier()==tier&&s.cycle()==AlvearyRuntime.cycle(be)&&s.feTick()==(tier>=3?20*tier:0)&&s.products().size()==expected.size(),"Tier recipe snapshot differs from runtime");
            h.assertTrue(s.products().getFirst().max()==expected.getFirst().maximum().getCount()&&s.products().getFirst().chance()==expected.getFirst().chance(),"Loaded comb recipe quantities/chances changed");
            h.assertTrue(before.equals(be.saveWithFullMetadata(h.getLevel().registryAccess())),"Read-only snapshot changed saved inventory/job");
            AlvearyRuntime.frames(be).insertItem(0,GeneticsRuntime.product("honeyed_frame"),false);var framed=AlvearyRecipeSync.describe(menu);
            h.assertTrue(framed.cycle()==AlvearyRuntime.cycle(be)&&framed.cycle()<s.cycle()&&framed.products().getFirst().max()==s.products().getFirst().max(),"Frame altered yield or snapshot missed timing");
            var light=new FluidStack(BuiltInRegistries.FLUID.get(ResourceLocation.parse("zerog_tweaks:liquid_starlight")),25);new AlvearyFluids(be).fill(light,FluidAction.EXECUTE);var boosted=AlvearyRecipeSync.describe(menu);
            h.assertTrue(boosted.boosted()==(tier>=6)&&boosted.cycle()==AlvearyRuntime.cycle(be)&&boosted.honey().isEmpty()==(tier<3),"Tank tier/boost/honey disclosure wrong");
            GeneticsRuntime.inventory(be).setStackInSlot(0,ItemStack.EMPTY);h.assertTrue(AlvearyRecipeSync.describe(menu).products().isEmpty(),"Removed bee left stale recipe");
            h.assertTrue(!menu.clickMenuButton(player,999),"Recipe browsing introduced unvalidated job command");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_recipe_alveary",template="equipment_empty",timeoutTicks=100)
    public static void actual_pb_recipe_cycle_and_component_preserving_codec(GameTestHelper h){
        try {
            var origin=new BlockPos(4,1,4);
            for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){boolean core=(y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3;String role=y==4?"roof":x==0&&y==0&&z==0?"controller":x==1&&y==0&&z==0?"energy_port":"casing";h.setBlock(origin.offset(-x,y,-z),core?Blocks.AIR:BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:tier3_"+role)));}
            var be=h.getBlockEntity(origin);be.getClass().getMethod("updateFormation").invoke(be);h.assertTrue(AlvearyRuntime.formed(be),"Recipe fixture not formed");
            String pb="cy.jdkdigital.productivebees.";var bee=(net.minecraft.world.entity.animal.Bee)BuiltInRegistries.ENTITY_TYPE.get(ResourceLocation.parse("productivebees:configurable_bee")).create(h.getLevel());bee.getClass().getMethod("setBeeType",String.class).invoke(bee,"productivebees:iron");
            Class<?> attr=Class.forName(pb+"util.GeneAttribute"),value=Class.forName(pb+"util.GeneValue");var set=bee.getClass().getMethod("setAttributeValue",attr,value);String[] values={"PRODUCTIVITY_HIGH","ENDURANCE_STRONG","TEMPER_PASSIVE","BEHAVIOR_DIURNAL","WEATHER_TOLERANCE_ANY"};for(int i=0;i<5;i++)set.invoke(bee,attr.getField(ProductiveBeeGenes.GENES[i].toUpperCase(java.util.Locale.ROOT)).get(null),value.getField(values[i]).get(null));
            var cage=new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("productivebees:bee_cage")));Class.forName(pb+"common.item.BeeCage").getMethod("captureEntity",net.minecraft.world.entity.animal.Bee.class,ItemStack.class).invoke(null,bee,cage);
            GeneticsRuntime.inventory(be).setStackInSlot(0,cage);AlvearyRuntime.energy(be).receiveEnergy(100000,false);h.getLevel().setDayTime(1000);
            var player=h.makeMockPlayer(GameType.SURVIVAL);var menu=new AlvearyMenu(9,player.getInventory(),be);var snapshot=AlvearyRecipeSync.describe(menu);h.assertTrue(!snapshot.products().isEmpty(),"Loaded PB recipe missing from snapshot");
            var buffer=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),h.getLevel().registryAccess());
            try{AlvearyRecipeSync.Snapshot.CODEC.encode(buffer,snapshot);var decoded=AlvearyRecipeSync.Snapshot.CODEC.decode(buffer);h.assertTrue(decoded.menu()==9&&decoded.controller().equals(be.getBlockPos())&&decoded.products().size()==snapshot.products().size(),"Recipe snapshot binding lost");for(int i=0;i<snapshot.products().size();i++)h.assertTrue(ItemStack.isSameItemSameComponents(decoded.products().get(i).icon(),snapshot.products().get(i).icon())&&decoded.products().get(i).max()==snapshot.products().get(i).max(),"PB product components/count lost on network");}finally{buffer.release();}
            int energy=AlvearyRuntime.energy(be).getEnergyStored();for(int i=0;i<snapshot.cycle();i++)AlvearyRuntime.tick(be);
            h.assertTrue(AlvearyRuntime.energy(be).getEnergyStored()==energy-snapshot.cycle()*snapshot.feTick()&&new AlvearyFluids(be).getFluidInTank(0).getAmount()==250,"Advertised cycle FE/honey differs from real processing");
            h.assertTrue(ItemStack.isSameItemSameComponents(cage,GeneticsRuntime.inventory(be).getStackInSlot(0)),"Production consumed specimen");
            for(var p:snapshot.products())if(p.chance()==1){int count=0;var inv=GeneticsRuntime.inventory(be);for(int i=AlvearyRuntime.outputStart(be);i<inv.getSlots();i++)if(ItemStack.isSameItemSameComponents(inv.getStackInSlot(i),p.icon()))count+=inv.getStackInSlot(i).getCount();h.assertTrue(count>=p.min()&&count<=p.max(),"Advertised product range differs from actual output");}
            h.succeed();
        }catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}
    }
    @GameTest(templateNamespace="zerog_recipe_alveary",template="equipment_empty",timeoutTicks=100)
    public static void existing_honey_port_and_blocked_output_regression(GameTestHelper h){AlvearyRuntimeGameTests.formed_controller_uses_actual_pb_recipe_components_and_honey_save(h);}
}
