package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.npc.VillagerType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Native synchronized clothing variants; vanilla villager head/face geometry stays intact. */
public final class ZGVillagerAttire {
    private static final DeferredRegister<VillagerType> REGISTER=DeferredRegister.create(Registries.VILLAGER_TYPE,"zerog_tweaks");
    public static final Map<String,DeferredHolder<VillagerType,VillagerType>> TYPES=new LinkedHashMap<>();
    static {
        for(String theme:new String[]{"moon","mars","cerulon","skarn","eidolon","solvane"})
            for(int palette=0;palette<4;palette++) {
                String id=theme+"_space_"+palette;
                TYPES.put(id,REGISTER.register(id,()->new VillagerType(id)));
            }
    }
    public static void register(IEventBus bus) {REGISTER.register(bus);}
    private ZGVillagerAttire() {}
}
