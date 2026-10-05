package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.zerog.tweaks.transport.*;

public final class TransportFilterScreen extends AbstractContainerScreen<TransportFilterMenu>{
    public TransportFilterScreen(TransportFilterMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=176;imageHeight=182;inventoryLabelY=88;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){super.init();String[] labels={"List","Tags","Data","Clear"};for(int i=0;i<4;i++){final int action=i;addRenderableWidget(Button.builder(Component.literal(labels[i]),b->send(action)).bounds(leftPos+8+i*40,topPos+53,38,18).build());}}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.fill(leftPos,topPos,leftPos+176,topPos+182,0xffc6c6c6);for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff373c46);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff8b8b8b);}}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,menu.fluid?"Fluid filter card":"Item filter card",8,6,0xff303844,false);g.drawString(font,"Cursor adds; right-click clears",8,18,0xff303844,false);g.drawString(font,(menu.value(0)==1?"Blacklist":"Whitelist")+" | Tags "+menu.value(1)+" | Data "+menu.value(2),8,76,0xff303844,false);g.drawString(font,"Inventory",8,88,0xff303844,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration{@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(TransportMenus.FILTER.get(),TransportFilterScreen::new);}}
}
