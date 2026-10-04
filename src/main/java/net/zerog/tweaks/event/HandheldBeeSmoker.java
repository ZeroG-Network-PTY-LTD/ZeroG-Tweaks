package net.zerog.tweaks.event;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.animal.Bee;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Existing aeroapiary:bee_smoker; visual smoke and local anger clearing, not fire. */
public final class HandheldBeeSmoker {
    private static final Map<UUID,Long> CLOUDS=new HashMap<>();
    public static int calm(ServerLevel level,Vec3 centre) {
        int count=0;
        for(var bee:level.getEntitiesOfClass(Bee.class,new AABB(centre,centre).inflate(6),bee->bee.distanceToSqr(centre)<=36)) {
            bee.stopBeingAngry();bee.setTarget(null);bee.setLastHurtByMob(null);count++;
        }
        return count;
    }
    private static void use(PlayerInteractEvent event) {
        var stack=event.getItemStack();
        if(!BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals("aeroapiary:bee_smoker"))return;
        if(event instanceof PlayerInteractEvent.RightClickItem item) {item.setCanceled(true);item.setCancellationResult(InteractionResult.SUCCESS);}
        else if(event instanceof PlayerInteractEvent.RightClickBlock block) {block.setCanceled(true);block.setCancellationResult(InteractionResult.SUCCESS);}
        if(!(event.getEntity() instanceof ServerPlayer player)||player.getCooldowns().isOnCooldown(stack.getItem()))return;
        var level=player.serverLevel();
        player.getCooldowns().addCooldown(stack.getItem(),20);
        CLOUDS.put(player.getUUID(),level.getGameTime()+100);
        puff(player,12);calm(level,player.position());
    }
    public static void item(PlayerInteractEvent.RightClickItem event) {use(event);}
    public static void block(PlayerInteractEvent.RightClickBlock event) {use(event);}
    private static void puff(ServerPlayer player,int count) {
        var point=player.getEyePosition().add(player.getLookAngle().scale(.65)).add(0,-.35,0);
        player.serverLevel().sendParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE,point.x,point.y,point.z,count,.12,.08,.12,.015);
    }
    public static void tick(PlayerTickEvent.Post event) {
        if(!(event.getEntity() instanceof ServerPlayer player))return;
        Long until=CLOUDS.get(player.getUUID());if(until==null)return;
        long time=player.serverLevel().getGameTime();
        boolean held=java.util.stream.Stream.of(player.getMainHandItem(),player.getOffhandItem())
            .anyMatch(stack->BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals("aeroapiary:bee_smoker"));
        if(time>=until||!held){CLOUDS.remove(player.getUUID());return;}
        if(time%5==0){calm(player.serverLevel(),player.position());puff(player,2);}
    }
    public static void logout(net.neoforged.neoforge.event.entity.player.PlayerEvent.PlayerLoggedOutEvent event) {CLOUDS.remove(event.getEntity().getUUID());}
    public static void stopped(net.neoforged.neoforge.event.server.ServerStoppedEvent event) {CLOUDS.clear();}
    private HandheldBeeSmoker() {}
}
