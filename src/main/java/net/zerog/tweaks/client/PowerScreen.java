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
    private boolean showInputs;
    private boolean fuelFaces;
    private GeneratorRecipePanel inputs;
    public PowerScreen(PowerMenu m,Inventory inv,Component title){super(m,inv,title);imageWidth=278;imageHeight=194;inventoryLabelY=101;}
    @Override protected void init(){
        super.init();leftPos=MachineItemCatalog.machineLeft(width,imageWidth,showInputs);
        if(inputs==null)inputs=new GeneratorRecipePanel(menu);
        var recipes=addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal("Recipes"),b->{showInputs=!showInputs;rebuildWidgets();}).bounds(leftPos+119,topPos+3,49,16).build());
        recipes.active=MachineItemCatalog.panelWidth(width,imageWidth)>=120;
        if(!menu.solar()){
            addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal(fuelFaces?"Show power":"Show fuel"),b->{fuelFaces=!fuelFaces;rebuildWidgets();}).bounds(leftPos+180,topPos+148,94,18).build());
        }
        var panel=fuelFaces&&!menu.solar()?new SideConfigurationPanel(leftPos+180,topPos+18,s->menu.fuelDisabled(s)?3:1,s->send(200+s*2+(menu.fuelDisabled(s)?0:1))," (Fusion Dust only)",true).labels("Fuel faces","Items only"):
            new SideConfigurationPanel(leftPos+180,topPos+18,s->menu.outputDisabled(s)?3:2,s->send((menu.outputDisabled(s)?106:100)+s)," (generator output)").outputOnly();
        addRenderableWidget(panel);
    }
    private void send(int button){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,button);}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.fill(leftPos,topPos,leftPos+176,topPos+194,0xff101b2b);g.fill(leftPos+6,topPos+18,leftPos+170,topPos+98,0xff24354b);
        if(!menu.solar()){g.fill(leftPos+25,topPos+43,leftPos+43,topPos+61,0xff08111d);g.drawString(font,"Fuel",leftPos+8,topPos+26,0xffe0eeff,false);}
        g.drawString(font,font.plainSubstrByWidth(menu.value(0)+" / "+menu.value(1)+" FE",158),leftPos+8,topPos+76,0xffe0eeff,false);
        boolean producing=menu.value(4)>0&&(menu.solar()?menu.value(0)<menu.value(1):menu.value(0)<=menu.value(1)-menu.value(4));
        g.drawString(font,(producing?menu.value(4):0)+" FE/t",leftPos+65,topPos+28,0xffb8f7ff,false);
        g.drawString(font,"Flux "+menu.value(5)+" / 3",leftPos+72,topPos+44,0xffe0eeff,false);
        g.drawString(font,font.plainSubstrByWidth(menu.solar()?(producing?"Generating / sunlight":"Idle / check sky & buffer"):"Fuel: "+menu.value(2)+" / "+menu.value(3)+" ticks",158),leftPos+8,topPos+88,0xffe0eeff,false);
        int fill=menu.value(1)>0?(int)(150L*menu.value(0)/menu.value(1)):0;g.fill(leftPos+8,topPos+65,leftPos+158,topPos+71,0xff08111d);g.fillGradient(leftPos+8,topPos+65,leftPos+8+fill,topPos+71,0xffaef5ff,0xff655edd);
        for(var slot:menu.slots)g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff08111d);
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,font.plainSubstrByWidth(title.getString(),105),titleLabelX,titleLabelY,0xffe0eeff,false);g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe0eeff,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(showInputs)inputs.render(g,font,leftPos,topPos,width,imageWidth,x,y);if(x>=leftPos+8&&x<leftPos+166&&y>=topPos+65&&y<topPos+86)g.renderTooltip(font,Component.literal(menu.value(0)+" / "+menu.value(1)+" FE"),x,y);int sx=menu.solar()?26:48;if(isHovering(sx,44,16,16,x,y))g.renderTooltip(font,Component.literal("Generator Flux Modules (maximum 3). Drain stored FE below the smaller buffer before removing a module."),x,y);}
    private boolean recipeArea(double x,double y){return showInputs&&inputs.contains(x,y,leftPos,topPos,width,imageWidth);}
    private void cancelRecipeDrag(){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();}
    @Override public boolean mouseClicked(double x,double y,int button){if(recipeArea(x,y)){cancelRecipeDrag();return inputs.click(x,y,button,leftPos,topPos,width,imageWidth);}return super.mouseClicked(x,y,button);}
    @Override protected boolean hasClickedOutside(double x,double y,int left,int top,int button){return !recipeArea(x,y)&&super.hasClickedOutside(x,y,left,top,button);}
    @Override public boolean mouseDragged(double x,double y,int button,double dx,double dy){if(recipeArea(x,y)){cancelRecipeDrag();return true;}return super.mouseDragged(x,y,button,dx,dy);}
    @Override public boolean mouseReleased(double x,double y,int button){if(recipeArea(x,y))cancelRecipeDrag();return super.mouseReleased(x,y,button);}
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical){if(showInputs&&inputs.scroll(x,y,vertical,leftPos,topPos,width,imageWidth))return true;return super.mouseScrolled(x,y,horizontal,vertical);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {@SubscribeEvent public static void screens(RegisterMenuScreensEvent e){e.register(PowerRegistry.MENU.get(),PowerScreen::new);}}
}
