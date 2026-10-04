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
import net.zerog.tweaks.genetics.GeneticsMenu;
import net.zerog.tweaks.genetics.GeneticsRuntime;
import net.zerog.tweaks.genetics.ProductiveBeeGenes;
import net.zerog.tweaks.registry.MenuInit;

/** Server synced data; vanilla menu button packets, no client-authored gene values. */
public final class GeneticsScreen extends AbstractContainerScreen<GeneticsMenu> {
    private final boolean splicer;
    private final java.util.List<Button> jobButtons=new java.util.ArrayList<>();
    private final java.util.List<Button> geneButtons=new java.util.ArrayList<>();
    public GeneticsScreen(GeneticsMenu menu,Inventory inv,Component title) {
        super(menu,inv,title);imageWidth=256;imageHeight=270;inventoryLabelX=90;inventoryLabelY=158;
        splicer=menu.machineId.equals("genetic_splicer");
    }
    private void send(int button){if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,button);}
    @Override protected void init() {
        super.init();jobButtons.clear();geneButtons.clear();
        if(!splicer)for(int i=0;i<5;i++){final int gene=i;
            geneButtons.add(addRenderableWidget(Button.builder(Component.literal(ProductiveBeeGenes.GENES[i].replace('_',' ')),b->send(10+gene)).bounds(leftPos+48,topPos+20+i*14,166,14).build()));
        }
        if(splicer)jobButtons.add(addRenderableWidget(Button.builder(Component.literal("Splice"),b->send(2)).bounds(leftPos+48,topPos+96,80,16).build()));
        else {
            jobButtons.add(addRenderableWidget(Button.builder(Component.literal("Analyse"),b->send(0)).bounds(leftPos+48,topPos+96,80,16).build()));
            jobButtons.add(addRenderableWidget(Button.builder(Component.literal("Sample"),b->send(1)).bounds(leftPos+134,topPos+96,80,16).build()));
        }
        addRenderableWidget(Button.builder(Component.literal("X"),b->send(3)).bounds(leftPos+224,topPos+96,18,16).build());
    }
    @Override protected void containerTick(){super.containerTick();for(var button:jobButtons)button.active=menu.value(6)==0;
        for(int i=0;i<geneButtons.size();i++){var button=geneButtons.get(i);button.active=menu.value(6)==0;
            button.setMessage(Component.literal((menu.value(5)==i?"> ":"")+ProductiveBeeGenes.GENES[i].replace('_',' ')));}
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int mx,int my) {
        var bg=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/workbench/"+menu.machineId+".png");
        g.blit(bg,leftPos,topPos,0,0,256,236,256,256);
        g.fill(leftPos+4,topPos+16,leftPos+252,topPos+imageHeight-4,0xffc6c6c6);
        g.fill(leftPos+42,topPos+16,leftPos+216,topPos+114,0xff24313e);
        g.fill(leftPos+48,topPos+114,leftPos+214,topPos+117,0xff111722);
        if(menu.value(1)>0)g.fill(leftPos+48,topPos+114,leftPos+48+Math.min(166,menu.value(0)*166/menu.value(1)),topPos+117,0xffdda343);
        for(var slot:menu.slots){int x=leftPos+slot.x,y=topPos+slot.y;g.fill(x-1,y-1,x+17,y+17,0xff373c46);g.fill(x,y,x+16,y+16,0xff8b8b8b);g.fill(x+1,y+1,x+16,y+16,0xff9da0a3);}
        g.drawString(font,"Inputs",leftPos+9,topPos+11,0x34303d,false);
        g.drawString(font,"Out",leftPos+220,topPos+11,0x34303d,false);
        g.drawString(font,"Legacy recovery / bottle returns",leftPos+48,topPos+119,0x34303d,false);
        if(splicer){var trait=GeneticsRuntime.serum(menu.slots.get(1).getItem());
            g.drawString(font,"Selected serum",leftPos+50,topPos+23,0xffcbe7ff,false);
            g.drawString(font,trait.getString("gene").replace('_',' '),leftPos+50,topPos+38,0xff8de8ee,false);
            g.drawString(font,trait.getString("value").replace('_',' '),leftPos+50,topPos+51,0xffc3b4ff,false);
            g.drawString(font,"Catalyst: "+menu.value(8)+"%",leftPos+50,topPos+68,0xffffd185,false);
        }
        g.drawString(font,"FE "+menu.value(2)*10+" / "+menu.value(3)*10,leftPos+48,topPos+248,0xff24313e,false);
        g.drawString(font,font.plainSubstrByWidth(status(),236),leftPos+10,topPos+258,0xff24313e,false);
    }
    @Override public void render(GuiGraphics g,int mx,int my,float partial) {
        super.render(g,mx,my,partial);renderTooltip(g,mx,my);
        var genes=ProductiveBeeGenes.read(menu.slots.get(0).getItem());
        if(!splicer&&mx>=leftPos+48&&mx<leftPos+214&&my>=topPos+20&&my<topPos+90) {
            int index=(my-topPos-20)/14;if(index<5){String gene=ProductiveBeeGenes.GENES[index];g.renderTooltip(font,Component.literal((menu.value(5)==index?"Selected: ":"")+genes.getOrDefault(gene,"No supported specimen")),mx,my);}
        }
        if(mx>=leftPos+48&&mx<leftPos+214&&my>=topPos+114&&my<topPos+118)g.renderTooltip(font,Component.literal(status()),mx,my);
        if(mx>=leftPos+10&&mx<leftPos+246&&my>=topPos+258&&my<topPos+268)g.renderTooltip(font,Component.literal(status()),mx,my);
    }
    private String status(){return switch(menu.value(7)){case 1->"Insert a filled Productive Bees cage with saved traits";case 2->"Missing reagent/catalyst";case 3->"Missing vial, selected gene or valid serum";case 4->"Output or bottle-return slots blocked";case 5->"Splicer needs 60 FE per tick";default->menu.value(6)==1?"Processing":"Ready";};}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT,bus=EventBusSubscriber.Bus.MOD)
    public static class Registration {
        @SubscribeEvent public static void register(RegisterMenuScreensEvent event){event.register(MenuInit.GENETICS.get(),GeneticsScreen::new);}
    }
}
