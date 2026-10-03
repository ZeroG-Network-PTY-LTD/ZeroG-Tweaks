package net.zerog.tweaks.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Bee;
import net.minecraft.world.level.Level;

/** Small pollinating alien insect using the vanilla Java bee rig and behavior. */
public final class AlienGlowbug extends Bee {
    public final String planet;
    public AlienGlowbug(EntityType<? extends Bee> type,Level level,String planet){super(type,level);this.planet=planet;}
    @Override public AlienGlowbug getBreedOffspring(ServerLevel level,AgeableMob mate){
        return net.zerog.tweaks.registry.ZGGlowbugs.TYPES.get(planet).get().create(level);
    }
}
