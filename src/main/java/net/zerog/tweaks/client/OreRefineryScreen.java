package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.MenuInit;
import net.zerog.tweaks.registry.OreRefineryMenu;

/** Ore refinery screen: 176x166, custom background, progress strip. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID, value = Dist.CLIENT)
public final class OreRefineryScreen extends AbstractContainerScreen<OreRefineryMenu> {

    private static final ResourceLocation BG =
            ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "textures/gui/ore_refinery.png");

    public OreRefineryScreen(OreRefineryMenu menu, Inventory playerInv, Component title) {
        super(menu, playerInv, title);
    }

    @Override
    protected void init() {
        super.init();
        this.imageWidth = 176;
        this.imageHeight = 166;
        this.inventoryLabelY = this.imageHeight - 94;
    }

    @Override
    protected void renderBg(GuiGraphics gfx, float partialTick, int mouseX, int mouseY) {
        int x = (this.width - this.imageWidth) / 2;
        int y = (this.height - this.imageHeight) / 2;
        gfx.blit(BG, x, y, 0, 0, this.imageWidth, this.imageHeight, 256, 256);

        int pct = this.menu.machine() != null ? this.menu.machine().progressPercent() : 0;
        if (pct > 0) {
            int w = Math.max(1, 24 * pct / 100);
            gfx.blit(BG, x + 79, y + 34, 176, 0, w, 17, 256, 256);
        }
        gfx.drawString(this.font, OreRefineryMenu.catalystHint(), x + 26, y + 56, 0x8AB0C8, false);
    }

    @EventBusSubscriber(modid = ZeroGTweaks.MODID, value = Dist.CLIENT)
    public static class Screens {
        @SubscribeEvent
        public static void onRegisterScreens(RegisterMenuScreensEvent event) {
            event.register(MenuInit.ORE_REFINERY.get(), OreRefineryScreen::new);
        }
    }
}