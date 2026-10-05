package net.zerog.tweaks.event;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.zerog.tweaks.config.ZGProgressionConfig;

/** Transient modifier, removed outside ZeroG; periodic reconciliation handles respawns. */
public final class PlanetGravity {
    public static final ResourceLocation ID=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planet_gravity");
    public static double multiplier(String dimension,long seed) {
        if(!dimension.startsWith("zerog_tweaks:"))return 1.0;
        String name=dimension.substring(13);
        String[] ids={"moon","mars","cerulon","skarn","eidolon","solvane"};
        for(int i=0;i<ids.length;i++)if(ids[i].equals(name))return ZGProgressionConfig.GRAVITY.get(i).get();
        if(name.matches("g[2-5]_(p[1-6]|moons)"))return 0.6+Math.floorMod(seed^name.hashCode()*0x9E3779B97F4A7C15L,701)/1000.0;
        return 1.0;
    }
    public static void apply(ServerPlayer player) {
        var attribute=player.getAttribute(Attributes.GRAVITY);if(attribute==null)return;
        double amount=multiplier(player.level().dimension().location().toString(),player.serverLevel().getSeed())-1;
        var old=attribute.getModifier(ID);
        if(old!=null&&Math.abs(old.amount()-amount)<0.000001)return;
        attribute.removeModifier(ID);
        if(amount!=0)attribute.addTransientModifier(new AttributeModifier(ID,amount,AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL));
    }
    public static void changed(PlayerEvent.PlayerChangedDimensionEvent event){if(event.getEntity() instanceof ServerPlayer p){apply(p);net.zerog.tweaks.item.ConcordCodexItem.recordArrival(p);}}
    public static void tick(PlayerTickEvent.Post event){if(event.getEntity() instanceof ServerPlayer p&&p.tickCount%20==0)apply(p);}
    public static void cloned(PlayerEvent.Clone event){
        var old=event.getOriginal().getPersistentData();var data=event.getEntity().getPersistentData();
        for(String key:new String[]{"zerog_codex_moon","zerog_codex_mars"})if(old.getBoolean(key))data.putBoolean(key,true);
        if(old.contains("zerog_home_gate"))data.put("zerog_home_gate",old.getCompound("zerog_home_gate").copy());
        if(old.contains("zerog_recall_until"))data.putLong("zerog_recall_until",old.getLong("zerog_recall_until"));
    }
    private PlanetGravity(){}
}
