package net.zerog.tweaks.client;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.zerog.tweaks.storage.StorageTankRegistry;
import net.zerog.tweaks.storage.WoodStorageRegistry;

/** Dedicated servers never load the renderer implementations. */
@EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
public final class StorageClientRenderers {
    @SubscribeEvent public static void register(EntityRenderersEvent.RegisterRenderers event) {
        event.registerBlockEntityRenderer(StorageTankRegistry.TYPE.get(),StorageTankRenderer::new);
        event.registerBlockEntityRenderer(WoodStorageRegistry.TYPE.get(),WoodStorageRenderer::new);
        event.registerBlockEntityRenderer(net.zerog.tweaks.transport.TransportRegistry.TYPE.get(),TransportMotionRenderer::new);
    }
    private StorageClientRenderers(){}
}
