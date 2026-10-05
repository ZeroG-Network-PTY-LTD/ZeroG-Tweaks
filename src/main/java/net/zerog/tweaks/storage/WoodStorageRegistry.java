package net.zerog.tweaks.storage;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.TrapDoorBlock;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockSetType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.items.wrapper.InvWrapper;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;
import net.zerog.tweaks.registry.ZGDoorBlock;

/** Original planetary joinery and independent item storage; no external machine API. */
public final class WoodStorageRegistry {
    public static final String[] WOODS = {"shardwood", "charwood", "hoarwood", "gildwood"};
    public static final Map<String, DeferredHolder<Block, WoodStorageBlock>> CONTAINERS = new LinkedHashMap<>();
    public static final Map<String, DeferredHolder<Block, ? extends Block>> JOINERY = new LinkedHashMap<>();
    public static final DeferredRegister<BlockEntityType<?>> TYPES = DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, "zerog_tweaks");
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<WoodStorageBlockEntity>> TYPE = TYPES.register("wood_storage",
        () -> BlockEntityType.Builder.of(WoodStorageBlockEntity::new, CONTAINERS.values().stream().map(DeferredHolder::get).toArray(Block[]::new)).build(null));
    public static final DeferredHolder<Item, Item> EXPANSION = ItemInit.ITEMS.registerItem("storage_expansion_module", Item::new, new Item.Properties());
    static {
        for (String wood : WOODS) {
            for (String kind : new String[]{"chest", "barrel"}) {
                String id = wood + "_" + kind;
                var block = BlockInit.BLOCKS.register(id, () -> kind.equals("barrel")
                    ? new WoodStorageBlock.Barrel(BlockBehaviour.Properties.ofFullCopy(Blocks.BARREL))
                    : new WoodStorageBlock.Chest(BlockBehaviour.Properties.ofFullCopy(Blocks.OAK_PLANKS).noOcclusion()));
                CONTAINERS.put(id, block);
                ItemInit.ITEMS.registerSimpleBlockItem(id, block);
            }
            String doorId = wood + "_panel_door";
            var door = BlockInit.BLOCKS.register(doorId, () -> new ZGDoorBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.OAK_DOOR)));
            JOINERY.put(doorId, door);
            ItemInit.ITEMS.register(doorId, () -> new net.minecraft.world.item.DoubleHighBlockItem(door.get(), new Item.Properties()));
            String trapId = wood + "_lattice_trapdoor";
            var trap = BlockInit.BLOCKS.register(trapId, () -> new TrapDoorBlock(BlockSetType.OAK, BlockBehaviour.Properties.ofFullCopy(Blocks.OAK_TRAPDOOR)));
            JOINERY.put(trapId, trap);
            ItemInit.ITEMS.registerSimpleBlockItem(trapId, trap);
        }
    }
    public static void register(IEventBus bus) {
        TYPES.register(bus);
        bus.addListener(net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent.class,
            event -> event.registerBlockEntity(Capabilities.ItemHandler.BLOCK, TYPE.get(), (be, side) -> new InvWrapper(be)));
    }
    private WoodStorageRegistry() {}
}
