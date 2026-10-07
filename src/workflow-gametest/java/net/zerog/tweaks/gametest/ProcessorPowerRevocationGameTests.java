package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.machine.ProcessingBlockEntity;
import net.zerog.tweaks.registry.BlockInit;

@GameTestHolder("zerog_power_revocation") @PrefixGameTestTemplate(false)
public final class ProcessorPowerRevocationGameTests {
    @GameTest(templateNamespace="zerog_power_revocation",template="equipment_empty",timeoutTicks=100)
    public static void disabled_then_reenabled_faces_do_not_revive_old_power_handlers(GameTestHelper h){
        var blocks=java.util.List.of(BlockInit.ALLOY_FORGE.get(),BlockInit.ORE_REFINERY.get(),BlockInit.CRYSTAL_GROWTH_CHAMBER.get(),BlockInit.SALVAGE_STATION.get());
        for(int index=0;index<blocks.size();index++){
            var relative=new BlockPos(1+index*2,1,1);h.setBlock(relative,blocks.get(index));
            var be=(ProcessingBlockEntity)h.getBlockEntity(relative);
            for(var side:Direction.values()){
                var stale=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),side);
                h.assertTrue(stale!=null&&stale.receiveEnergy(10,false)==10,"Enabled face rejected power");
                be.setFaceDisabled(side,true);
                h.assertTrue(!stale.canReceive()&&stale.receiveEnergy(10,false)==0,"Disabled handler still accepted power");
                be.setFaceDisabled(side,false);
                h.assertTrue(!stale.canReceive()&&stale.receiveEnergy(10,false)==0,"Re-enabled face revived a stale handler");
                var fresh=h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),side);
                int before=be.stored;
                h.assertTrue(fresh!=null&&fresh.canReceive()&&fresh.receiveEnergy(10,true)==10&&be.stored==before,"Fresh handler simulation mutated storage");
                h.assertTrue(fresh.receiveEnergy(10,false)==10&&be.stored==before+10,"Fresh handler delivery failed");
                be.setFaceDisabled(side,false);
                h.assertTrue(fresh.canReceive(),"Unchanged face setting revoked a live handler");
            }
        }
        h.succeed();
    }
}
