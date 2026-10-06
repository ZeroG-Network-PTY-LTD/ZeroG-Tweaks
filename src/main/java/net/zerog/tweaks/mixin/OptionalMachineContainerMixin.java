package net.zerog.tweaks.mixin;

import net.minecraft.core.Direction;
import net.minecraft.world.WorldlyContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.zerog.tweaks.machine.LegacyMachineSides;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;

/** Vanilla hopper fallback must obey the same permissions as capabilities. */
@Pseudo @Mixin(targets="com.zerog.aeroapiary.ZeroGMachineBlockEntity",remap=false)
public abstract class OptionalMachineContainerMixin implements WorldlyContainer {
    public int[] getSlotsForFace(Direction side){
        var be=(BlockEntity)(Object)this;
        int count=LegacyMachineSides.supports(be)?LegacyMachineSides.items(be,side).getSlots():getContainerSize();
        return java.util.stream.IntStream.range(0,count).toArray();
    }
    public boolean canPlaceItemThroughFace(int slot,ItemStack stack,Direction side){
        var be=(BlockEntity)(Object)this;
        return LegacyMachineSides.supports(be)?LegacyMachineSides.items(be,side).isItemValid(slot,stack):canPlaceItem(slot,stack);
    }
    public boolean canTakeItemThroughFace(int slot,ItemStack stack,Direction side){
        var be=(BlockEntity)(Object)this;
        return LegacyMachineSides.supports(be)?!LegacyMachineSides.items(be,side).extractItem(slot,1,true).isEmpty():slot>=0&&slot<getContainerSize();
    }
}
