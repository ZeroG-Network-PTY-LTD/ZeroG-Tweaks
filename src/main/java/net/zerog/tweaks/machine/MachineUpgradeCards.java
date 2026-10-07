package net.zerog.tweaks.machine;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Typed, independent upgrade families; legacy ingredients are never new cards. */
public final class MachineUpgradeCards {
    public enum Family { ACCELERATION, ENERGY_COIL, ITEM_COMPACT }
    public static final class Card extends Item {
        public final Family family;
        public final int tier;
        public Card(Family family,int tier){super(new Item.Properties().stacksTo(1));this.family=family;this.tier=tier;}
    }
    public static Map<String,DeferredItem<Item>> register(DeferredRegister.Items registry){
        var cards=new LinkedHashMap<String,DeferredItem<Item>>();
        for(var family:Family.values())for(int tier=1;tier<=6;tier++){
            int selected=tier;
            String id=switch(family){case ACCELERATION->"acceleration";case ENERGY_COIL->"energy_coil";case ITEM_COMPACT->"item_compact";}+"_upgrade_card_t"+tier;
            cards.put(id,registry.register(id,()->new Card(family,selected)));
        }
        return cards;
    }
    public static int tier(ItemStack stack,Family family){return !stack.isEmpty()&&stack.getItem() instanceof Card card&&card.family==family?card.tier:0;}
    private MachineUpgradeCards(){}
}
