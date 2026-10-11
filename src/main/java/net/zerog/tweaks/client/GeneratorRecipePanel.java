package net.zerog.tweaks.client;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.zerog.tweaks.machine.CombustionMenu;
import net.zerog.tweaks.power.PowerMenu;
import net.zerog.tweaks.power.GeneratorRecipeCatalogue;
import net.zerog.tweaks.registry.ItemInit;

/** Fuel selection and exact production rules outside the inventory. */
public final class GeneratorRecipePanel implements RecipeBrowserPanel {
    @Override public int contentHeight(){return 224;}
    private final CombustionMenu combustion;
    private final PowerMenu power;
    private final MachineItemCatalog items;
    private ItemStack selected=ItemStack.EMPTY;
    private int tab=1,scroll;
    public GeneratorRecipePanel(CombustionMenu menu){
        combustion=menu;power=null;
        items=new MachineItemCatalog(s->GeneratorRecipeCatalogue.combustion(s,0).ticks()>0)
            .onSelect(s->{selected=s;tab=1;scroll=0;});
    }
    public GeneratorRecipePanel(PowerMenu menu){
        power=menu;combustion=null;
        items=new MachineItemCatalog(s->!menu.solar()&&s.is(ItemInit.FUSION_DUST.get()))
            .onSelect(s->{selected=s;tab=1;scroll=0;});
    }
    private int modules(){return combustion!=null?combustion.value(4):power.value(5);}
    private List<String> lines(){
        var lines=new ArrayList<String>();int modules=modules();
        if(tab==2){
            lines.add("Generator Flux Modules: "+modules+" / 3");
            lines.add("Each module: +25% production rate");
            lines.add("Each module: +100% base buffer");
            lines.add("Acceleration / Coil / Compact / Void unsupported");
            if(power!=null)lines.add("Drain excess FE before removing a module");
            else lines.add("Install modules using the generator interaction");
            lines.add("Module count does not change fuel duration");
            lines.add("No item output or catalyst recipe");return lines;
        }
        if(power!=null&&power.solar()){
            lines.add("Solar generation: no fuel consumed");lines.add("Module slot accepts Flux Modules only");
            lines.add("Requires skylight, daytime and visible sky");lines.add("Opaque roof blocks generation");
            lines.add("Thunder stops output; rain reduces output");lines.add("Moon/Eidolon/Solvane use server multipliers");
            lines.add("Current environment rate: "+power.value(4)+" FE/t");
            lines.add("Actual generation is limited by free buffer");
        }else{
            ItemStack fuel=selected.isEmpty()?(combustion!=null?combustion.slots.get(0).getItem():power.slots.get(0).getItem()):selected;
            if(fuel.isEmpty())fuel=new ItemStack(combustion!=null?Items.COAL:ItemInit.FUSION_DUST.get());
            var burn=combustion!=null?GeneratorRecipeCatalogue.combustion(fuel,modules):GeneratorRecipeCatalogue.fusion(power.configured(0),power.configured(1),modules,power.value(1));
            lines.add("Fuel: "+fuel.getHoverName().getString());lines.add("Input: 1 item, consumed on ignition");
            lines.add("Burn duration: "+burn.ticks()+" active ticks");lines.add("Production rate: "+burn.quarterRate()/4.0+" FE/t");
            lines.add("Fresh burn budget: "+burn.energy()+" FE");
            if(combustion!=null){lines.add("Fractional carry may add 1 FE between burns");lines.add("Dusts rejected; wood/coals and planetary fuels only");}
            else{lines.add("Fusion Dust only; no liquid/gas fuel");lines.add("Future burn uses current server configuration");lines.add("Already ignited fuel retains its saved base rate");}
            lines.add("Full buffer pauses burn; no paid fuel wasted");lines.add("Outputs: FE only; no item/byproduct");
        }
        lines.add("Power faces: Output / Off; no FE input");
        lines.add("Buffer: "+(combustion!=null?combustion.capacity():power.value(1))+" FE");
        lines.add("Automatic push limit: "+(combustion!=null?1000:power.configured(2))+" FE/t, shared");
        lines.add("Production rate is not cable transfer rate");lines.add("Read-only; no autofill or inventory changes");return lines;
    }
    public boolean contains(double x,double y,int left,int top,int viewport,int machineWidth){int w=MachineItemCatalog.panelWidth(viewport,machineWidth);return w>=120&&x>=left-w-4&&x<left-4&&y>=top&&y<top+224;}
    public void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mx,int my){
        int w=MachineItemCatalog.panelWidth(viewport,machineWidth);if(w<120)return;int x=left-w-4;
        g.fill(x,top,x+w,top+224,0xee142735);String[] tabs={"Items","Recipes","Upgrades"};
        for(int i=0;i<3;i++){int tx=x+i*w/3;g.fill(tx,top,tx+w/3-1,top+18,i==tab?0xff365675:0xff24354b);g.drawString(font,font.plainSubstrByWidth(tabs[i],w/3-4),tx+2,top+5,0xffe6f4ff,false);}
        if(tab==0){items.render(g,font,left,top+20,viewport,machineWidth,mx,my,power!=null&&power.solar()?"No fuel input":"Click fuel for its recipe");return;}
        var lines=lines();scroll=Math.clamp(scroll,0,Math.max(0,lines.size()-9));
        for(int i=0;i<9&&scroll+i<lines.size();i++){int y=top+24+i*19;String line=lines.get(scroll+i);g.drawString(font,font.plainSubstrByWidth(line,w-10),x+5,y,0xffe6f4ff,false);if(mx>=x&&mx<x+w&&my>=y&&my<y+18)g.renderTooltip(font,Component.literal(line),mx,my);}
        g.drawString(font,"Scroll / hover for details",x+4,top+210,0xff9edbda,false);
    }
    public boolean click(double x,double y,int button,int left,int top,int viewport,int machineWidth){
        if(!contains(x,y,left,top,viewport,machineWidth))return false;if(button!=0)return true;
        int w=MachineItemCatalog.panelWidth(viewport,machineWidth);
        if(y<top+18){tab=Math.min(2,(int)((x-(left-w-4))*3/w));scroll=0;}
        else if(tab==0)items.click(x,y,left,top+20,viewport,machineWidth);return true;
    }
    public boolean scroll(double x,double y,double delta,int left,int top,int viewport,int machineWidth){if(!contains(x,y,left,top,viewport,machineWidth))return false;if(tab!=0)scroll=Math.clamp(scroll+(delta>0?-1:delta<0?1:0),0,Math.max(0,lines().size()-9));return true;}
}
