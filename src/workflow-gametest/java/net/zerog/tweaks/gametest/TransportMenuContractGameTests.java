package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.transport.TransportBlockEntity;
import net.zerog.tweaks.transport.TransportMenu;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class TransportMenuContractGameTests {
    @GameTest(templateNamespace="zerog_tweaks", template="equipment_empty", timeoutTicks=100)
    public static void energy_and_fluid_buffers_recover_old_items_but_refuse_new_storage(GameTestHelper h) {
        var pos=new BlockPos(1,1,1);
        for(var id:java.util.List.of("copper_energy_cell","copper_fluid_pipe")){
            h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:"+id)));
            var be=(TransportBlockEntity)h.getBlockEntity(pos);
            be.items.setStackInSlot(0,new ItemStack(Items.DIAMOND,7));
            var player=h.makeMockPlayer(GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
            var menu=new TransportMenu(1,player.getInventory(),be);
            h.assertTrue(!menu.getSlot(0).isActive()&&!menu.getSlot(menu.machineSlots).isActive(),"Non-item family displays item storage/templates");
            h.assertTrue(!be.items.isItemValid(0,new ItemStack(Items.STONE)),"Raw inventory bypasses family restriction");
            h.assertTrue(menu.clickMenuButton(player,6)&&menu.getSlot(0).isActive(),"Explicit legacy recovery cannot be opened");
            h.assertTrue(!menu.getSlot(0).mayPlace(new ItemStack(Items.STONE)),id+" unintentionally provides insertable item storage");
            h.assertTrue(!menu.quickMoveStack(player,0).isEmpty()&&be.items.getStackInSlot(0).isEmpty(),id+" lost old incidental items instead of permitting take-only recovery");
            int diamonds=0;for(int i=0;i<player.getInventory().getContainerSize();i++)if(player.getInventory().getItem(i).is(Items.DIAMOND))diamonds+=player.getInventory().getItem(i).getCount();
            h.assertTrue(diamonds==7,"Recovery lost or duplicated items");
            player.getInventory().setItem(9,new ItemStack(Items.STONE,4));
            menu.quickMoveStack(player,menu.playerStart);
            h.assertTrue(player.getInventory().getItem(9).getCount()==4&&be.items.getStackInSlot(0).isEmpty(),"Shift-click bypassed recovery-only protection");
        }
        h.succeed();
    }
}
