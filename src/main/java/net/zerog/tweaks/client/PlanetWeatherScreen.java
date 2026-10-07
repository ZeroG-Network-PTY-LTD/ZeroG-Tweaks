package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.zerog.tweaks.registry.ZGWeatherConfig;

/** Independent of Iris: native particles/bolts still work with shaders disabled. */
public final class PlanetWeatherScreen extends Screen {
    private final Screen parent;
    public PlanetWeatherScreen(Screen parent) { super(Component.literal("ZeroG Alien Weather")); this.parent=parent; }
    @Override protected void init() {
        int x=width/2-110, y=Math.max(55,height/2-45);
        if(!net.zerog.tweaks.event.PlanetStorms.enabled()) {
            addRenderableWidget(Button.builder(Component.literal("Done"),b -> onClose()).bounds(x,y,220,20).build());
            return;
        }
        addRenderableWidget(Button.builder(qualityLabel(),b -> {
            ZGWeatherConfig.QUALITY.set((ZGWeatherConfig.QUALITY.get()+1)%3);
            ZGWeatherConfig.SPEC.save();b.setMessage(qualityLabel());
        }).bounds(x,y,220,20).build());
        addRenderableWidget(Button.builder(thunderLabel(),b -> {
            ZGWeatherConfig.THUNDER.set(!ZGWeatherConfig.THUNDER.get());ZGWeatherConfig.SPEC.save();b.setMessage(thunderLabel());
        }).bounds(x,y+24,220,20).build());
        addRenderableWidget(Button.builder(flashLabel(),b -> {
            ZGWeatherConfig.REDUCED_FLASH.set(!ZGWeatherConfig.REDUCED_FLASH.get());ZGWeatherConfig.SPEC.save();b.setMessage(flashLabel());
        }).bounds(x,y+48,220,20).build());
        addRenderableWidget(Button.builder(Component.literal("Done"),b -> onClose()).bounds(x,y+80,220,20).build());
    }
    private Component qualityLabel() {return Component.literal("Ambient particles: "+switch(ZGWeatherConfig.QUALITY.get()) {case 1->"Low";case 2->"High";default->"Off";});}
    private Component thunderLabel(){return Component.literal("Thunder audio: "+(ZGWeatherConfig.THUNDER.get()?"On":"Off"));}
    private Component flashLabel(){return Component.literal("Extra sky flashes: "+(ZGWeatherConfig.REDUCED_FLASH.get()?"Off":"On"));}
    @Override public void onClose(){minecraft.setScreen(parent);}
    @Override public void render(GuiGraphics graphics,int mouseX,int mouseY,float tick) {
        super.render(graphics,mouseX,mouseY,tick);
        graphics.drawCenteredString(font,title,width/2,22,0xFFFFFF);
        graphics.drawCenteredString(font,net.zerog.tweaks.event.PlanetStorms.enabled()?"Acid is harmless • native lightning can damage and ignite":"Custom weather disabled in this build • vanilla weather unchanged",width/2,37,0xAAAAAA);
    }
}
