package net.zerog.tweaks.genetics;

import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.core.component.DataComponents;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;

@EventBusSubscriber(modid="zerog_tweaks")
public final class GeneticsIntegration {
    @SubscribeEvent public static void open(PlayerInteractEvent.RightClickBlock event) {
        if(event.getHand()!=InteractionHand.MAIN_HAND||event.getEntity().isShiftKeyDown()||!event.getItemStack().isEmpty())return;
        var be=event.getLevel().getBlockEntity(event.getPos());String id=GeneticsRuntime.id(be);
        if(!GeneticsRuntime.handles(id))return;
        if(event.getEntity() instanceof ServerPlayer player)player.openMenu(new SimpleMenuProvider(
            (window,inv,p)->new GeneticsMenu(window,inv,be),Component.literal(id.equals("geno_station")?"Geno Station":"Genetic Splicer")),buf->buf.writeBlockPos(event.getPos()));
        event.setCanceled(true);event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));
    }
    @SubscribeEvent public static void tooltip(ItemTooltipEvent event) {
        var serum=GeneticsRuntime.serum(event.getItemStack());
        if(!serum.isEmpty())event.getToolTip().add(Component.literal(serum.getString("gene").replace('_',' ')+": "+serum.getString("value").replace('_',' ')));
        var data=event.getItemStack().get(DataComponents.CUSTOM_DATA);
        if(data!=null&&data.copyTag().getBoolean("zerog_tweaks:analysed"))ProductiveBeeGenes.read(event.getItemStack()).forEach((gene,value)->event.getToolTip().add(Component.literal(gene.replace('_',' ')+": "+value.replace('_',' '))));
    }
    public static void capabilities(RegisterCapabilitiesEvent event) {
        for(String id:new String[]{"genetic_splicer","geno_station"}) {
            var key=ResourceLocation.fromNamespaceAndPath("aeroapiary",id);
            if(BuiltInRegistries.BLOCK.containsKey(key))event.registerBlock(Capabilities.EnergyStorage.BLOCK,
                (level,pos,state,be,side)->be!=null&&GeneticsRuntime.handles(GeneticsRuntime.id(be))?GeneticsRuntime.energy(be):null,BuiltInRegistries.BLOCK.get(key));
        }
    }
    private GeneticsIntegration(){}
}
