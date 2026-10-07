package net.zerog.tweaks.genetics;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.entity.BlockEntity;

/** Schedule verified addon work steps; cumulative rounding preserves whole-job FE. */
public final class LegacyCardJobs {
    public static void tick(BlockEntity be){
        if(!(be.getLevel() instanceof ServerLevel level))return;
        var state=GeneticsRuntime.state(be);var inv=GeneticsRuntime.inventory(be);
        var job=new CompoundTag();
        int[] inputs=GeneticsRuntime.id(be).equals("centrifuge")?new int[]{0}:new int[]{0,2};
        for(int i:inputs)if(!inv.getStackInSlot(i).isEmpty())job.put("s"+i,inv.getStackInSlot(i).save(level.registryAccess()));
        int speed=LegacyMachineCards.speed(be),saving=LegacyMachineCards.saving(be),cost=LegacyMachinePower.cost(GeneticsRuntime.id(be));
        job.putInt("speed",speed);job.putInt("saving",saving);job.putInt("cost",cost);
        if(state.contains("card_job")&&!state.getCompound("card_job").equals(job))LegacyMachineCards.resetJob(be);
        if(!LegacyMachinePower.ready(be))return;
        if(!state.contains("card_job"))state.put("card_job",job);
        int duration=(20100+speed-1)/speed,elapsed=state.getInt("card_elapsed"),next=elapsed+1;
        long total=((long)201*cost*(100-saving)+99)/100;
        int paid=(int)((total*next+duration-1)/duration),charge=paid-state.getInt("card_paid");
        if(state.getInt("energy")<charge)return;
        int steps=next*201/duration-elapsed*201/duration;
        try{
            int before=(Integer)be.getClass().getMethod("getProgress").invoke(be),count=inv.getStackInSlot(0).getCount();
            state.putBoolean("card_dispatch",true);
            var tick=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("tick",be.getClass(),net.minecraft.world.level.Level.class);
            for(int i=0;i<steps;i++)tick.invoke(null,be,level);
            int after=(Integer)be.getClass().getMethod("getProgress").invoke(be);
            if(after==before&&inv.getStackInSlot(0).getCount()==count)return;
            state.putInt("energy",state.getInt("energy")-charge);
            state.putInt("card_elapsed",next);state.putInt("card_paid",paid);be.setChanged();
            net.zerog.tweaks.machine.MachineActivity.work(level,be.getBlockPos(),GeneticsRuntime.id(be));
            if(next>=duration)LegacyMachineCards.resetJob(be);
        }catch(ReflectiveOperationException ex){throw new IllegalStateException("Verified addon recipe tick API changed",ex);}
        finally{state.remove("card_dispatch");}
    }
    private LegacyCardJobs(){}
}
