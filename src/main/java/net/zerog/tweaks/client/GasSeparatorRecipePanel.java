package net.zerog.tweaks.client;
import java.util.*;
import net.minecraft.client.gui.*;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.*;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.*;
/** Container icons are examples, not recipes consuming entire buckets/canisters. */
public final class GasSeparatorRecipePanel implements RecipeBrowserPanel {
    private final GasSeparatorMenu menu;
    private int tab=1,scroll;
    public GasSeparatorRecipePanel(GasSeparatorMenu menu){this.menu=menu;}
    @Override public int contentHeight(){return 224;}
    private List<String> lines(){
        var page=GasSeparatorRecipeCatalogue.page(menu);
        if(page==null)return List.of("Waiting for server recipe values");
        if(tab==2)return List.of("One card per family, tiers 1-6","Acceleration: up to 2.5x speed","Energy Coil: up to 30% FE saved","Current: "+page.energy()+" FE / "+page.ticks()+" ticks","Cards keep gas quantities unchanged","Compact / Void unsupported","Exact crafting costs deferred");
        return List.of("Input: "+page.water()+" mB water","Output: "+page.hydrogen()+" mB hydrogen","Output: "+page.oxygen()+" mB oxygen","Base: "+page.baseEnergy()+" FE / "+page.baseTicks()+" ticks","With cards: "+page.energy()+" FE / "+page.ticks()+" ticks","All resources commit together","Blocked/full output pauses safely","Water faces: input only","H2 / O2 faces: output only","Collect gas in canisters","Use gas tubes, not liquid pipes","Pressure means fullness only");
    }
    private List<ItemStack> examples(){return List.of(new ItemStack(Items.WATER_BUCKET),new ItemStack(ZGGases.CANISTER.get()),ZGGases.filled(ZGGases.HYDROGEN),ZGGases.filled(ZGGases.OXYGEN),new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("acceleration_upgrade_card_t1").get()),new ItemStack(ItemInit.MACHINE_UPGRADE_CARDS.get("energy_coil_upgrade_card_t1").get()));}
    @Override public void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mx,int my){
        int w=MachineItemCatalog.panelWidth(viewport,machineWidth);if(w<120)return;int x=left-w-4;
        g.fill(x,top,x+w,top+224,0xee142735);String[] tabs={"Items","Recipes","Upgrades"};
        for(int i=0;i<3;i++){int xx=x+i*w/3;g.fill(xx,top,xx+w/3-1,top+18,i==tab?0xff365675:0xff24354b);g.drawString(font,tabs[i],xx+2,top+5,0xffe6f4ff,false);}
        if(tab==0){var icons=examples();for(int i=0;i<icons.size();i++){var icon=icons.get(i);int y=top+24+i*26;g.renderItem(icon,x+6,y);g.drawString(font,font.plainSubstrByWidth(icon.getHoverName().getString(),w-34),x+28,y+3,0xffe6f4ff,false);if(mx>=x&&mx<x+w&&my>=y&&my<y+20)g.renderComponentTooltip(font,List.of(icon.getHoverName(),Component.literal(i<4?"Container example; recipe uses mB, not this whole item.":"One supported card per family; tiers 1-6.")),mx,my);}}
        else{var rows=lines();scroll=Math.clamp(scroll,0,Math.max(0,rows.size()-9));for(int i=0;i<9&&i+scroll<rows.size();i++){int y=top+24+i*19;String text=rows.get(i+scroll);g.drawString(font,font.plainSubstrByWidth(text,w-10),x+5,y,0xffe6f4ff,false);if(mx>=x&&mx<x+w&&my>=y&&my<y+18)g.renderTooltip(font,Component.literal(text),mx,my);}}
        g.drawString(font,"Read-only / scroll for details",x+5,top+210,0xff9edbda,false);
    }
    private boolean contains(double x,double y,int left,int top,int viewport,int machineWidth){int w=MachineItemCatalog.panelWidth(viewport,machineWidth);return w>=120&&x>=left-w-4&&x<left-4&&y>=top&&y<top+224;}
    @Override public boolean click(double x,double y,int button,int left,int top,int viewport,int machineWidth){if(!contains(x,y,left,top,viewport,machineWidth))return false;if(button==0&&y<top+18){int w=MachineItemCatalog.panelWidth(viewport,machineWidth);tab=Math.min(2,(int)((x-(left-w-4))*3/w));scroll=0;}else if(button==0&&tab==0&&y>=top+24&&y<top+180){tab=((int)(y-top-24)/26)>=4?2:1;scroll=0;}return true;}
    @Override public boolean scroll(double x,double y,double delta,int left,int top,int viewport,int machineWidth){if(!contains(x,y,left,top,viewport,machineWidth))return false;scroll=Math.clamp(scroll+(delta>0?-1:delta<0?1:0),0,Math.max(0,lines().size()-9));return true;}
}
