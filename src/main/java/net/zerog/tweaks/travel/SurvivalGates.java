package net.zerog.tweaks.travel;

import net.minecraft.core.registries.Registries;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.network.chat.Component;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.minecraft.world.item.Item;
import net.zerog.tweaks.item.RecallAnchorItem;
import net.zerog.tweaks.registry.BlockInit;

public final class SurvivalGates {
    public static final DeferredRegister<BlockEntityType<?>> ENTITIES=DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE,"zerog_tweaks");
    public static final DeferredRegister<MenuType<?>> MENUS=DeferredRegister.create(Registries.MENU,"zerog_tweaks");
    public static final DeferredRegister.Items ITEMS=DeferredRegister.createItems("zerog_tweaks");
    public static final net.neoforged.neoforge.registries.DeferredItem<RecallAnchorItem> RECALL=ITEMS.register("recall_anchor",()->new RecallAnchorItem(new Item.Properties().stacksTo(1),false));
    public static final net.neoforged.neoforge.registries.DeferredItem<RecallAnchorItem> GROUP=ITEMS.register("group_anchor",()->new RecallAnchorItem(new Item.Properties().stacksTo(1),true));
    public static final DeferredHolder<BlockEntityType<?>,BlockEntityType<SurvivalGateBlockEntity>> CONTROLLER=ENTITIES.register("survival_gate_controller",()->BlockEntityType.Builder.of(SurvivalGateBlockEntity::new,BlockInit.GATE_CONTROLLER.get()).build(null));
    public static final DeferredHolder<MenuType<?>,MenuType<SurvivalGateMenu>> MENU=MENUS.register("survival_gate",()->IMenuTypeExtension.create((id,inventory,buf)->new SurvivalGateMenu(id,inventory,inventory.player.level().getBlockEntity(buf.readBlockPos()))));
    public static void register(IEventBus bus){ENTITIES.register(bus);MENUS.register(bus);ITEMS.register(bus);bus.addListener(SurvivalGates::capabilities);}
    public static void capabilities(RegisterCapabilitiesEvent event){
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK,CONTROLLER.get(),(gate,direction)->gate.energy());
        event.registerBlock(Capabilities.EnergyStorage.BLOCK,(level,pos,state,entity,side)->{
            if(!(level instanceof ServerLevel server))return null;
            BlockPos port=pos.immutable();
            // Resolve the formed controller on every access: cached handlers must not
            // retain a removed controller or stay disconnected after gate formation.
            return new IEnergyStorage(){
                private IEnergyStorage target(){return portEnergy(server,port);}
                public int receiveEnergy(int amount,boolean simulate){var energy=target();return energy==null?0:energy.receiveEnergy(amount,simulate);}
                public int extractEnergy(int amount,boolean simulate){return 0;}
                public int getEnergyStored(){var energy=target();return energy==null?0:energy.getEnergyStored();}
                public int getMaxEnergyStored(){var energy=target();return energy==null?0:energy.getMaxEnergyStored();}
                public boolean canExtract(){return false;}
                public boolean canReceive(){var energy=target();return energy!=null&&energy.canReceive();}
            };
        },BlockInit.GATE_ENERGY_PORT.get());
    }
    public static void interact(PlayerInteractEvent.RightClickBlock event){
        if(event.getHand()!=InteractionHand.MAIN_HAND||!(event.getEntity() instanceof ServerPlayer player)||!(event.getLevel() instanceof ServerLevel level))return;
        if(!(level.getBlockEntity(event.getPos()) instanceof SurvivalGateBlockEntity gate))return;
        // Hub routing keeps the authored test-world semantics and takes priority.
        if(GateLedger.get(level.getServer()).controller(level,event.getPos())!=null)return;
        if(!player.getMainHandItem().isEmpty())return;
        gate.claim(player);player.openMenu(new SimpleMenuProvider((id,inv,p)->new SurvivalGateMenu(id,inv,gate),Component.literal("Concord Star Chart")),buf->buf.writeBlockPos(event.getPos()));
        event.setCanceled(true);event.setCancellationResult(InteractionResult.SUCCESS);
    }
    public static IEnergyStorage portEnergy(ServerLevel level,BlockPos pos){
        if(!level.getBlockState(pos).is(BlockInit.GATE_ENERGY_PORT.get()))return null;
        for(var at:BlockPos.betweenClosed(pos.offset(-8,-3,-8),pos.offset(8,3,8))){
            if(!level.hasChunkAt(at))continue;
            if(level.getBlockEntity(at) instanceof SurvivalGateBlockEntity gate&&gate.formedTier()>0&&gate.isPort(pos))return gate.energy();
        }return null;
    }
    private SurvivalGates(){}
}
