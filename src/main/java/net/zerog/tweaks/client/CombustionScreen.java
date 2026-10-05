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
import net.zerog.tweaks.machine.*;

public final class CombustionScreen extends AbstractContainerScreen<CombustionMenu> {
    private static final ResourceLocation BACKGROUND=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/combustion_generator.png");
    public CombustionScreen(CombustionMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=176;imageHeight=184;inventoryLabelY=91;}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.blit(BACKGROUND,leftPos,topPos,0,0,imageWidth,imageHeight,imageWidth,imageHeight);
        int fill=menu.capacity()>0?Math.max(0,Math.min(56,menu.energy()*56/menu.capacity())):0;
        g.fillGradient(leftPos+128,topPos+78-fill,leftPos+140,topPos+78,0xffb4f7ff,0xff3e69d5);
        if(menu.value(3)>0&&menu.value(2)>0){int burn=Math.max(1,Math.min(14,menu.value(2)*14/menu.value(3)));g.fillGradient(leftPos+72,topPos+51-burn,leftPos+86,topPos+51,0xffffef98,0xffff713a);}
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_fuel"),leftPos+30,topPos+24,0xffe6f4ff,false);
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_modules",menu.value(4)),leftPos+8,topPos+65,0xffe6f4ff,false);
        int numerator=menu.value(5);String rate=numerator/4+switch(numerator%4){case 1->".25";case 2->".5";case 3->".75";default->"";};
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_output",rate),leftPos+8,topPos+78,0xffe6f4ff,false);
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,title,titleLabelX,titleLabelY,0xffe6f4ff,false);g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe6f4ff,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(x>=leftPos+128&&x<leftPos+140&&y>=topPos+22&&y<topPos+78)g.renderTooltip(font,Component.literal(menu.energy()+" / "+menu.capacity()+" FE"),x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {@SubscribeEvent public static void screens(RegisterMenuScreensEvent event){event.register(CombustionRegistry.MENU.get(),CombustionScreen::new);}}
}
