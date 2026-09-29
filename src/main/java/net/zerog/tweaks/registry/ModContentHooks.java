package net.zerog.tweaks.registry;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;

import net.zerog.tweaks.entity.CrystalStag;
import net.zerog.tweaks.entity.DuneBurrower;
import net.zerog.tweaks.entity.FrostYak;
import net.zerog.tweaks.entity.Prismling;
import net.zerog.tweaks.entity.RustBeetle;

/** Mod-bus registry-time hooks: entity attributes. */
public final class ModContentHooks {
    private ModContentHooks() {}

    public static void register(IEventBus modBus) {
        modBus.addListener(EntityAttributeCreationEvent.class, event -> {
            event.put(EntityInit.CRYSTAL_STAG.get(), CrystalStag.createAttributes().build());
            event.put(EntityInit.FROST_YAK.get(), FrostYak.createAttributes().build());
            event.put(EntityInit.PRISMLING_HOLDER.get(), Prismling.createAttributes().build());
            event.put(EntityInit.RUST_BEETLE.get(), RustBeetle.createAttributes().build());
            event.put(EntityInit.DUNE_BURROWER.get(), DuneBurrower.createAttributes().build());
        });
    }
}