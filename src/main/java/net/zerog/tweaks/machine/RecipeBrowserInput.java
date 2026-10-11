package net.zerog.tweaks.machine;
/** Overlay-owned mouse presses retain their release even when Back closes it. */
public final class RecipeBrowserInput {
    private boolean open;
    private int held;
    public boolean isOpen(){return open;}
    public void open(){open=true;}
    public void close(){open=false;}
    public void press(int button){if(open&&button>=0&&button<8)held|=1<<button;}
    public boolean consumeRelease(int button){boolean owned=button>=0&&button<8&&(held&(1<<button))!=0;if(owned)held&=~(1<<button);return open||owned;}
}
