package net.zerog.tweaks.client;

import java.util.List;
import java.util.Comparator;
import java.util.function.Predicate;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.Font;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

/** Read-only accepted-input catalogue. Never changes recipes or player inventory. */
public final class MachineItemCatalog {
    private record Entry(ItemStack stack,String category) {}
    private final List<Entry> entries;
    private final java.util.function.Function<ItemStack,String> detail;
    private int page;
    private java.util.function.Consumer<ItemStack> selection;
    public MachineItemCatalog onSelect(java.util.function.Consumer<ItemStack> callback){selection=callback;return this;}
    public MachineItemCatalog(Predicate<ItemStack> accepted) {
        this(accepted,stack->category(stack));
    }
    public MachineItemCatalog(Predicate<ItemStack> accepted,java.util.function.Function<ItemStack,String> detail) {
        this.detail=detail;
        entries=BuiltInRegistries.ITEM.stream().map(ItemStack::new).filter(accepted)
            .map(stack->new Entry(stack,category(stack)))
            .sorted(Comparator.comparing(Entry::category).thenComparing(e->e.stack().getHoverName().getString(),String.CASE_INSENSITIVE_ORDER)
                .thenComparing(e->BuiltInRegistries.ITEM.getKey(e.stack().getItem()).toString())).toList();
    }
    private static String category(ItemStack stack) {
        var tags=stack.getTags().map(tag->tag.location().toString()).sorted().toList();
        for(String category:List.of("logs","planks","coals","ores","ingots","dusts","gems","flowers"))
            if(tags.stream().anyMatch(tag->tag.endsWith(":"+category)||tag.contains(":"+category+"/")))return category;
        return stack.getItem() instanceof net.minecraft.world.item.BlockItem?"blocks":"items";
    }
    public static int panelWidth(int viewport,int machineWidth){return Math.max(0,Math.min(174,viewport-machineWidth-12));}
    public static int machineLeft(int viewport,int machineWidth,boolean shown){
        int panel=panelWidth(viewport,machineWidth);
        return shown&&panel>=32?(viewport-machineWidth-panel-4)/2+panel+4:(viewport-machineWidth)/2;
    }
    public void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mouseX,int mouseY,String title) {
        int width=panelWidth(viewport,machineWidth);if(width<32)return;
        int x=left-width-4;g.fill(x,top,x+width,top+184,0xee142735);
        if(width>=90)g.drawString(font,font.plainSubstrByWidth(title,width-12),x+6,top+6,0xffe6f4ff,false);
        for(int row=0;row<6;row++){
            int index=page*6+row;if(index>=entries.size())break;
            var entry=entries.get(index);int y=top+23+row*24;g.renderItem(entry.stack(),x+6,y);
            if(width>=90){
                g.drawString(font,font.plainSubstrByWidth(entry.stack().getHoverName().getString(),width-32),x+26,y,0xffe6f4ff,false);
                g.drawString(font,font.plainSubstrByWidth(detail.apply(entry.stack()),width-32),x+26,y+10,0xff9edbda,false);
            }
            if(mouseX>=x+6&&mouseX<x+width-4&&mouseY>=y&&mouseY<y+20)
                g.renderTooltip(font,List.of(entry.stack().getHoverName(),Component.literal(entry.category()+" / "+detail.apply(entry.stack())),
                    Component.literal(BuiltInRegistries.ITEM.getKey(entry.stack().getItem()).toString())),java.util.Optional.empty(),mouseX,mouseY);
        }
        g.drawString(font,font.plainSubstrByWidth((page+1)+"/"+Math.max(1,(entries.size()+5)/6)+" >",width-12),x+6,top+170,0xff9edbda,false);
    }
    public boolean click(double x,double y,int left,int top,int viewport,int machineWidth){
        int width=panelWidth(viewport,machineWidth);if(width<32||x<left-width-4||x>=left-4||y<top||y>=top+184)return false;
        if(selection!=null){
            int row=(int)(y-top-23)/24;
            if(y>=top+23&&row>=0&&row<6&&y<top+23+row*24+20){
                int index=page*6+row;if(index<entries.size())selection.accept(entries.get(index).stack().copy());return true;
            }
            if(y<top+168)return true;
        }
        page=(page+1)%Math.max(1,(entries.size()+5)/6);return true;
    }
}
