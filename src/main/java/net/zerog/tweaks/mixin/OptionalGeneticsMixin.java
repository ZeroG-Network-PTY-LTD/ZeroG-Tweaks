package net.zerog.tweaks.mixin;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.genetics.GeneticsRuntime;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Coerce;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Optional addon only; replace its two placeholder jobs, not other machines. */
@Pseudo
@Mixin(targets="com.zerog.aeroapiary.ZeroGMachines",remap=false)
public abstract class OptionalGeneticsMixin {
    @Inject(method="tick",at=@At("HEAD"),cancellable=true,require=1)
    private static void zeroGGeneticsTick(@Coerce Object machine,Level level,CallbackInfo ci) {
        if(GeneticsRuntime.handles(GeneticsRuntime.id(machine))){GeneticsRuntime.tick(machine);ci.cancel();}
    }
    @Inject(method="mayPlaceIn",at=@At("HEAD"),cancellable=true,require=1)
    private static void zeroGGeneticsFilter(String id,int slot,ItemStack stack,CallbackInfoReturnable<Boolean> ci) {
        if(GeneticsRuntime.handles(id))ci.setReturnValue(GeneticsRuntime.mayPlace(id,slot,stack));
    }
}
