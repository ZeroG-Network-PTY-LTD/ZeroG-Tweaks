package net.zerog.tweaks.machine;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;

/** Successful-work feedback only: no ticking registries, chunk tickets or inventory writes. */
public final class MachineActivity {
    public static void work(Level level,BlockPos pos,String id){
        if(!(level instanceof ServerLevel server))return;
        long time=level.getGameTime();int offset=Math.floorMod(pos.hashCode(),40);
        boolean hot=id.contains("forge")||id.contains("smelt")||id.contains("combustion")||id.contains("fusion");
        boolean biology=id.contains("geno")||id.contains("genetic")||id.contains("alveary")||id.contains("apiary")||id.contains("hive");
        if((time+offset)%10==0){
            var state=level.getBlockState(pos);var face=state.hasProperty(BlockStateProperties.HORIZONTAL_FACING)?state.getValue(BlockStateProperties.HORIZONTAL_FACING):net.minecraft.core.Direction.NORTH;
            double phase=time*.16,side=.17*Math.sin(phase),height=.16*Math.cos(phase);
            double x=pos.getX()+.5+face.getStepX()*.53+face.getStepZ()*side;
            double z=pos.getZ()+.5+face.getStepZ()*.53-face.getStepX()*side;
            server.sendParticles(hot?ParticleTypes.SMALL_FLAME:biology?ParticleTypes.END_ROD:ParticleTypes.ELECTRIC_SPARK,x,pos.getY()+.55+height,z,2,.015,.015,.015,.003);
        }
        if((time+offset)%80==0){
            var sound=hot?SoundEvents.FURNACE_FIRE_CRACKLE:id.contains("solar")||biology||id.contains("crystal")?SoundEvents.BEACON_AMBIENT:SoundEvents.GRINDSTONE_USE;
            level.playSound(null,pos,sound,SoundSource.BLOCKS,.10F,hot?.8F:1.1F);
        }
    }
    private MachineActivity(){}
}
