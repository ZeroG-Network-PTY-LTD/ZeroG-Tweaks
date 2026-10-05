package net.zerog.tweaks.client;

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
import net.zerog.tweaks.storage.*;

public final class StorageTankScreen extends AbstractContainerScreen<StorageTankMenu> {
    private static final ResourceLocation PANEL=ResourceLocation.parse("zerog_tweaks:textures/gui/fluid_tank.png");private final Button[] faces=new Button[6];
    public StorageTankScreen(StorageTankMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=176;imageHeight=204;inventoryLabelY=113;}
    @Override protected void init(){super.init();for(int i=0;i<6;i++){final int action=i;faces[i]=addRenderableWidget(Button.builder(Component.empty(),button->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,action);}).bounds(leftPos+8+(i%3)*54,topPos+76+(i/3)*21,50,18).build());}}
    @Override protected void containerTick(){super.containerTick();String[] names={"D","U","N","S","W","E"},modes={"Both","In","Out","Off"};for(int i=0;i<6;i++)faces[i].setMessage(Component.literal(names[i]+": "+modes[menu.mode(i)]));}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.blit(PANEL,leftPos,topPos,0,0,176,204,176,204);int width=(int)(160L*menu.amount()/menu.tank.capacity());g.fill(leftPos+8,topPos+58,leftPos+8+width,topPos+68,0xff68cddb);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,"Fluid Storage Tank",8,6,0xffd8ecfa,false);var fluid=menu.fluid();String name=fluid.isEmpty()?"Empty":fluid.getHoverName().getString();g.drawString(font,font.plainSubstrByWidth(name,160),8,24,0xffd8ecfa,false);g.drawString(font,String.format(java.util.Locale.ROOT,"%,d / %,d mB",menu.amount(),menu.tank.capacity()),8,40,0xffd8ecfa,false);g.drawString(font,"Inventory",8,113,0xffd8ecfa,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)public static class Registration{@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(StorageTankRegistry.MENU.get(),StorageTankScreen::new);}}
}
