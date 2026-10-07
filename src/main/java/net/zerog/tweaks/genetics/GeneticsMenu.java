package net.zerog.tweaks.genetics;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.items.SlotItemHandler;
import net.zerog.tweaks.registry.MenuInit;

/** Five operational slots plus eleven take-only legacy recovery slots. */
public final class GeneticsMenu extends AbstractContainerMenu implements net.zerog.tweaks.machine.MachineSideMenu {
    public final BlockEntity machine;
    public final String machineId;
    private final ContainerData data;
    public GeneticsMenu(int id,Inventory playerInv,BlockEntity machine) {
        super(MenuInit.GENETICS.get(),id);
        this.machine=machine;this.machineId=GeneticsRuntime.id(machine);
        var handler=GeneticsRuntime.inventory(machine);
        if(handler.getSlots()!=16)throw new IllegalStateException("Unsupported addon inventory size; refusing unsafe migration");
        for(int i=0;i<16;i++) {
            final int slot=i;
            int x=i<3?18:i<5?220:28+(i-5)*18;
            int y=i<3?22+i*24:i<5?22+(i-3)*48:130;
            addSlot(new SlotItemHandler(handler,i,x,y) {
                @Override public boolean mayPlace(ItemStack stack){return slot<3&&GeneticsRuntime.mayPlace(machineId,slot,stack);}
                @Override public int getMaxStackSize(){return slot==0?1:super.getMaxStackSize();}
                @Override public void setChanged(){super.setChanged();machine.setChanged();}
            });
        }
        for(int row=0;row<3;row++)for(int col=0;col<9;col++)addSlot(new Slot(playerInv,9+row*9+col,48+col*18,159+row*18));
        for(int col=0;col<9;col++)addSlot(new Slot(playerInv,col,48+col*18,217));
        for(var slot:LegacyMachineCards.slots(machine))addSlot(slot);
        data=playerInv.player.level().isClientSide?new SimpleContainerData(29):new ContainerData() {
            public int get(int index) {
                if(index>=11&&index<29)return net.zerog.tweaks.machine.LegacyMachineSides.mode(machine,index-11);
                var state=GeneticsRuntime.state(machine);
                return switch(index) {
                    case 0->state.getInt("progress")/4;
                    case 1->GeneticsRuntime.duration(machineId,state.getInt("mode"));
                    case 2->GeneticsRuntime.energy(machine).getEnergyStored()/10;
                    case 3->GeneticsRuntime.capacity(machineId)/10;
                    case 4->state.getInt("mode");case 5->state.getInt("gene");
                    case 6->state.getBoolean("requested")?1:0;
                    case 7->GeneticsRuntime.status(machine);
                    case 8->GeneticsRuntime.chance(machine);
                    case 9->state.getBoolean("last_success")?1:0;case 10->new GeneticsTank(machine).amount();default->0;
                };
            }
            public void set(int index,int value){}public int getCount(){return 29;}
        };
        addDataSlots(data);
    }
    public int value(int index){return data.get(index);}
    public BlockEntity sideMachine(){return machine;}
    public int sideMode(int face){return value(11+face);}
    @Override public boolean stillValid(Player player) {
        return !machine.isRemoved()&&player.level()==machine.getLevel()&&player.distanceToSqr(machine.getBlockPos().getCenter())<=64
            &&player.level().hasChunkAt(machine.getBlockPos())&&player.level().getBlockEntity(machine.getBlockPos())==machine;
    }
    @Override public boolean clickMenuButton(Player player,int button) {
        if(player.level().isClientSide||!stillValid(player))return false;
        if(net.zerog.tweaks.machine.LegacyMachineSides.command(machine,player,button)){broadcastChanges();return true;}
        var state=GeneticsRuntime.state(machine);
        if(button==3){GeneticsRuntime.cancel(machine);return true;}
        if(state.getBoolean("requested"))return false;
        if(button>=10&&button<15&&machineId.equals("geno_station")){state.putInt("gene",button-10);machine.setChanged();return true;}
        boolean splicer=machineId.equals("genetic_splicer");
        if(button==1||button==2){var specimen=GeneticsRuntime.inventory(machine).getStackInSlot(0).get(net.minecraft.core.component.DataComponents.CUSTOM_DATA);if(specimen==null||!specimen.copyTag().getBoolean("zerog_tweaks:analysed"))return false;}
        if((splicer&&button!=2)||(!splicer&&button!=0&&button!=1))return false;
        state.putInt("mode",button==1?1:0);
        if(GeneticsRuntime.status(machine)!=0)return false;
        state.putBoolean("requested",true);state.putInt("progress",0);state.remove("input");machine.setChanged();broadcastChanges();return true;
    }
    @Override public ItemStack quickMoveStack(Player player,int index) {
        if(!stillValid(player)||index<0||index>=slots.size())return ItemStack.EMPTY;
        var cardMove=LegacyMachineCards.quickMove(this,machine,player,index);if(cardMove!=null)return cardMove;
        var slot=slots.get(index);if(!slot.hasItem())return ItemStack.EMPTY;
        var source=slot.getItem();var before=source.copy();
        if(index<16){if(!moveItemStackTo(source,16,52,true))return ItemStack.EMPTY;}
        else {
            boolean moved=false;
            for(int i=0;i<3;i++)if(slots.get(i).mayPlace(source)&&moveItemStackTo(source,i,i+1,false)){moved=true;break;}
            if(!moved)return ItemStack.EMPTY;
        }
        if(source.isEmpty())slot.setByPlayer(ItemStack.EMPTY);else slot.setChanged();
        slot.onTake(player,source);return before;
    }
}
