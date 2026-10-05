package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.zerog.tweaks.travel.SurvivalGateMenu;
import net.zerog.tweaks.travel.SurvivalGateBlockEntity;
import net.zerog.tweaks.travel.SurvivalGateLayout;
import net.zerog.tweaks.travel.SurvivalGates;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

/** Paginated destinations, live charge/tier and ready controls; no optimistic client actions. */
public final class SurvivalGateScreen extends AbstractContainerScreen<SurvivalGateMenu> {
    private int page;
    public SurvivalGateScreen(SurvivalGateMenu menu,Inventory inventory,Component title){super(menu,inventory,title);imageWidth=256;imageHeight=252;inventoryLabelY=158;}
    private void send(int button){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,button);}
    @Override protected void init(){super.init();buttons();}
    private void buttons(){
        clearWidgets();var ids=SurvivalGateBlockEntity.destinations();
        for(int row=0;row<4;row++){
            int index=page*4+row;if(index>=ids.size())break;String id=ids.get(index);
            var button=addRenderableWidget(Button.builder(Component.literal(id.substring(id.indexOf(':')+1).replace('_',' ')),b->send(index)).bounds(leftPos+18,topPos+35+row*20,220,18).build());
            button.active=menu.value(5)==1&&menu.value(6)==0&&SurvivalGateLayout.galaxy(id)<=Math.min(5,menu.value(0))&&menu.value(4)==0;
        }
        addRenderableWidget(Button.builder(Component.literal("<"),b->{page=Math.max(0,page-1);buttons();}).bounds(leftPos+18,topPos+116,22,18).build());
        addRenderableWidget(Button.builder(Component.literal(">"),b->{page=Math.min((ids.size()-1)/4,page+1);buttons();}).bounds(leftPos+43,topPos+116,22,18).build());
        addRenderableWidget(Button.builder(Component.literal("Engage"),b->send(100)).bounds(leftPos+110,topPos+137,65,18).build()).active=menu.value(5)==1&&menu.value(4)==0;
        addRenderableWidget(Button.builder(Component.literal("Ready"),b->send(101)).bounds(leftPos+178,topPos+137,60,18).build()).active=menu.value(4)>0;
        addRenderableWidget(Button.builder(Component.literal("Preview"),b->send(102)).bounds(leftPos+110,topPos+116,65,18).build()).active=menu.value(5)==1;
        addRenderableWidget(Button.builder(Component.literal("Cancel"),b->send(103)).bounds(leftPos+178,topPos+116,60,18).build()).active=menu.value(5)==1&&menu.value(4)>0;
    }
    @Override protected void containerTick(){super.containerTick();buttons();}
    @Override protected void renderBg(GuiGraphics g,float partial,int mouseX,int mouseY){
        g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xff17232f);g.fill(leftPos+2,topPos+2,leftPos+254,topPos+250,0xffd3d9de);
        int countdown=menu.value(4);
        g.drawString(font,countdown>0?"Tier "+menu.value(0)+" | Ready check: "+(countdown+19)/20+"s":"Tier "+menu.value(0)+" | "+menu.value(1)*10000+" / "+menu.value(2)*10000+" FE",leftPos+18,topPos+21,0xff243747,false);
        if(countdown>0){g.fill(leftPos+18,topPos+31,leftPos+238,topPos+33,0xff38435a);g.fill(leftPos+18,topPos+31,leftPos+18+(100-countdown)*220/100,topPos+33,0xff966ad6);}
        for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff46535c);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff87929a);}
    }
    @Override public void render(GuiGraphics g,int x,int y,float partial){super.render(g,x,y,partial);renderTooltip(g,x,y);}
    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration{@SubscribeEvent public static void screens(RegisterMenuScreensEvent event){event.register(SurvivalGates.MENU.get(),SurvivalGateScreen::new);}}
}
