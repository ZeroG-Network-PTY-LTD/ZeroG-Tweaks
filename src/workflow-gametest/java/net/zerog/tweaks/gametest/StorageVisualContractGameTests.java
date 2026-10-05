package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.storage.*;

/** Server-safe packet and animation contracts, not GPU visual approval. */
@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class StorageVisualContractGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void exact_contents_packet_changes_within_same_gauge_step(GameTestHelper h) {
        var pos=new BlockPos(1,1,1);
        h.setBlock(pos,StorageTankRegistry.BLOCKS.get(0).get());
        var be=(StorageTankBlockEntity)h.getBlockEntity(pos);
        be.tank.fill(new FluidStack(Fluids.WATER,100),IFluidHandler.FluidAction.EXECUTE);
        int before=be.getBlockState().getValue(StorageTankBlock.LEVEL);
        var oldTag=be.getUpdatePacket().getTag().copy();
        be.tank.fill(new FluidStack(Fluids.WATER,100),IFluidHandler.FluidAction.EXECUTE);
        var tag=be.getUpdateTag(h.getLevel().registryAccess());
        var copy=new StorageTankBlockEntity(be.getBlockPos(),be.getBlockState());
        copy.loadWithComponents(tag,h.getLevel().registryAccess());
        h.assertTrue(before==be.getBlockState().getValue(StorageTankBlock.LEVEL)&&!oldTag.equals(tag),
            "Sub-gauge contents must still synchronize");
        h.assertTrue(copy.tank.getFluidAmount()==200&&copy.tank.getFluid().getFluid()==Fluids.WATER,
            "Client update lost exact fluid identity/amount");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void lid_interpolation_is_bounded_and_closes(GameTestHelper h) {
        var pos=new BlockPos(2,1,2);
        h.setBlock(pos,WoodStorageRegistry.CONTAINERS.get("shardwood_chest").get());
        var be=(WoodStorageBlockEntity)h.getBlockEntity(pos);
        var closed=be.getBlockState();
        var open=closed.setValue(BlockStateProperties.OPEN,true);
        for(int i=0;i<20;i++)WoodStorageBlockEntity.clientTick(h.getLevel(),be.getBlockPos(),open,be);
        h.assertTrue(be.lidOpenness(1)==1,"Lid failed to fully open or exceeded clamp");
        WoodStorageBlockEntity.clientTick(h.getLevel(),be.getBlockPos(),closed,be);
        h.assertTrue(be.lidOpenness(0)>be.lidOpenness(1)&&be.lidOpenness(.5F)>.9F,
            "Lid closure must interpolate, not jump");
        for(int i=0;i<20;i++)WoodStorageBlockEntity.clientTick(h.getLevel(),be.getBlockPos(),closed,be);
        h.assertTrue(be.lidOpenness(1)==0,"Lid failed to close");
        h.succeed();
    }
}
