package net.zerog.tweaks.mixin;

import net.minecraft.world.entity.player.*;
import net.minecraft.world.inventory.*;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.zerog.tweaks.machine.*;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import net.minecraft.world.item.ItemStack;

/** Standard menu data/buttons on the verified optional addon's original menu. */
@Pseudo @Mixin(targets="com.zerog.aeroapiary.ZeroGMachineMenu",remap=false)
public abstract class OptionalMachineMenuMixin extends AbstractContainerMenu implements MachineSideMenu {
    @Unique private BlockEntity zeroGSideMachine;
    @Unique private ContainerData zeroGSideData;
    protected OptionalMachineMenuMixin(MenuType<?> type,int id){super(type,id);}
    @Inject(method="<init>",at=@At("TAIL"),require=1)
    private void zeroGSideInit(MenuType<?> type,int id,Inventory inv,@Coerce Object machine,CallbackInfo ci){
        zeroGSideMachine=(BlockEntity)machine;
        if(net.zerog.tweaks.genetics.LegacyMachineCards.supports(zeroGSideMachine))for(var slot:net.zerog.tweaks.genetics.LegacyMachineCards.slots(zeroGSideMachine))addSlot(slot);
        zeroGSideData=inv.player.level().isClientSide||!LegacyMachineSides.supports(zeroGSideMachine)?new SimpleContainerData(18):new ContainerData(){
            public int get(int i){return LegacyMachineSides.mode(zeroGSideMachine,i);}
            public void set(int i,int value){}public int getCount(){return 18;}
        };
        addDataSlots(zeroGSideData);
    }
    public BlockEntity sideMachine(){return zeroGSideMachine;}
    @Inject(method="quickMoveStack",at=@At("HEAD"),cancellable=true,require=1)
    private void zeroGCardTransfer(Player player,int index,CallbackInfoReturnable<ItemStack> ci){if(net.zerog.tweaks.genetics.LegacyMachineCards.supports(zeroGSideMachine)){var moved=net.zerog.tweaks.genetics.LegacyMachineCards.quickMove(this,zeroGSideMachine,player,index);if(moved!=null)ci.setReturnValue(moved);}}
    public int sideMode(int face){return zeroGSideData.get(face);}
    @Override public boolean clickMenuButton(Player player,int button){
        if(LegacyMachineSides.command(zeroGSideMachine,player,button)){broadcastChanges();return true;}
        return super.clickMenuButton(player,button);
    }
}
