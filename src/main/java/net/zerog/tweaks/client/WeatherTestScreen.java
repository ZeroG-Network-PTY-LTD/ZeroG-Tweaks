package net.zerog.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

/** Local creative preview. No packets, world commands or destructive weather actions. */
public final class WeatherTestScreen extends Screen {
    public WeatherTestScreen() { super(Component.literal("Z-Admintools — Weather tester")); }
    @Override protected void init() {
        var modes=PlanetWeatherEffects.Preview.values();
        int top=Math.max(48,height/2-100);
        for(int i=0;i<modes.length;i++) {
            var mode=modes[i];
            addRenderableWidget(Button.builder(Component.literal(mode.label),button->{
                PlanetWeatherEffects.setPreview(mode);
                onClose();
            }).bounds(width/2-152+(i%2)*156,top+(i/2)*24,148,20).build());
        }
        addRenderableWidget(Button.builder(Component.literal("Quality / thunder / flashes"),button ->
                minecraft.setScreen(new PlanetWeatherScreen(this))).bounds(width/2-152,top+144,304,20).build());
        addRenderableWidget(Button.builder(Component.literal("Close"),button->onClose())
                .bounds(width/2-152,top+168,304,20).build());
    }
    @Override public boolean isPauseScreen() { return false; }
    @Override public void render(GuiGraphics graphics,int mouseX,int mouseY,float tick) {
        super.render(graphics,mouseX,mouseY,tick);
        graphics.drawCenteredString(font,title,width/2,18,0xFFFFFF);
        graphics.drawCenteredString(font,"Creative • planets only • visual effects, no damage",width/2,32,0xA8CBDF);
    }
}
