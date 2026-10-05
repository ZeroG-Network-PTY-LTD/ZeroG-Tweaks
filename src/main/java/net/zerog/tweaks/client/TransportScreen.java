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
import net.zerog.tweaks.transport.TransportMenu;
import net.zerog.tweaks.transport.TransportMenus;
import net.zerog.tweaks.transport.TransportBlockEntity;

public final class TransportScreen extends AbstractContainerScreen<TransportMenu> {
    public TransportScreen(TransportMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=176;imageHeight=258;inventoryLabelY=164;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){super.init();if(!(menu.machine instanceof TransportBlockEntity))return;
        for(int i=0;i<6;i++){final int side=i;addRenderableWidget(Button.builder(Component.literal(net.minecraft.core.Direction.values()[i].getName().substring(0,1).toUpperCase()),b->send(hasShiftDown()?20+side:10+side)).bounds(leftPos+8+i*27,topPos+32,25,16).build());}
        addRenderableWidget(Button.builder(Component.literal("Signal"),b->send(0)).bounds(leftPos+8,topPos+51,50,16).build());addRenderableWidget(Button.builder(Component.literal("Route"),b->send(1)).bounds(leftPos+62,topPos+51,50,16).build());addRenderableWidget(Button.builder(Component.literal("Filter"),b->send(2)).bounds(leftPos+116,topPos+51,50,16).build());
        addRenderableWidget(Button.builder(Component.literal("Tags"),b->send(3)).bounds(leftPos+65,topPos+135,32,17).build());addRenderableWidget(Button.builder(Component.literal("Data"),b->send(4)).bounds(leftPos+99,topPos+135,32,17).build());addRenderableWidget(Button.builder(Component.literal("Clear"),b->send(5)).bounds(leftPos+133,topPos+135,35,17).build());
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xffc6c6c6);g.fill(leftPos+4,topPos+4,leftPos+imageWidth-4,topPos+28,0xff203444);g.drawString(font,"FE "+menu.energy()+" | "+menu.value(2),leftPos+8,topPos+18,0xffa5efff,false);for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff373c46);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff8b8b8b);}}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(menu.machine instanceof TransportBlockEntity&&x>=leftPos+8&&x<leftPos+170&&y>=topPos+32&&y<topPos+48){int side=Math.min(5,(x-leftPos-8)/27);g.renderTooltip(font,Component.literal(new String[]{"Normal","Push","Pull","Disabled"}[menu.value(6+side)]),x,y);}if(y>=topPos+51&&y<topPos+67)g.renderTooltip(font,Component.literal("Signal: "+new String[]{"ignore","high","low","never"}[menu.value(3)]+" | Routing: "+new String[]{"nearest","round robin","random"}[menu.value(4)]+" | "+(menu.value(5)==1?"Blacklist":"Whitelist")),x,y);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,title,8,6,0xffe8f7ff,false);g.drawString(font,"Inventory",8,164,0xff303844,false);if(menu.machine instanceof TransportBlockEntity){g.drawString(font,"Item templates (not items)",8,94,0xff303844,false);g.drawString(font,"Fluid templates",8,126,0xff303844,false);g.drawString(font,"Tags "+(menu.value(12)==1?"ON":"OFF")+" | Data "+(menu.value(13)==1?"ON":"OFF"),8,155,0xff303844,false);}}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration {@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(TransportMenus.MENU.get(),TransportScreen::new);}}
}
