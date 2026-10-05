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
    private int fuelPage;
    private java.util.List<net.minecraft.world.item.ItemStack> fuels=java.util.List.of();
    public CombustionScreen(CombustionMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=176;imageHeight=184;inventoryLabelY=91;}
    @Override protected void init(){super.init();fuels=net.minecraft.core.registries.BuiltInRegistries.ITEM.stream().map(net.minecraft.world.item.ItemStack::new).filter(s->CombustionBlockEntity.burnTime(s)>0).sorted(java.util.Comparator.comparing(s->net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(s.getItem()).toString())).toList();addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal("Fuels"),b->{showFuels=!showFuels;}).bounds(leftPos+115,topPos+3,53,16).build());}
    @Override protected void renderBg(GuiGraphics g,float partial,int x,int y){
        g.blit(BACKGROUND,leftPos,topPos,0,0,imageWidth,imageHeight,imageWidth,imageHeight);
        int fill=menu.capacity()>0?Math.max(0,Math.min(56,menu.energy()*56/menu.capacity())):0;
        g.fillGradient(leftPos+128,topPos+78-fill,leftPos+140,topPos+78,0xffb4f7ff,0xff3e69d5);
        boolean active=menu.value(2)>0&&menu.energy()<=menu.capacity()-(menu.value(5)+3)/4;
        if(menu.value(3)>0&&menu.value(2)>0){int burn=Math.max(1,Math.min(14,menu.value(2)*14/menu.value(3)));int flicker=active&&minecraft!=null&&minecraft.level!=null?(int)(minecraft.level.getGameTime()/3%3):0;g.fillGradient(leftPos+72+flicker,topPos+51-burn,leftPos+86-flicker,topPos+51,active?0xffffef98:0xff9a957e,active?0xffff713a:0xff706553);}
        g.fill(leftPos+94,topPos+36,leftPos+100,topPos+42,active?0xff70ec9a:0xff737d87);
        g.drawString(font,active?"ON 1 fuel-tick/t":menu.value(2)>0?"PAUSED / buffer full":"OFF / needs fuel",leftPos+8,topPos+54,0xffe6f4ff,false);
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_fuel"),leftPos+30,topPos+24,0xffe6f4ff,false);
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_modules",menu.value(4)),leftPos+8,topPos+65,0xffe6f4ff,false);
        int numerator=active?menu.value(5):0;String rate=numerator/4+switch(numerator%4){case 1->".25";case 2->".5";case 3->".75";default->"";};
        g.drawString(font,Component.translatable("gui.zerog_tweaks.generator_output",rate),leftPos+8,topPos+78,0xffe6f4ff,false);
        if(showFuels){int xx=leftPos+imageWidth+4;g.fill(xx,topPos,xx+174,topPos+184,0xee142735);g.drawString(font,"Fuels / no dust",xx+6,topPos+6,0xffe6f4ff,false);for(int row=0;row<6;row++){int i=fuelPage*6+row;if(i>=fuels.size())break;var stack=fuels.get(i);int yy=topPos+23+row*24;g.renderItem(stack,xx+6,yy);g.drawString(font,font.plainSubstrByWidth(stack.getHoverName().getString(),140),xx+26,yy,0xffe6f4ff,false);g.drawString(font,CombustionBlockEntity.burnTime(stack)+" ticks/item",xx+26,yy+10,0xff9edbda,false);}g.drawString(font,"Click here: next page",xx+6,topPos+170,0xff9edbda,false);}
    }
    @Override public boolean mouseClicked(double x,double y,int button){if(showFuels&&x>=leftPos+imageWidth+4&&x<leftPos+imageWidth+178&&y>=topPos&&y<topPos+184){fuelPage=(fuelPage+1)%Math.max(1,(fuels.size()+5)/6);return true;}return super.mouseClicked(x,y,button);}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){g.drawString(font,title,titleLabelX,titleLabelY,0xffe6f4ff,false);g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe6f4ff,false);}
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);if(x>=leftPos+128&&x<leftPos+140&&y>=topPos+22&&y<topPos+78)g.renderTooltip(font,Component.literal(menu.energy()+" / "+menu.capacity()+" FE"),x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {@SubscribeEvent public static void screens(RegisterMenuScreensEvent event){event.register(CombustionRegistry.MENU.get(),CombustionScreen::new);}}
}
