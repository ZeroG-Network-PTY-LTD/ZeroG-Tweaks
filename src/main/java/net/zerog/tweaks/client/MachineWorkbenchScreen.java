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
    private boolean showInputs;
    private MachineItemCatalog inputs;
    private ProcessingRecipePanel recipes;
    private final MachineFaceControls faceControls=new MachineFaceControls();
    public MachineWorkbenchScreen(AbstractContainerMenu menu,Inventory inventory,Component title,MachineGuiProfile profile) {
        super(menu,inventory,title);this.profile=profile;original=List.copyOf(menu.slots);
        imageWidth=256;imageHeight=236;inventoryLabelX=47;inventoryLabelY=143;
        if(menu instanceof net.zerog.tweaks.machine.MachineSideMenu sides&&net.zerog.tweaks.machine.LegacyMachineSides.supports(sides.sideMachine()))imageWidth=358;
        AlvearyMenuSync.clientState=new AlvearyMenuSync.State(-1,0,false,"");
    }
    @Override protected void init() {
        super.init();leftPos=MachineItemCatalog.machineLeft(width,imageWidth,showInputs);int n=profile.roles().size();
        inputs=new MachineItemCatalog(stack->original.stream().limit(profile.outputStart()).anyMatch(slot->slot.mayPlace(stack)));
        if(recipes==null&&net.zerog.tweaks.machine.LegacyRecipeCatalogue.supports(profile.id())&&menu instanceof net.zerog.tweaks.machine.MachineSideMenu sides)
            recipes=new ProcessingRecipePanel(sides.sideMachine());
        if(imageWidth>256&&menu instanceof net.zerog.tweaks.machine.MachineSideMenu sides)
            faceControls.add(leftPos+260,topPos+18,sides,w->addRenderableWidget(w),command->{if(minecraft!=null&&minecraft.gameMode!=null)minecraft.gameMode.handleInventoryButtonClick(menu.containerId,command);});
        var browse=addRenderableWidget(net.minecraft.client.gui.components.Button.builder(Component.literal(recipes==null?"Inputs":"Recipes"),b->{showInputs=!showInputs;rebuildWidgets();}).bounds(leftPos+196,topPos+3,52,16).build());
        if(recipes!=null)browse.active=MachineItemCatalog.panelWidth(width,imageWidth)>=120;
        for(int i=0;i<original.size();i++) {
            if(menu instanceof net.zerog.tweaks.machine.MachineSideMenu sides&&net.zerog.tweaks.genetics.LegacyMachineCards.supports(sides.sideMachine())&&i>=original.size()-2)continue;
            int x,y;
            if(i<n) {var xy=profile.positions().get(i);x=xy[0];y=xy[1];}
            else {int j=i-n;x=47+j%9*18;y=j<27?154+j/9*18:212;}
            menu.slots.set(i,new AlvearyControllerScreen.PositionedSlot(original.get(i),x,y,true));
        }
    }
    @Override protected void renderBg(GuiGraphics g,float partial,int mouseX,int mouseY) {
        g.fill(leftPos,topPos,leftPos+imageWidth,topPos+imageHeight,0xff152432);
        g.fill(leftPos+8,topPos+20,leftPos+248,topPos+88,0xff24354b);
        for(var slot:menu.slots){g.fill(leftPos+slot.x-1,topPos+slot.y-1,leftPos+slot.x+17,topPos+slot.y+17,0xff536578);g.fill(leftPos+slot.x,topPos+slot.y,leftPos+slot.x+16,topPos+slot.y+16,0xff08131f);}
        var state=AlvearyMenuSync.clientState;
        if(state.menu()==menu.containerId && state.progress()>0)
            g.fill(leftPos+14,topPos+81,leftPos+14+228*state.progress()/100,topPos+84,0xffffc765);
    }
    @Override protected void renderLabels(GuiGraphics g,int mouseX,int mouseY) {
        g.drawString(font,font.plainSubstrByWidth(title.getString(),180),8,5,0xffe1edf7,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.inputs"),15,23,0xffb8d6e5,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.outputs"),155,23,0xffb8d6e5,false);
        String purpose=switch(profile.id()){case "silk_weaver"->"One silk thread becomes woven silk. Unused slots are recovery only.";case "starmetal_smelter"->"Process registered starmetal inputs. Unused alloy slot is recovery only.";default->profile.purpose();};
        var lines=font.split(Component.literal(purpose),226);
        for(int i=0;i<Math.min(3,lines.size());i++)g.drawString(font,lines.get(i),14,94+i*10,0xffb8d6e5,false);
        var state=AlvearyMenuSync.clientState;
        String suffix=state.menu()==menu.containerId?state.progress()+"%":"--";
        g.drawString(font,Component.literal("Cycle: "+suffix),14,125,0xff9edbda,false);
        if(state.menu()==menu.containerId&&state.capacity()>0)g.drawString(font,font.plainSubstrByWidth("FE "+state.energy()+"/"+state.capacity(),130),110,125,0xff9edbda,false);
        g.drawString(font,playerInventoryTitle,inventoryLabelX,inventoryLabelY,0xffe1edf7,false);
        if(menu instanceof net.zerog.tweaks.machine.MachineSideMenu sides&&net.zerog.tweaks.genetics.LegacyMachineCards.supports(sides.sideMachine())){
            g.drawString(font,"A",218,163,0xff9edbda,false);g.drawString(font,"E",218,199,0xff9edbda,false);
        }
    }
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partial) {
        super.render(g,mouseX,mouseY,partial);renderTooltip(g,mouseX,mouseY);
        if(showInputs){if(recipes!=null)recipes.render(g,font,leftPos,topPos,width,imageWidth,mouseX,mouseY);else inputs.render(g,font,leftPos,topPos,width,imageWidth,mouseX,mouseY,"Accepted inputs");}
        var status=AlvearyMenuSync.clientState;
        if(status.menu()==menu.containerId&&status.capacity()>0&&isHovering(110,125,130,10,mouseX,mouseY))g.renderTooltip(font,Component.literal("Stored FE: "+status.energy()+" / "+status.capacity()+". Requires power; idle and blocked jobs do not consume energy."),mouseX,mouseY);
        for(int i=0;i<profile.positions().size();i++) {
            var xy=profile.positions().get(i);
            if(isHovering(xy[0],xy[1],16,16,mouseX,mouseY)&&!menu.slots.get(i).hasItem())
                g.renderTooltip(font,Component.literal((profile.id().equals("silk_weaver")&&(i==1||i==2)||profile.id().equals("starmetal_smelter")&&i==1)?"Recovery only / no operating input":profile.id().equals("starmetal_smelter")?(i==0?"Starmetal recipe input":i==2?"Redstone flux":"Starmetal output"):profile.roles().get(i)),mouseX,mouseY);
        }
    }
    private boolean recipeArea(double x,double y){int panel=MachineItemCatalog.panelWidth(width,imageWidth);return showInputs&&recipes!=null&&panel>=120&&x>=leftPos-panel-4&&x<leftPos-4&&y>=topPos&&y<topPos+208;}
    @Override public boolean mouseClicked(double x,double y,int button){
        if(recipeArea(x,y)){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();return recipes.click(x,y,button,leftPos,topPos,width,imageWidth);}
        if(showInputs&&recipes==null&&inputs.click(x,y,leftPos,topPos,width,imageWidth))return true;return super.mouseClicked(x,y,button);
    }
    @Override protected boolean hasClickedOutside(double x,double y,int left,int top,int button){return !recipeArea(x,y)&&super.hasClickedOutside(x,y,left,top,button);}
    @Override public boolean mouseDragged(double x,double y,int button,double dx,double dy){if(recipeArea(x,y)){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();return true;}return super.mouseDragged(x,y,button,dx,dy);}
    @Override public boolean mouseReleased(double x,double y,int button){if(recipeArea(x,y)){quickCraftSlots.clear();isQuickCrafting=false;clearDraggingState();}return super.mouseReleased(x,y,button);}
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical){if(showInputs&&recipes!=null&&recipes.scroll(x,y,vertical,leftPos,topPos,width,imageWidth))return true;return super.mouseScrolled(x,y,horizontal,vertical);}
}
