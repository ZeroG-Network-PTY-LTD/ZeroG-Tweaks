package net.zerog.tweaks.registry;

import java.util.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.zerog.tweaks.entity.PlanetVillager;

public final class ZGPlanetVillagers {
    public static final Map<String,String> THEMES=Map.of("moon","lunari","mars","rustborn","cerulon","glintfolk",
            "skarn","ashwright","eidolon","hollow_kin","solvane","sunwarden");
    public static final Map<String,DeferredHolder<EntityType<?>,EntityType<PlanetVillager>>> TYPES=new LinkedHashMap<>();
    public static void init(IEventBus bus){
        String[] ids={"lunari","rustborn","glintfolk","ashwright","hollow_kin","sunwarden"};
        int[] base={0xd9dce3,0xb5523a,0x2b697d,0x302a2c,0xdde8ee,0xeee6ca};
        int[] spots={0x58e1ff,0xffd279,0x7ff6ff,0xff772e,0x9cffff,0xffcf64};
        for(int i=0;i<ids.length;i++){
            String id=ids[i];int colour=base[i],spot=spots[i];
            var type=EntityInit.ENTITIES.register(id,()->{
                var builder=EntityType.Builder.<PlanetVillager>of(PlanetVillager::new,MobCategory.MISC).sized(.6F,1.95F).clientTrackingRange(10);
                if(id.equals("ashwright"))builder.fireImmune();
                return builder.build("zerog_tweaks:"+id);
            });
            TYPES.put(id,type);
            ItemInit.ITEMS.register(id+"_spawn_egg",()->new DeferredSpawnEggItem(type,colour,spot,new Item.Properties()));
        }
        bus.addListener((net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent event)->TYPES.forEach((id,type)->{
            var attributes=Villager.createAttributes();
            if(id.equals("ashwright")) attributes.add(Attributes.MOVEMENT_SPEED,.425).add(Attributes.KNOCKBACK_RESISTANCE,.6);
            event.put(type.get(),attributes.build());
        }));
    }
    private ZGPlanetVillagers(){}
}
