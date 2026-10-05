package net.zerog.tweaks.mixin;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.zerog.tweaks.genetics.AlvearyFormation;
import net.zerog.tweaks.genetics.AlvearyRuntime;
import net.zerog.tweaks.genetics.GeneticsRuntime;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Pseudo @Mixin(targets="com.zerog.aeroapiary.ZeroGMachineBlockEntity",remap=false)
public abstract class OptionalAlvearyFormationMixin {
    @Shadow private boolean formed;
    @Shadow private String lastStructureError;
    @Inject(method="updateFormation",at=@At("HEAD"),cancellable=true,require=1)
    private void zeroGServiceModules(CallbackInfo ci){var be=(BlockEntity)(Object)this;int tier=AlvearyRuntime.tier(be);if(tier==0||GeneticsRuntime.id(be).equals("zero_g_hive")||!(be.getLevel() instanceof ServerLevel level))return;var result=AlvearyFormation.validate(level,be.getBlockPos(),tier);if(formed!=result.formed()||!java.util.Objects.equals(lastStructureError,result.error())){formed=result.formed();lastStructureError=result.error();be.setChanged();level.sendBlockUpdated(be.getBlockPos(),be.getBlockState(),be.getBlockState(),3);}ci.cancel();}
}
