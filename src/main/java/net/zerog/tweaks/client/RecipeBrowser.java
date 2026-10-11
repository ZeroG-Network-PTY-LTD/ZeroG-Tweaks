package net.zerog.tweaks.client;
import java.util.List;
import java.util.function.Consumer;
import net.minecraft.client.gui.*;
import net.minecraft.client.gui.components.*;
import net.minecraft.network.chat.Component;
import net.zerog.tweaks.machine.RecipeBrowserLayout;

/** Read-only view inside an existing menu; never closes or replaces that menu. */
public final class RecipeBrowser {
    private final net.zerog.tweaks.machine.RecipeBrowserInput input=new net.zerog.tweaks.machine.RecipeBrowserInput();
    public boolean isOpen(){return input.isOpen();}
    public void open(){input.open();}
    public boolean consumeRelease(int button){return input.consumeRelease(button);}
    public boolean init(int width,int height,RecipeBrowserPanel panel,Consumer<Button> add,Runnable rebuild){
        if(!isOpen())return false;
        var b=RecipeBrowserLayout.fit(width,height,panel.contentHeight());
        add.accept(Button.builder(Component.literal("Back to machine"),w->{input.close();rebuild.run();}).bounds(b.backLeft(),b.backTop(),140,18).build());
        return true;
    }
    public boolean render(GuiGraphics g,Font font,int width,int height,int x,int y,float partial,RecipeBrowserPanel panel,List<Renderable> widgets){
        if(!isOpen())return false;var b=RecipeBrowserLayout.fit(width,height,panel.contentHeight());
        g.fill(0,0,width,height,0xff101c29);g.drawCenteredString(font,"Machine recipes and upgrades",width/2,7,0xffe1edf7);
        g.pose().pushPose();g.pose().translate(b.left(),b.top(),0);g.pose().scale(b.scale(),b.scale(),1);
        panel.render(g,font,178,0,186,0,(int)b.localX(x),(int)b.localY(y));g.pose().popPose();
        for(var widget:widgets)widget.render(g,x,y,partial);return true;
    }
    public void click(RecipeBrowserPanel panel,double x,double y,int button,int width,int height){input.press(button);var b=RecipeBrowserLayout.fit(width,height,panel.contentHeight());panel.click(b.localX(x),b.localY(y),button,178,0,186,0);}
    public boolean scroll(RecipeBrowserPanel panel,double x,double y,double delta,int width,int height){var b=RecipeBrowserLayout.fit(width,height,panel.contentHeight());panel.scroll(b.localX(x),b.localY(y),delta,178,0,186,0);return true;}
    public boolean key(int key,Runnable rebuild){if(!isOpen())return false;if(key==256){input.close();rebuild.run();}return true;}
}
