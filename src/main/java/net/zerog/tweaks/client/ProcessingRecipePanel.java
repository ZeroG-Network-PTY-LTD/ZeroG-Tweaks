package net.zerog.tweaks.client;

import java.util.*;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.machine.*;

/** Three read-only tabs outside player slots: clickable items, exact recipes, current upgrades. */
public final class ProcessingRecipePanel {
    private record Row(String label,List<ItemStack> alternatives,List<Component> tooltip){}
    private final ProcessingBlockEntity machine;
    private final MachineItemCatalog items;
    private int tab,page,scroll;
    private ItemStack selected=ItemStack.EMPTY;
    public ProcessingRecipePanel(ProcessingBlockEntity machine){
        this.machine=machine;
        items=new MachineItemCatalog(stack->!ProcessingRecipeCatalogue.pages(machine,stack).isEmpty())
            .onSelect(stack->{selected=stack;tab=1;page=0;scroll=0;});
    }
    private List<Row> rows(){
        var rows=new ArrayList<Row>();
        if(tab==2){
            text(rows,"Installed upgrades");
            for(int i=0;i<4;i++){
                var stack=machine.inventory.getStackInSlot(machine.kind.upgrades()+i);
                rows.add(new Row((i==0?"Acceleration":i==1?"Item Compact":i==2?"Energy Coil":"Void")+": "+(stack.isEmpty()?"none":stack.getHoverName().getString()),stack.isEmpty()?List.of():List.of(stack.copy()),List.of()));
            }
            text(rows,"Cards: tiers 1 through 6");text(rows,"One card per family");
            text(rows,"Speed now: "+machine.speedPercent()/100.0+"x");
            text(rows,"Acceleration cap: 2.5x");text(rows,"Coil saving cap: 30%");
            text(rows,"Server-configured effects");
            text(rows,machine.usesCards()?"Legacy bonuses inactive":"Legacy bonuses preserved");
            text(rows,"Old items remain recoverable");text(rows,"No new casing/dust installs");
            text(rows,"Compact: safe input reserves");text(rows,"Void: selected new outputs");text(rows,"Upgrades button edits filter");text(rows,"Crafting costs deferred");return rows;
        }
        var pages=ProcessingRecipeCatalogue.pages(machine,selected);
        if(pages.isEmpty()){text(rows,"No registered recipes");return rows;}
        page=Math.min(page,pages.size()-1);var recipe=pages.get(page);
        text(rows,recipe.id().toString());text(rows,"Shapeless: one slot each");
        for(int i=0;i<recipe.inputs().size();i++)ingredient(rows,"Input "+(i+1),recipe.inputs().get(i));
        if(recipe.catalyst().isPresent())ingredient(rows,"Catalyst",recipe.catalyst().get());else text(rows,"Catalyst: none required");
        for(var output:recipe.outputs()){
            String chance=String.format(Locale.ROOT,"%.1f%%",output.chance()*100);
            rows.add(new Row("Out: "+output.stack().getCount()+"x / "+chance,List.of(output.stack().copy()),List.of(output.stack().getHoverName(),Component.literal("Output chance: "+chance))));
        }
        text(rows,"Base: "+recipe.baseEnergy()+" FE");text(rows,"Base: "+recipe.baseTicks()+" ticks");
        text(rows,"Now: "+recipe.energy()+" FE");text(rows,"Now: "+recipe.ticks()+" ticks");
        text(rows,"Browse only; no autofill");return rows;
    }
    private static void text(List<Row> rows,String text){rows.add(new Row(text,List.of(),List.of(Component.literal(text))));}
    private static void ingredient(List<Row> rows,String role,ProcessingRecipe.Counted counted){
        var alternatives=Arrays.stream(counted.ingredient().getItems()).map(ItemStack::copy).toList();
        var tooltip=new ArrayList<Component>();tooltip.add(Component.literal(role+": "+counted.count()+"x; "+(counted.consumed()?"consumed":"reusable, not consumed")));
        tooltip.add(Component.literal("Any ONE alternative per slot:"));
        for(var stack:alternatives)tooltip.add(stack.getHoverName());
        rows.add(new Row(role+": "+counted.count()+"x "+(counted.consumed()?"used":"kept")+(alternatives.size()>1?" (OR)":""),alternatives,tooltip));
    }
    public void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mouseX,int mouseY){
        int width=MachineItemCatalog.panelWidth(viewport,machineWidth);if(width<120)return;int x=left-width-4;
        g.fill(x,top,x+width,top+208,0xee142735);
        String[] tabs={"Items","Recipes","Upgrades"};for(int i=0;i<3;i++){
            int tx=x+i*width/3;g.fill(tx,top,tx+width/3-1,top+18,i==tab?0xff365675:0xff24354b);
            g.drawString(font,font.plainSubstrByWidth(tabs[i],width/3-4),tx+2,top+5,0xffe6f4ff,false);
        }
        if(tab==0){items.render(g,font,left,top+20,viewport,machineWidth,mouseX,mouseY,"Click an item for recipes");return;}
        var rows=rows();int visible=8;scroll=Math.clamp(scroll,0,Math.max(0,rows.size()-visible));
        for(int i=0;i<visible&&scroll+i<rows.size();i++){
            var row=rows.get(scroll+i);int y=top+23+i*20;
            int labelX=x+5;
            var tips=new ArrayList<Component>(row.tooltip());
            if(!row.alternatives().isEmpty()){
                int choice=(int)((System.currentTimeMillis()/1200)%row.alternatives().size());var stack=row.alternatives().get(choice);
                g.renderItem(stack,x+5,y);g.renderItemDecorations(font,stack,x+5,y);labelX=x+25;
                if(row.tooltip().isEmpty())tips.add(stack.getHoverName());
            }
            g.drawString(font,font.plainSubstrByWidth(row.label(),x+width-5-labelX),labelX,y+4,0xffe6f4ff,false);
            if(mouseX>=x+4&&mouseX<x+width-4&&mouseY>=y&&mouseY<y+19)g.renderComponentTooltip(font,tips,mouseX,mouseY);
        }
        if(tab==1){
            String[] labels={"< "+(page+1)+"/"+Math.max(1,ProcessingRecipeCatalogue.pages(machine,selected).size()),"Next >","All"};
            for(int i=0;i<3;i++){
                int bx=x+i*width/3;g.fill(bx,top+186,bx+width/3-1,top+208,0xff24354b);
                g.drawString(font,font.plainSubstrByWidth(labels[i],width/3-6),bx+3,top+192,0xff9edbda,false);
            }
        }else g.drawString(font,"Scroll for details",x+4,top+192,0xff9edbda,false);
    }
    public boolean click(double mx,double my,int button,int left,int top,int viewport,int machineWidth){
        int width=MachineItemCatalog.panelWidth(viewport,machineWidth),x=left-width-4;
        if(width<120||mx<x||mx>=x+width||my<top||my>=top+208)return false;
        if(button!=0)return true;
        if(my<top+18){tab=Math.min(2,(int)((mx-x)*3/width));scroll=0;return true;}
        if(tab==0)return items.click(mx,my,left,top+20,viewport,machineWidth);
        if(tab==1&&my>=top+186){
            int count=ProcessingRecipeCatalogue.pages(machine,selected).size();
            if(mx>=x+width*2/3){selected=ItemStack.EMPTY;page=0;}
            else if(count>0)page=Math.floorMod(page+(mx<x+width/3?-1:1),count);
            scroll=0;
        }
        return true;
    }
    public boolean scroll(double mx,double my,double delta,int left,int top,int viewport,int machineWidth){
        int width=MachineItemCatalog.panelWidth(viewport,machineWidth),x=left-width-4;
        if(width<120||mx<x||mx>=x+width||my<top||my>=top+208||tab==0)return false;
        scroll=Math.clamp(scroll+(delta>0?-1:delta<0?1:0),0,Math.max(0,rows().size()-8));return true;
    }
}
