package net.zerog.tweaks.machine;

/** Independent bounded geometry; no client classes so server tests can check it. */
public record RecipeBrowserLayout(int left,int top,float scale,int backLeft,int backTop,int panelHeight) {
    public static RecipeBrowserLayout fit(int width,int height,int contentHeight){
        float scale=Math.min(1F,Math.min(Math.max(1,width-8)/174F,Math.max(1,height-44)/(float)contentHeight));
        return new RecipeBrowserLayout((int)((width-174*scale)/2),20,scale,(width-140)/2,
            24+(int)Math.ceil(contentHeight*scale),contentHeight);
    }
    public double localX(double screenX){return (screenX-left)/scale;}
    public double localY(double screenY){return (screenY-top)/scale;}
}
