package net.zerog.tweaks.client;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
public interface RecipeBrowserPanel {
    void render(GuiGraphics g,Font font,int left,int top,int viewport,int machineWidth,int mouseX,int mouseY);
    boolean click(double x,double y,int button,int left,int top,int viewport,int machineWidth);
    boolean scroll(double x,double y,double delta,int left,int top,int viewport,int machineWidth);
    default int contentHeight(){return 208;}
}
