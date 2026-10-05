package net.zerog.tweaks.power;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.zerog.tweaks.registry.BlockInit;

public final class PowerRegistry {
    public static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    public static final java.util.function.Supplier<BlockEntityType<PowerBlockEntity>> TYPE=TYPES.register("planet_power",()->BlockEntityType.Builder.of(PowerBlockEntity::new,BlockInit.SOLAR_ARRAY.get(),BlockInit.FUSION_REACTOR.get()).build(null));
    public static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<MenuType<PowerMenu>> MENU=MENUS.register("planet_power",()->IMenuTypeExtension.create((id,inv,buf)->new PowerMenu(id,inv,inv.player.level().getBlockEntity(buf.readBlockPos()))));
    public static void register(IEventBus bus){TYPES.register(bus);MENUS.register(bus);bus.addListener(PowerRegistry::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent event){
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->be.energy);
        event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.solar()||side!=null&&side!=net.minecraft.core.Direction.UP?null:be.fuel);
    }
    private PowerRegistry(){}
}
