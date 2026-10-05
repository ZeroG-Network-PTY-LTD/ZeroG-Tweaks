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
public final class OreRefineryScreen extends AbstractContainerScreen<OreRefineryMenu> {

    private static final ResourceLocation BG =
            ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "textures/gui/ore_refinery.png");

    public OreRefineryScreen(OreRefineryMenu menu, Inventory playerInv, Component title) {
        super(menu, playerInv, title);
        this.imageWidth = 176;
        this.imageHeight = 166;
        this.inventoryLabelY = 72;
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

        // The legacy PNG has neither inventory slots nor a safely placed progress
        // strip. Draw exact menu-bound frames instead of stretching its swatches.
        gfx.fill(x + 1, y + 1, x + 175, y + 165, 0xff172532);
        gfx.fill(x + 5, y + 18, x + 171, y + 70, 0xff0c1722);
        for (var slot : menu.slots) {
            int sx=x+slot.x-1, sy=y+slot.y-1;
            gfx.fill(sx,sy,sx+18,sy+18,0xff8096a6);
            gfx.fill(sx+1,sy+1,sx+17,sy+17,0xff101c28);
        }
        int pct = menu.progressPercent();
        gfx.fill(x + 57, y + 64, x + 145, y + 68, 0xff34424f);
        if (pct > 0) gfx.fill(x + 57, y + 64, x + 57 + 88 * pct / 100, y + 68, 0xff75dbc8);
        gfx.drawString(font, Component.translatable("gui.zerog_tweaks.refinery.input"), x+57,y+24,0xffe6f4ff,false);
        gfx.drawString(font, Component.translatable("gui.zerog_tweaks.refinery.catalyst"), x+88,y+24,0xffe6f4ff,false);
        gfx.drawString(font, Component.translatable("gui.zerog_tweaks.refinery.output"), x+128,y+24,0xffe6f4ff,false);
        gfx.drawString(font, Component.translatable("gui.zerog_tweaks.refinery.cycle",pct), x+8,y+54,0xffe6f4ff,false);
    }

    @Override protected void renderLabels(GuiGraphics gfx,int mouseX,int mouseY) {
        gfx.drawString(font,font.plainSubstrByWidth(title.getString(),160),titleLabelX,titleLabelY,0xffe6f4ff,false);
        gfx.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe6f4ff,false);
    }

    @Override public void render(GuiGraphics gfx,int mouseX,int mouseY,float partialTick) {
        super.render(gfx,mouseX,mouseY,partialTick);renderTooltip(gfx,mouseX,mouseY);
        for(int i=0;i<3;i++) {
            var slot=menu.getSlot(i);
            if(!slot.hasItem()&&isHovering(slot.x,slot.y,16,16,mouseX,mouseY)) {
                Component hint=switch(i){case 0->Component.translatable("gui.zerog_tweaks.refinery.input_hint");case 1->OreRefineryMenu.catalystHint();default->Component.translatable("gui.zerog_tweaks.refinery.output_hint");};
                gfx.renderTooltip(font,font.split(hint,230),mouseX,mouseY);
            }
        }
    }

    @EventBusSubscriber(modid = ZeroGTweaks.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static class Screens {
        @SubscribeEvent
        public static void onRegisterScreens(RegisterMenuScreensEvent event) {
            event.register(MenuInit.ORE_REFINERY.get(), OreRefineryScreen::new);
        }
    }
}
