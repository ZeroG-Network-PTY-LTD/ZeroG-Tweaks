package net.zerog.tweaks.genetics;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;
import net.zerog.tweaks.transport.TransportBlock;
import net.zerog.tweaks.transport.TransportBlockEntity;
import net.zerog.tweaks.storage.StorageTankBlockEntity;

/** Internal service transfers move real buffers; native external capabilities are never replaced. */
public final class AlvearyServiceModules {
    public static boolean sideAllowed(TransportBlockEntity port,Direction side){if(side==null||!port.block().family.endsWith("port")||!(port.getLevel() instanceof ServerLevel level)||AlvearyFormation.role(port.getBlockState())==AlvearyFormation.Role.NONE)return true;return !AlvearyPorts.hasFormedController(level,port.getBlockPos())||side==port.getBlockState().getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING);}
    private static boolean neighborChunksLoaded(ServerLevel level,BlockPos pos){for(var face:Direction.values())if(!level.hasChunkAt(pos.relative(face)))return false;return true;}
    private static boolean inward(BlockEntity owner,BlockPos pos,Direction face){return AlvearyPorts.inside(owner,pos.relative(face));}
    public static void tick(BlockEntity owner){if(!(owner.getLevel() instanceof ServerLevel level)||!AlvearyPorts.footprintLoaded(level,AlvearyFormation.anchor(owner))||!AlvearyRuntime.formed(owner))return;
        for(int y=0;y<4;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){var pos=AlvearyFormation.anchor(owner).offset(-x,y,-z);var state=level.getBlockState(pos);if(AlvearyFormation.role(state)==AlvearyFormation.Role.NONE||AlvearyPorts.controller(level,pos)!=owner)continue;var module=level.getBlockEntity(pos);if(module instanceof TransportBlockEntity t){if(!neighborChunksLoaded(level,pos)||!t.enabled())continue;String family=t.block().family;if(family.equals("energy_port")||family.equals("energy_cell")){boolean allowed=family.equals("energy_port")?t.getBlockState().getValue(TransportBlock.MODE)!=TransportBlock.PortMode.OUTPUT:false;if(family.equals("energy_cell"))for(var face:Direction.values())allowed|=inward(owner,pos,face)&&t.output(face);if(allowed){var sink=AlvearyRuntime.energy(owner);int n=sink.receiveEnergy(Math.min(t.stored,t.tier().energy()),true);n=sink.receiveEnergy(n,false);if(n>0){t.stored-=n;t.setChanged();}}}
                else if(family.equals("item_port")&&level.getGameTime()%20==0)transferItems(owner,t);
                else if(family.equals("fluid_port"))fluids(owner,t);
            }else if(module instanceof StorageTankBlockEntity tank)storage(owner,tank);
        }
    }
    public static void transferItems(BlockEntity owner,TransportBlockEntity port){if(!(owner.getLevel() instanceof ServerLevel level)||!port.block().family.equals("item_port")||AlvearyPorts.controller(level,port.getBlockPos())!=owner||!neighborChunksLoaded(level,port.getBlockPos())||!port.enabled())return;var mode=port.getBlockState().getValue(TransportBlock.MODE);int budget=port.tier().items();if(mode!=TransportBlock.PortMode.OUTPUT){var sink=AlvearyRuntime.automation(owner);for(int i=0;i<port.items.getSlots()&&budget>0;i++){var stack=port.items.getStackInSlot(i).copyWithCount(Math.min(budget,port.items.getStackInSlot(i).getCount()));if(stack.isEmpty()||!port.permittedItem(stack))continue;var rest=TransportBlockEntity.insert(sink,stack,false);int n=stack.getCount()-rest.getCount();port.items.extractItem(i,n,false);budget-=n;}}
        if(mode!=TransportBlock.PortMode.INPUT&&AlvearyRuntime.state(owner).getBoolean("eject")){var source=GeneticsRuntime.inventory(owner);for(int i=AlvearyRuntime.outputStart(owner);i<source.getSlots()&&budget>0;i++){var stack=source.getStackInSlot(i).copyWithCount(Math.min(budget,source.getStackInSlot(i).getCount()));if(stack.isEmpty()||!port.permittedItem(stack))continue;var rest=TransportBlockEntity.insert(port.items,stack,false);int n=stack.getCount()-rest.getCount();source.extractItem(i,n,false);budget-=n;}}port.setChanged();owner.setChanged();}
    private static void fluids(BlockEntity owner,TransportBlockEntity port){var mode=port.getBlockState().getValue(TransportBlock.MODE);var target=new AlvearyFluids(owner);int budget=port.tier().fluid();if(mode!=TransportBlock.PortMode.OUTPUT&&!port.tank.isEmpty()&&target.isFluidValid(1,port.tank.getFluid())&&port.permittedFluid(port.tank.getFluid())){var fluid=port.tank.drain(budget,FluidAction.SIMULATE);int n=target.fill(fluid,FluidAction.SIMULATE);if(n>0){fluid=port.tank.drain(n,FluidAction.EXECUTE);target.fill(fluid,FluidAction.EXECUTE);budget-=n;}}
        if(mode!=TransportBlock.PortMode.INPUT&&budget>0){var fluid=target.drainTank(0,budget,FluidAction.SIMULATE);if(!fluid.isEmpty()&&port.permittedFluid(fluid)){int n=port.tank.fill(fluid,FluidAction.SIMULATE);if(n>0)port.tank.fill(target.drainTank(0,n,FluidAction.EXECUTE),FluidAction.EXECUTE);}}}
    private static void storage(BlockEntity owner,StorageTankBlockEntity tank){var target=new AlvearyFluids(owner);int budget=1000;for(var face:Direction.values()){if(budget<=0||!inward(owner,tank.getBlockPos(),face))continue;var handler=tank.handler(face);var catalyst=handler.drain(budget,FluidAction.SIMULATE);if(!catalyst.isEmpty()&&target.isFluidValid(1,catalyst)){int n=target.fill(catalyst,FluidAction.SIMULATE);if(n>0){target.fill(handler.drain(n,FluidAction.EXECUTE),FluidAction.EXECUTE);budget-=n;}}var honey=target.drainTank(0,budget,FluidAction.SIMULATE);if(!honey.isEmpty()){int n=handler.fill(honey,FluidAction.SIMULATE);if(n>0){handler.fill(target.drainTank(0,n,FluidAction.EXECUTE),FluidAction.EXECUTE);budget-=n;}}}}
    private AlvearyServiceModules(){}
}
