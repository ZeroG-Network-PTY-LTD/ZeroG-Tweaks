package net.zerog.tweaks.gametest;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.player.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.genetics.*;
@GameTestHolder("zerog_legacy_cards") @PrefixGameTestTemplate(false)
public final class LegacyCardGameTests {
    static ItemStack card(String family){return new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:"+family+"_upgrade_card_t6")));}
    static AbstractContainerMenu menu(BlockEntity be,Player player){try{return GeneticsRuntime.handles(GeneticsRuntime.id(be))?new GeneticsMenu(1,player.getInventory(),be):(AbstractContainerMenu)be.getClass().getMethod("createMenu",int.class,Inventory.class,Player.class).invoke(be,1,player.getInventory(),player);}catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}}
    static void tick(BlockEntity be){try{Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class).invoke(null,be,be.getLevel());}catch(ReflectiveOperationException ex){throw new RuntimeException(ex);}}
    @GameTest(templateNamespace="zerog_legacy_cards",template="equipment_empty",timeoutTicks=100)
    public static void powered_cards_preserve_recipes_and_exact_job_energy(GameTestHelper h){
        for(String id:java.util.List.of("centrifuge","starmetal_smelter")){
            var pos=new BlockPos(2,1,2);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));var be=h.getBlockEntity(pos);
            var cards=LegacyMachineCards.inventory(be);cards.setStackInSlot(0,card("acceleration"));cards.setStackInSlot(1,card("energy_coil"));
            var inv=GeneticsRuntime.inventory(be);inv.setStackInSlot(0,GeneticsRuntime.product(id.equals("centrifuge")?"meteor_comb":"stardust"));
            if(id.equals("starmetal_smelter"))inv.setStackInSlot(2,new ItemStack(net.minecraft.world.item.Items.REDSTONE));
            GeneticsRuntime.state(be).putInt("energy",40000);
            for(int i=0;i<80;i++)tick(be);
            h.assertTrue(!inv.getStackInSlot(0).isEmpty(),"Recipe consumed before full job");tick(be);
            h.assertTrue(inv.getStackInSlot(0).isEmpty(),"Acceleration did not finish at 81 ticks: "+id);
            int spent=(201*LegacyMachinePower.cost(id)*70+99)/100;
            h.assertTrue(GeneticsRuntime.state(be).getInt("energy")==40000-spent,"Job FE not exact: "+id);
            if(id.equals("starmetal_smelter"))h.assertTrue(inv.getStackInSlot(3).getCount()==3&&GeneticsRuntime.item(inv.getStackInSlot(3),"starmetal_nugget"),"Authoritative output changed");
        }h.succeed();
    }
    @GameTest(templateNamespace="zerog_legacy_cards",template="equipment_empty",timeoutTicks=100)
    public static void card_jobs_pause_reload_reset_and_refund_without_output_loss(GameTestHelper h){
        var pos=new BlockPos(3,1,3);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:starmetal_smelter")));var be=h.getBlockEntity(pos);
        var cards=LegacyMachineCards.inventory(be);cards.setStackInSlot(0,card("acceleration"));cards.setStackInSlot(1,card("energy_coil"));
        var inv=GeneticsRuntime.inventory(be);inv.setStackInSlot(0,GeneticsRuntime.product("stardust"));inv.setStackInSlot(2,new ItemStack(net.minecraft.world.item.Items.REDSTONE));inv.setStackInSlot(3,new ItemStack(net.minecraft.world.item.Items.STONE,64));
        GeneticsRuntime.state(be).putInt("energy",40000);for(int i=0;i<20;i++)tick(be);
        h.assertTrue(GeneticsRuntime.state(be).getInt("energy")==40000&&inv.getStackInSlot(0).getCount()==1,"Blocked job spent FE/input");
        inv.setStackInSlot(3,ItemStack.EMPTY);for(int i=0;i<40;i++)tick(be);
        var tag=be.saveWithFullMetadata(h.getLevel().registryAccess());var loaded=BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),tag,h.getLevel().registryAccess());loaded.setLevel(h.getLevel());h.getLevel().setBlockEntity(loaded);be=loaded;
        for(int i=0;i<41;i++)tick(be);h.assertTrue(GeneticsRuntime.state(be).getInt("energy")==28744&&GeneticsRuntime.inventory(be).getStackInSlot(3).getCount()==3,"Reload duplicated job FE/output");
        inv=GeneticsRuntime.inventory(be);inv.setStackInSlot(0,GeneticsRuntime.product("stardust"));inv.setStackInSlot(2,new ItemStack(net.minecraft.world.item.Items.REDSTONE));for(int i=0;i<10;i++)tick(be);
        cards=LegacyMachineCards.inventory(be);cards.extractItem(0,1,false);h.assertTrue(GeneticsRuntime.state(be).getInt("card_elapsed")==0,"Removal kept accelerated paid job");
        h.assertTrue(inv.getStackInSlot(0).getCount()==1&&inv.getStackInSlot(3).getCount()==3,"Card removal destroyed operating inventory");
        var bounds=new net.minecraft.world.phys.AABB(be.getBlockPos()).inflate(2);h.getLevel().destroyBlock(be.getBlockPos(),true);
        h.assertTrue(cards.getStackInSlot(1).isEmpty(),"Real block break did not refund card");LegacyMachineCards.drop(be);
        int count=h.getLevel().getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,bounds).stream().filter(e->e.getItem().is(card("energy_coil").getItem())).mapToInt(e->e.getItem().getCount()).sum();
        h.assertTrue(count==1,"Break refunded card incorrectly: "+count);h.succeed();
    }
    @GameTest(templateNamespace="zerog_legacy_cards",template="equipment_empty",timeoutTicks=100)
    public static void four_machine_card_sockets_are_separate_filtered_and_persistent(GameTestHelper h){
        for(String id:java.util.List.of("geno_station","genetic_splicer","centrifuge","starmetal_smelter")){
            var pos=new BlockPos(1,1,1);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:"+id)));var be=h.getBlockEntity(pos);
            var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());var menu=menu(be,player);
            int operating=GeneticsRuntime.handles(id)?16:id.equals("centrifuge")?7:4,first=operating+36;
            h.assertTrue(menu.slots.size()==first+2,"Missing separate card sockets: "+id);
            h.assertTrue(menu.getSlot(first).mayPlace(card("acceleration"))&&!menu.getSlot(first).mayPlace(card("energy_coil"))&&menu.getSlot(first+1).mayPlace(card("energy_coil"))&&!menu.getSlot(first+1).mayPlace(card("item_compact")),"Card family filter wrong");
            player.getInventory().setItem(9,card("acceleration"));h.assertTrue(!menu.quickMoveStack(player,operating).isEmpty()&&menu.getSlot(first).hasItem()&&player.getInventory().getItem(9).isEmpty(),"Card quick move lost/rejected item");
            menu.getSlot(first+1).set(card("energy_coil"));
            var saved=be.saveWithFullMetadata(h.getLevel().registryAccess());var loaded=BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),saved,h.getLevel().registryAccess());loaded.setLevel(h.getLevel());h.getLevel().setBlockEntity(loaded);
            var restored=menu(loaded,player);h.assertTrue(restored.getSlot(first).getItem().is(card("acceleration").getItem())&&restored.getSlot(first+1).getItem().is(card("energy_coil").getItem()),"Cards lost on reload");
            h.assertTrue(!restored.quickMoveStack(player,first).isEmpty()&&!restored.getSlot(first).hasItem(),"Card removal failed");
        }h.succeed();
    }
}
