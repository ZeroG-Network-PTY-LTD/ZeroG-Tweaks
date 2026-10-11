package net.zerog.tweaks.machine;
/** Read-only recipe quantities from the menu's authoritative synchronized values. */
public final class GasSeparatorRecipeCatalogue {
    public record Page(int water,int hydrogen,int oxygen,int baseEnergy,int energy,int baseTicks,int ticks){}
    public static Page page(GasSeparatorMenu menu){
        int water=menu.value(10),base=menu.baseCost(),cost=menu.cost(),ticks=menu.value(6),baseTicks=menu.value(13);
        if(water<=0||base<=0||cost<=0||ticks<=0||baseTicks<=0)return null;
        return new Page(water,water*2,water,base,cost,baseTicks,ticks);
    }
    private GasSeparatorRecipeCatalogue(){}
}
