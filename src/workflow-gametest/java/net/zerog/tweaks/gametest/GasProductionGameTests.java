package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.gametest.framework.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.gametest.*;
import net.neoforged.neoforge.fluids.*;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.*;
@GameTestHolder("zerog_gas_production")
@PrefixGameTestTemplate(false)
public final class GasProductionGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=80)
    public static void registered_ticker_pipe_extraction_and_canister(GameTestHelper h){
        var b=machine(h);feed(b);var ticker=((net.minecraft.world.level.block.EntityBlock)b.getBlockState().getBlock()).getTicker(h.getLevel(),b.getBlockState(),GasSeparatorRegistry.TYPE.get());h.assertTrue(ticker!=null,"No registered server ticker");
        for(int i=0;i<b.duration();i++)ticker.tick(h.getLevel(),b.getBlockPos(),b.getBlockState(),b);
        int produced=b.hydrogen.getFluidAmount();var pos=b.getBlockPos().east();h.getLevel().setBlock(pos,net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.parse("zerog_tweaks:copper_gas_tube")).defaultBlockState(),3);
        var pipe=(net.zerog.tweaks.transport.TransportBlockEntity)h.getLevel().getBlockEntity(pos);java.util.Arrays.fill(pipe.modes,3);pipe.modes[Direction.WEST.ordinal()]=2;
        net.zerog.tweaks.transport.TransportBlockEntity.tick(h.getLevel(),pos,pipe.getBlockState(),pipe);
        h.assertTrue(b.hydrogen.isEmpty()&&pipe.tank.getFluidAmount()==produced,"Gas tube could not extract actual produced hydrogen");
        pipe.modes[Direction.EAST.ordinal()]=0;
        var result=FluidUtil.tryFillContainer(new ItemStack(ZGGases.CANISTER.get()),pipe.fluidHandler(Direction.EAST),1000,null,true);
        h.assertTrue(result.isSuccess()&&FluidUtil.getFluidContained(result.getResult()).orElseThrow().getAmount()==produced&&pipe.tank.isEmpty(),"Canister collection duplicated/lost produced gas");h.succeed();
    }
    private static GasSeparatorBlockEntity machine(GameTestHelper h){var pos=h.absolutePos(new BlockPos(3,2,3));h.getLevel().setBlock(pos,GasSeparatorRegistry.BLOCK.get().defaultBlockState(),3);return (GasSeparatorBlockEntity)h.getLevel().getBlockEntity(pos);}
    private static void feed(GasSeparatorBlockEntity b){b.water.fill(new FluidStack(Fluids.WATER,1000),FluidAction.EXECUTE);b.stored=100000;}
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=80)
    public static void conservation_and_pauses(GameTestHelper h){var b=machine(h);feed(b);int w=GasProductionConfig.WATER.get(),fe=b.cost();for(int i=0;i<b.duration();i++)b.work();h.assertTrue(b.water.getFluidAmount()==1000-w&&b.hydrogen.getFluidAmount()==w*2&&b.oxygen.getFluidAmount()==w&&b.stored==100000-fe,"Cycle duplicated/lost water, FE or gas");
        b.oxygen.fill(new FluidStack(ZGGases.OXYGEN.fluid().get(),16000),FluidAction.EXECUTE);int before=b.stored,water=b.water.getFluidAmount(),hydrogen=b.hydrogen.getFluidAmount();for(int i=0;i<120;i++)b.work();h.assertTrue(b.stored==before&&b.water.getFluidAmount()==water&&b.hydrogen.getFluidAmount()==hydrogen,"Full oxygen did not pause both outputs");
        b.oxygen.setFluid(FluidStack.EMPTY);b.hydrogen.setFluid(new FluidStack(ZGGases.HYDROGEN.fluid().get(),16000));b.work();h.assertTrue(b.stored==before&&b.water.getFluidAmount()==water,"Full hydrogen consumed inputs");
        b.hydrogen.setFluid(FluidStack.EMPTY);b.stored=0;b.work();h.assertTrue(b.water.getFluidAmount()==water&&b.hydrogen.isEmpty(),"Unpowered production");b.water.setFluid(FluidStack.EMPTY);b.stored=before;b.work();h.assertTrue(b.stored==before&&b.oxygen.isEmpty(),"Dry production");h.succeed();}
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=80)
    public static void faces_simulation_and_stale_handlers(GameTestHelper h){var b=machine(h);var water=b.fluid(Direction.UP);h.assertTrue(water.fill(new FluidStack(Fluids.WATER,1000),FluidAction.SIMULATE)==1000&&b.water.isEmpty(),"Simulation mutated water");h.assertTrue(water.fill(new FluidStack(Fluids.LAVA,1000),FluidAction.EXECUTE)==0,"Accepted lava");water.fill(new FluidStack(Fluids.WATER,1000),FluidAction.EXECUTE);h.assertTrue(water.drain(1000,FluidAction.EXECUTE).isEmpty(),"Water input drained");b.cycle(Direction.UP);h.assertTrue(water.fill(new FluidStack(Fluids.WATER,10),FluidAction.EXECUTE)==0,"Cached handler ignored reassignment");
        b.hydrogen.fill(new FluidStack(ZGGases.HYDROGEN.fluid().get(),1000),FluidAction.EXECUTE);var out=b.fluid(Direction.EAST);h.assertTrue(out.fill(new FluidStack(ZGGases.HYDROGEN.fluid().get(),10),FluidAction.EXECUTE)==0,"Output accepted insertion");h.assertTrue(out.drain(1000,FluidAction.SIMULATE).getAmount()==1000&&b.hydrogen.getFluidAmount()==1000,"Drain simulation mutated gas");
        var energy=b.energy(Direction.NORTH);h.assertTrue(energy.receiveEnergy(20000,true)==10000&&b.stored==0,"Energy simulation/limit failed");b.togglePower(Direction.NORTH);h.assertTrue(energy.receiveEnergy(100,false)==0,"Cached disabled FE face accepted power");h.getLevel().removeBlock(b.getBlockPos(),false);h.assertTrue(out.drain(1000,FluidAction.EXECUTE).isEmpty()&&water.fill(new FluidStack(Fluids.WATER,10),FluidAction.EXECUTE)==0,"Removed machine retained capability access");h.succeed();}
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=80)
    public static void cards_save_reload_and_menu_contract(GameTestHelper h){var b=machine(h);feed(b);var speed=new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("acceleration_upgrade_card_t6").get());var coil=new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("energy_coil_upgrade_card_t6").get());
        h.assertTrue(b.cards.isItemValid(0,speed)&&!b.cards.isItemValid(0,coil)&&!b.cards.isItemValid(1,new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("void_upgrade_card").get())),"Wrong card family accepted");b.cards.insertItem(0,speed,false);b.cards.insertItem(1,coil,false);h.assertTrue(b.speed()==250&&b.cost()==(GasProductionConfig.ENERGY.get()*70+99)/100,"Upgrade caps failed");b.work();b.togglePower(Direction.NORTH);b.cycle(Direction.DOWN);var tag=b.saveWithFullMetadata(h.getLevel().registryAccess());int progress=b.progress;var pos=b.getBlockPos();h.getLevel().removeBlock(pos,false);h.getLevel().setBlock(pos,GasSeparatorRegistry.BLOCK.get().defaultBlockState(),3);var restored=(GasSeparatorBlockEntity)h.getLevel().getBlockEntity(pos);restored.loadWithComponents(tag,h.getLevel().registryAccess());h.assertTrue(restored.stored==100000&&restored.water.getFluidAmount()==1000&&restored.progress==progress&&restored.speed()==250&&!restored.power(Direction.NORTH)&&restored.role(Direction.DOWN)==1,"Reload lost settings/contents");
        var player=h.makeMockServerPlayerInLevel();player.moveTo(pos.getX()+.5,pos.getY()+1,pos.getZ()+.5);var menu=new GasSeparatorMenu(0,player.getInventory(),restored);h.assertTrue(menu.value(10)==GasProductionConfig.WATER.get()&&menu.cost()==restored.cost()&&menu.value(6)==restored.duration(),"Recipe panel values do not match backend");h.assertTrue(!menu.clickMenuButton(player,99)&&menu.clickMenuButton(player,0),"Button validation failed");player.moveTo(pos.getX()+100,pos.getY(),pos.getZ());h.assertTrue(!menu.clickMenuButton(player,10),"Remote menu accepted changes");player.discard();h.succeed();}
}
