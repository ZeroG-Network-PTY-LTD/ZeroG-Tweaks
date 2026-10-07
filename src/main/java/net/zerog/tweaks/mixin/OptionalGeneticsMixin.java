package net.zerog.tweaks.mixin;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.genetics.GeneticsRuntime;
import net.zerog.tweaks.genetics.AlvearyRuntime;
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
        if(machine instanceof net.minecraft.world.level.block.entity.BlockEntity be&&GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be))) {
            if(GeneticsRuntime.state(be).getBoolean("card_dispatch"))return;
            if(net.zerog.tweaks.genetics.LegacyMachineCards.installed(be)){
                net.zerog.tweaks.genetics.LegacyCardJobs.tick(be);ci.cancel();return;
            }
            if(GeneticsRuntime.state(be).contains("card_job"))net.zerog.tweaks.genetics.LegacyMachineCards.resetJob(be);
            if(level.isClientSide||!net.zerog.tweaks.genetics.LegacyMachinePower.before(be))ci.cancel();
            return;
        }
        if(GeneticsRuntime.handles(GeneticsRuntime.id(machine))){GeneticsRuntime.tick(machine);ci.cancel();}
        else if(GeneticsRuntime.id(machine).equals("silk_weaver")){net.zerog.tweaks.genetics.SilkWeaverRuntime.tick(machine);ci.cancel();}
        else if(machine instanceof net.minecraft.world.level.block.entity.BlockEntity be&&AlvearyRuntime.tier(be)>0){AlvearyRuntime.tick(be);ci.cancel();}
    }
    @Inject(method="tick",at=@At("RETURN"),require=1)
    private static void zeroGLegacyCharge(@Coerce Object machine,Level level,CallbackInfo ci){
        if(!level.isClientSide&&machine instanceof net.minecraft.world.level.block.entity.BlockEntity be&&GeneticsRuntime.legacyPowered(GeneticsRuntime.id(be))&&!GeneticsRuntime.state(be).getBoolean("card_dispatch"))net.zerog.tweaks.genetics.LegacyMachinePower.after(be);
    }
    @Inject(method="mayPlaceIn",at=@At("HEAD"),cancellable=true,require=1)
    private static void zeroGGeneticsFilter(String id,int slot,ItemStack stack,CallbackInfoReturnable<Boolean> ci) {
        if(GeneticsRuntime.handles(id))ci.setReturnValue(GeneticsRuntime.mayPlace(id,slot,stack));
        // The installed recipes never read these legacy placeholder inputs.
        // Existing stacks remain extractable; no inventory indices are removed.
        else if(id.equals("starmetal_smelter")&&slot==1||id.equals("silk_weaver")&&(slot==1||slot==2)||id.equals("frame_infusion_altar")&&slot==2)ci.setReturnValue(false);
    }
}
