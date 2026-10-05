package net.zerog.tweaks.mixin;

import net.minecraft.core.Direction;
import net.neoforged.neoforge.items.IItemHandler;
import net.zerog.tweaks.genetics.GeneticsRuntime;
import net.zerog.tweaks.genetics.AlvearyRuntime;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Coerce;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Wrap the addon's own capability provider, avoiding provider ordering races. */
@Pseudo
@Mixin(targets="com.zerog.aeroapiary.ModCapabilities",remap=false)
public abstract class OptionalGeneticsCapabilityMixin {
    @Inject(method="lambda$register$0",at=@At("HEAD"),cancellable=true,require=1)
    private static void zeroGGeneticsItems(@Coerce Object machine,Direction side,CallbackInfoReturnable<IItemHandler> ci) {
        if(GeneticsRuntime.handles(GeneticsRuntime.id(machine)))ci.setReturnValue(GeneticsRuntime.automation(machine));
        else if(machine instanceof net.minecraft.world.level.block.entity.BlockEntity be&&AlvearyRuntime.tier(be)>0)ci.setReturnValue(AlvearyRuntime.automation(be));
        else if(machine instanceof net.minecraft.world.level.block.entity.BlockEntity be&&net.zerog.tweaks.genetics.AlvearyPorts.itemPort(GeneticsRuntime.id(be)))ci.setReturnValue(be.getLevel() instanceof net.minecraft.server.level.ServerLevel level?net.zerog.tweaks.genetics.AlvearyPorts.items(level,be.getBlockPos()):null);
    }
}
