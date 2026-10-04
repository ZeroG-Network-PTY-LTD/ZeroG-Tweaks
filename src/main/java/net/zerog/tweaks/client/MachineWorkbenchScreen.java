package net.zerog.tweaks.client;

import java.util.List;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.Slot;
import net.zerog.tweaks.event.AlvearyMenuSync;

/** Use-specific presentation for all eleven existing non-alveary addon machines.
 * No slot/filter/recipe/server-inventory edits and no fabricated genetics controls.
 */
public final class MachineWorkbenchScreen extends AbstractContainerScreen<AbstractContainerMenu> {
    private final MachineGuiProfile profile;
    private final List<Slot> original;
    public MachineWorkbenchScreen(AbstractContainerMenu menu,Inventory inventory,Component title,MachineGuiProfile profile) {
        super(menu,inventory,title);this.profile=profile;original=List.copyOf(menu.slots);
        imageWidth=256;imageHeight=236;inventoryLabelX=47;inventoryLabelY=143;
        AlvearyMenuSync.clientState=new AlvearyMenuSync.State(-1,0,false,"");
    }
    @Override protected void init() {
        super.init();int n=profile.roles().size();
        for(int i=0;i<original.size();i++) {
            int x,y;
            if(i<n) {var xy=profile.positions().get(i);x=xy[0];y=xy[1];}
            else {int j=i-n;x=47+j%9*18;y=j<27?154+j/9*18:212;}
            menu.slots.set(i,new AlvearyControllerScreen.PositionedSlot(original.get(i),x,y,true));
        }
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int mouseX,int mouseY) {
        g.blit(profile.background(),leftPos,topPos,0,0,imageWidth,imageHeight,256,256);
        var state=AlvearyMenuSync.clientState;
        if(state.menu()==menu.containerId && state.progress()>0)
            g.fill(leftPos+14,topPos+81,leftPos+14+228*state.progress()/100,topPos+84,0xffffc765);
    }
    @Override protected void renderLabels(GuiGraphics g,int mouseX,int mouseY) {
        g.drawString(font,font.plainSubstrByWidth(title.getString(),180),8,5,0x403830,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.inputs"),15,23,0x403830,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.outputs"),155,23,0x403830,false);
        var lines=font.split(Component.literal(profile.purpose()),226);
        for(int i=0;i<Math.min(3,lines.size());i++)g.drawString(font,lines.get(i),14,94+i*10,0x403830,false);
        var state=AlvearyMenuSync.clientState;
        String suffix=state.menu()==menu.containerId?state.progress()+"%":"--";
        g.drawString(font,Component.translatable(profile.pending()?"screen.zerog_tweaks.workbench.legacy_cycle":"screen.zerog_tweaks.workbench.cycle",suffix),14,125,0x66523c,false);
        if(profile.pending())g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.pending"),128,125,0x864429,false);
        g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0x403830,false);
    }
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partial) {
        super.render(g,mouseX,mouseY,partial);renderTooltip(g,mouseX,mouseY);
        for(int i=0;i<profile.positions().size();i++) {
            var xy=profile.positions().get(i);
            if(isHovering(xy[0],xy[1],16,16,mouseX,mouseY)&&!menu.slots.get(i).hasItem())
                g.renderTooltip(font,Component.literal(profile.roles().get(i)),mouseX,mouseY);
        }
        if(profile.pending() && isHovering(8,90,239,45,mouseX,mouseY))
            g.renderTooltip(font,font.split(Component.translatable("screen.zerog_tweaks.workbench.genetics_pending"),240),mouseX,mouseY);
    }
}
