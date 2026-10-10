package net.zerog.tweaks.client;

import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.zerog.tweaks.genetics.GeneticsMenu;
import net.zerog.tweaks.genetics.GeneticsRecipeCatalogue;

/** Separate read-only recipe region; all clicks are consumed before inventory handling. */
public final class GeneticsRecipePanel {
    private final GeneticsMenu menu;
    private final MachineItemCatalog items;
    private int tab = 1, mode, scroll;
    public GeneticsRecipePanel(GeneticsMenu menu) {
        this.menu = menu;
        items = new MachineItemCatalog(stack -> java.util.stream.IntStream.range(0, 3)
                .anyMatch(i -> menu.slots.get(i).mayPlace(stack)));
    }
    public boolean contains(double x, double y, int left, int top, int viewport, int machineWidth) {
        int width = MachineItemCatalog.panelWidth(viewport, machineWidth);
        return width >= 120 && x >= left-width-4 && x < left-4 && y >= top && y < top+224;
    }
    private java.util.List<String> lines() {
        if (tab != 2) return GeneticsRecipeCatalogue.page(menu.machineId, mode, menu.value(29), menu.value(30)).lines();
        return java.util.List.of("One card per family, tiers 1-6", "Acceleration: " + menu.value(29)/100.0 + "x",
                "Energy Coil: " + menu.value(30) + "% FE saving", "Caps: 2.5x / 30% total FE", "Compact / Void unsupported",
                "Cards never change genes or success chance", "Card changes reset job; inputs retained", "Exact crafting costs deferred");
    }
    public void render(GuiGraphics g, Font font, int left, int top, int viewport, int machineWidth, int mx, int my) {
        int width = MachineItemCatalog.panelWidth(viewport, machineWidth); if (width < 120) return;
        int x = left-width-4;
        g.fill(x, top, x+width, top+224, 0xee142735);
        String[] tabs = {"Items", "Recipes", "Upgrades"};
        for (int i=0; i<3; i++) {
            int tx = x+i*width/3;
            g.fill(tx, top, tx+width/3-1, top+18, i==tab?0xff365675:0xff24354b);
            g.drawString(font, font.plainSubstrByWidth(tabs[i], width/3-4), tx+2, top+5, 0xffe6f4ff, false);
        }
        if (tab==0) {items.render(g,font,left,top+20,viewport,machineWidth,mx,my,"Accepted reagents");return;}
        var lines = lines(); scroll = Math.clamp(scroll, 0, Math.max(0, lines.size()-9));
        for (int i=0; i<9 && i+scroll<lines.size(); i++) {
            int y = top+24+i*19; String line = lines.get(i+scroll);
            g.drawString(font, font.plainSubstrByWidth(line,width-10),x+5,y,0xffe6f4ff,false);
            if (mx>=x && mx<x+width && my>=y && my<y+18) g.renderTooltip(font,Component.literal(line),mx,my);
        }
        String footer = tab==2?"Scroll for details":menu.machineId.equals("genetic_splicer")?"Splice / scroll for details":(mode==0?"Analyse":"Sample")+" / click to switch";
        g.fill(x,top+204,x+width,top+224,0xff24354b);
        g.drawString(font,font.plainSubstrByWidth(footer,width-8),x+4,top+210,0xff9edbda,false);
    }
    public boolean click(double x,double y,int button,int left,int top,int viewport,int machineWidth) {
        if (!contains(x,y,left,top,viewport,machineWidth)) return false;
        if (button!=0) return true;
        int width=MachineItemCatalog.panelWidth(viewport,machineWidth),start=left-width-4;
        if(y<top+18){tab=Math.min(2,(int)((x-start)*3/width));scroll=0;}
        else if(tab==0)items.click(x,y,left,top+20,viewport,machineWidth);
        else if(tab==1&&y>=top+204&&!menu.machineId.equals("genetic_splicer")){mode=1-mode;scroll=0;}
        return true;
    }
    public boolean scroll(double x,double y,double delta,int left,int top,int viewport,int machineWidth) {
        if(!contains(x,y,left,top,viewport,machineWidth))return false;
        if(tab!=0)scroll=Math.clamp(scroll+(delta>0?-1:delta<0?1:0),0,Math.max(0,lines().size()-9));
        return true;
    }
}
