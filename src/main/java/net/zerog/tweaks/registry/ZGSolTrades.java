package net.zerog.tweaks.registry;

import com.google.common.collect.ImmutableSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.ai.village.poi.PoiType;
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.*;
import net.neoforged.neoforge.event.village.VillagerTradesEvent;

/** Planet trades use ordinary limited villager offers; no gate progression bypass. */
public final class ZGSolTrades {
    private static final DeferredRegister<PoiType> POIS=DeferredRegister.create(Registries.POINT_OF_INTEREST_TYPE,"zerog_tweaks");
    private static final DeferredRegister<VillagerProfession> JOBS=DeferredRegister.create(Registries.VILLAGER_PROFESSION,"zerog_tweaks");
    public static final DeferredHolder<PoiType,PoiType> REFINERY=POIS.register("regolith_refiner",()->new PoiType(java.util.Set.copyOf(BlockInit.ORE_REFINERY.get().getStateDefinition().getPossibleStates()),1,1));
    public static final DeferredHolder<PoiType,PoiType> GENERATOR=POIS.register("rust_mechanic",()->new PoiType(java.util.Set.copyOf(BlockInit.COMBUSTION_GENERATOR.get().getStateDefinition().getPossibleStates()),1,1));
    public static final DeferredHolder<VillagerProfession,VillagerProfession> REFINER=JOBS.register("regolith_refiner",()->new VillagerProfession("regolith_refiner",h->h.is(REFINERY.getKey()),h->h.is(REFINERY.getKey()),ImmutableSet.of(),ImmutableSet.of(),net.minecraft.sounds.SoundEvents.VILLAGER_WORK_MASON));
    public static final DeferredHolder<VillagerProfession,VillagerProfession> MECHANIC=JOBS.register("rust_mechanic",()->new VillagerProfession("rust_mechanic",h->h.is(GENERATOR.getKey()),h->h.is(GENERATOR.getKey()),ImmutableSet.of(),ImmutableSet.of(),net.minecraft.sounds.SoundEvents.VILLAGER_WORK_TOOLSMITH));
    public static void register(IEventBus bus) { POIS.register(bus);JOBS.register(bus); }
    public static void trades(VillagerTradesEvent event) {
        if(event.getType()==REFINER.get()) {
            event.getTrades().get(1).add((villager,random)->new MerchantOffer(new ItemCost(ItemInit.REGOLITH_ITEM.get(),24),new ItemStack(Items.EMERALD),12,2,.05F));
            event.getTrades().get(2).add((villager,random)->new MerchantOffer(new ItemCost(Items.EMERALD,3),new ItemStack(ItemInit.LUNAR_LICHEN_ITEM.get(),4),8,5,.05F));
            event.getTrades().get(3).add((villager,random)->new MerchantOffer(new ItemCost(Items.EMERALD,8),new ItemStack(ItemInit.MOONSTEEL_INGOT.get()),4,10,.05F));
        } else if(event.getType()==MECHANIC.get()) {
            event.getTrades().get(1).add((villager,random)->new MerchantOffer(new ItemCost(Items.COAL,16),new ItemStack(Items.EMERALD),12,2,.05F));
            event.getTrades().get(2).add((villager,random)->new MerchantOffer(new ItemCost(Items.EMERALD,3),new ItemStack(ItemInit.RUST_TUBER.get(),4),8,5,.05F));
            event.getTrades().get(3).add((villager,random)->new MerchantOffer(new ItemCost(Items.EMERALD,8),new ItemStack(ItemInit.FERROX_INGOT.get()),4,10,.05F));
        }
    }
    private ZGSolTrades() {}
}
