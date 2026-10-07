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
    public TransportScreen(TransportMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=276;imageHeight=258;inventoryLabelY=164;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){super.init();if(!(menu.machine instanceof TransportBlockEntity))return;
        addRenderableWidget(new SideConfigurationPanel(leftPos+182,topPos+30,side->switch(menu.value(6+side)){case 1->2;case 2->1;case 3->3;default->0;},side->send(hasShiftDown()?20+side:10+side),"; Shift-click changes priority"));
        addRenderableWidget(Button.builder(Component.literal("Signal"),b->send(0)).bounds(leftPos+8,topPos+51,50,16).build());addRenderableWidget(Button.builder(Component.literal("Route"),b->send(1)).bounds(leftPos+62,topPos+51,50,16).build());if(menu.itemFamily()||menu.fluidFamily())addRenderableWidget(Button.builder(Component.literal("Filter"),b->send(2)).bounds(leftPos+116,topPos+51,50,16).build());
        if(menu.itemFamily()||menu.fluidFamily()){
            addRenderableWidget(Button.builder(Component.literal("Tags"),b->send(3)).bounds(leftPos+65,topPos+135,32,17).build());addRenderableWidget(Button.builder(Component.literal("Data"),b->send(4)).bounds(leftPos+99,topPos+135,32,17).build());addRenderableWidget(Button.builder(Component.literal("Clear"),b->send(5)).bounds(leftPos+133,topPos+135,35,17).build());
        }
        if(!menu.itemFamily())addRenderableWidget(Button.builder(Component.literal("Old item recovery"),b->send(6)).bounds(leftPos+8,topPos+108,112,17).build());
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xffc6c6c6);g.fill(leftPos+4,topPos+4,leftPos+imageWidth-4,topPos+28,0xff203444);g.drawString(font,menu.machine instanceof TransportBlockEntity t&&t.block().family.equals("gas_tube")?"Gas "+menu.value(2)+" / 16000 mB":"FE "+menu.energy()+(menu.fluidFamily()?" | "+menu.value(2)+" mB":""),leftPos+8,topPos+18,0xffa5efff,false);for(var slot:menu.slots){if(!slot.isActive())continue;g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff373c46);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff8b8b8b);}
        if(menu.machine instanceof TransportBlockEntity t&&!menu.itemFamily()){
            if(!menu.fluidFamily()){g.fill(leftPos+8,topPos+74,leftPos+168,topPos+82,0xff142534);int fill=(int)Math.min(160,(long)menu.energy()*160/Math.max(1,menu.capacity()));g.fillGradient(leftPos+8,topPos+74,leftPos+8+fill,topPos+82,0xff9aeaff,0xff376eb3);}
            g.drawString(font,"Limit "+menu.transferLimit()+(menu.fluidFamily()?" mB/t":" FE/t"),leftPos+8,topPos+85,0xff203444,false);
        }
    }
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(x>=leftPos+8&&x<leftPos+168&&y>=topPos+51&&y<topPos+67)g.renderTooltip(font,Component.literal("Signal: "+new String[]{"ignore","high","low","never"}[menu.value(3)]+" | Routing: "+new String[]{"nearest","round robin","random"}[menu.value(4)]+" | "+(menu.value(5)==1?"Blacklist":"Whitelist")),x,y);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,font.plainSubstrByWidth(title.getString(),260),8,6,0xffe8f7ff,false);g.drawString(font,"Inventory",8,164,0xff303844,false);if(menu.machine instanceof TransportBlockEntity){if(menu.itemFamily())g.drawString(font,"Item templates (not items)",8,94,0xff303844,false);else g.drawString(font,font.plainSubstrByWidth(menu.recoveryVisible()?"Recovery only: take old items":"No item storage",160),8,94,0xff303844,false);if(menu.fluidFamily())g.drawString(font,"Fluid templates",8,126,0xff303844,false);if(menu.itemFamily()||menu.fluidFamily())g.drawString(font,"Tags "+(menu.value(12)==1?"ON":"OFF")+" | Data "+(menu.value(13)==1?"ON":"OFF"),8,155,0xff303844,false);}}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration {@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(TransportMenus.MENU.get(),TransportScreen::new);}}
}
