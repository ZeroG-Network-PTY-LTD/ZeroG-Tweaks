package net.zerog.tweaks.machine;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.zerog.tweaks.registry.BlockInit;

public final class CombustionRegistry {
    public static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    public static final java.util.function.Supplier<BlockEntityType<CombustionBlockEntity>> TYPE=TYPES.register("combustion_generator",()->BlockEntityType.Builder.of(CombustionBlockEntity::new,BlockInit.COMBUSTION_GENERATOR.get()).build(null));
    public static void register(IEventBus bus){TYPES.register(bus);bus.addListener(CombustionRegistry::capabilities);}
    public static void capabilities(RegisterCapabilitiesEvent event){event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->be.energy);event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.fuel);}
    private CombustionRegistry(){}
}
