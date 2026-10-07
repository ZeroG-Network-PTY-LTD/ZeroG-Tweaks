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
    private boolean showRecipes;
    private boolean lastUpgradeView,ghostPressed;
    private ProcessingRecipePanel inputs;
    @Override protected void init(){
        super.init();
        leftPos=MachineItemCatalog.machineLeft(width,imageWidth,showRecipes||menu.upgradesView());
        if(inputs==null)inputs=new ProcessingRecipePanel(menu.machine);
        var catalog=addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal("Inputs"),b->{if(menu.upgradesView())send(300);showRecipes=!showRecipes;rebuildWidgets();}).bounds(leftPos+145,topPos+3,49,18).build());
        var upgrades=addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal("Upgrades"),b->{showRecipes=false;send(300);}).bounds(leftPos+80,topPos+3,63,18).build());
        upgrades.active=MachineItemCatalog.panelWidth(width,imageWidth)>=120;
        if(!upgrades.active)upgrades.setTooltip(net.minecraft.client.gui.components.Tooltip.create(Component.literal("Reduce GUI scale to make room for the upgrade filter.")));
        catalog.active=MachineItemCatalog.panelWidth(width,imageWidth)>=120;
        if(!catalog.active)catalog.setTooltip(net.minecraft.client.gui.components.Tooltip.create(Component.literal("Reduce GUI scale to make room for the input catalogue.")));
        var power=addRenderableWidget(new SideConfigurationPanel(leftPos+198,topPos+24,face->menu.value(8+face)==1?3:1,face->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,(menu.value(8+face)==1?106:100)+face);}," (power only)",true));
        var items=addRenderableWidget(new SideConfigurationPanel(leftPos+198,topPos+24,face->menu.value(14+face),face->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,200+face*5+(menu.value(14+face)+1)%5);}," (items only; Auto preserves original routing)",false,true));
        power.visible=!showItems;items.visible=showItems;
        addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal(showItems?"Show power":"Show items"),button->{showItems=!showItems;power.visible=!showItems;items.visible=showItems;button.setMessage(Component.literal(showItems?"Show power":"Show items"));}).bounds(leftPos+198,topPos+3,94,18).build());
    }
    @Override protected void renderBg(GuiGraphics g,float p,int x,int y){if(menu.upgradesView())renderVoidFilter(g,x,y);g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xFF152432);for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xFF536578);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xFF08131F);}int ticks=Math.max(1,menu.value(5));g.fill(leftPos+80,topPos+40,leftPos+80+Math.min(26,menu.value(2)*26/ticks),topPos+48,0xFF79D6E7);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,font.plainSubstrByWidth(title.getString(),68),8,7,0xE1EDF7,false);g.drawString(font,menu.machine.kind==ProcessingRegistry.Kind.CRYSTAL?"Seed / Feed":"Inputs",16,24,0xB8D6E5,false);g.drawString(font,"Outputs",120,24,0xB8D6E5,false);g.drawString(font,"Catalyst",16,59,0xB8D6E5,false);g.drawString(font,"Upgrades",120,59,0xB8D6E5,false);g.drawString(font,font.plainSubstrByWidth(menu.energy()+" / 1,000,000 FE",176),16,96,0x8BE3D9,false);g.drawString(font,font.plainSubstrByWidth((menu.value(20)/100.0)+"x  Job: "+menu.jobCost()+" FE",176),16,106,0xB8D6E5,false);g.drawString(font,"Inventory",16,116,0xB8D6E5,false);}
    @Override public void render(GuiGraphics g,int x,int y,float p){renderBackground(g,x,y,p);super.render(g,x,y,p);renderTooltip(g,x,y);if(menu.upgradesView())renderVoidTooltip(g,x,y);else if(showRecipes)inputs.render(g,font,leftPos,topPos,width,imageWidth,x,y);
        for(int i=0;i<4;i++)if(isHovering(120+i*20,72,16,16,x,y))g.renderComponentTooltip(font,java.util.List.of(Component.literal(i==0?"Acceleration cards: tiers 1–6":i==1?"Item Compact cards: tiers 1–6":i==2?"Energy Coil cards: tiers 1–6":"Void card: selected new outputs only"),Component.literal(i==0?"Configured speed bonus; maximum 2.5x.":i==1?"Input capacity: 212 / 360 / 508 / 656 / 804 / 952.":i==2?"Configured total job FE saving; maximum 30%.":"Use Upgrades to edit the saved output filter."),Component.literal("One card per family. Cards disable legacy bonuses.")),x,y);
        for(int i=0;i<menu.machine.kind.inputCount;i++){
            var slot=menu.slots.get(i);
            if(isHovering(slot.x,slot.y,16,16,x,y))g.renderComponentTooltip(font,java.util.List.of(Component.literal("Stored input: "+menu.value(21+i)+" / "+menu.value(24)),Component.literal("Reserves refill normal-sized stacks."),Component.literal("Removing the card preserves stored inputs.")),x,y);
        }
    }
    private void send(int button){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,button);}
    @Override protected void containerTick(){super.containerTick();if(lastUpgradeView!=menu.upgradesView()){lastUpgradeView=menu.upgradesView();rebuildWidgets();}}
    private int filterLeft(){return leftPos-MachineItemCatalog.panelWidth(width,imageWidth)-4;}
    private boolean filterArea(double x,double y){return menu.upgradesView()&&MachineItemCatalog.panelWidth(width,imageWidth)>=120&&x>=filterLeft()&&x<leftPos-4&&y>=topPos&&y<topPos+imageHeight;}
    private int ghostAt(double x,double y){
        if(!filterArea(x,y))return -1;
        for(int i=0;i<9;i++){int gx=filterLeft()+12+(i%3)*20,gy=topPos+64+(i/3)*20;if(x>=gx&&x<gx+16&&y>=gy&&y<gy+16)return i;}
        return -1;
    }
    private void renderVoidFilter(GuiGraphics g,int mx,int my){
        int w=MachineItemCatalog.panelWidth(width,imageWidth);if(w<120)return;int x=filterLeft();
        g.fill(x,topPos,x+w,topPos+imageHeight,0xEE142735);
        g.drawString(font,font.plainSubstrByWidth("Void output filter",w-12),x+6,topPos+8,0xE6F4FF,false);
        g.drawString(font,font.plainSubstrByWidth(menu.voidCardPresent()?"Active: new products only":"Install card in fourth socket",w-12),x+6,topPos+24,menu.voidCardPresent()?0x8BE3D9:0xFFC58A,false);
        g.drawString(font,font.plainSubstrByWidth("Click/drop: copy type",w-12),x+6,topPos+40,0xB8D6E5,false);
        g.drawString(font,font.plainSubstrByWidth("Right-click: clear",w-12),x+6,topPos+51,0xB8D6E5,false);
        for(int i=0;i<9;i++){
            int gx=x+12+(i%3)*20,gy=topPos+64+(i/3)*20;
            g.fill(gx-1,gy-1,gx+17,gy+17,0xFF536578);g.fill(gx,gy,gx+16,gy+16,0xFF08131F);
            var template=menu.voidTemplate(i);if(!template.isEmpty())g.renderItem(template,gx,gy);
        }
        g.fill(x+8,topPos+128,x+40,topPos+148,0xFF24354B);g.fill(x+w-40,topPos+128,x+w-8,topPos+148,0xFF24354B);
        g.drawString(font,"<",x+20,topPos+134,menu.voidPage()>0?0x9EDBDA:0x536578,false);
        g.drawString(font,">",x+w-26,topPos+134,menu.voidPage()<3?0x9EDBDA:0x536578,false);
        g.drawString(font,(menu.voidPage()+1)+" / 4",x+44,topPos+134,0xE6F4FF,false);
        g.drawString(font,font.plainSubstrByWidth("Scroll to change page",w-12),x+6,topPos+158,0xB8D6E5,false);
        g.drawString(font,font.plainSubstrByWidth("Stored outputs stay safe",w-12),x+6,topPos+172,0x8BE3D9,false);
    }
    private void renderVoidTooltip(GuiGraphics g,int mx,int my){
        int hovered=ghostAt(mx,my);
        if(hovered>=0){var template=menu.voidTemplate(hovered);g.renderComponentTooltip(font,java.util.List.of(template.isEmpty()?Component.literal("Empty filter entry"):template.getHoverName(),Component.literal("Matches item type, not individual item data."),Component.literal("Only newly produced matching items are discarded.")),mx,my);}
    }
    @Override public boolean mouseClicked(double x,double y,int button){
        ghostPressed=false;
        if(filterArea(x,y)){
            int ghost=ghostAt(x,y);ghostPressed=ghost>=0;
            if(ghost>=0&&menu.voidCardPresent()&&(button==0||button==1))send((button==1?420:400)+ghost);
            else if(button==0&&y>=topPos+128&&y<topPos+148){if(x<filterLeft()+40)send(301);else if(x>=leftPos-44)send(302);}
            return true;
        }
        if(showRecipes&&inputs.click(x,y,button,leftPos,topPos,width,imageWidth))return true;
        return super.mouseClicked(x,y,button);
    }
    @Override public boolean mouseReleased(double x,double y,int button){
        int ghost=ghostAt(x,y);
        if(ghost>=0&&button==0&&!ghostPressed&&!menu.getCarried().isEmpty()&&menu.voidCardPresent())send(400+ghost);
        ghostPressed=false;
        if(filterArea(x,y)){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();}
        // Release widget/drag bookkeeping without treating the side panel as an
        // outside-container drop target or distributing items through real slots.
        return super.mouseReleased(x,y,button);
    }
    @Override protected boolean hasClickedOutside(double x,double y,int guiLeft,int guiTop,int button){
        if(filterArea(x,y))return false;
        int panel=MachineItemCatalog.panelWidth(width,imageWidth);
        if(showRecipes&&panel>=120&&x>=leftPos-panel-4&&x<leftPos-4&&y>=topPos&&y<topPos+imageHeight)return false;
        return super.hasClickedOutside(x,y,guiLeft,guiTop,button);
    }
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical){if(filterArea(x,y)){if(vertical!=0&&menu.voidCardPresent())send(vertical>0?301:302);return true;}if(showRecipes&&inputs.scroll(x,y,vertical,leftPos,topPos,width,imageWidth))return true;return super.mouseScrolled(x,y,horizontal,vertical);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration{@SubscribeEvent public static void screens(RegisterMenuScreensEvent e){e.register(ProcessingRegistry.MENU.get(),ProcessingScreen::new);}}
}
