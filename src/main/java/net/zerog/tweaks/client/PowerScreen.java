package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.zerog.tweaks.power.*;

public final class PowerScreen extends AbstractContainerScreen<PowerMenu> {
    public PowerScreen(PowerMenu m,Inventory inv,Component title){super(m,inv,title);imageWidth=176;imageHeight=194;inventoryLabelY=101;}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.fill(leftPos,topPos,leftPos+176,topPos+194,0xff101b2b);g.fill(leftPos+6,topPos+18,leftPos+170,topPos+98,0xff24354b);
        if(!menu.solar()){g.fill(leftPos+25,topPos+43,leftPos+43,topPos+61,0xff08111d);g.drawString(font,"Fusion Dust",leftPos+8,topPos+26,0xffe0eeff,false);}
        g.drawString(font,menu.value(0)+" / "+menu.value(1)+" FE",leftPos+8,topPos+76,0xffe0eeff,false);
        g.drawString(font,menu.value(4)+" FE/t",leftPos+65,topPos+28,0xffb8f7ff,false);
        g.drawString(font,"Flux "+menu.value(5)+" / 3",leftPos+65,topPos+44,0xffe0eeff,false);
        g.drawString(font,menu.solar()?"Daylight + clear sky":"Fuel: "+menu.value(2)+" / "+menu.value(3)+" ticks",leftPos+8,topPos+88,0xffe0eeff,false);
        int fill=menu.value(1)>0?(int)(150L*menu.value(0)/menu.value(1)):0;g.fill(leftPos+8,topPos+65,leftPos+158,topPos+71,0xff08111d);g.fillGradient(leftPos+8,topPos+65,leftPos+8+fill,topPos+71,0xffaef5ff,0xff655edd);
        for(var slot:menu.slots)g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff08111d);
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,title,titleLabelX,titleLabelY,0xffe0eeff,false);g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe0eeff,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {@SubscribeEvent public static void screens(RegisterMenuScreensEvent e){e.register(PowerRegistry.MENU.get(),PowerScreen::new);}}
}
