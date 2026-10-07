package net.zerog.tweaks.machine;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.crafting.*;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.registries.*;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.capabilities.*;
import net.neoforged.bus.api.IEventBus;
import net.zerog.tweaks.registry.BlockInit;
import java.util.*;

public final class ProcessingRegistry {
    public enum Kind {
        REFINING("refining",1,1), ALLOYING("alloying",3,3),
        CRYSTAL("crystal_growth",2,3), SALVAGING("salvaging",1,3);
        public final String id;public final int inputCount,outputCount;
        Kind(String id,int in,int out){this.id=id;inputCount=in;outputCount=out;}
        public int catalyst(){return inputCount;}
        public int output(){return inputCount+1;}
        public int upgrades(){return output()+outputCount;}
        // Append Void; never shift legacy inputs, outputs or the three older cards.
        public int slots(){return upgrades()+4;}
    }
    private static final DeferredRegister<RecipeType<?>> TYPES=DeferredRegister.create(Registries.RECIPE_TYPE,"zerog_tweaks");
    private static final DeferredRegister<RecipeSerializer<?>> SERIALIZERS=DeferredRegister.create(Registries.RECIPE_SERIALIZER,"zerog_tweaks");
    private static final DeferredRegister<BlockEntityType<?>> ENTITIES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    private static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final Map<Kind,DeferredHolder<RecipeType<?>,RecipeType<ProcessingRecipe>>> TYPES_BY_KIND=new EnumMap<>(Kind.class);
    public static final Map<Kind,DeferredHolder<RecipeSerializer<?>,ProcessingRecipe.Serializer>> SERIALIZERS_BY_KIND=new EnumMap<>(Kind.class);
    static{for(var kind:Kind.values()){TYPES_BY_KIND.put(kind,TYPES.register(kind.id,()->new RecipeType<ProcessingRecipe>(){public String toString(){return "zerog_tweaks:"+kind.id;}}));SERIALIZERS_BY_KIND.put(kind,SERIALIZERS.register(kind.id,()->new ProcessingRecipe.Serializer(kind)));}}
    public static final DeferredHolder<BlockEntityType<?>,BlockEntityType<ProcessingBlockEntity>> TYPE=ENTITIES.register("processing_machine",()->BlockEntityType.Builder.of(ProcessingBlockEntity::new,BlockInit.ALLOY_FORGE.get(),BlockInit.CRYSTAL_GROWTH_CHAMBER.get(),BlockInit.SALVAGE_STATION.get()).build(null));
    public static final DeferredHolder<MenuType<?>,MenuType<ProcessingMenu>> MENU=MENUS.register("processing_machine",()->IMenuTypeExtension.create((id,inv,buf)->{
        var pos=buf.readBlockPos();if(inv.player.level().getBlockEntity(pos) instanceof ProcessingBlockEntity be)return new ProcessingMenu(id,inv,be);throw new IllegalStateException("Missing processing machine");}));
    public static void register(IEventBus bus){TYPES.register(bus);SERIALIZERS.register(bus);ENTITIES.register(bus);MENUS.register(bus);bus.addListener(ProcessingRegistry::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent event){
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,net.zerog.tweaks.registry.BlockEntityInit.ORE_REFINERY.get(),(be,side)->be.energyInput(side));
        event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,net.zerog.tweaks.registry.BlockEntityInit.ORE_REFINERY.get(),(be,side)->be.itemsFor(side));
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,TYPE.get(),(be,side)->be.energyInput(side));
        event.registerBlockEntity(Capabilities.ItemHandler.BLOCK,TYPE.get(),(be,side)->be.itemsFor(side));
    }
    private ProcessingRegistry(){}
}
