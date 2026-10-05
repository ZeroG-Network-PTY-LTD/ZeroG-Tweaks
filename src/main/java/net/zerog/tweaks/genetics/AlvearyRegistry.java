package net.zerog.tweaks.genetics;

import net.minecraft.core.registries.Registries;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.bus.api.IEventBus;

public final class AlvearyRegistry {
    private static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<MenuType<AlvearyMenu>> MENU=MENUS.register("alveary_runtime",()->IMenuTypeExtension.create((id,inv,buf)->new AlvearyMenu(id,inv,inv.player.level().getBlockEntity(buf.readBlockPos()))));
    public static void register(IEventBus bus){MENUS.register(bus);bus.addListener(AlvearyRegistry::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent event){for(String id:new String[]{"zero_g_hive"}){var key=ResourceLocation.fromNamespaceAndPath("aeroapiary",id);if(!BuiltInRegistries.BLOCK.containsKey(key))continue;var block=BuiltInRegistries.BLOCK.get(key);event.registerBlock(Capabilities.EnergyStorage.BLOCK,(level,pos,state,be,side)->be!=null&&AlvearyRuntime.tier(be)>0?AlvearyRuntime.energy(be):null,block);event.registerBlock(Capabilities.FluidHandler.BLOCK,(level,pos,state,be,side)->be!=null&&AlvearyRuntime.tier(be)>0?new AlvearyFluids(be):null,block);}
        for(int tier=1;tier<=7;tier++)for(String role:new String[]{"energy_port","honey_port","fluid_port","input_hatch","output_hatch","frame_loader"}){var key=ResourceLocation.fromNamespaceAndPath("aeroapiary","tier"+tier+"_"+role);if(!BuiltInRegistries.BLOCK.containsKey(key))continue;var block=BuiltInRegistries.BLOCK.get(key);if(role.equals("energy_port"))event.registerBlock(Capabilities.EnergyStorage.BLOCK,(level,pos,state,be,side)->level instanceof net.minecraft.server.level.ServerLevel server?AlvearyPorts.energy(server,pos):null,block);else if(role.equals("honey_port")||role.equals("fluid_port")){boolean honey=role.equals("honey_port");event.registerBlock(Capabilities.FluidHandler.BLOCK,(level,pos,state,be,side)->level instanceof net.minecraft.server.level.ServerLevel server?AlvearyPorts.fluids(server,pos,honey):null,block);}else event.registerBlock(Capabilities.ItemHandler.BLOCK,(level,pos,state,be,side)->level instanceof net.minecraft.server.level.ServerLevel server?AlvearyPorts.items(server,pos):null,block);}}
    private AlvearyRegistry(){}
}
