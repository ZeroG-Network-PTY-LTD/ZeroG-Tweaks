package net.zerog.tweaks.guide;

/** Adaptation of the supplied GUI to the shipped addon, without changing inventory indices. */
public final class AlvearyLayout {
    public static final int WIDTH=256, HEIGHT=250;
    public static int tier(String id) {
        if(id.equals("apiary_controller"))return 1;
        if(id.equals("zero_g_hive"))return 8;
        if(id.matches("tier[1-7]_controller"))return id.charAt(4)-'0';
        return 0;
    }
    public static int frames(int tier) { return tier==8?3:Math.min(tier+1,7); }
    public static int products(int tier) { return tier==8?10:Math.min(6+tier*2,18); }
    public static int machineSlots(int tier) { return 2+frames(tier)+products(tier); }
    public static int[] position(int tier,int index) {
        return position(tier,index,0);
    }
    public static boolean visible(int tier,int index,int page) {
        int first=2+frames(tier),last=machineSlots(tier);
        return index<first || index>=last || (index-first)/9==page;
    }
    public static int[] position(int tier,int index,int page) {
        int count=machineSlots(tier);
        if(index==0)return new int[]{17,27};
        if(index==1)return new int[]{17,55};
        if(index<2+frames(tier)) { int i=index-2;return new int[]{12+(i%9)*18,99+(i/9)*18}; }
        if(index<count) { int i=(index-2-frames(tier))%9;return new int[]{140+(i%3)*18,23+(i/3)*18}; }
        int player=index-count;
        if(player<27)return new int[]{48+(player%9)*18,169+(player/9)*18};
        return new int[]{48+(player-27)*18,227};
    }
    private AlvearyLayout() {}
}
