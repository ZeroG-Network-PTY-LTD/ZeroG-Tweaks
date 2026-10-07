package net.zerog.tweaks.transport;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

public final class TransportRegistry {
    private static final List<DeferredHolder<Block,TransportBlock>> BLOCKS=new ArrayList<>();
    public static final DeferredRegister<BlockEntityType<?>> TYPES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    public static final DeferredHolder<BlockEntityType<?>,BlockEntityType<TransportBlockEntity>> TYPE=TYPES.register("transport",()->BlockEntityType.Builder.of(TransportBlockEntity::new,BLOCKS.stream().map(DeferredHolder::get).toArray(Block[]::new)).build(null));
    static {
        for(int tier=0;tier<6;tier++)for(String suffix:new String[]{"energy_conduit","fluid_pipe","gas_tube","item_tube","energy_cell"})add(TransportTier.ALL[tier].name()+"_"+suffix,suffix,tier);
        for(String family:new String[]{"item","fluid","energy"})add(family+"_port",family+"_port",0);
        add("null_link","null_link",5);
        for(String id:new String[]{"flux_wrench","item_filter_card","fluid_filter_card","null_frequency_card"})ItemInit.ITEMS.registerItem(id,p->new TransportToolItem(p,id),new Item.Properties().stacksTo(1));
    }
    private static void add(String id,String family,int tier){var holder=BlockInit.BLOCKS.register(id,()->{var props=BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_BLOCK).noOcclusion();return family.endsWith("cell")?new TransportBlock.Cell(props,family,tier):family.endsWith("port")?new TransportBlock.Port(props,family,tier):family.equals("null_link")?new TransportBlock(props,family,tier):new TransportBlock.Wire(props,family,tier);});BLOCKS.add(holder);ItemInit.ITEMS.registerSimpleBlockItem(id,holder);}
    public static void register(IEventBus bus){TYPES.register(bus);bus.addListener(TransportRegistry::capabilities);}
    public static void capabilities(RegisterCapabilitiesEvent event){
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->be.supports("energy")?be.energy(side):null);
        event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.supports("item")?be.itemHandler(side):null);
        event.registerBlockEntity(Capabilities.FluidHandler.BLOCK,TYPE.get(),(be,side)->be.supports("fluid")?be.fluidHandler(side):null);
    }
    private TransportRegistry(){}
}
