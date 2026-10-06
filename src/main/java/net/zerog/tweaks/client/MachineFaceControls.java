package net.zerog.tweaks.client;

import net.minecraft.client.gui.components.*;
import net.minecraft.network.chat.Component;
import net.zerog.tweaks.machine.*;

/** Show only capability families the actual machine supports. */
public final class MachineFaceControls {
    private int family;
    public void add(int x,int y,MachineSideMenu menu,java.util.function.Consumer<AbstractWidget> add,java.util.function.IntConsumer send){
        var panel=new SideConfigurationPanel(x,y,s->menu.sideMode(family*6+s),s->{int old=menu.sideMode(family*6+s),next=family==1?(old==3?1:3):(old+1)%4;send.accept(500+family*24+s*4+next);},"",false);
        add.accept(panel);
        for(int i=0;i<3;i++)if(LegacyMachineSides.supportsFamily(menu.sideMachine(),i)){
            final int selected=i;
            add.accept(Button.builder(Component.literal(i==0?"Items":i==1?"Power":"Fluids"),b->{family=selected;panel.labels(iLabel(),family==1?"FE only":"");panel.inputOnly(family==1);}).bounds(x,y+130+i*19,94,18).build());
        }
        panel.labels(iLabel(),family==1?"FE only":"");panel.inputOnly(family==1);
        var upgrades=Button.builder(Component.literal("Upgrades: none"),b->{}).bounds(x,y+197,94,18).build();
        upgrades.active=false;
        upgrades.setTooltip(Tooltip.create(Component.literal("This machine has no supported upgrade sockets. Recipe reagents and genetics catalysts are not upgrades.")));
        add.accept(upgrades);
    }
    private String iLabel(){return family==0?"Item faces":family==1?"Power faces":"Fluid faces";}
}
