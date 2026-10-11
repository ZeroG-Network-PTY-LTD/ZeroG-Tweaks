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
import net.zerog.tweaks.machine.*;
/** Server-synchronized three-tank panel, never client-selected production rates. */
public final class GasSeparatorScreen extends AbstractContainerScreen<GasSeparatorMenu> {
    private boolean recipe;
    public GasSeparatorScreen(GasSeparatorMenu m,Inventory i,Component t){super(m,i,t);imageWidth=392;imageHeight=246;inventoryLabelY=152;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){super.init();
        addRenderableWidget(Button.builder(Component.literal("Recipe"),b->recipe=!recipe).bounds(leftPos+112,topPos+104,68,18).build());
        var panel=new SideConfigurationPanel(leftPos+292,topPos+22,s->menu.value(20+s)==1?1:3,s->send(10+s),"",true);addRenderableWidget(panel);
        String[] faces={"D","U","N","S","W","E"};
        for(int side=0;side<6;side++){int selected=side;addRenderableWidget(Button.builder(Component.literal(faces[side]),b->send(selected)).bounds(leftPos+194+(side%2)*46,topPos+40+(side/2)*26,44,20).build());}
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xff10202c);
        for(int tank=0;tank<3;tank++){int xx=leftPos+18+tank*54,amount=menu.value(2+tank),height=amount*48/16000;g.fill(xx,topPos+31,xx+34,topPos+81,0xff07121b);g.fillGradient(xx+1,topPos+80-height,xx+33,topPos+80,tank==0?0xff50a4dc:tank==1?0xffb080ed:0xff65e0ea,0xff29465c);g.drawString(font,new String[]{"Water","H2","O2"}[tank],xx,topPos+20,0xffddedf5,false);g.drawString(font,amount+" mB",xx,topPos+83,0xffc9dce7,false);g.drawString(font,amount*100/16000+"% fill",xx,topPos+94,0xff94aabb,false);}
        g.fill(leftPos+18,topPos+133,leftPos+180,topPos+139,0xff06101a);g.fill(leftPos+18,topPos+133,leftPos+18+(int)((long)menu.value(5)*162/Math.max(1,menu.value(6))),topPos+139,0xff75dae6);
        for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff426071);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff172d3c);}
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){
        g.drawString(font,title,10,7,0xffecf6fc,false);g.drawString(font,"Fluid faces",194,22,0xffdaedf7,false);
        String[] names={"Off","Water","H2","O2"};int[] colors={0xff82909c,0xffef8790,0xffba94f1,0xff72e0e9};for(int side=0;side<6;side++){int role=Math.max(0,Math.min(3,menu.value(14+side)));g.drawString(font,names[role],194+(side%2)*46,62+(side/2)*26,colors[role],false);}
        g.drawString(font,"FE "+menu.energy()+" / 200000",194,130,0xffb9e8f5,false);
        g.drawString(font,new String[]{"Working","Needs water","Needs FE","Output full"}[Math.max(0,Math.min(3,menu.value(9)))],18,143,0xffb8cdd8,false);g.drawString(font,"Inventory",18,152,0xffd4e5ef,false);
        if(recipe){int yy=166;g.drawString(font,"Water separation",194,yy,0xffedf6ff,false);g.drawString(font,menu.value(10)+" mB water",194,yy+12,0xffafcbe0,false);g.drawString(font,"-> "+menu.value(10)*2+" mB H2 + "+menu.value(10)+" mB O2",194,yy+24,0xffb6dded,false);g.drawString(font,"Base "+menu.baseCost()+" FE / "+menu.value(13)+"t",194,yy+36,0xffafcbe0,false);g.drawString(font,"Cards "+menu.cost()+" FE / "+menu.value(6)+"t",194,yy+48,0xffc6a3ed,false);}
    }
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(x>=leftPos+18&&x<leftPos+60&&y>=topPos+106&&y<topPos+124)g.renderTooltip(font,Component.literal("Left: Acceleration; right: Energy Coil. Tier 1–6. No Compact/Void."),x,y);for(int tank=0;tank<3;tank++)if(x>=leftPos+18+tank*54&&x<leftPos+52+tank*54&&y>=topPos+31&&y<topPos+81)g.renderTooltip(font,Component.literal((tank==0?"Water level: ":"Pressure (fullness): ")+menu.value(2+tank)*100/16000+"%. Outputs full: production pauses safely; no physical pressure simulation."),x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static final class Registration {@SubscribeEvent public static void register(RegisterMenuScreensEvent e){e.register(GasSeparatorRegistry.MENU.get(),GasSeparatorScreen::new);}}
}
