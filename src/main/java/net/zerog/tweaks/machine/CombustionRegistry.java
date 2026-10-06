package net.zerog.tweaks.machine;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.zerog.tweaks.registry.BlockInit;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;

public final class CombustionRegistry {
    public static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    public static final java.util.function.Supplier<BlockEntityType<CombustionBlockEntity>> TYPE=TYPES.register("combustion_generator",()->BlockEntityType.Builder.of(CombustionBlockEntity::new,BlockInit.COMBUSTION_GENERATOR.get()).build(null));
    public static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<MenuType<CombustionMenu>> MENU=MENUS.register("combustion_generator",()->IMenuTypeExtension.create((id,inventory,buffer)->new CombustionMenu(id,inventory,inventory.player.level().getBlockEntity(buffer.readBlockPos()))));
    public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems("zerog_tweaks");
    public static final net.neoforged.neoforge.registries.DeferredItem<Item> FLUX_MODULE=ITEMS.registerSimpleItem("generator_flux_module",new Item.Properties());
    public static void register(IEventBus bus){TYPES.register(bus);MENUS.register(bus);ITEMS.register(bus);bus.addListener(CombustionRegistry::capabilities);}
    public static void capabilities(RegisterCapabilitiesEvent event){event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->be.energyFor(side));event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.fuelFor(side));}
    private CombustionRegistry(){}
}
