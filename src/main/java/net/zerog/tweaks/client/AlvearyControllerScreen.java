package net.zerog.tweaks.client;

import java.util.List;
import com.mojang.datafixers.util.Pair;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import net.zerog.tweaks.event.AlvearyMenuSync;
import net.zerog.tweaks.guide.AlvearyLayout;
import net.zerog.tweaks.guide.ApiaryMachineAccess;

/** Classic honey/vanilla panels, preserving the addon's real slot numbering and filters. */
public final class AlvearyControllerScreen extends AbstractContainerScreen<AbstractContainerMenu> {
    private static final ResourceLocation BG=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/alveary_controller_runtime.png");
    private static final ResourceLocation ATLAS=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/alveary_controller_widgets.png");
    private final int tier;
    private final List<Slot> originals;
    private int page=0,ledger=-1;
    public AlvearyControllerScreen(AbstractContainerMenu menu,Inventory inventory,Component title,int tier) {
        super(menu,inventory,title);this.tier=tier;originals=List.copyOf(menu.slots);
        imageWidth=AlvearyLayout.WIDTH;imageHeight=AlvearyLayout.HEIGHT;
        inventoryLabelX=47;inventoryLabelY=158;
        AlvearyMenuSync.clientState=new AlvearyMenuSync.State(-1,0,false,"");
    }
    private static Component label(String key,Object... values) {return Component.translatable("screen.zerog_tweaks.alveary."+key,values);}
    @Override protected void init() {
        super.init();
        positionSlots();
        var previous=addRenderableWidget(Button.builder(Component.literal("<"),button->{page=0;positionSlots();})
                .bounds(leftPos+139,topPos+79,12,12).build());
        var next=addRenderableWidget(Button.builder(Component.literal(">"),button->{page=(AlvearyLayout.products(tier)-1)/9;positionSlots();})
                .bounds(leftPos+153,topPos+79,12,12).build());
        previous.active=next.active=AlvearyLayout.products(tier)>9;
        addRenderableWidget(new SpriteButton(leftPos+181,topPos+79,12,12,42,82,false,label("sort"),
                button->PacketDistributor.sendToServer(new AlvearyMenuSync.Sort(menu.containerId))));
        for(int i=0;i<5;i++) {
            final int tab=i;
            addRenderableWidget(new SpriteButton(leftPos+255,topPos+4+i*26,24,24,i*26,194,true,label("ledger_"+i),
                    button->ledger=ledger==tab?-1:tab));
        }
        addRenderableWidget(new SpriteButton(leftPos+19,topPos+76,12,12,0,82,false,label("hive_help"),button->ledger=ledger==0?-1:0));
    }
    private void positionSlots() {
        for(int i=0;i<originals.size();i++) {
            int[] pos=AlvearyLayout.position(tier,i,page);
            menu.slots.set(i,new PositionedSlot(originals.get(i),pos[0],pos[1],AlvearyLayout.visible(tier,i,page)));
        }
    }
    @Override protected void renderBg(GuiGraphics graphics,float partial,int mouseX,int mouseY) {
        graphics.blit(BG,leftPos,topPos,0,0,imageWidth,imageHeight,256,256);
        var status=AlvearyMenuSync.clientState;boolean ready=status.menu()==menu.containerId;
        // Actual frame/output counts, never unlocked slots invented from the design document.
        for(int i=AlvearyLayout.frames(tier);i<27;i++)sprite(graphics,60,82,18,18,11+(i%9)*18,98+(i/9)*18);
        for(int cell=0;cell<9;cell++)if(page*9+cell>=AlvearyLayout.products(tier))sprite(graphics,60,82,18,18,139+(cell%3)*18,22+(cell/3)*18);
        sprite(graphics,80,82,6,62,44,22); // lifespan isn't implemented by this addon
        for(int[] tank:new int[][]{{205,22,8},{216,22,14},{233,22,12}})
            sprite(graphics,80,82,tank[2],62,tank[0],tank[1]);
        int progress=ready?Mth.clamp(status.progress(),0,100):0;
        int fill=64*progress/100;
        if(fill>0)sprite(graphics,36,64-fill,4,fill,55,87-fill);
        // Biome values are real; no fabricated bee tolerance bands or gravity modifiers.
        ApiaryMachineAccess.read(menu).ifPresent(machine->{
            var biome=minecraft.level.getBiome(machine.entity().getBlockPos()).value();
            int temperature=Mth.clamp((int)((biome.getBaseTemperature()+.5F)/2.5F*48),0,48);
            int humidity=Mth.clamp((int)(biome.getModifiedClimateSettings().downfall()*48),0,48);
            if(temperature>0)sprite(graphics,0,48-temperature,8,temperature,76,80-temperature);
            if(humidity>0)sprite(graphics,10,48-humidity,8,humidity,96,80-humidity);
            sprite(graphics,68,0,10,2,75,Math.max(31,79-temperature));
            sprite(graphics,68,0,10,2,95,Math.max(31,79-humidity));
        });
        sprite(graphics,80,82,10,50,115,31); // gravity tolerance requires future backend data
        // Atlas: working=0, incomplete=12th status at x144 (the thirteenth status).
        sprite(graphics,ready && status.formed()?0:144,68,10,10,199,4);
        for(int i=0;i<4;i++)sprite(graphics,80+i*20,0,9,8,73+i*14,84);
        for(int i=0;i<5;i++)sprite(graphics,i*26,194,24,24,255,4+i*26);
    }
    private void sprite(GuiGraphics g,int u,int v,int w,int h,int x,int y) {
        g.blit(ATLAS,leftPos+x,topPos+y,u,v,w,h,256,256);
    }
    @Override protected void renderLabels(GuiGraphics g,int mouseX,int mouseY) {
        g.drawString(font,font.plainSubstrByWidth(title.getString(),120),8,5,0x404040,false);
        int badge=tier==8?0:tier-1;
        g.blit(ATLAS,131,3,(badge%3)*66,148+(badge/3)*14,64,12,256,256);
        g.drawString(font,tier==8?label("hive"):label("tier_name_"+tier),146,5,0xffffff,true);
        var state=AlvearyMenuSync.clientState;boolean ready=state.menu()==menu.containerId;
        g.drawString(font,font.plainSubstrByWidth(label(!ready?"syncing":state.formed()?"formed":"broken").getString(),38),211,5,ready&&state.formed()?0x285f2c:0x8d3030,false);
        g.drawString(font,label("inventory"),inventoryLabelX,inventoryLabelY,0x404040,false);
        for(int y:new int[]{101,114,127,140})g.drawString(font,"--",193,y,0x5b5345,false);
    }
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partial) {
        super.render(g,mouseX,mouseY,partial);renderTooltip(g,mouseX,mouseY);
        if(isHovering(199,3,50,12,mouseX,mouseY)) {
            var state=AlvearyMenuSync.clientState;
            if(state.menu()==menu.containerId && !state.error().isBlank())g.renderTooltip(font,Component.literal(state.error()),mouseX,mouseY);
        }
        if(isHovering(201,20,46,67,mouseX,mouseY)||isHovering(115,31,10,50,mouseX,mouseY)||isHovering(44,22,6,66,mouseX,mouseY))
            g.renderTooltip(font,label("reserved_details"),mouseX,mouseY);
        if(isHovering(75,31,10,50,mouseX,mouseY))g.renderTooltip(font,label("temperature"),mouseX,mouseY);
        if(isHovering(95,31,10,50,mouseX,mouseY))g.renderTooltip(font,label("humidity"),mouseX,mouseY);
        if(isHovering(7,16,31,6,mouseX,mouseY))g.renderTooltip(font,label("hive_help"),mouseX,mouseY);
        if(isHovering(69,16,62,3,mouseX,mouseY))g.renderTooltip(font,label("climate_help"),mouseX,mouseY);
        if(isHovering(135,16,62,6,mouseX,mouseY))g.renderTooltip(font,label("output_help"),mouseX,mouseY);
        if(isHovering(7,96,162,3,mouseX,mouseY))g.renderTooltip(font,label("frame_help"),mouseX,mouseY);
        if(isHovering(177,98,68,54,mouseX,mouseY))g.renderTooltip(font,label("modifier_help"),mouseX,mouseY);
        if(isHovering(139,79,30,12,mouseX,mouseY))g.renderTooltip(font,label("page",page+1,(AlvearyLayout.products(tier)+8)/9),mouseX,mouseY);
        if(ledger>=0 && width-leftPos>=400) {
            int x=leftPos+280,y=topPos+4;
            g.fill(x,y,x+120,y+150,0xffc6c6c6);g.renderOutline(x,y,120,150,0xff555555);
            g.fill(x+2,y+2,x+118,y+4,0xffe8a82c);
            g.drawString(font,label("ledger_"+ledger),x+6,y+8,0x404040,false);
            Component details=ledger==4?label(AlvearyMenuSync.clientState.formed()?"structure_ok":"structure_error",AlvearyMenuSync.clientState.error()):label("ledger_details_"+ledger);
            var lines=font.split(details,108);
            for(int i=0;i<Math.min(12,lines.size());i++)g.drawString(font,lines.get(i),x+6,y+24+i*10,0x404040,false);
        } else if(ledger>=0)g.renderTooltip(font,ledger==4?label("structure_error",AlvearyMenuSync.clientState.error()):label("ledger_details_"+ledger),mouseX,mouseY);
    }
    @Override protected boolean hasClickedOutside(double x,double y,int left,int top,int button) {
        if(ledger>=0 && x>=left+255 && x<left+400 && y>=top && y<top+160)return false;
        return super.hasClickedOutside(x,y,left,top,button);
    }
    /** Reposition only; all operations delegate to the original filtered SlotItemHandler. */
    private static final class SpriteButton extends Button {
        private final int u,v;private final boolean tab;
        SpriteButton(int x,int y,int width,int height,int u,int v,boolean tab,Component name,OnPress action) {
            super(x,y,width,height,name,action,DEFAULT_NARRATION);this.u=u;this.v=v;this.tab=tab;
            setTooltip(net.minecraft.client.gui.components.Tooltip.create(name));
        }
        @Override protected void renderWidget(GuiGraphics g,int mouseX,int mouseY,float partial) {
            g.blit(ATLAS,getX(),getY(),u,v+(!tab&&isHoveredOrFocused()?14:0),getWidth(),getHeight(),256,256);
            if(tab&&isHoveredOrFocused())g.renderOutline(getX(),getY(),getWidth(),getHeight(),0xffffd678);
        }
    }
    static final class PositionedSlot extends Slot {
        private final Slot original;
        private final boolean visible;
        PositionedSlot(Slot original,int x,int y,boolean visible) {super(original.container,original.getContainerSlot(),x,y);this.original=original;this.visible=visible;index=original.index;}
        @Override public ItemStack getItem(){return original.getItem();}
        @Override public boolean hasItem(){return original.hasItem();}
        @Override public boolean mayPlace(ItemStack stack){return original.mayPlace(stack);}
        @Override public boolean mayPickup(Player player){return original.mayPickup(player);}
        @Override public void set(ItemStack stack){original.set(stack);}
        @Override public void setByPlayer(ItemStack stack){original.setByPlayer(stack);}
        @Override public void setByPlayer(ItemStack stack,ItemStack previous){original.setByPlayer(stack,previous);}
        @Override public void setChanged(){original.setChanged();}
        @Override public ItemStack remove(int amount){return original.remove(amount);}
        @Override public int getMaxStackSize(){return original.getMaxStackSize();}
        @Override public int getMaxStackSize(ItemStack stack){return original.getMaxStackSize(stack);}
        @Override public boolean isActive(){return visible && original.isActive();}
        @Override public boolean isHighlightable(){return original.isHighlightable();}
        @Override public boolean isFake(){return original.isFake();}
        @Override public boolean isSameInventory(Slot other){return original.isSameInventory(other instanceof PositionedSlot positioned?positioned.original:other);}
        @Override public boolean allowModification(Player player){return original.allowModification(player);}
        @Override public void onTake(Player player,ItemStack stack){original.onTake(player,stack);}
        @Override public void onQuickCraft(ItemStack before,ItemStack after){original.onQuickCraft(before,after);}
        @Override public Pair<ResourceLocation,ResourceLocation> getNoItemIcon(){return original.getNoItemIcon();}
    }
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
    public static final class Opening {
        @SubscribeEvent public static void open(ScreenEvent.Opening event) {
            if(!(event.getNewScreen() instanceof AbstractContainerScreen<?> screen)||screen instanceof AlvearyControllerScreen||screen instanceof MachineWorkbenchScreen)return;
            var menu=screen.getMenu();
            ApiaryMachineAccess.read(menu).ifPresent(machine->{
                int tier=AlvearyLayout.tier(machine.id());
                var player=Minecraft.getInstance().player;
                if(tier>0 && player!=null && menu.slots.size()==AlvearyLayout.machineSlots(tier)+36)
                    event.setNewScreen(new AlvearyControllerScreen(menu,player.getInventory(),screen.getTitle(),tier));
                else if(tier==0 && player!=null)
                    MachineGuiProfile.read("aeroapiary",machine.id()).filter(profile->!profile.designOnly()
                        &&menu.slots.size()==profile.roles().size()+36).ifPresent(profile->
                            event.setNewScreen(new MachineWorkbenchScreen(menu,player.getInventory(),screen.getTitle(),profile)));
            });
        }
    }
}
