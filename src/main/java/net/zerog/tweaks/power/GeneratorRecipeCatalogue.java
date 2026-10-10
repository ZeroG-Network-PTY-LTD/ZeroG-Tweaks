package net.zerog.tweaks.power;

import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.machine.CombustionBlockEntity;

/** Production budgets, not crafting recipes. No mutation or client-authored power values. */
public final class GeneratorRecipeCatalogue {
    public record Burn(int ticks,int quarterRate,long energy) {}
    public static Burn combustion(ItemStack fuel,int modules){
        int ticks=CombustionBlockEntity.burnTime(fuel);
        int quarters=CombustionBlockEntity.fuelOutput(fuel)*(4+Math.clamp(modules,0,3));
        return new Burn(ticks,quarters,(long)ticks*quarters/4);
    }
    public static Burn fusion(int configuredRate,int configuredTicks,int modules,int capacity){
        int rate=(int)Math.min(Math.max(0,capacity),Math.max(0L,(long)configuredRate)*(4+Math.clamp(modules,0,3))/4);
        int ticks=Math.max(0,configuredTicks);
        return new Burn(ticks,rate*4,(long)ticks*rate);
    }
    private GeneratorRecipeCatalogue() {}
}
