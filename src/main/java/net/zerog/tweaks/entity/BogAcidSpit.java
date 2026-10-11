package net.zerog.tweaks.entity;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.*;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.projectile.ThrowableItemProjectile;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.*;

/** Collision-based acid spit; never damages blocks or leaves permanent hazards. */
public final class BogAcidSpit extends ThrowableItemProjectile {
    public BogAcidSpit(EntityType<? extends ThrowableItemProjectile> type,Level level){super(type,level);}
    @Override protected Item getDefaultItem(){return net.zerog.tweaks.registry.ItemInit.VENOM_GLAND.get();}
    @Override protected void onHitEntity(EntityHitResult result){
        if(level().isClientSide)return;
        var key=ResourceKey.create(Registries.DAMAGE_TYPE,ResourceLocation.parse("zerog_tweaks:acid"));
        var source=new DamageSource(registryAccess().registryOrThrow(Registries.DAMAGE_TYPE).getHolderOrThrow(key),this,getOwner());
        if(result.getEntity().hurt(source,5)&&result.getEntity() instanceof LivingEntity living)
            living.addEffect(new MobEffectInstance(MobEffects.POISON,80,1));
    }
    @Override protected void onHit(HitResult result){super.onHit(result);if(!level().isClientSide)discard();}
    @Override public void tick(){super.tick();if(!level().isClientSide&&tickCount>100)discard();}
}
