package net.zerog.tweaks.event;

import java.util.ArrayList;
import net.minecraft.core.GlobalPos;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.neoforged.neoforge.event.tick.EntityTickEvent;
import net.zerog.tweaks.registry.ZGFarmlandBlock;

/** Supplies custom secondary farmland POIs without replacing native farmer AI. */
public final class AlienFarmlandSensor {
    public static void tick(EntityTickEvent.Post event) {
        if(!(event.getEntity() instanceof Villager villager) || !(villager.level() instanceof net.minecraft.server.level.ServerLevel level)
                || villager.tickCount%40!=0 || villager.getVillagerData().getProfession()!=VillagerProfession.FARMER) return;
        var brain=villager.getBrain();
        if(brain.hasMemoryValue(MemoryModuleType.SECONDARY_JOB_SITE)) return;
        var sites=new ArrayList<GlobalPos>();var centre=villager.blockPosition();
        for(int x=-4;x<=4;x++) for(int z=-4;z<=4;z++) for(int y=-2;y<=2;y++) {
            var pos=centre.offset(x,y,z);
            if(level.hasChunkAt(pos) && level.getBlockState(pos).getBlock() instanceof ZGFarmlandBlock)
                sites.add(GlobalPos.of(level.dimension(),pos));
        }
        if(!sites.isEmpty()) brain.setMemory(MemoryModuleType.SECONDARY_JOB_SITE,sites);
    }
    private AlienFarmlandSensor() {}
}
