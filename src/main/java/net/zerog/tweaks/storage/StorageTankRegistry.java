package net.zerog.tweaks.storage;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

/** Original ZeroG tanks; no mandatory third-party machine dependency. */
public final class StorageTankRegistry {
    public static final String[] TIERS={"copper","nullifite","cyrrium","tectium","wraithsteel","astrium"};
    public static final int[] CAPACITIES={5000,20000,100000,500000,2000000,5000000};
    public static final List<DeferredHolder<Block,StorageTankBlock>> BLOCKS=new ArrayList<>();
    private static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    private static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final java.util.function.Supplier<BlockEntityType<StorageTankBlockEntity>> TYPE=TYPES.register("fluid_storage_tank",()->BlockEntityType.Builder.of(StorageTankBlockEntity::new,BLOCKS.stream().map(DeferredHolder::get).toArray(Block[]::new)).build(null));
    public static final java.util.function.Supplier<MenuType<StorageTankMenu>> MENU=MENUS.register("fluid_storage_tank",()->IMenuTypeExtension.create((id,inv,buf)->new StorageTankMenu(id,inv,inv.player.level().getBlockEntity(buf.readBlockPos()))));
    static {for(int i=0;i<TIERS.length;i++){final int tier=i;String id=TIERS[i]+"_fluid_tank";var block=BlockInit.BLOCKS.register(id,()->new StorageTankBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_BLOCK).noOcclusion(),tier));BLOCKS.add(block);ItemInit.ITEMS.register(id,()->new net.minecraft.world.item.BlockItem(block.get(),new net.minecraft.world.item.Item.Properties().stacksTo(1)));}}
    public static void register(IEventBus bus){TYPES.register(bus);MENUS.register(bus);bus.addListener(StorageTankRegistry::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent event){event.registerBlockEntity(Capabilities.FluidHandler.BLOCK,TYPE.get(),(be,face)->be.handler(face));}
    private StorageTankRegistry(){}
}
