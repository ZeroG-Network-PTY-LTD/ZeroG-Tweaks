package net.zerog.tweaks.mixin;

import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.genetics.AlvearyRuntime;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** The legacy drop method does not know about the separate new frame storage. */
@Pseudo @Mixin(targets="com.zerog.aeroapiary.ZeroGMachineBlockEntity",remap=false)
public abstract class OptionalAlvearyDropMixin {
    @Inject(method="dropInventory",at=@At("HEAD"),require=1)
    private void zeroGDropAdditionalFrames(CallbackInfo ci){var be=(BlockEntity)(Object)this;if(AlvearyRuntime.tier(be)==0||be.getLevel()==null||be.getLevel().isClientSide)return;var frames=AlvearyRuntime.frames(be);for(int i=0;i<27;i++){var stack=frames.getStackInSlot(i);if(!stack.isEmpty()){net.minecraft.world.Containers.dropItemStack(be.getLevel(),be.getBlockPos().getX()+.5,be.getBlockPos().getY()+.5,be.getBlockPos().getZ()+.5,stack);frames.setStackInSlot(i,ItemStack.EMPTY);}}}
}
