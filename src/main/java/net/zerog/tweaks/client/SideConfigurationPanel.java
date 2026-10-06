package net.zerog.tweaks.client;

import java.util.function.IntConsumer;
import java.util.function.IntUnaryOperator;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.AbstractWidget;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.network.chat.Component;

/** Shared world-face matrix. Empty cells never send a routing command. */
public final class SideConfigurationPanel extends AbstractWidget {
    // Direction ordinal: Down, Up, North, South, West, East. A labelled world-face map, not camera-relative.
    private static final int[][] CELLS={{0,2},{1,0},{1,1},{1,2},{0,1},{2,1}};
    private static final String[] LABELS={"D","U","N","S","W","E"};
    private static final String[] FACES={"Down","Up","North","South","West","East"};
    private static final String[] MODES={"Both","Input","Output","Off"};
    private static final int[] COLORS={0xffb169e8,0xffdf5059,0xff64cd84,0xff596674};
    private final IntUnaryOperator mode;
    private final IntConsumer send;
    private final String extra;
    private final boolean powerOnly;
    private int selected;
    public SideConfigurationPanel(int x,int y,IntUnaryOperator mode,IntConsumer send,String extra){
        this(x,y,mode,send,extra,false);
    }
    public SideConfigurationPanel(int x,int y,IntUnaryOperator mode,IntConsumer send,String extra,boolean powerOnly){super(x,y,94,126,Component.literal("Side configuration"));this.mode=mode;this.send=send;this.extra=extra;this.powerOnly=powerOnly;}
    private int mode(int side){return Math.max(0,Math.min(3,mode.applyAsInt(side)));}
    private Component description(int side){return Component.literal(FACES[side]+": "+MODES[mode(side)]+extra);}
    private int hit(double x,double y){for(int i=0;i<6;i++){int xx=getX()+13+CELLS[i][0]*23,yy=getY()+26+CELLS[i][1]*23;if(x>=xx&&x<xx+21&&y>=yy&&y<yy+21)return i;}return -1;}
    @Override protected void renderWidget(GuiGraphics g,int mouseX,int mouseY,float partial){
        var font=Minecraft.getInstance().font;g.fill(getX(),getY(),getX()+width,getY()+height,0xff172733);
        g.drawString(font,powerOnly?"Power faces":"Side config",getX()+6,getY()+6,0xffe0eff7,false);
        g.drawString(font,"World faces",getX()+6,getY()+16,0xffa7bdcb,false);
        for(int col=0;col<3;col++)for(int row=0;row<3;row++){int xx=getX()+13+col*23,yy=getY()+26+row*23;g.fill(xx,yy,xx+21,yy+21,0xff263641);}
        int hover=hit(mouseX,mouseY);
        for(int i=0;i<6;i++){int xx=getX()+13+CELLS[i][0]*23,yy=getY()+26+CELLS[i][1]*23;g.fill(xx,yy,xx+21,yy+21,i==hover||isFocused()&&selected==i?0xffedf5ff:0xff0b141e);g.fill(xx+1,yy+1,xx+20,yy+20,COLORS[mode(i)]);g.drawCenteredString(font,LABELS[i],xx+10,yy+6,0xff101b24);}
        if(powerOnly){g.drawString(font,"Input",getX()+7,getY()+100,COLORS[1],false);g.drawString(font,"Off",getX()+49,getY()+100,0xffacbac5,false);g.drawString(font,"FE only",getX()+7,getY()+113,0xffa7bdcb,false);}
        else{g.drawString(font,"In",getX()+7,getY()+100,COLORS[1],false);g.drawString(font,"Out",getX()+35,getY()+100,COLORS[2],false);g.drawString(font,"Both",getX()+7,getY()+113,COLORS[0],false);g.drawString(font,"Off",getX()+49,getY()+113,0xffacbac5,false);}
        setTooltip(hover>=0?Tooltip.create(description(hover)):null);
    }
    @Override public void onClick(double x,double y){int side=hit(x,y);if(side>=0){selected=side;send.accept(side);}}
    @Override public boolean keyPressed(int key,int scan,int modifiers){if(!isFocused())return false;if(key==262||key==264){selected=(selected+1)%6;return true;}if(key==263||key==265){selected=(selected+5)%6;return true;}if(key==257||key==32){send.accept(selected);return true;}return false;}
    @Override protected void updateWidgetNarration(NarrationElementOutput output){setMessage(description(selected));defaultButtonNarrationText(output);}
}
