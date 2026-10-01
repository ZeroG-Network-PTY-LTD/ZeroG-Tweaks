package net.zerog.tweaks.client;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.network.chat.Component;
import net.minecraft.util.Mth;
import net.zerog.tweaks.guide.MultiblockGuides;
import net.zerog.tweaks.guide.MultiblockGuides.Cell;
import net.zerog.tweaks.guide.MultiblockGuides.Layout;

/** Rotatable, clickable schematic. Colour cubes are role references, not fake working blocks. */
public final class MultiblockGuideScreen extends Screen {
    private int index, layer, roleScroll;
    private boolean cumulative = true;
    private double yaw = 215, pitch = 25, zoom = 1;
    private Cell selected;
    private Button modeButton, layerButton;
    private List<Face> faces = List.of();
    private record Point(float x, float y, double depth) {}
    private record Face(Cell cell, Point[] points, double depth, int color) {}

    public MultiblockGuideScreen() {
        super(Component.literal("ZeroG Multiblock Reference"));
        layer = layout().maxY();
    }
    private Layout layout() { return MultiblockGuides.layouts().get(index); }
    private int panelX() { return width - Math.min(174, width / 2); }
    private static Component text(String value) { return Component.literal(value); }
    private static String label(String value) {
        StringBuilder result = new StringBuilder();
        for (String word : value.split("_")) {
            if (!result.isEmpty()) result.append(' ');
            result.append(Character.toUpperCase(word.charAt(0))).append(word.substring(1));
        }
        return result.toString();
    }
    private Button button(String title, int x, int y, int w, Button.OnPress action) {
        return addRenderableWidget(Button.builder(text(title), action).bounds(x,y,w,20).build());
    }
    @Override protected void init() {
        button("< Structure", 8, 25, 91, b -> change(-1));
        button("Structure >", 102, 25, 91, b -> change(1));
        button("Close", width-58, 25, 50, b -> onClose());
        button("Y -", 8, 49, 42, b -> setLayer(layer-1));
        layerButton = button("Y="+layer, 53, 49, 55, b -> setLayer(layout().maxY()));
        button("Y +", 111, 49, 42, b -> setLayer(layer+1));
        modeButton = button(cumulative ? "From Y=0" : "One layer", 156, 49, 84, b -> {
            cumulative = !cumulative; b.setMessage(text(cumulative ? "From Y=0" : "One layer"));
        });
        button("Turn 90", 8, 73, 70, b -> yaw = (yaw+90)%360);
        button("Reset view", 82, 73, 84, b -> { yaw=215;pitch=25;zoom=1; });
    }
    private void change(int amount) {
        index = Math.floorMod(index+amount, MultiblockGuides.layouts().size());
        layer = layout().maxY(); selected=null; roleScroll=0;
        layerButton.setMessage(text("Y="+layer));
    }
    private void setLayer(int value) {
        layer = Mth.clamp(value,0,layout().maxY());
        layerButton.setMessage(text("Y="+layer));
        if (selected != null && (selected.y()>layer || !cumulative && selected.y()!=layer)) selected=null;
    }
    /** Opt-in client test pose; read-only schematic state, no world changes. */
    public void reviewPose(double angle, int y, boolean through) {
        yaw=angle; cumulative=through; setLayer(y);
        modeButton.setMessage(text(cumulative ? "From Y=0" : "One layer"));
    }
    public int renderedFaces() { return faces.size(); }
    public void reviewLayout(int value) {
        index=Math.floorMod(value,MultiblockGuides.layouts().size());
        selected=null;roleScroll=0;setLayer(layout().maxY());
    }
    public static int partColor(String part) {
        return switch (part) {
            case "controller" -> 0xffe4b74d;
            case "input_hatch", "hatch", "frame_loader" -> 0xff53ca78;
            case "output_hatch", "honey_port" -> 0xffe68b45;
            case "energy_port" -> 0xffee5965;
            case "fluid_port", "humidifier" -> 0xff55bbdf;
            case "frame_housing" -> 0xffb987de;
            case "glass" -> 0xff7197aa;
            case "roof", "crown" -> 0xff6a7b92;
            case "heater", "dryer" -> 0xffd09169;
            case "coil", "emitter", "focus", "lens" -> 0xffb76fcd;
            default -> 0xff8d9caa;
        };
    }
    private Point project(double x, double y, double z) {
        double a=Math.toRadians(yaw), b=Math.toRadians(pitch);
        double rx=x*Math.cos(a)+z*Math.sin(a), rz=-x*Math.sin(a)+z*Math.cos(a);
        double ry=y*Math.cos(b)-rz*Math.sin(b), depth=y*Math.sin(b)+rz*Math.cos(b);
        double size=Math.max(layout().maxX()+1, Math.max(layout().maxZ()+1, layout().maxY()+1));
        double scale=Math.min((panelX()-20)/(size*1.65), Math.max(24,height-135)/(size*1.65))*zoom;
        return new Point((float)(panelX()/2.0+rx*scale), (float)((105+height-35)/2.0-ry*scale),depth);
    }
    private void buildFaces() {
        List<Face> result=new ArrayList<>();
        int[][] sides={{0,3,2,1},{4,5,6,7},{0,4,7,3},{1,2,6,5},{0,1,5,4},{3,7,6,2}};
        double[][] normals={{0,0,-1},{0,0,1},{-1,0,0},{1,0,0},{0,-1,0},{0,1,0}};
        double a=Math.toRadians(yaw), b=Math.toRadians(pitch);
        for (Cell cell:layout().cells()) {
            if (cell.y()>layer || !cumulative && cell.y()!=layer) continue;
            double x=cell.x()-(layout().maxX()+1)/2.0;
            double y=cell.y()-(layout().maxY()+1)/2.0;
            double z=cell.z()-(layout().maxZ()+1)/2.0;
            // Tiny gaps keep individual reference blocks identifiable; no geometry is exported.
            double lo=.025, hi=.975;
            Point[] corners={project(x+lo,y+lo,z+lo),project(x+hi,y+lo,z+lo),
                    project(x+hi,y+hi,z+lo),project(x+lo,y+hi,z+lo),
                    project(x+lo,y+lo,z+hi),project(x+hi,y+lo,z+hi),
                    project(x+hi,y+hi,z+hi),project(x+lo,y+hi,z+hi)};
            for (int n=0;n<sides.length;n++) {
                double[] normal=normals[n];
                double facing=normal[1]*Math.sin(b)+(-normal[0]*Math.sin(a)+normal[2]*Math.cos(a))*Math.cos(b);
                if (facing<=0) continue;
                Point[] vertices=new Point[4]; double depth=0;
                for (int j=0;j<4;j++) { vertices[j]=corners[sides[n][j]];depth+=vertices[j].depth(); }
                int base=selected!=null && selected.equals(cell) ? 0xffffff7a : partColor(cell.part());
                double shade=.55+.45*facing;
                int color=0xff000000 | (int)(((base>>16)&255)*shade)<<16
                        | (int)(((base>>8)&255)*shade)<<8 | (int)((base&255)*shade);
                result.add(new Face(cell,vertices,depth/4,color));
            }
        }
        result.sort(Comparator.comparingDouble(Face::depth)); faces=result;
    }
    @Override public void render(GuiGraphics g, int mouseX, int mouseY, float delta) {
        g.fill(0,0,width,height,0xff101723);
        g.drawString(font,title,8,8,0xffdce9ff,false);
        g.drawString(font,font.plainSubstrByWidth(label(layout().id()),panelX()-16),8,100,0xffdce9ff,false);
        g.fill(6,113,panelX()-6,height-30,0xff182332);
        buildFaces();
        g.enableScissor(6,113,panelX()-6,height-30);
        var consumer=g.bufferSource().getBuffer(RenderType.gui());
        for (Face face:faces) for (Point point:face.points())
            consumer.addVertex(g.pose().last().pose(),point.x(),point.y(),0).setColor(face.color());
        g.flush(); g.disableScissor();
        renderDetails(g);
        g.drawString(font,"Drag: 360 view | Wheel: zoom | Click: part",8,height-23,0xffaabed6,false);
        g.drawString(font,"Reference diagram only - not machine formation",8,height-12,0xffd6b472,false);
        super.render(g,mouseX,mouseY,delta);
    }
    private void renderDetails(GuiGraphics g) {
        int x=panelX()+4, w=width-x-6;
        g.drawString(font,String.format(Locale.ROOT,"View %.0f degrees / Y %s%d",Math.floorMod((int)yaw,360)*1.0,
                cumulative?"0..":"",layer),x,77,0xffb2cee7,false);
        g.drawString(font,"Base origin: (0,0,0)",x,89,0xffb2cee7,false);
        int y=104;
        if (selected!=null) {
            g.drawString(font,label(selected.part()),x,y,0xffffff7a,false);y+=11;
            g.drawString(font,"X="+selected.x()+" Y="+selected.y()+" Z="+selected.z(),x,y,0xffdce9ff,false);y+=11;
            g.drawString(font,"Only authored part at this cell",x,y,0xffa9bcd1,false);y+=12;
        }
        g.drawString(font,"Parts / total quantity",x,y,0xffdce9ff,false);y+=12;
        var roles=new ArrayList<>(layout().quantities().entrySet());
        int available=Math.max(1,(height-71-y)/11);
        roleScroll=Mth.clamp(roleScroll,0,Math.max(0,roles.size()-available));
        for (int i=roleScroll;i<Math.min(roles.size(),roleScroll+available);i++) {
            var entry=roles.get(i);
            g.fill(x,y+2,x+6,y+8,partColor(entry.getKey()));
            String line=label(entry.getKey())+" x"+entry.getValue();
            g.drawString(font,font.plainSubstrByWidth(line,w-10),x+10,y,0xffdce9ff,false);y+=11;
        }
        g.drawString(font,"Genes + cryo: external modules",x,height-58,0xffb987de,false);
        g.drawString(font,"No shell/hatch replacements",x,height-47,0xffa9bcd1,false);
        g.drawString(font,"Apiary blocks: runtime pending",x,height-36,0xffd6b472,false);
    }
    private static boolean contains(Face face,double x,double y) {
        boolean positive=false, negative=false;
        for(int i=0;i<4;i++) {
            Point a=face.points()[i], b=face.points()[(i+1)%4];
            double cross=(b.x()-a.x())*(y-a.y())-(b.y()-a.y())*(x-a.x());
            positive|=cross>0;negative|=cross<0;
        }
        return !(positive&&negative);
    }
    @Override public boolean mouseClicked(double x,double y,int button) {
        if(super.mouseClicked(x,y,button)) return true;
        if(button==0 && x>6 && x<panelX()-6 && y>113 && y<height-30) {
            selected=null;
            for(Face face:faces) if(contains(face,x,y)) selected=face.cell();
            return true;
        }
        return false;
    }
    @Override public boolean mouseDragged(double x,double y,int button,double dx,double dy) {
        if(button==0 && x<panelX() && y>105 && y<height-30) {
            yaw=(yaw+dx*.7)%360;pitch=Mth.clamp(pitch+dy*.7,-80,80);return true;
        }
        return super.mouseDragged(x,y,button,dx,dy);
    }
    @Override public boolean mouseScrolled(double x,double y,double horizontal,double vertical) {
        if(x>=panelX()) roleScroll+=vertical>0?-1:1;
        else zoom=Mth.clamp(zoom+vertical*.1,.5,2.5);
        return true;
    }
    @Override public boolean isPauseScreen() { return false; }
}
