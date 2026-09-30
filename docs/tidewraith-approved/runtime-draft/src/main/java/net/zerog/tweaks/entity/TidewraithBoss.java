package net.zerog.tweaks.entity;

import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.BossEvent;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;

/** Eight-eye manta-mouth boss. The approved authored size is retained (no x6 scaling). */
public final class TidewraithBoss extends Tidewraith {
    private final ServerBossEvent bossBar = new ServerBossEvent(getDisplayName(),
            BossEvent.BossBarColor.BLUE, BossEvent.BossBarOverlay.PROGRESS);

    public TidewraithBoss(EntityType<? extends TidewraithBoss> type, Level level) {
        super(type, level);
        setPersistenceRequired();
        this.xpReward = 50;
    }

    @Override
    public boolean isBoss() { return true; }

    public static AttributeSupplier.Builder createAttributes() {
        return Tidewraith.createAttributes().add(Attributes.MAX_HEALTH, 180)
                .add(Attributes.ATTACK_DAMAGE, 8).add(Attributes.FOLLOW_RANGE, 40)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8);
    }

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        bossBar.addPlayer(player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossBar.removePlayer(player);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        bossBar.setName(getDisplayName());
        bossBar.setProgress(getHealth() / getMaxHealth());
    }

    @Override
    public void remove(RemovalReason reason) {
        super.remove(reason);
        bossBar.removeAllPlayers();
    }
}
