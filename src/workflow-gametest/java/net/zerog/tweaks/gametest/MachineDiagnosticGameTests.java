package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.*;
@GameTestHolder("zerog_machine_diagnostics") @PrefixGameTestTemplate(false)
public final class MachineDiagnosticGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void diagnostic_snapshot_matches_disabled_faces_without_changing_machine(GameTestHelper h){
        var pos=new BlockPos(3,2,3);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:alloy_forge")));
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);be.stored=500;be.inventory.setStackInSlot(0,new ItemStack(Items.IRON_INGOT,2));
        be.setFaceDisabled(Direction.EAST,true);be.setItemMode(Direction.EAST,4);
        var before=be.saveWithoutMetadata(h.getLevel().registryAccess());var s=MachineDiagnostics.describe(be);
        h.assertTrue(s!=null&&s.masks().size()==6&&s.faces().size()==6&&s.energy()==500&&s.capacity()==1000000,"Diagnostic lost bounded actual energy/face state");
        h.assertTrue(s.masks().get(Direction.EAST.ordinal())==0&&s.masks().get(Direction.NORTH.ordinal())==5,"Diagnostic ignored disabled power/item faces");
        h.assertTrue(before.equals(be.saveWithoutMetadata(h.getLevel().registryAccess())),"Read-only diagnostic changed processing/inventory state");
        boolean rejected=false;try{new MachineDiagnostics.Status(s.dimension(),s.position(),s.block(),0,0,java.util.List.of(8,0,0,0,0,0),s.faces());}catch(IllegalArgumentException expected){rejected=true;}
        h.assertTrue(rejected,"Diagnostic payload accepted out-of-range port flags");
        var buffer=new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(),h.getLevel().registryAccess());
        try{MachineDiagnostics.Status.CODEC.encode(buffer,s);h.assertTrue(s.equals(MachineDiagnostics.Status.CODEC.decode(buffer)),"Diagnostic codec changed actual face state");}finally{buffer.release();}
        for(var side:Direction.values())be.setFaceDisabled(side,true);
        var closed=MachineDiagnostics.describe(be);h.assertTrue(closed.energy()==500,"Disabled interfaces hid the machine's stored charge");
        h.setBlock(new BlockPos(6,2,3),net.minecraft.world.level.block.Blocks.CHEST);
        h.assertTrue(MachineDiagnostics.describe(h.getBlockEntity(new BlockPos(6,2,3)))==null,"Diagnostic exposed unrelated chest contents");h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void wrench_diagnostic_is_local_read_only_and_does_not_open_a_menu(GameTestHelper h){
        var pos=new BlockPos(3,2,3);h.setBlock(pos,BuiltInRegistries.BLOCK.get(ResourceLocation.parse("zerog_tweaks:alloy_forge")));
        var be=(ProcessingBlockEntity)h.getBlockEntity(pos);be.stored=500;
        var player=h.makeMockServerPlayerInLevel();player.setPos(be.getBlockPos().getCenter());
        player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:flux_wrench"))));
        var menu=player.containerMenu;var before=be.saveWithoutMetadata(h.getLevel().registryAccess());
        var event=new net.neoforged.neoforge.event.entity.player.PlayerInteractEvent.RightClickBlock(player,net.minecraft.world.InteractionHand.MAIN_HAND,be.getBlockPos(),new net.minecraft.world.phys.BlockHitResult(be.getBlockPos().getCenter(),Direction.NORTH,be.getBlockPos(),false));
        MachineDiagnosticInteraction.read(event);
        h.assertTrue(event.isCanceled()&&event.getCancellationResult().consumesAction()&&player.containerMenu==menu,"Wrench diagnostic opened or fell through to a machine menu");
        h.assertTrue(before.equals(be.saveWithoutMetadata(h.getLevel().registryAccess())),"Wrench snapshot altered settings or processing state");
        player.setPos(be.getBlockPos().getCenter().add(10,0,0));h.assertTrue(!MachineDiagnostics.show(player,be),"Remote diagnostic ignored range boundary");
        player.setPos(be.getBlockPos().getCenter());player.setItemInHand(net.minecraft.world.InteractionHand.MAIN_HAND,new ItemStack(Items.STICK));h.assertTrue(!MachineDiagnostics.show(player,be),"Non-wrench item requested diagnostics");
        h.succeed();
    }
}
