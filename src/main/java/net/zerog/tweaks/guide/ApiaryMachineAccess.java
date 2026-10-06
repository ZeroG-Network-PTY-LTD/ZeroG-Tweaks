package net.zerog.tweaks.guide;

import java.lang.reflect.Method;
import java.util.Optional;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.level.block.entity.BlockEntity;

/** Optional addon bridge: only verified public methods, no required addon linkage. */
public final class ApiaryMachineAccess {
    public record Machine(BlockEntity entity,String id,int progress,boolean formed,String error) {}
    public static Optional<Machine> read(AbstractContainerMenu menu) {
        if(menu instanceof net.zerog.tweaks.genetics.AlvearyMenu modern){
            var entity=modern.machine;
            if(!(entity.getLevel() instanceof net.minecraft.server.level.ServerLevel level)||entity.isRemoved())return Optional.empty();
            var result=net.zerog.tweaks.genetics.GeneticsRuntime.id(entity).equals("zero_g_hive")
                    ?new net.zerog.tweaks.genetics.AlvearyFormation.Result(true,null)
                    :net.zerog.tweaks.genetics.AlvearyFormation.locate(level,entity.getBlockPos(),modern.value(0));
            int cycle=modern.value(4);
            return Optional.of(new Machine(entity,net.zerog.tweaks.genetics.GeneticsRuntime.id(entity),
                    cycle>0?Math.max(0,Math.min(100,modern.value(3)*100/cycle)):0,result.formed(),result.error()==null?"":result.error()));
        }
        if(!menu.getClass().getName().equals("com.zerog.aeroapiary.ZeroGMachineMenu"))return Optional.empty();
        try {
            Object object=menu.getClass().getMethod("getMachine").invoke(menu);
            if(!(object instanceof BlockEntity entity))return Optional.empty();
            Class<?> type=object.getClass();
            String id=(String)type.getMethod("getMachineId").invoke(object);
            int progress=(Integer)type.getMethod("getProgressPercent").invoke(object);
            boolean formed=(Boolean)type.getMethod("isFormed").invoke(object);
            String error=(String)type.getMethod("getLastStructureError").invoke(object);
            return Optional.of(new Machine(entity,id,Math.max(0,Math.min(100,progress)),formed,error==null?"":error));
        } catch(ReflectiveOperationException|ClassCastException ex) { return Optional.empty(); }
    }
    private ApiaryMachineAccess() {}
}
