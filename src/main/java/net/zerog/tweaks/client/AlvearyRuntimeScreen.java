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
    public AlvearyRuntimeScreen(AlvearyMenu menu,Inventory inv,Component title){super(menu,inv,title);imageWidth=256;imageHeight=250;inventoryLabelX=48;inventoryLabelY=158;}
    private void send(int id){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,id);}
    @Override protected void init(){super.init();addRenderableWidget(Button.builder(Component.literal("?"),b->genome=!genome).bounds(leftPos+19,topPos+76,12,12).build());addRenderableWidget(Button.builder(Component.literal("E"),b->send(0)).bounds(leftPos+139,topPos+79,12,12).build());addRenderableWidget(Button.builder(Component.literal("S"),b->send(1)).bounds(leftPos+181,topPos+79,12,12).build());addRenderableWidget(Button.builder(Component.literal(">"),b->send(2)).bounds(leftPos+167,topPos+79,12,12).build());addRenderableWidget(Button.builder(Component.literal("V"),b->send(hasShiftDown()?4:3)).bounds(leftPos+153,topPos+79,12,12).build());}
    private void sprite(GuiGraphics g,int u,int v,int w,int h,int x,int y){g.blit(ATLAS,leftPos+x,topPos+y,u,v,w,h,256,256);}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.blit(BG,leftPos,topPos,0,0,256,250,256,256);
        for(int i=menu.value(2);i<27;i++)sprite(g,60,82,18,18,11+i%9*18,98+i/9*18);
        sprite(g,80,82,6,62,44,22); // Actual API exposes endurance, not a lifetime counter.
        int cycle=menu.value(4)>0?Math.min(64,menu.value(3)*64/menu.value(4)):0;if(cycle>0)sprite(g,36,64-cycle,4,cycle,55,87-cycle);
        if(menu.value(0)<3){sprite(g,80,82,8,62,205,22);sprite(g,80,82,14,62,216,22);}else {int h=Math.min(60,menu.value(5)*100*60/(50000*menu.value(0)));if(h>0)sprite(g,42,60-h,6,h,206,83-h);int honey=menu.value(6)*60/8000;if(honey>0)sprite(g,50,60-honey,12,honey,217,83-honey);}
        if(menu.value(0)<6)sprite(g,80,82,12,62,233,22);else{int h=menu.value(7)*60/4000;if(h>0)g.fill(leftPos+234,topPos+83-h,leftPos+244,topPos+83,0xff82e9ff);}
        if(minecraft!=null&&minecraft.level!=null){var biome=minecraft.level.getBiome(menu.machine.getBlockPos()).value();int temp=Math.max(0,Math.min(48,(int)((biome.getBaseTemperature()+.5F)/2.5F*48))),humidity=Math.max(0,Math.min(48,(int)(biome.getModifiedClimateSettings().downfall()*48)));if(temp>0)sprite(g,0,48-temp,8,temp,76,80-temp);if(humidity>0)sprite(g,10,48-humidity,8,humidity,96,80-humidity);}
        sprite(g,80,82,10,50,115,31);g.drawString(font,"x"+String.format(java.util.Locale.ROOT,"%.2f",menu.value(8)/100.0),leftPos+191,topPos+102,0xff554321,false);g.drawString(font,"API",leftPos+191,topPos+115,0xff554321,false);g.drawString(font,"--",leftPos+191,topPos+128,0xff554321,false);g.drawString(font,"--",leftPos+191,topPos+141,0xff554321,false);
    }
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,"Alveary T"+menu.value(0),8,5,0x404040,false);g.drawString(font,font.plainSubstrByWidth(status(),100),142,5,0x404040,false);g.drawString(font,"Inventory",48,158,0x404040,false);}
    private String status(){return switch(menu.value(1)){case 12->"Structure incomplete";case 11->"Needs FE";case 10->"Outputs full";case 8->"Resting";case 9->"Rain";case 1->"Missing supported bee / recipe";default->"Working";};}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);
        if(genome&&isHovering(7,16,124,78,x,y)){var lines=new ArrayList<Component>();var specimen=menu.slots.get(0).getItem();var genes=ProductiveBeeGenes.read(specimen);if(genes.isEmpty())lines.add(Component.literal("Orbital species: "+AlvearyRuntime.species(specimen)+" (no genome exposed)"));else genes.forEach((gene,value)->lines.add(Component.literal(gene+": "+value)));lines.add(Component.literal("No native lifespan / temperature allele exposed"));g.renderComponentTooltip(font,lines,x,y);}
        if(isHovering(201,16,48,78,x,y))g.renderTooltip(font,Component.literal("FE "+menu.value(5)*100+" | Honey "+menu.value(6)+"mB | Catalyst "+menu.value(7)+"mB"),x,y);
        if(isHovering(139,79,54,12,x,y))g.renderTooltip(font,Component.literal("E: eject | S: compact | >: outputs/recovery page | Shift+V: confirm void excess; V: disable"),x,y);
    }
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration {@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(AlvearyRegistry.MENU.get(),AlvearyRuntimeScreen::new);}}
}
