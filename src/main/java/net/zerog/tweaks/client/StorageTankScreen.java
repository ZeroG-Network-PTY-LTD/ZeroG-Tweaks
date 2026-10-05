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
    private static final ResourceLocation PANEL=ResourceLocation.parse("zerog_tweaks:textures/gui/fluid_tank.png");
    public StorageTankScreen(StorageTankMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=276;imageHeight=204;inventoryLabelY=113;}
    @Override protected void init(){super.init();addRenderableWidget(new SideConfigurationPanel(leftPos+182,topPos+30,menu::mode,action->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,action);},""));}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){g.blit(PANEL,leftPos,topPos,0,0,176,204,176,204);int width=(int)(160L*menu.amount()/menu.tank.capacity());var fluid=menu.fluid();if(!fluid.isEmpty()){var ext=net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions.of(fluid.getFluid());var id=ext.getStillTexture(fluid);int tint=ext.getTintColor(fluid);if((tint>>>24)==0)tint|=0xff000000;if(id!=null){var sprite=minecraft.getTextureAtlas(net.minecraft.world.inventory.InventoryMenu.BLOCK_ATLAS).apply(id);com.mojang.blaze3d.systems.RenderSystem.setShaderColor(((tint>>16)&255)/255F,((tint>>8)&255)/255F,(tint&255)/255F,((tint>>>24)&255)/255F);try{for(int dx=0;dx<width;dx+=10)g.blit(leftPos+8+dx,topPos+58,0,Math.min(10,width-dx),10,sprite);}finally{com.mojang.blaze3d.systems.RenderSystem.setShaderColor(1,1,1,1);}}else g.fill(leftPos+8,topPos+58,leftPos+8+width,topPos+68,tint);}}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,"Fluid Storage Tank",8,6,0xffd8ecfa,false);var fluid=menu.fluid();String name=fluid.isEmpty()?"Empty":fluid.getHoverName().getString();g.drawString(font,font.plainSubstrByWidth(name,160),8,24,0xffd8ecfa,false);g.drawString(font,String.format(java.util.Locale.ROOT,"%,d / %,d mB",menu.amount(),menu.tank.capacity()),8,40,0xffd8ecfa,false);g.drawString(font,"Inventory",8,113,0xffd8ecfa,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)public static class Registration{@SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(StorageTankRegistry.MENU.get(),StorageTankScreen::new);}}
}
