package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.zerog.tweaks.machine.*;

public final class CombustionScreen extends AbstractContainerScreen<CombustionMenu> {
    private static final ResourceLocation BACKGROUND=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/combustion_generator.png");
    private boolean showFuels;
    private boolean fuelFaces;
    private MachineItemCatalog fuels;
    public CombustionScreen(CombustionMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=278;imageHeight=184;inventoryLabelY=91;}
    @Override protected void init(){
        super.init();leftPos=MachineItemCatalog.machineLeft(width,imageWidth,showFuels);
        fuels=new MachineItemCatalog(s->CombustionBlockEntity.burnTime(s)>0,s->CombustionBlockEntity.burnTime(s)+" ticks/item");
        addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal("Fuels"),b->{showFuels=!showFuels;rebuildWidgets();}).bounds(leftPos+115,topPos+3,53,16).build());
        addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal(fuelFaces?"Show power":"Show fuel"),b->{fuelFaces=!fuelFaces;rebuildWidgets();}).bounds(leftPos+180,topPos+148,94,18).build());
        addRenderableWidget(fuelFaces?new SideConfigurationPanel(leftPos+180,topPos+18,s->menu.fuelDisabled(s)?3:1,s->send(200+s*2+(menu.fuelDisabled(s)?0:1))," (fuel only)",true).labels("Fuel faces","Items only"):
            new SideConfigurationPanel(leftPos+180,topPos+18,s->menu.outputDisabled(s)?3:2,s->send((menu.outputDisabled(s)?106:100)+s)," (generator output)").outputOnly());
    }
    private void send(int button){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,button);}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.blit(BACKGROUND,leftPos,topPos,0,0,176,184,176,184);
        int fill=menu.capacity()>0?Math.max(0,Math.min(56,menu.energy()*56/menu.capacity())):0;
        g.fillGradient(leftPos+128,topPos+78-fill,leftPos+140,topPos+78,0xffb4f7ff,0xff3e69d5);
        boolean active=menu.value(2)>0&&menu.energy()<=menu.capacity()-(menu.value(5)+3)/4;
        if(menu.value(3)>0&&menu.value(2)>0){int burn=Math.max(1,Math.min(14,menu.value(2)*14/menu.value(3)));int flicker=active&&minecraft!=null&&minecraft.level!=null?(int)(minecraft.level.getGameTime()/3%3):0;g.fillGradient(leftPos+72+flicker,topPos+51-burn,leftPos+86-flicker,topPos+51,active?0xffffef98:0xff9a957e,active?0xffff713a:0xff706553);}
        g.fill(leftPos+94,topPos+36,leftPos+100,topPos+42,active?0xff70ec9a:0xff737d87);
        g.drawString(font,font.plainSubstrByWidth(active?"ON 1 fuel-tick/t":menu.value(2)>0?"PAUSED / buffer full":"OFF / needs fuel",116),leftPos+8,topPos+54,0xffe6f4ff,false);
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_fuel"),leftPos+30,topPos+24,0xffe6f4ff,false);
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_modules",menu.value(4)),leftPos+8,topPos+65,0xffe6f4ff,false);
        int numerator=active?menu.value(5):0;String rate=numerator/4+switch(numerator%4){case 1->".25";case 2->".5";case 3->".75";default->"";};
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_output",rate),leftPos+8,topPos+78,0xffe6f4ff,false);
    }
    @Override public boolean mouseClicked(double x,double y,int button){if(showFuels&&fuels.click(x,y,leftPos,topPos,width,imageWidth))return true;return super.mouseClicked(x,y,button);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,font.plainSubstrByWidth(title.getString(),103),titleLabelX,titleLabelY,0xffe6f4ff,false);g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe6f4ff,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(showFuels)fuels.render(g,font,leftPos,topPos,width,imageWidth,x,y,"Fuels / no dust");if(x>=leftPos+128&&x<leftPos+140&&y>=topPos+22&&y<topPos+78)g.renderTooltip(font,Component.literal(menu.energy()+" / "+menu.capacity()+" FE"),x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {@SubscribeEvent public static void screens(RegisterMenuScreensEvent event){event.register(CombustionRegistry.MENU.get(),CombustionScreen::new);}}
}
