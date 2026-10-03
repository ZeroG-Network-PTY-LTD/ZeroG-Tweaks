package net.zerog.tweaks.registry;

import java.util.Map;
import java.util.LinkedHashMap;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.monster.Blaze;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.zerog.tweaks.entity.PlanetBlaze;

public final class ZGPlanetBlazes {
    public static final Map<String,String> HOMES=Map.of("void","moon","nova","solvane","nebula","cerulon","void_c","skarn","pulsar","mars","comet","eidolon");
    public static final Map<String,DeferredHolder<EntityType<?>,EntityType<PlanetBlaze>>> TYPES=new LinkedHashMap<>();
    public static void init(IEventBus bus){
        for(String style:java.util.List.of("void","nova","nebula","void_c","pulsar","comet")){
            var type=EntityInit.ENTITIES.register(style+"_blaze",()->EntityType.Builder.<PlanetBlaze>of((entity,level)->new PlanetBlaze(entity,level,style),MobCategory.MONSTER).sized(.6F,1.8F).fireImmune().clientTrackingRange(8).build("zerog_tweaks:"+style+"_blaze"));
            TYPES.put(style,type);
            ItemInit.ITEMS.register(style+"_blaze_spawn_egg",()->new DeferredSpawnEggItem(type,0x242032,ZGGasVents.COLOURS.get(HOMES.get(style)),new Item.Properties()));
            ItemInit.ITEMS.register(style+"_blaze_rod",()->new Item(new Item.Properties()));
        }
        bus.addListener(EntityAttributeCreationEvent.class,event->TYPES.values().forEach(type->event.put(type.get(),Blaze.createAttributes().build())));
    }
    private ZGPlanetBlazes(){}
}
