package net.zerog.tweaks.client;

import com.mojang.blaze3d.platform.NativeImage;
import com.mojang.blaze3d.systems.RenderSystem;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.BooleanSupplier;
import net.minecraft.Util;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.ReceivingLevelScreen;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterDimensionTransitionScreenEvent;
import net.zerog.tweaks.registry.ZGDimensionTerrain;
import net.zerog.tweaks.registry.ZGWeatherConfig;
import net.zerog.tweaks.travel.GateLaunchSync;

/**
 * Gate transition screen v1 (Design branch: docs/gate-transition-screen-v1/README.md): the destination galaxy, a zoom
 * into its star system, then the planet with its nameplate, held until the level has loaded. Everything is drawn on a
 * fixed 480x270 stage at the largest whole-number pixel scale. Only replaces the vanilla screen for ZeroG jumps that
 * sent a GateLaunchSync.Destination; other dimension changes keep the vanilla screen.
 */
public final class GateTransitionScreen extends ReceivingLevelScreen {
    private static final int W=480,H=270,SPACE=0xFF0B0A16,SUB=0x9692B0,NAME=0xE8E4F6,GLOW=0xC48CFF,ORBIT=0x3C4268,DOT=0x6A6F94;
    /** Seconds: minimum before exit (the zoom always finishes), exit white-out, and how far SHORT skips ahead. */
    private static final double MIN=4.4,EXIT=0.4,SKIP=3.6,TYPE_RATE=24;
    private static final int[][] TARGET={{126,112},{64,76},{132,70},{58,118},{130,116}};
    private static final int[] SOL_ORBITS={34,58,86,120},ORBITS={40,70,100,132},WASTE_ORBITS={30,52,76,102,130};
    private static final int GRAVITY=0,HEAT=1,COLD=2,ACID=3,STORM=4,VOID=5,SAFE=6;
    private static final Map<String,ResourceLocation> TINTED=new HashMap<>();
    private record Chip(int icon,String label){}

    private final BooleanSupplier received;
    private final boolean shortMode;
    private final long start=Util.getMillis();
    private long exitAt=-1;
    private boolean chimed;
    private final int galaxy,slot;
    private final int[] orbits;
    private final ResourceLocation planetTexture;
    private final String galaxyLabel,systemLabel,catalog,name,klass,echo;
    private final List<Chip> chips=new ArrayList<>();

    private GateTransitionScreen(BooleanSupplier received,Reason reason,GateLaunchSync.Destination d,boolean shortMode){
        super(received,reason);
        this.received=received;this.shortMode=shortMode;
        galaxy=Mth.clamp(d.galaxy(),1,5);
        String prefix=galaxy==1?"SOL":galaxy==2?"ZG-855":"ZG-8"+galaxy+"0";
        galaxyLabel="GALAXY "+galaxy+"  |  "+prefix;
        String planet=d.planet(),gravity=String.format(Locale.ROOT,"%.1f×",d.gravity());
        String path=d.dimension().substring(d.dimension().indexOf(':')+1);
        switch(planet){
            case "earth"->{catalog="SOL III";name="Earth";klass="Home";systemLabel="SOL SYSTEM  |  3RD PLANET";orbits=SOL_ORBITS;slot=2;chips.add(new Chip(SAFE,"calm"));}
            case "moon"->{catalog="SOL III a";name="The Moon";klass="Earth's moon | Low gravity";systemLabel="SOL SYSTEM  |  3RD PLANET > 1ST MOON";orbits=SOL_ORBITS;slot=2;
                chips.add(new Chip(GRAVITY,gravity));chips.add(new Chip(SAFE,"calm"));}
            case "mars"->{catalog="SOL IV";name="Mars";klass="Rust world";systemLabel="SOL SYSTEM  |  4TH PLANET";orbits=SOL_ORBITS;slot=3;
                chips.add(new Chip(GRAVITY,gravity));chips.add(new Chip(STORM,"dust"));}
            case "cerulon","skarn","eidolon","solvane"->{catalog=prefix+" b";name=Character.toUpperCase(planet.charAt(0))+planet.substring(1);klass="Resource World";
                systemLabel=prefix+" SYSTEM  |  PLANET b";orbits=ORBITS;slot=0;chips.add(new Chip(GRAVITY,gravity));
                switch(planet){case "skarn","solvane"->chips.add(new Chip(HEAT,"heat"));case "eidolon"->chips.add(new Chip(COLD,"cold"));default->chips.add(new Chip(SAFE,"calm"));}}
            default->{
                if(planet.startsWith("wasteland_")){
                    // Until the seeded generator exists: ZG-8<N>0 <letter>, with the type name in place of the seeded name.
                    String type=planet.substring("wasteland_".length()),typeName=Character.toUpperCase(type.charAt(0))+type.substring(1);
                    boolean moons=path.endsWith("_moons");int m=moons?6:Math.max(1,path.length()>4?path.charAt(path.length()-1)-'0':1);
                    char letter=(char)('a'+m);
                    catalog=prefix+" "+letter+(moons?" I":"");name=typeName;klass=moons?"Moon":"Wasteland | "+typeName;
                    systemLabel=prefix+" SYSTEM  |  PLANET "+letter;orbits=WASTE_ORBITS;slot=(m-1)%WASTE_ORBITS.length;
                    chips.add(new Chip(GRAVITY,gravity));
                    switch(type){case "volcanic"->chips.add(new Chip(HEAT,"heat"));case "frozen"->chips.add(new Chip(COLD,"cold"));case "toxic"->chips.add(new Chip(ACID,"acid"));
                        case "desert","barren"->chips.add(new Chip(STORM,"dust"));default->chips.add(new Chip(SAFE,"calm"));}
                }else{planet="unknown";catalog="ZG-??";name="Unknown";klass="Signal only";systemLabel=prefix+" SYSTEM  |  ???";orbits=ORBITS;slot=1;chips.add(new Chip(VOID,"void"));}
            }
        }
        planetTexture=planetTexture(planet,galaxy);
        echo=echoLine(planet.startsWith("wasteland_")?"wasteland":planet,d.echo());
    }

    static ReceivingLevelScreen create(BooleanSupplier received,Reason reason){
        var d=GateLaunchSync.pendingDestination();var mode=ZGWeatherConfig.TRANSITION_SCREEN.get();
        return d==null||mode==ZGWeatherConfig.TransitionScreen.OFF?new ReceivingLevelScreen(received,reason)
                :new GateTransitionScreen(received,reason,d,mode==ZGWeatherConfig.TransitionScreen.SHORT);
    }

    @EventBusSubscriber(modid="zerog_tweaks",bus=EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
    public static final class Registration {
        @SubscribeEvent public static void register(RegisterDimensionTransitionScreenEvent event){
            for(String id:ZGDimensionTerrain.dimensions()){
                var key=ResourceKey.create(Registries.DIMENSION,ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id));
                event.registerIncomingEffect(key,GateTransitionScreen::create);event.registerOutgoingEffect(key,GateTransitionScreen::create);
            }
        }
        private Registration(){}
    }

    private static ResourceLocation tex(String name){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/transition/"+name+".png");}

    /** Echo's line from lang pool zerog_tweaks.transition.echo.<id>.<n>; locked or empty pools show the signal line. */
    private static String echoLine(String id,boolean unlocked){
        var pool=new ArrayList<String>();
        for(int n=0;unlocked&&I18n.exists("zerog_tweaks.transition.echo."+id+"."+n);n++)pool.add("zerog_tweaks.transition.echo."+id+"."+n);
        return I18n.get(pool.isEmpty()?"zerog_tweaks.transition.echo.locked":pool.get(ThreadLocalRandom.current().nextInt(pool.size())));
    }

    /** Wasteland sprites are gray: tint gray pixels with the block-tint maths; coloured (ember, glow) pixels stay as drawn. */
    private static ResourceLocation planetTexture(String planet,int galaxy){
        var base=tex("planet_"+planet);
        if(!planet.startsWith("wasteland_"))return base;
        return TINTED.computeIfAbsent(planet+"_g"+galaxy,key->{
            var mc=Minecraft.getInstance();
            try(var in=mc.getResourceManager().open(base)){
                NativeImage image=NativeImage.read(in);
                int tint=ZGBlockColors.tint(ZGBlockColors.WastelandType.valueOf(planet.substring("wasteland_".length()).toUpperCase(Locale.ROOT)),galaxy);
                int tr=tint>>16&255,tg=tint>>8&255,tb=tint&255;
                for(int y=0;y<image.getHeight();y++)for(int x=0;x<image.getWidth();x++){
                    int abgr=image.getPixelRGBA(x,y),a=abgr>>>24,b=abgr>>16&255,g=abgr>>8&255,r=abgr&255;
                    if(a!=0&&r==g&&g==b)image.setPixelRGBA(x,y,(a<<24)|((b*tb/255)<<16)|((g*tg/255)<<8)|(r*tr/255));
                }
                return mc.getTextureManager().register("zerog_transition_"+key,new DynamicTexture(image));
            }catch(IOException|IllegalArgumentException e){return base;}
        });
    }

    private double seconds(){return (Util.getMillis()-start)/1000.0;}
    private double stageTime(double t){return shortMode?t+SKIP:t;}
    private static float ease(double x){x=Mth.clamp(x,0,1);return (float)(x*x*(3-2*x));}
    private static float clamp01(double x){return (float)Mth.clamp(x,0,1);}
    private static int argb(int rgb,float alpha){return (Math.round(clamp01(alpha)*255)<<24)|(rgb&0xFFFFFF);}

    @Override public void tick(){
        long now=Util.getMillis();double t=seconds(),min=shortMode?MIN-SKIP:MIN;
        // Never leave before the zoom has finished; like vanilla, give up waiting after 30 seconds.
        if(exitAt<0&&(received.getAsBoolean()&&t>=min||t>30+min))exitAt=now;
        if(exitAt>=0&&now-exitAt>=EXIT*1000)onClose();
    }

    @Override public void onClose(){GateLaunchSync.clearDestination();super.onClose();}

    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partialTick){
        double t=seconds(),st=stageTime(t);
        g.fill(0,0,width,height,SPACE);
        var window=minecraft.getWindow();
        int pixels=Math.min(window.getWidth()/W,window.getHeight()/H);
        float k=pixels>=1?(float)(pixels/window.getGuiScale()):(float)(Math.min(window.getWidth()/(double)W,window.getHeight()/(double)H)/window.getGuiScale());
        float ox=(width-W*k)/2F,oy=(height-H*k)/2F;
        g.enableScissor(Mth.floor(ox),Mth.floor(oy),Mth.ceil(ox+W*k),Mth.ceil(oy+H*k));
        g.pose().pushPose();g.pose().translate(ox,oy,0);g.pose().scale(k,k,1);
        RenderSystem.enableBlend();RenderSystem.defaultBlendFunc();
        drawStage(g,st);
        g.setColor(1,1,1,1);
        g.pose().popPose();
        g.disableScissor();
        // Stage 0 continues the launch flash; stage 6 whites out again before the world appears.
        float white=Math.max(t<0.5?1F-(float)(t/0.5):0F,exitAt>=0?clamp01((Util.getMillis()-exitAt)/(EXIT*1000)):0F);
        if(white>0)g.fill(0,0,width,height,argb(0xFFFFFF,white));
    }

    @Override public void renderBackground(GuiGraphics g,int mouseX,int mouseY,float partialTick){}

    private void drawStage(GuiGraphics g,double st){
        g.fill(0,0,W,H,SPACE);
        starfield(g,"starfield_far",6,1,st,1);starfield(g,"nebula",3,.5,st,.25F);
        starfield(g,"starfield_mid",12,2,st,1);starfield(g,"starfield_near",18,3,st,1);
        float streak=st<2.5?bump(st,1.5,2.5):bump(st,3.2,3.9);
        if(streak>0)streaks(g,st,streak);
        if(st<2.5)galaxy(g,st);
        if(st>=2.2&&st<3.9)system(g,st);
        if(st>=3.6)planet(g,st);
    }

    private static float bump(double st,double from,double to){return st<=from||st>=to?0:(float)Math.sin(Math.PI*(st-from)/(to-from));}

    private void starfield(GuiGraphics g,String name,double driftX,double driftY,double st,float alpha){
        g.setColor(1,1,1,alpha);
        g.blit(tex(name),0,0,(float)((st*driftX)%256),(float)((st*driftY)%256),W,H,256,256);
        g.setColor(1,1,1,1);
    }

    /** Near stars become radial streaks during the two zooms. */
    private void streaks(GuiGraphics g,double st,float strength){
        int cx=W/2,cy=H/2;
        for(int i=0;i<48;i++){
            double angle=i*2.39996,speed=.6+(i*37%10)/10.0,r=((i*53%240)+st*160*speed)%260+10;int len=(int)(4+strength*16*speed);
            double dx=Math.cos(angle),dy=Math.sin(angle);
            for(int p=0;p<len;p++){int x=(int)(cx+dx*(r+p)),y=(int)(cy+dy*(r+p));g.fill(x,y,x+1,y+1,argb(NAME,strength*(p+1)/len));}
        }
    }

    private void galaxy(GuiGraphics g,double st){
        int[] target=TARGET[galaxy-1];int cx=144+target[0],cy=33+target[1];
        float zoom=st<1.5?1:1+9*ease((st-1.5)/1.0),alpha=st<2.2?1:1-clamp01((st-2.2)/.3);
        g.pose().pushPose();g.pose().translate(cx,cy,0);g.pose().scale(zoom,zoom,1);g.pose().translate(-target[0],-target[1],0);
        g.setColor(1,1,1,alpha);g.blit(tex("galaxy_"+galaxy),0,0,0,0,192,192,192,192);g.setColor(1,1,1,1);
        g.pose().popPose();
        if(st<1.5){
            float size=st<.4?3:3-2*ease((st-.4)/.6);
            reticle(g,cx,cy,size,st);
        }
        g.drawString(font,galaxyLabel,12,11,argb(SUB,alpha),false);
        if(st>.9&&st<2.2)g.drawString(font,I18n.get("zerog_tweaks.transition.locking"),12,22,argb(GLOW,1),false);
    }

    private void reticle(GuiGraphics g,float x,float y,float scale,double st){
        g.pose().pushPose();g.pose().translate(x,y,0);g.pose().scale(scale,scale,1);
        g.blit(tex("reticle"),-12,-12,0,((int)(st*8)%4)*24,24,24,24,96);
        g.pose().popPose();
    }

    private void system(GuiGraphics g,double st){
        float alpha=st<2.5?clamp01((st-2.2)/.3):st>3.6?1-clamp01((st-3.6)/.3):1;
        float zoom=st<3.2?1:1+3*ease((st-3.2)/.7);
        int cx=190,cy=135,dx=cx-orbits[slot],dy=cy;
        g.pose().pushPose();g.pose().translate(dx,dy,0);g.pose().scale(zoom,zoom,1);g.pose().translate(-dx,-dy,0);
        for(int i=0;i<orbits.length;i++){
            boolean target=i==slot;int colour=argb(target?GLOW:ORBIT,alpha);
            for(int deg=0;deg<360;deg++){
                if(!target&&deg%6>=3)continue;                              // off-target orbits are dotted
                double a=Math.toRadians(deg);int x=(int)Math.round(cx+orbits[i]*Math.cos(a)),y=(int)Math.round(cy+orbits[i]*.32*Math.sin(a));
                g.fill(x,y,x+1,y+1,colour);
            }
            if(!target){double a=Math.toRadians((i*97+40)%360);int x=(int)Math.round(cx+orbits[i]*Math.cos(a)),y=(int)Math.round(cy+orbits[i]*.32*Math.sin(a));g.fill(x-1,y-1,x+1,y+1,argb(DOT,alpha));}
        }
        g.setColor(1,1,1,alpha);g.blit(tex("star_"+galaxy),166,111,0,((int)(st*8)%4)*48,48,48,48,192);
        g.fill(dx-1,dy-1,dx+2,dy+2,argb(0xFFFFFF,alpha));reticle(g,dx,dy,1,st);g.setColor(1,1,1,1);
        g.pose().popPose();
        g.drawString(font,systemLabel,12,11,argb(SUB,alpha),false);
    }

    private void planet(GuiGraphics g,double st){
        float grow=.2F+.8F*ease((st-3.6)/.9);int frame=st<4.4?0:(int)((st-4.4)*6)%16;
        g.pose().pushPose();g.pose().translate(168,128,0);g.pose().scale(grow,grow,1);
        g.blit(planetTexture,-64,-64,0,frame*128,128,128,128,2048);
        g.pose().popPose();
        // Nameplate slides in from the right to x=262 and chimes when it lands.
        int x=st<3.9?W:Math.round(Mth.lerp(ease((st-3.9)/.6),W,262)),y=82;
        if(!chimed&&st>=4.5){chimed=true;minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.AMETHYST_BLOCK_CHIME,1.2F,.8F));}
        if(x<W){
            nineSlice(g,tex("nameplate"),x,y,196,92);
            g.drawString(font,catalog,x+12,y+11,argb(SUB,1),false);
            g.drawString(font,name,x+12,y+22,argb(NAME,1),false);
            g.drawString(font,klass,x+12,y+33,argb(GLOW,1),false);
            int chipX=x+12;
            for(var chip:chips){g.blit(tex("hazard_icons"),chipX,146,chip.icon()*9,0,9,9,63,9);g.drawString(font,chip.label(),chipX+11,147,argb(SUB,1),false);chipX+=21+font.width(chip.label());}
        }
        if(st<4.4)return;
        int typed=Math.min(echo.length(),(int)((st-4.4)*TYPE_RATE));
        g.drawString(font,echo.substring(0,typed),148,206,argb(NAME,1),false);
        g.blit(tex("echo_wisp"),126,221+Math.round((float)Math.sin(st*3)),0,((int)(st*4)%2)*16,16,16,16,32);
        // ReceivingLevelScreen has no load percentage: ease towards 90% over time, fill when the level has arrived.
        boolean done=received.getAsBoolean();float progress=done?1F:.9F*(1F-(float)Math.exp(-(st-4.4)/2.5));
        g.blit(tex("progress_frame"),148,226,0,0,184,9,184,9);
        int fill=Math.round(180*progress);if(fill>0)g.blit(tex("progress_fill"),150,228,0,0,fill,5,180,5);
        g.drawString(font,I18n.get(done?"zerog_tweaks.transition.stable":"zerog_tweaks.transition.stabilising"),148,239,argb(done?GLOW:SUB,1),false);
    }

    /** 32x32 nameplate, 9-slice with 8 px borders. */
    private static void nineSlice(GuiGraphics g,ResourceLocation tex,int x,int y,int w,int h){
        int b=8,iw=w-2*b,ih=h-2*b;
        g.blit(tex,x,y,0,0,b,b,32,32);g.blit(tex,x+w-b,y,24,0,b,b,32,32);g.blit(tex,x,y+h-b,0,24,b,b,32,32);g.blit(tex,x+w-b,y+h-b,24,24,b,b,32,32);
        g.blit(tex,x+b,y,iw,b,8,0,16,8,32,32);g.blit(tex,x+b,y+h-b,iw,b,8,24,16,8,32,32);
        g.blit(tex,x,y+b,b,ih,0,8,8,16,32,32);g.blit(tex,x+w-b,y+b,b,ih,24,8,8,16,32,32);
        g.blit(tex,x+b,y+b,iw,ih,8,8,16,16,32,32);
    }
}
