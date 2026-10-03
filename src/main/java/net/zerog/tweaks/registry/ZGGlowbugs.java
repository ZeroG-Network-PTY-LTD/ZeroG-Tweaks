package net.zerog.tweaks.registry;

import java.util.Map;
import java.util.LinkedHashMap;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.animal.Bee;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.zerog.tweaks.entity.AlienGlowbug;

public final class ZGGlowbugs {
    public static final Map<String,DeferredHolder<EntityType<?>,EntityType<AlienGlowbug>>> TYPES=new LinkedHashMap<>();
    public static final Map<String,String> HOMES=new LinkedHashMap<>();
    public static String entityId(String variant){return variant.endsWith("bee")?variant:variant+"_glowbug";}
    public static void init(IEventBus bus){
        for(String planet:java.util.List.of("moon","mars","cerulon","skarn","eidolon","solvane")) HOMES.put(planet,planet);
        HOMES.put("flora_bee","cerulon"); HOMES.put("midnight_bee","moon"); HOMES.put("crimson_bee","mars");
        HOMES.put("tropical_bee","cerulon"); HOMES.put("gold_dust_bee","solvane"); HOMES.put("magma_bee","skarn");
        for(String planet:HOMES.keySet()){
            String id=entityId(planet);
            var type=EntityInit.ENTITIES.register(id,()->EntityType.Builder.<AlienGlowbug>of(
                    (entity,level)->new AlienGlowbug(entity,level,planet),MobCategory.CREATURE).sized(.35F,.3F).clientTrackingRange(8).build("zerog_tweaks:"+id));
            TYPES.put(planet,type);
            ItemInit.ITEMS.register(id+"_spawn_egg",()->new DeferredSpawnEggItem(type,0x242032,ZGGasVents.COLOURS.get(HOMES.get(planet)),new Item.Properties()));
        }
        bus.addListener(EntityAttributeCreationEvent.class,event->TYPES.values().forEach(type->event.put(type.get(),Bee.createAttributes().build())));
    }
    private ZGGlowbugs(){}
}
