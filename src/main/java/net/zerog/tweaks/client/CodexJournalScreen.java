package net.zerog.tweaks.client;

import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.zerog.tweaks.item.ConcordCodexItem;
import net.zerog.tweaks.lore.CodexJournalSync;

/** A responsive, scrollable Concord field journal. All story pages originate from the server reader snapshot. */
public final class CodexJournalScreen extends Screen {
    private final List<Component> pages;
    private int page,scroll,left,top,panelWidth,panelHeight,side;
    public CodexJournalScreen(List<Component> pages){super(Component.literal("Concord Codex"));this.pages=List.copyOf(pages);}
    private void guide(String path){
        if(minecraft.player!=null)guideme.GuidesCommon.openGuide(minecraft.player,ConcordCodexItem.GUIDE,
                guideme.PageAnchor.page(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",path)));
    }
    private void button(String title,int x,int y,int width,Button.OnPress action){
        addRenderableWidget(Button.builder(Component.literal(title),action).bounds(x,y,width,20).build());
    }
    @Override protected void init(){
        panelWidth=Math.min(620,width-16);panelHeight=Math.min(420,height-16);
        left=(width-panelWidth)/2;top=(height-panelHeight)/2;side=Math.max(92,Math.min(145,panelWidth/3));
        int w=side-16,x=left+8;
        button("Field guide",x,top+60,w,b->guide("index.md"));
        button("Gate layers",x,top+84,w,b->guide("16_gate_atlas.md"));
        button("Machines",x,top+108,w,b->guide("17_machine_fieldbook.md"));
        button("Impacts",x,top+132,w,b->guide("18_impacts.md"));
        button("Next task",x,top+156,w,b->{
            for(int i=0;i<pages.size();i++)if(pages.get(i).getString().lines().anyMatch(line->line.strip().startsWith("[ ]"))){page=i;scroll=0;break;}
        });
        button("<",left+side+10,top+panelHeight-28,30,b->{page=Math.max(0,page-1);scroll=0;});
        button(">",left+side+44,top+panelHeight-28,30,b->{page=Math.min(Math.max(0,pages.size()-1),page+1);scroll=0;});
        button("Close",left+panelWidth-62,top+panelHeight-28,54,b->onClose());
    }
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partial){
        renderBackground(g,mouseX,mouseY,partial);
        g.fill(left,top,left+panelWidth,top+panelHeight,0xff101a2c);
        g.fill(left+side,top+48,left+panelWidth-6,top+panelHeight-34,0xffe9e0c6);
        g.fill(left,top,left+panelWidth,top+3,0xff67dacb);
        g.drawString(font,"CONCORD / FIELD JOURNAL",left+12,top+12,0xffd7f7ed,false);
        g.drawString(font,"Echo's recovered memories",left+12,top+28,0xffbba3e2,false);
        super.render(g,mouseX,mouseY,partial);
        if(pages.isEmpty())return;
        int bodyX=left+side+10,bodyY=top+104,bodyWidth=panelWidth-side-28,bottom=top+panelHeight-38;
        var content=pages.get(page).getString();
        var lines=font.split(Component.literal(content),bodyWidth);
        int visible=Math.max(1,(bottom-bodyY)/11);scroll=Math.clamp(scroll,0,Math.max(0,lines.size()-visible));
        String[] icons=content.toLowerCase(java.util.Locale.ROOT).contains("signal")
                ?new String[]{"raw_nullifite","dormant_wisp","concord_codex"}
                :content.toLowerCase(java.util.Locale.ROOT).contains("mars")?new String[]{"aresite_block","gate_controller","moonsteel_ingot"}
                :new String[]{"concord_codex","gate_controller","star_map_fragment"};
        for(int i=0;i<icons.length;i++){
            g.pose().pushPose();g.pose().translate(bodyX+i*44,top+57,0);g.pose().scale(2,2,1);
            g.renderItem(new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",icons[i]))),0,0);g.pose().popPose();
        }
        g.enableScissor(bodyX,bodyY,left+panelWidth-12,bottom);
        for(int i=scroll;i<Math.min(lines.size(),scroll+visible);i++)g.drawString(font,lines.get(i),bodyX,bodyY+(i-scroll)*11,0xff263849,false);
        g.disableScissor();
        g.drawString(font,""+(page+1)+" / "+pages.size(),left+side+86,top+panelHeight-22,0xffd7f7ed,false);
        if(lines.size()>visible){
            int track=bottom-bodyY,thumb=Math.max(10,track*visible/lines.size());
            int offset=scroll*(track-thumb)/Math.max(1,lines.size()-visible);
            g.fill(left+panelWidth-10,bodyY,left+panelWidth-8,bottom,0xffc6bfa9);
            g.fill(left+panelWidth-10,bodyY+offset,left+panelWidth-8,bodyY+offset+thumb,0xff675c83);
        }
    }
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical){scroll=Math.max(0,scroll-(int)Math.signum(vertical)*3);return true;}
    @Override public boolean isPauseScreen(){return false;}
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
    public static final class Events {
        @SubscribeEvent public static void tick(ClientTickEvent.Post event){
            var packet=CodexJournalSync.take();var client=Minecraft.getInstance();
            if(packet!=null&&client.player!=null)client.setScreen(new CodexJournalScreen(packet.pages()));
        }
    }
}
