package net.zerog.tweaks.item;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGArmorMaterials;

/** Small, server-authoritative subset of the documented set abilities. */
public final class ZGArmorSetBonuses {
    private static final ArmorItem.Type[] PIECES = {ArmorItem.Type.HELMET,
            ArmorItem.Type.CHESTPLATE, ArmorItem.Type.LEGGINGS, ArmorItem.Type.BOOTS};
    private static final ResourceLocation STURDY = id("ferrox_sturdy");
    private static final ResourceLocation STAR_FORGED = id("astrium_star_forged");

    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, path);
    }

    public static boolean wearsFullSet(LivingEntity entity, String material) {
        var profile = ZGArmorMaterials.profiles().get(material);
        if (profile == null) return false;
        for (var type : PIECES) {
            var stack = entity.getItemBySlot(type.getSlot());
            if (!(stack.getItem() instanceof ArmorItem armor) || armor.getType() != type
                    || !armor.getMaterial().equals(profile.material())) return false;
        }
        return true;
    }

    public static void incomingDamage(LivingIncomingDamageEvent event) {
        if (!(event.getEntity() instanceof Player player) || player.level().isClientSide) return;
        var source = event.getSource();
        if ((source.is(DamageTypeTags.IS_FALL) && wearsFullSet(player, "nullifite"))
                || (source.is(DamageTypeTags.IS_FIRE) && wearsFullSet(player, "skarnite"))
                || (source.is(DamageTypeTags.IS_FREEZING) && wearsFullSet(player, "eidolite"))) {
            event.setCanceled(true);
        } else if (source.is(DamageTypeTags.IS_FALL) && wearsFullSet(player, "moonsteel")) {
            event.setAmount(event.getAmount() * 0.5F);
        } else if (source.is(DamageTypeTags.IS_FIRE) && wearsFullSet(player, "ruskite")) {
            event.setAmount(event.getAmount() * 0.75F);
        }
    }
    /** Dust Shield filters dust/vortex visuals; acid rain remains visual-only. */
    public static boolean dustProtected(LivingEntity entity) { return wearsFullSet(entity, "olympium"); }

    public static void breakSpeed(PlayerEvent.BreakSpeed event) {
        if (wearsFullSet(event.getEntity(), "cobaltium")) event.setNewSpeed(event.getNewSpeed() * 1.1F);
    }

    /** Public to allow in-world regression tests without waiting for network player ticks. */
    public static void updateSetAttributes(Player player) {
        var toughness = player.getAttribute(Attributes.ARMOR_TOUGHNESS);
        if (toughness != null) {
            boolean active = wearsFullSet(player, "ferrox");
            if (active && !toughness.hasModifier(STURDY))
                toughness.addTransientModifier(new AttributeModifier(STURDY, 1, AttributeModifier.Operation.ADD_VALUE));
            if (!active) toughness.removeModifier(STURDY);
        }
        var health = player.getAttribute(Attributes.MAX_HEALTH);
        if (health != null) {
            boolean active = wearsFullSet(player, "astrium");
            if (active && !health.hasModifier(STAR_FORGED))
                health.addTransientModifier(new AttributeModifier(STAR_FORGED, 2, AttributeModifier.Operation.ADD_VALUE));
            if (!active) health.removeModifier(STAR_FORGED);
            if (player.getHealth() > player.getMaxHealth()) player.setHealth(player.getMaxHealth());
        }
    }

    public static void playerTick(PlayerTickEvent.Post event) {
        var player = event.getEntity();
        if (player.level().isClientSide) return;
        updateSetAttributes(player);
        if (wearsFullSet(player, "skarnite")) player.clearFire();
    }

    private ZGArmorSetBonuses() {}
}
