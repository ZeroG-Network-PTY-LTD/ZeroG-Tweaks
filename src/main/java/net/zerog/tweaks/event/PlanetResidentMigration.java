package net.zerog.tweaks.event;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.entity.npc.VillagerType;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.EntityTickEvent;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGPlanetVillagers;
import net.zerog.tweaks.worldgen.PlanetEcologyProfile;

/** Upgrade loaded planetary residents through vanilla's native conversion path. */
@EventBusSubscriber(modid="zerog_tweaks")
public final class PlanetResidentMigration {
    @SubscribeEvent public static void tick(EntityTickEvent.Post event) {
        if(!(event.getEntity() instanceof Villager old) || old.getType()!=EntityType.VILLAGER
                || !(old.level() instanceof ServerLevel level) || !old.isAlive()
                || old.tickCount%20!=0 || !level.getServer().isSameThread()) return;
        var dimension=level.dimension().location();
        if(!dimension.getNamespace().equals("zerog_tweaks") || !ZGDimensionTerrain.SOILS.containsKey(dimension.getPath())) return;
        var species=ZGPlanetVillagers.THEMES.get(PlanetEcologyProfile.theme(dimension.getPath()));
        if(species==null)return;
        var data=old.saveWithoutId(new CompoundTag());
        var replacement=old.convertTo(ZGPlanetVillagers.TYPES.get(species).get(),true);
        if(replacement==null)return;
        // convertTo registers the new entity with its own UUID. Never overwrite that
        // UUID with the old one after registration (would corrupt the entity index).
        data.putUUID("UUID",replacement.getUUID());
        replacement.load(data);
        replacement.setVillagerData(replacement.getVillagerData().setType(VillagerType.PLAINS));
        replacement.setStyle(old.getUUID().hashCode());
    }
    private PlanetResidentMigration() {}
}
