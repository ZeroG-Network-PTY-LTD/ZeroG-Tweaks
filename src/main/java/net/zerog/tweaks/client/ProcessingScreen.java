package net.zerog.tweaks.client;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.zerog.tweaks.machine.*;
public final class ProcessingScreen extends AbstractContainerScreen<ProcessingMenu>{
    public ProcessingScreen(ProcessingMenu m,Inventory i,Component t){super(m,i,t);imageWidth=294;imageHeight=208;inventoryLabelX=16;inventoryLabelY=114;}
    private boolean showItems;
    @Override protected void init(){
        super.init();
        var power=addRenderableWidget(new SideConfigurationPanel(leftPos+198,topPos+24,face->menu.value(8+face)==1?3:1,face->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,(menu.value(8+face)==1?106:100)+face);}," (power only)",true));
        var items=addRenderableWidget(new SideConfigurationPanel(leftPos+198,topPos+24,face->menu.value(14+face),face->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,200+face*5+(menu.value(14+face)+1)%5);}," (items only; Auto preserves original routing)",false,true));
        power.visible=!showItems;items.visible=showItems;
        addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal(showItems?"Show power":"Show items"),button->{showItems=!showItems;power.visible=!showItems;items.visible=showItems;button.setMessage(Component.literal(showItems?"Show power":"Show items"));}).bounds(leftPos+198,topPos+3,94,18).build());
    }
    @Override protected void renderBg(GuiGraphics g,float p,int x,int y){g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xFF152432);for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xFF536578);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xFF08131F);}int ticks=Math.max(1,menu.value(5));g.fill(leftPos+80,topPos+40,leftPos+80+Math.min(26,menu.value(2)*26/ticks),topPos+48,0xFF79D6E7);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,title,8,7,0xE1EDF7,false);g.drawString(font,menu.machine.kind==ProcessingRegistry.Kind.CRYSTAL?"Seed / Feed":"Inputs",16,24,0xB8D6E5,false);g.drawString(font,"Outputs",120,24,0xB8D6E5,false);g.drawString(font,"Catalyst",16,59,0xB8D6E5,false);g.drawString(font,"Upgrades",120,59,0xB8D6E5,false);g.drawString(font,menu.energy()+" / 1,000,000 FE",16,96,0x8BE3D9,false);g.drawString(font,(menu.value(4)/4.0)+"x  Job: "+menu.jobCost()+" FE",16,106,0xB8D6E5,false);g.drawString(font,"Inventory",16,116,0xB8D6E5,false);}
    @Override public void render(GuiGraphics g,int x,int y,float p){renderBackground(g,x,y,p);super.render(g,x,y,p);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration{@SubscribeEvent public static void screens(RegisterMenuScreensEvent e){e.register(ProcessingRegistry.MENU.get(),ProcessingScreen::new);}}
}
