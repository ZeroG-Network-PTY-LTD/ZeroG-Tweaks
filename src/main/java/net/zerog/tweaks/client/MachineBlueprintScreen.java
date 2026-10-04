package net.zerog.tweaks.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

/** Read-only use diagrams for six plain blocks that currently have no machine BE.
 * Deliberately not a menu: no fictitious slots, FE or server inventory.
 */
public final class MachineBlueprintScreen extends Screen {
    private final MachineGuiProfile profile;
    public MachineBlueprintScreen(Component title,MachineGuiProfile profile){super(title);this.profile=profile;}
    @Override protected void init() {
        addRenderableWidget(Button.builder(Component.translatable("gui.done"),b->onClose()).bounds(width/2-40,height/2+96,80,18).build());
    }
    @Override public boolean isPauseScreen(){return false;}
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partial) {
        int x=(width-256)/2,y=(height-236)/2;
        g.blit(profile.background(),x,y,0,0,256,236,256,256);
        g.drawString(font,font.plainSubstrByWidth(title.getString(),238),x+8,y+5,0x403830,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.inputs"),x+15,y+23,0x403830,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.outputs"),x+155,y+23,0x403830,false);
        var lines=font.split(Component.literal(profile.purpose()),226);
        for(int i=0;i<Math.min(3,lines.size());i++)g.drawString(font,lines.get(i),x+14,y+94+i*10,0x403830,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.blueprint"),x+14,y+125,0x864429,false);
        g.drawString(font,Component.translatable("screen.zerog_tweaks.workbench.planned_metrics"),x+14,y+143,0x403830,false);
        for(int i=0;i<Math.min(3,profile.metrics().size());i++) {
            g.drawCenteredString(font,profile.metrics().get(i),x+48+i*80,y+158,0xffd5d6e0);
            g.drawCenteredString(font,"--",x+48+i*80,y+175,0xffa8a093);
        }
        g.drawCenteredString(font,Component.translatable("screen.zerog_tweaks.workbench.no_storage"),x+128,y+196,0xff5d5146);
        super.render(g,mouseX,mouseY,partial);
        for(int i=0;i<profile.positions().size();i++) {
            var pos=profile.positions().get(i);
            g.drawCenteredString(font,Integer.toString(i+1),x+pos[0]+8,y+pos[1]+4,0xffa8a093);
            if(mouseX>=x+pos[0]&&mouseX<x+pos[0]+16&&mouseY>=y+pos[1]&&mouseY<y+pos[1]+16)
                g.renderTooltip(font,Component.literal(profile.roles().get(i)),mouseX,mouseY);
        }
    }
    @EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
    public static final class Opening {
        @SubscribeEvent public static void click(PlayerInteractEvent.RightClickBlock event) {
            if(!event.getLevel().isClientSide||event.getHand()!=InteractionHand.MAIN_HAND
                    ||!event.getItemStack().isEmpty()||event.getEntity().isShiftKeyDown())return;
            var id=BuiltInRegistries.BLOCK.getKey(event.getLevel().getBlockState(event.getPos()).getBlock());
            if(!id.getNamespace().equals("zerog_tweaks")&&!id.getNamespace().equals("aeroapiary"))return;
            MachineGuiProfile.read(id.getNamespace(),id.getPath()).filter(MachineGuiProfile::designOnly).ifPresent(profile->{
                event.setCanceled(true);event.setCancellationResult(InteractionResult.SUCCESS);
                Minecraft.getInstance().execute(()->Minecraft.getInstance().setScreen(
                    new MachineBlueprintScreen(event.getLevel().getBlockState(event.getPos()).getBlock().getName(),profile)));
            });
        }
    }
}
