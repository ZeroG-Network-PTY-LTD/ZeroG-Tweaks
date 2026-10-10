package net.zerog.tweaks.client;

import java.util.*;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.genetics.*;

/** Read-only combinations; recipes are resolved on the server, not inferred from cage icons. */
public final class AlvearyRecipePanel {
    private final AlvearyMenu menu;private int tab=1,scroll;
    private final MachineItemCatalog frames=new MachineItemCatalog(AlvearyRuntime::isFrame);
    public AlvearyRecipePanel(AlvearyMenu menu){this.menu=menu;}
    private AlvearyRecipeSync.Snapshot snapshot(){var s=AlvearyRecipeSync.clientState;return s!=null&&s.menu()==menu.containerId&&s.controller().equals(menu.machine.getBlockPos())?s:null;}
    private record Row(ItemStack icon,String text){}
    private List<Row> rows(){var rows=new ArrayList<Row>();var s=snapshot();
        if(s==null){rows.add(new Row(ItemStack.EMPTY,"Waiting for server recipe snapshot"));return rows;}
        if(tab==2){
            add(rows,"Frame slots: "+menu.value(2)+" / 27 persistent slots");
            add(rows,"Honeyed / Starlit / Starmetal: +15% each");
            add(rows,"Proven / Impregnated: +10% each");
            add(rows,"Restraint / Oblivion: -5% each");
            add(rows,"Other supported frames: +5% each");
            add(rows,"Total frame multiplier bounded x0.25 to x4");
            add(rows,"Frames change cycle time, not output counts");
            add(rows,"Acceleration / Coil / Compact / Void cards unsupported");
            add(rows,"Research / lifespan / territory rules pending");return rows;
        }
        rows.add(new Row(menu.slots.get(0).getItem(),"Input: one supported bee, retained each cycle"));
        add(rows,"Current cycle: "+s.cycle()+" active ticks");
        add(rows,"Power: "+s.feTick()+" FE/t; full cycle "+(long)s.feTick()*s.cycle()+" FE");
        add(rows,"FE budget assumes unchanged frames/catalyst");
        add(rows,"Current frame multiplier: x"+String.format(Locale.ROOT,"%.2f",menu.value(8)/100.0));
        if(s.products().isEmpty())add(rows,"No loaded production recipe for this bee");
        for(var p:s.products())rows.add(new Row(p.icon(),p.icon().getHoverName().getString()+": "+p.min()+"-"+p.max()+", "+Float.toString(p.chance()*100)+"% chance"));
        if(s.truncated())add(rows,"More than 32 product entries: display truncated");
        add(rows,"Ranges include saved PB productivity; frame bonus does not multiply yield");
        if(s.tier()>=3){add(rows,"Also produces 250 mB "+s.honey()+" each completed cycle");add(rows,"Honey tank: 8,000 mB; drain through honey port");add(rows,"Different honey types cannot mix");}
        else add(rows,"No FE requirement or cycle-honey tank at T1/T2");
        if(s.tier()>=6){add(rows,"Optional Starlight: 25 mB consumed per cycle");add(rows,"At least 25 mB: x1.2 cycle speed; currently "+(s.boosted()?"boosted":"unboosted"));add(rows,"Starlight tank: 4,000 mB; catalyst port input");}
        add(rows,"Day/night and rain may pause PB bees");add(rows,"Incomplete shell / full output / honey tank pauses work");
        add(rows,"Use service ports for power, item and fluid automation");
        add(rows,"Eject / void are existing controller controls, not card upgrades");
        add(rows,"Read-only browsing; no items moved or jobs started");return rows;
    }
    private void add(List<Row> rows,String text){rows.add(new Row(ItemStack.EMPTY,text));}
    public boolean contains(double x,double y,int left,int top,int viewport,int machineWidth){int w=MachineItemCatalog.panelWidth(viewport,machineWidth);return w>=120&&x>=left-w-4&&x<left-4&&y>=top&&y<top+250;}
    public void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mx,int my){
        int w=MachineItemCatalog.panelWidth(viewport,machineWidth);if(w<120)return;int x=left-w-4;g.fill(x,top,x+w,top+250,0xee142735);
        String[] tabs={"Items","Recipes","Upgrades"};for(int i=0;i<3;i++){int tx=x+i*w/3;g.fill(tx,top,tx+w/3-1,top+18,tab==i?0xff365675:0xff24354b);g.drawString(font,font.plainSubstrByWidth(tabs[i],w/3-4),tx+2,top+5,0xffe6f4ff,false);}
        if(tab==0){frames.render(g,font,left,top+20,viewport,machineWidth,mx,my,"Accepted frames; bee in main slot");return;}
        var rows=rows();scroll=Math.clamp(scroll,0,Math.max(0,rows.size()-10));
        for(int i=0;i<10&&scroll+i<rows.size();i++){var row=rows.get(scroll+i);int y=top+24+i*20,dx=row.icon().isEmpty()?5:24;if(!row.icon().isEmpty())g.renderItem(row.icon(),x+5,y-3);g.drawString(font,font.plainSubstrByWidth(row.text(),w-dx-5),x+dx,y,0xffe6f4ff,false);if(mx>=x&&mx<x+w&&my>=y-3&&my<y+17)g.renderTooltip(font,Component.literal(row.text()),mx,my);}
        g.drawString(font,"Scroll / hover for full details",x+4,top+236,0xff9edbda,false);
    }
    public boolean click(double x,double y,int button,int left,int top,int viewport,int machineWidth){if(!contains(x,y,left,top,viewport,machineWidth))return false;if(button!=0)return true;int w=MachineItemCatalog.panelWidth(viewport,machineWidth);if(y<top+18){tab=Math.min(2,(int)((x-(left-w-4))*3/w));scroll=0;}else if(tab==0)frames.click(x,y,left,top+20,viewport,machineWidth);return true;}
    public boolean scroll(double x,double y,double delta,int left,int top,int viewport,int machineWidth){if(!contains(x,y,left,top,viewport,machineWidth))return false;if(tab!=0)scroll=Math.clamp(scroll+(delta>0?-1:delta<0?1:0),0,Math.max(0,rows().size()-10));return true;}
}
