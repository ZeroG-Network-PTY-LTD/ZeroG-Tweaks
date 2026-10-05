package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.zerog.tweaks.genetics.*;

@GameTestHolder("zerog_workflow") @PrefixGameTestTemplate(false)
public final class GeneticsTankGameTests {
    @GameTest(templateNamespace="zerog_tweaks",template="equipment_empty",timeoutTicks=100)
    public static void honey_tank_simulation_dose_and_persistence(GameTestHelper h){
        h.setBlock(new BlockPos(1,1,1),BuiltInRegistries.BLOCK.get(ResourceLocation.parse("aeroapiary:geno_station")));var be=h.getBlockEntity(new BlockPos(1,1,1));var tank=new GeneticsTank(be);
        var honey=BuiltInRegistries.FLUID.entrySet().stream().filter(e->e.getKey().location().getNamespace().equals("zerog_tweaks")&&e.getKey().location().getPath().endsWith("_honey")&&!e.getKey().location().getPath().startsWith("flowing_")).findFirst().orElseThrow().getValue();var stack=new FluidStack(honey,500);
        h.assertTrue(tank.fill(stack,IFluidHandler.FluidAction.SIMULATE)==500&&tank.amount()==0,"Simulation altered catalyst");tank.fill(stack,IFluidHandler.FluidAction.EXECUTE);
        h.assertTrue(tank.ready(),"Valid honey not usable");tank.consume();h.assertTrue(tank.amount()==250,"Wrong catalyst dose");
        var copy=BlockEntity.loadStatic(be.getBlockPos(),be.getBlockState(),be.saveWithFullMetadata(h.getLevel().registryAccess()),h.getLevel().registryAccess());h.assertTrue(new GeneticsTank(copy).amount()==250,"Catalyst lost on reload");
        h.assertTrue(tank.fill(new FluidStack(net.minecraft.world.level.material.Fluids.LAVA,1000),IFluidHandler.FluidAction.EXECUTE)==0,"Invalid catalyst accepted");h.succeed();
    }
}
