package net.zerog.tweaks.client;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.zerog.tweaks.genetics.*;

public final class AlvearyRuntimeScreen extends AbstractContainerScreen<AlvearyMenu> {
    private static final ResourceLocation BG=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/alveary_controller_runtime.png"),ATLAS=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/alveary_controller_widgets.png");
    private boolean genome;
    private boolean showRecipes;private AlvearyRecipePanel recipes;
    private final RecipeBrowser browser=new RecipeBrowser();
    public AlvearyRuntimeScreen(AlvearyMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=256;imageHeight=250;inventoryLabelX=48;inventoryLabelY=158;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){
        super.init();leftPos=MachineItemCatalog.machineLeft(width,imageWidth,showRecipes);
        if(recipes==null){recipes=new AlvearyRecipePanel(menu);AlvearyRecipeSync.clientState=null;}
        if(browser.init(width,height,recipes,w->addRenderableWidget(w),this::rebuildWidgets))return;
        net.zerog.tweaks.event.AlvearyMenuSync.clientState=new net.zerog.tweaks.event.AlvearyMenuSync.State(-1,0,false,"");
        addRenderableWidget(Button.builder(Component.literal("Recipes"),b->{cancelRecipeDrag();browser.open();rebuildWidgets();}).bounds(leftPos+78,topPos+2,58,14).build());
        addRenderableWidget(Button.builder(Component.literal("?"),b->genome=!genome).bounds(leftPos+19,topPos+76,12,12).build());
        addRenderableWidget(Button.builder(Component.literal("E"),b->send(0)).bounds(leftPos+139,topPos+79,12,12).build());
        addRenderableWidget(Button.builder(Component.literal("S"),b->send(1)).bounds(leftPos+181,topPos+79,12,12).build());
        addRenderableWidget(Button.builder(Component.literal(">"),b->send(2)).bounds(leftPos+167,topPos+79,12,12).build());
        addRenderableWidget(Button.builder(Component.literal("V"),b->send(hasShiftDown()?4:3)).bounds(leftPos+153,topPos+79,12,12).build());
    }
    private void sprite(GuiGraphics g,int u,int v,int w,int h,int x,int y){g.blit(ATLAS,leftPos+x,topPos+y,u,v,w,h,256,256);}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.blit(BG,leftPos,topPos,0,0,256,250,256,256);
        if(menu.slots.get(1).getItem().isEmpty())sprite(g,80,82,18,18,16,54);
        for(int i=menu.value(2);i<27;i++)sprite(g,60,82,18,18,11+i%9*18,98+i/9*18);
        sprite(g,80,82,6,62,44,22); // Actual API exposes endurance, not a lifetime counter.
        int cycle=menu.value(4)>0?Math.min(64,menu.value(3)*64/menu.value(4)):0;if(cycle>0)sprite(g,36,64-cycle,4,cycle,55,87-cycle);
        if(menu.value(0)<3){sprite(g,80,82,8,62,205,22);sprite(g,80,82,14,62,216,22);}else {int h=Math.min(60,menu.value(5)*100*60/(50000*menu.value(0)));if(h>0)sprite(g,42,60-h,6,h,206,83-h);int honey=menu.value(6)*60/8000;if(honey>0)sprite(g,50,60-honey,12,honey,217,83-honey);}
        if(menu.value(0)<6)sprite(g,80,82,12,62,233,22);else{int h=menu.value(7)*60/4000;if(h>0)g.fill(leftPos+234,topPos+83-h,leftPos+244,topPos+83,0xff82e9ff);}
        if(minecraft!=null&&minecraft.level!=null){var biome=minecraft.level.getBiome(menu.machine.getBlockPos()).value();int temp=Math.max(0,Math.min(48,(int)((biome.getBaseTemperature()+.5F)/2.5F*48))),humidity=Math.max(0,Math.min(48,(int)(biome.getModifiedClimateSettings().downfall()*48)));if(temp>0)sprite(g,0,48-temp,8,temp,76,80-temp);if(humidity>0)sprite(g,10,48-humidity,8,humidity,96,80-humidity);}
        sprite(g,80,82,10,50,115,31);g.drawString(font,"x"+String.format(java.util.Locale.ROOT,"%.2f",menu.value(8)/100.0),leftPos+191,topPos+102,0xff554321,false);g.drawString(font,"API",leftPos+191,topPos+115,0xff554321,false);g.drawString(font,"--",leftPos+191,topPos+128,0xff554321,false);g.drawString(font,"--",leftPos+191,topPos+141,0xff554321,false);
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,"Alveary T"+menu.value(0),8,5,0x404040,false);g.drawString(font,font.plainSubstrByWidth(status(),100),142,5,0x404040,false);g.drawString(font,"Inventory",48,158,0x404040,false);}
    private String status(){return switch(menu.value(1)){case 13->"Honey tank blocked";case 12->"Structure incomplete";case 11->"Needs FE";case 10->"Outputs full";case 8->"Resting";case 9->"Rain";case 1->"Missing supported bee / recipe";default->"Working";};}
    @Override public void render(GuiGraphics g,int x,int y,float partial){if(browser.render(g,font,width,height,x,y,partial,recipes,renderables))return;super.render(g,x,y,partial);renderTooltip(g,x,y);
        if(showRecipes)recipes.render(g,font,leftPos,topPos,width,imageWidth,x,y);
        var formation=net.zerog.tweaks.event.AlvearyMenuSync.clientState;
        if(isHovering(142,3,106,12,x,y)&&menu.value(1)==13)
            g.renderComponentTooltip(font,List.of(Component.literal("Honey tank blocked"),Component.literal("Drain the tank: each cycle needs250mB free for "+AlvearyRuntime.cycleHoney(menu.machine).getHoverName().getString()+". Different honey types cannot mix.")),x,y);
        if(isHovering(142,3,106,12,x,y)&&menu.value(1)==12){
            String reason=formation.menu()==menu.containerId&&!formation.error().isBlank()?formation.error():"Waiting for structure diagnostics";
            g.renderComponentTooltip(font,List.of(Component.literal("Structure incomplete"),Component.literal(reason)),x,y);
        }
        if(genome&&isHovering(7,16,124,78,x,y)){var lines=new ArrayList<Component>();var specimen=menu.slots.get(0).getItem();var genes=ProductiveBeeGenes.read(specimen);if(genes.isEmpty())lines.add(Component.literal("Orbital species: "+AlvearyRuntime.species(specimen)+" (no genome exposed)"));else genes.forEach((gene,value)->lines.add(Component.literal(gene+": "+value)));lines.add(Component.literal("No native lifespan / temperature allele exposed"));g.renderComponentTooltip(font,lines,x,y);}
        if(isHovering(201,16,48,78,x,y))g.renderTooltip(font,Component.literal("FE "+menu.value(5)*100+" | Honey "+menu.value(6)+"mB | Catalyst "+menu.value(7)+"mB"),x,y);
        if(isHovering(139,79,54,12,x,y))g.renderTooltip(font,Component.literal("Eject "+((menu.value(10)&1)!=0?"ON":"OFF")+" | Void "+((menu.value(10)&2)!=0?"ON":"OFF")+" | "+(menu.recoveryPage()?"Legacy recovery":("Products "+(menu.value(9)+1)+"/"+menu.outputPages()))+" | S: compact; >: page; Shift+V: confirm void"),x,y);
        if(isHovering(12,22,26,26,x,y))g.renderTooltip(font,Component.literal("Supported orbital bee or captured Productive Bees specimen; one bee"),x,y);
        if(isHovering(16,54,18,18,x,y))g.renderTooltip(font,Component.literal("Legacy item recovery only; drone breeding is not implemented"),x,y);
        if(isHovering(139,22,54,54,x,y))g.renderTooltip(font,Component.literal(menu.recoveryPage()?"Recover items from old frame positions; extraction only":"Production outputs only; no manual insertion"),x,y);
    }
    private boolean recipeArea(double x,double y){return showRecipes&&recipes.contains(x,y,leftPos,topPos,width,imageWidth);}
    private void cancelRecipeDrag(){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();}
    @Override public boolean mouseClicked(double x,double y,int button){if(browser.isOpen()){browser.click(recipes,x,y,button,width,height);for(var child:children())if(child.mouseClicked(x,y,button))return true;return true;}if(recipeArea(x,y)){cancelRecipeDrag();return recipes.click(x,y,button,leftPos,topPos,width,imageWidth);}return super.mouseClicked(x,y,button);}
    @Override protected boolean hasClickedOutside(double x,double y,int left,int top,int button){return !recipeArea(x,y)&&super.hasClickedOutside(x,y,left,top,button);}
    @Override public boolean mouseDragged(double x,double y,int button,double dx,double dy){if(browser.isOpen())return true;if(recipeArea(x,y)){cancelRecipeDrag();return true;}return super.mouseDragged(x,y,button,dx,dy);}
    @Override public boolean mouseReleased(double x,double y,int button){if(browser.consumeRelease(button))return true;if(recipeArea(x,y))cancelRecipeDrag();return super.mouseReleased(x,y,button);}
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical){if(browser.isOpen())return browser.scroll(recipes,x,y,vertical,width,height);if(showRecipes&&recipes.scroll(x,y,vertical,leftPos,topPos,width,imageWidth))return true;return super.mouseScrolled(x,y,horizontal,vertical);}
    @Override public boolean keyPressed(int key,int scan,int modifiers){return browser.key(key,this::rebuildWidgets)||super.keyPressed(key,scan,modifiers);}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration {@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(AlvearyRegistry.MENU.get(),AlvearyRuntimeScreen::new);}}
}
