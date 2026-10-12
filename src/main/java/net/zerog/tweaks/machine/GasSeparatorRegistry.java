package net.zerog.tweaks.machine;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.*;
import net.neoforged.neoforge.capabilities.*;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.zerog.tweaks.registry.*;
public final class GasSeparatorRegistry {
    public static final DeferredBlock<GasSeparatorBlock> BLOCK=BlockInit.BLOCKS.register("water_separator",()->new GasSeparatorBlock(BlockBehaviour.Properties.of().strength(4).requiresCorrectToolForDrops()));
    public static final DeferredItem<net.minecraft.world.item.BlockItem> ITEM=ItemInit.ITEMS.registerSimpleBlockItem("water_separator",BLOCK);
    private static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    private static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<BlockEntityType<GasSeparatorBlockEntity>> TYPE=TYPES.register("water_separator",()->BlockEntityType.Builder.of(GasSeparatorBlockEntity::new,BLOCK.get()).build(null));
    public static final java.util.function.Supplier<MenuType<GasSeparatorMenu>> MENU=MENUS.register("water_separator",()->IMenuTypeExtension.create((id,inv,buf)->new GasSeparatorMenu(id,inv,(GasSeparatorBlockEntity)inv.player.level().getBlockEntity(buf.readBlockPos()))));
    public static void register(IEventBus bus){TYPES.register(bus);MENUS.register(bus);bus.addListener(GasSeparatorRegistry::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent e){
        e.registerBlockEntity(Capabilities.FluidHandler.BLOCK,TYPE.get(),(be,side)->side==null?null:be.fluid(side));
        e.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->side==null?null:be.energy(side));
        e.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.terminalFace(side)?null:be.items(side));
    }
    private GasSeparatorRegistry(){}
}
