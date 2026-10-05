package net.zerog.tweaks.client;

import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.minecraft.core.registries.BuiltInRegistries;
import org.lwjgl.glfw.GLFW;

/** Client-only reference book; does not pretend that controllers have live processing menus. */
public final class MultiblockGuideEvents {
    public static final KeyMapping OPEN = new KeyMapping("key.zerog_tweaks.multiblock_guide",
            GLFW.GLFW_KEY_G, "key.categories.zerog_tweaks");

    @EventBusSubscriber(modid = "zerog_tweaks", value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
    public static final class ModEvents {
        @SubscribeEvent public static void keys(RegisterKeyMappingsEvent event) { event.register(OPEN); }
    }
    @EventBusSubscriber(modid = "zerog_tweaks", value = Dist.CLIENT)
    public static final class GameEvents {
        @SubscribeEvent public static void tick(ClientTickEvent.Post event) {
            var client = Minecraft.getInstance();
            while (OPEN.consumeClick()) {
                if (client.player != null && client.screen == null) client.setScreen(new MultiblockGuideScreen());
            }
        }
        @SubscribeEvent public static void interact(PlayerInteractEvent.RightClickBlock event) {
            if (!event.getLevel().isClientSide || !event.getEntity().isShiftKeyDown()
                    || event.getHand() != net.minecraft.world.InteractionHand.MAIN_HAND) return;
            // Live controllers own both click modes. The separate guide remains available on G.
            if(event.getLevel().getBlockEntity(event.getPos())!=null)return;
            var id = BuiltInRegistries.BLOCK.getKey(event.getLevel().getBlockState(event.getPos()).getBlock());
            // Do not attach apiary plans to the unrelated Tweaks teleporter gate.
            boolean supported = id.getNamespace().equals("aeroapiary") && id.getPath().contains("controller");
            if (supported) {
                Minecraft.getInstance().execute(() -> Minecraft.getInstance().setScreen(new MultiblockGuideScreen()));
            }
        }
    }
    private MultiblockGuideEvents() {}
}
