package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;
@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class ProcessingGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void invalid_saved_cooling_item_grants_no_speed_bonus(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(p);
        be.inventory.setStackInSlot(be.kind.upgrades()+1,new ItemStack(net.minecraft.world.item.Items.DIRT));
        var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        var menu=new ProcessingMenu(1,player.getInventory(),be);
        h.assertTrue(menu.value(4)==4,"Invalid saved cooling item grants a speed bonus");
        h.assertTrue(be.inventory.getStackInSlot(be.kind.upgrades()+1).is(net.minecraft.world.item.Items.DIRT),"Invalid old item must remain recoverable");h.succeed();
    }
    private static ItemStack stack(String id,int n){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+id)),n);}
    private static void tick(GameTestHelper h,ProcessingBlockEntity be,int n){for(int i=0;i<n;i++)ProcessingBlockEntity.tick(h.getLevel(),be.getBlockPos(),be.getBlockState(),be);}
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void alloy_shapeless_exact_energy_output_blocking_and_reload(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(p);
        be.inventory.setStackInSlot(0,stack("pulsar_dust",2));be.inventory.setStackInSlot(2,stack("cyrrium_ingot",3));be.stored=8000;
        be.inventory.setStackInSlot(be.kind.output(),stack("cyrrium_casing",64));tick(h,be,10);h.assertTrue(be.stored==8000&&be.progress==0,"Blocked output consumed FE");
        be.inventory.setStackInSlot(be.kind.output(),ItemStack.EMPTY);tick(h,be,100);
        var copy=(ProcessingBlockEntity)BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());
        h.assertTrue(copy!=null&&copy.progress==100&&copy.stored==4000,"Job state lost on reload");tick(h,copy,100);
        h.assertTrue(copy.stored==0&&copy.inventory.getStackInSlot(copy.kind.output()).getCount()==2&&copy.inventory.getStackInSlot(0).isEmpty()&&copy.inventory.getStackInSlot(2).isEmpty(),"Alloy failed exact cost/output consumption");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void crystal_reusable_seed_and_feed(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.CRYSTAL_GROWTH_CHAMBER.get());var be=(ProcessingBlockEntity)h.getBlockEntity(p);be.inventory.setStackInSlot(0,stack("brine_crystal",1));be.inventory.setStackInSlot(1,stack("pulsar_dust",1));be.stored=6000;tick(h,be,1200);
        h.assertTrue(be.inventory.getStackInSlot(0).getCount()==1&&be.inventory.getStackInSlot(1).isEmpty()&&be.inventory.getStackInSlot(be.kind.output()).is(stack("lumenite",1).getItem())&&be.stored==0,"Crystal consumed seed or wrong output/FE");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void reusable_catalyst_required_and_upgrades_bounded(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.ALLOY_FORGE.get());var be=(ProcessingBlockEntity)h.getBlockEntity(p);be.inventory.setStackInSlot(0,stack("lumenite",2));be.inventory.setStackInSlot(1,stack("glimmer_scale",4));be.inventory.setStackInSlot(2,stack("brine_crystal",2));be.stored=40000;tick(h,be,400);h.assertTrue(be.progress==0&&be.stored==40000,"Required catalyst bypassed");
        be.inventory.setStackInSlot(be.kind.catalyst(),stack("stardust",1));be.inventory.setStackInSlot(be.kind.upgrades(),stack("astrium_casing",1));be.inventory.setStackInSlot(be.kind.upgrades()+1,stack("cryo_core",1));be.inventory.setStackInSlot(be.kind.upgrades()+2,stack("fusion_dust",1));
        var r=h.getLevel().getRecipeManager().getRecipeFor(ProcessingRegistry.TYPES_BY_KIND.get(be.kind).get(),be.input(),h.getLevel()).orElseThrow().value();h.assertTrue(be.duration(r)==160&&be.energyCost(r)==24000,"Upgrade bounds wrong");tick(h,be,160);
        h.assertTrue(be.stored==16000&&be.inventory.getStackInSlot(be.kind.catalyst()).getCount()==1&&be.inventory.getStackInSlot(be.kind.output()).is(stack("abyssal_pearl",1).getItem()),"Catalyst/upgrade completion wrong");h.assertTrue(!be.inventory.isItemValid(be.kind.upgrades()+1,stack("fusion_dust",1))&&be.inventory.getSlotLimit(be.kind.upgrades())==1,"Wrong or stacked upgrade accepted");h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void salvage_outputs_and_sided_ports(GameTestHelper h){
        var p=new BlockPos(1,1,1);h.setBlock(p,BlockInit.SALVAGE_STATION.get());var be=(ProcessingBlockEntity)h.getBlockEntity(p);var input=be.itemsFor(Direction.UP);h.assertTrue(input.insertItem(0,stack("meteorite_fragment",1),false).isEmpty(),"Valid top input rejected");h.assertTrue(input.extractItem(0,1,false).isEmpty(),"Automation extracted reserved input");var output=be.itemsFor(Direction.DOWN);h.assertTrue(!output.insertItem(0,stack("stardust",1),false).isEmpty(),"Output accepted input");be.stored=2000;tick(h,be,100);h.assertTrue(output.getStackInSlot(0).getCount()==1&&output.getStackInSlot(1).getCount()==4&&be.stored==0,"Salvage outputs incorrect");h.assertTrue(output.extractItem(1,4,false).getCount()==4,"Output extraction failed");h.succeed();
    }
}
