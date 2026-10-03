package net.zerog.tweaks.entity;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.TagKey;
import net.minecraft.util.Mth;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.arena.ConcordPrismBlockEntity;
import net.zerog.tweaks.arena.PrismArena;
import org.joml.Vector3f;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Prism Sentinel, the Galaxy 2 guardian (mob spec prism_sentinel; Design briefs/prism_sentinel_arena.md section 5).
 * A test, not a hunt: 3.6 x 10.8, glides on its pedestal just above the floor (so melee reaches it), shards orbit
 * the core on a 4 s loop.
 *
 * Phase 0: forms on the fight floor (invulnerable for 2 s). Phase 1 (above 2/3 health): beams that bounce off an orbiting
 * shard. Phase 2: the shards break loose and circle the arena (8 damage on contact), beams slow down. Phase 3 (below 1/3):
 * the core cracks open in windows; hits while it is open deal double. Beams stop on any solid block, so the arena's
 * refractor pylons (#zerog_tweaks:beam_blocking) are cover. Tied to its prism by an anchor; it stays on the fight
 * floor ({@link #LEASH} blocks) and reports its death back so the arena can open. Arena sizes: {@link PrismArena}.
 */
public class PrismSentinel extends Monster implements GeoEntity {
    public static final TagKey<Block> BEAM_BLOCKING =
            TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "beam_blocking"));
    public static final int INTRO_TICKS = 40;
    public static final double LEASH = PrismArena.FLOOR_RADIUS + 4;
    private static final float BEAM_DAMAGE = 10;
    private static final float SHARD_DAMAGE = 8;
    private static final double ORBIT_RADIUS = 4.0, ORBIT_HEIGHT = 6.8;
    private static final double SPIN_RADIUS = 15.0;
    private static final double GLIDE = 0.1;   // pedestal clearance over the floor
    private static final ParticleOptions BEAM_DUST = new DustParticleOptions(new Vector3f(0.35F, 0.9F, 1.0F), 1.6F);
    private static final ParticleOptions SHARD_DUST = new DustParticleOptions(new Vector3f(0.75F, 0.97F, 1.0F), 2.2F);

    private static final EntityDataAccessor<Integer> PHASE =
            SynchedEntityData.defineId(PrismSentinel.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Boolean> CORE_OPEN =
            SynchedEntityData.defineId(PrismSentinel.class, EntityDataSerializers.BOOLEAN);

    private final AnimatableInstanceCache animationCache = GeckoLibUtil.createInstanceCache(this);
    private final ServerBossEvent bossBar = new ServerBossEvent(getDisplayName(),
            BossEvent.BossBarColor.BLUE, BossEvent.BossBarOverlay.NOTCHED_6);
    private final Map<UUID, Integer> shardHitCooldown = new HashMap<>();
    @Nullable private BlockPos anchor;   // the Concord Prism; set to the spawn point when summoned by egg/command
    private boolean rematch;
    private int coreTimer;

    public PrismSentinel(EntityType<? extends PrismSentinel> type, Level level) {
        super(type, level);
        this.moveControl = new FlyingMoveControl(this, 10, true);
        this.setNoGravity(true);
        this.setPersistenceRequired();
        this.xpReward = 120;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 300).add(Attributes.ATTACK_DAMAGE, 10)
                .add(Attributes.ARMOR, 15).add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.MOVEMENT_SPEED, 0.2).add(Attributes.FLYING_SPEED, 0.3)
                .add(Attributes.FOLLOW_RANGE, 48);
    }

    // ---- state -------------------------------------------------------------------------------------------------------

    public int getPhase() { return entityData.get(PHASE); }
    public boolean isCoreOpen() { return entityData.get(CORE_OPEN); }
    public boolean isRematch() { return rematch; }
    @Nullable public BlockPos getAnchor() { return anchor; }

    /** Called by the Concord Prism when it summons the Sentinel. */
    public void bindToPrism(BlockPos prism, boolean rematch) {
        this.anchor = prism.immutable();
        this.rematch = rematch;
    }

    /** Phase from health once the intro is over: 1 above 2/3, 2 above 1/3, else 3. */
    public static int phaseFor(float health, float maxHealth) {
        float f = health / maxHealth;
        return f > 2F / 3F ? 1 : f > 1F / 3F ? 2 : 3;
    }

    private Vec3 homeCentre() {
        return Vec3.atBottomCenterOf(anchor != null ? anchor : blockPosition());
    }

    /** The y the Sentinel stands at: on top of the fight floor. */
    private double floorY() {
        return homeCentre().y - PrismArena.FLOOR_BELOW_PRISM + 1;
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(PHASE, 0);
        builder.define(CORE_OPEN, false);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        if (anchor != null) tag.put("Anchor", NbtUtils.writeBlockPos(anchor));
        tag.putBoolean("Rematch", rematch);   // the loot table skips the gate key on {Rematch:1b}
        tag.putInt("Phase", getPhase());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        anchor = NbtUtils.readBlockPos(tag, "Anchor").orElse(null);
        rematch = tag.getBoolean("Rematch");
        entityData.set(PHASE, tag.getInt("Phase"));
    }

    // ---- movement and AI ---------------------------------------------------------------------------------------------

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation navigation = new FlyingPathNavigation(this, level);
        navigation.setCanFloat(true);
        return navigation;
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new StayInArenaGoal());
        goalSelector.addGoal(1, new BeamAttackGoal());
        goalSelector.addGoal(2, new HoverGoal());
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, false));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        setNoGravity(true);
        if (level().isClientSide || isDeadOrDying()) return;   // no phase change (or chat line) while dying
        // egg/command: treat the spawn point as the fight floor of an imaginary arena around it
        if (anchor == null) anchor = blockPosition().above(PrismArena.FLOOR_BELOW_PRISM - 1);
        int phase = getPhase();
        if (phase == 0) {
            setDeltaMovement(Vec3.ZERO);                          // forming: light gathers into the body
            if (tickCount % 3 == 0) {
                ((ServerLevel) level()).sendParticles(BEAM_DUST, getX(), getY() + 5, getZ(), 6, 1.6, 4.5, 1.6, 0);
            }
            if (tickCount >= INTRO_TICKS) entityData.set(PHASE, 1);
            return;
        }
        int next = phaseFor(getHealth(), getMaxHealth());
        if (next > phase) enterPhase(next);
        if (phase >= 2) spinShards((ServerLevel) level());
        if (phase == 3) {
            // the core opens for 5 s, closes for 3 s
            coreTimer = (coreTimer + 1) % 160;
            boolean open = coreTimer < 100;
            if (open != isCoreOpen()) {
                entityData.set(CORE_OPEN, open);
                playSound(open ? SoundEvents.BEACON_ACTIVATE : SoundEvents.BEACON_DEACTIVATE, 2F, 1.4F);
            }
            if (open && tickCount % 4 == 0) {
                ((ServerLevel) level()).sendParticles(ParticleTypes.END_ROD, getX(), getY() + ORBIT_HEIGHT, getZ(),
                        3, 0.6, 0.6, 0.6, 0.05);
            }
        }
        if ((tickCount + getId() * 7) % 90 == 0) triggerAnim("eyes", "blink");
    }

    private void enterPhase(int phase) {
        entityData.set(PHASE, phase);
        playSound(SoundEvents.AMETHYST_BLOCK_BREAK, 4F, 0.6F);
        say(Component.translatable("chat.zerog_tweaks.prism_sentinel.phase" + phase));
        ((ServerLevel) level()).sendParticles(SHARD_DUST, getX(), getY() + ORBIT_HEIGHT, getZ(), 60, 3, 2, 3, 0.1);
    }

    /** Phase 2+: the four shards circle the arena at chest height and cut anyone they pass through. */
    private void spinShards(ServerLevel level) {
        Vec3 c = homeCentre();
        double y = floorY() + 1.2;   // chest height over the fight floor
        double turn = (tickCount % 200) / 200.0 * Math.PI * 2;
        shardHitCooldown.replaceAll((k, v) -> v - 1);
        shardHitCooldown.values().removeIf(v -> v <= 0);
        for (int k = 0; k < 4; k++) {
            double a = turn + k * Math.PI / 2;
            Vec3 shard = new Vec3(c.x + Math.cos(a) * SPIN_RADIUS, y, c.z + Math.sin(a) * SPIN_RADIUS);
            level.sendParticles(SHARD_DUST, shard.x, shard.y, shard.z, 2, 0.25, 0.4, 0.25, 0);
            for (Player p : level.getEntitiesOfClass(Player.class, new AABB(shard, shard).inflate(1.3, 1.6, 1.3))) {
                if (p.isSpectator() || p.isCreative() || shardHitCooldown.containsKey(p.getUUID())) continue;
                if (p.hurt(damageSources().mobAttack(this), SHARD_DAMAGE)) {
                    shardHitCooldown.put(p.getUUID(), 20);
                    level.playSound(null, p.blockPosition(), SoundEvents.AMETHYST_CLUSTER_BREAK, SoundSource.HOSTILE, 1.5F, 1.2F);
                }
            }
        }
    }

    /** Where shard k of the orbit ring is now (the beam bounces off it). Matches the 4 s orbit clip. */
    private Vec3 orbitShard(int k) {
        double a = (tickCount % 80) / 80.0 * Math.PI * 2 + k * Math.PI / 2;
        return new Vec3(getX() + Math.cos(a) * ORBIT_RADIUS, getY() + ORBIT_HEIGHT, getZ() + Math.sin(a) * ORBIT_RADIUS);
    }

    private Vec3 core() {
        return new Vec3(getX(), getY() + ORBIT_HEIGHT, getZ());
    }

    // ---- damage, death -----------------------------------------------------------------------------------------------

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (getPhase() == 0 && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return false;
        if (getPhase() == 3 && isCoreOpen()) amount *= 2;   // the heart light is exposed
        return super.hurt(source, amount);
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        if (level() instanceof ServerLevel server && anchor != null
                && server.getBlockEntity(anchor) instanceof ConcordPrismBlockEntity prism) {
            prism.onSentinelDefeated(this);
        } else {
            say(Component.translatable("chat.zerog_tweaks.prism_sentinel.heir"));
        }
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) { return false; }
    @Override
    public boolean isPushable() { return false; }
    @Override
    protected void pushEntities() {}
    @Override
    public boolean removeWhenFarAway(double distance) { return false; }
    @Override
    public boolean canChangeDimensions(Level from, Level to) { return false; }

    @Override
    protected SoundEvent getAmbientSound() { return SoundEvents.AMETHYST_BLOCK_CHIME; }
    @Override
    protected SoundEvent getHurtSound(DamageSource source) { return SoundEvents.AMETHYST_CLUSTER_HIT; }
    @Override
    protected SoundEvent getDeathSound() { return SoundEvents.BEACON_DEACTIVATE; }
    @Override
    protected float getSoundVolume() { return 3F; }

    // ---- boss bar: only players inside the arena ---------------------------------------------------------------------

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        bossBar.setName(getDisplayName());
        bossBar.setProgress(getHealth() / getMaxHealth());
        if (tickCount % 10 == 0) {
            AABB arena = arenaBox();
            for (ServerPlayer p : ((ServerLevel) level()).players()) {
                boolean inside = p.isAlive() && arena.contains(p.position());
                if (inside && !bossBar.getPlayers().contains(p)) bossBar.addPlayer(p);
                else if (!inside && bossBar.getPlayers().contains(p)) bossBar.removePlayer(p);
            }
        }
    }

    /** The arena (template footprint + 4) around the prism: who sees the boss bar and hears the Sentinel. */
    public AABB arenaBox() {
        Vec3 c = homeCentre();
        double h = PrismArena.HALF + 4, f = floorY();
        return new AABB(c.x - h, f - 6, c.z - h, c.x + h, f + 40, c.z + h);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossBar.removePlayer(player);
    }

    @Override
    public void remove(RemovalReason reason) {
        super.remove(reason);
        bossBar.removeAllPlayers();
    }

    private void say(Component line) {
        if (!(level() instanceof ServerLevel server)) return;
        AABB arena = arenaBox();
        for (ServerPlayer p : server.players()) if (arena.contains(p.position())) p.sendSystemMessage(speech(line));
    }

    /** "[Prism Sentinel] line", used for every Sentinel chat line. */
    public static Component speech(Component line) {
        return Component.translatable("chat.zerog_tweaks.prism_sentinel.speaker").withStyle(ChatFormatting.AQUA)
                .append(Component.literal(" ")).append(line.copy().withStyle(ChatFormatting.WHITE));
    }

    // ---- GeckoLib ----------------------------------------------------------------------------------------------------

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        String prefix = "animation.zerog_tweaks.prism_sentinel.";
        RawAnimation idle = RawAnimation.begin().thenLoop(prefix + "idle");
        RawAnimation walk = RawAnimation.begin().thenLoop(prefix + "walk");
        RawAnimation orbit = RawAnimation.begin().thenLoop(prefix + "orbit");
        controllers.add(new AnimationController<>(this, "body", 6,
                state -> state.setAndContinue(state.isMoving() ? walk : idle)));
        controllers.add(new AnimationController<>(this, "orbit", 0, state -> state.setAndContinue(orbit)));
        controllers.add(new AnimationController<>(this, "eyes", 0, state -> PlayState.STOP)
                .triggerableAnim("blink", RawAnimation.begin().thenPlay(prefix + "blink")));
        controllers.add(new AnimationController<>(this, "attack", 2, state -> PlayState.STOP)
                .triggerableAnim("attack", RawAnimation.begin().thenPlay(prefix + "attack")));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() { return animationCache; }

    // ---- goals -------------------------------------------------------------------------------------------------------

    /** Teleports back onto the fight floor if it is ever pushed off it or lifted away. */
    private final class StayInArenaGoal extends Goal {
        StayInArenaGoal() { setFlags(EnumSet.of(Flag.MOVE)); }
        @Override
        public boolean canUse() {
            if (getPhase() == 0) return false;
            Vec3 c = homeCentre();
            return Mth.square(getX() - c.x) + Mth.square(getZ() - c.z) > LEASH * LEASH || Math.abs(getY() - floorY()) > 6;
        }
        @Override
        public void start() {
            Vec3 c = homeCentre();
            ((ServerLevel) level()).sendParticles(BEAM_DUST, getX(), getY() + 5, getZ(), 40, 1.5, 4, 1.5, 0);
            double a = Math.atan2(getZ() - c.z, getX() - c.x);
            teleportTo(c.x + Math.cos(a) * PrismArena.SENTINEL_START, floorY() + GLIDE, c.z + Math.sin(a) * PrismArena.SENTINEL_START);
            playSound(SoundEvents.ENDERMAN_TELEPORT, 2F, 0.6F);
        }
    }

    /** Glides over the fight floor around the dais, on the far side from its target so beams cross the floor. */
    private final class HoverGoal extends Goal {
        private int retarget;
        HoverGoal() { setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK)); }
        @Override
        public boolean canUse() { return getPhase() > 0; }
        @Override
        public boolean requiresUpdateEveryTick() { return true; }
        @Override
        public void tick() {
            LivingEntity target = getTarget();
            if (target != null) getLookControl().setLookAt(target.getX(), target.getEyeY(), target.getZ(), 10, 10);
            if (--retarget > 0) return;
            retarget = 40 + random.nextInt(30);
            Vec3 c = homeCentre();
            double y = floorY() + GLIDE;
            if (target == null || !target.isAlive()) {
                getMoveControl().setWantedPosition(getX(), y, getZ(), 0.6);   // no challenger: hold its ground
                return;
            }
            // stay on the open floor: clear of the dais (r4 + half its width) and inside the floor edge
            double a = Math.atan2(target.getZ() - c.z, target.getX() - c.x) + Math.PI + (random.nextDouble() - 0.5);
            double r = PrismArena.DAIS_RADIUS + 4 + random.nextDouble() * (PrismArena.FLOOR_RADIUS - PrismArena.DAIS_RADIUS - 8);
            getMoveControl().setWantedPosition(c.x + Math.cos(a) * r, y, c.z + Math.sin(a) * r, 0.8);
        }
    }

    /**
     * Charges for 1 s (light gathers on a shard), then fires core -> shard -> target. Anything solid on the second leg
     * stops it; a refractor pylon block scatters it. Targets that close in get the body slam instead.
     */
    private final class BeamAttackGoal extends Goal {
        private int cooldown = 40;
        private int charge;
        private int shard;

        BeamAttackGoal() { setFlags(EnumSet.of(Flag.LOOK)); }
        @Override
        public boolean canUse() {
            LivingEntity t = getTarget();
            return getPhase() > 0 && t != null && t.isAlive() && t.distanceToSqr(PrismSentinel.this) < 48 * 48;
        }
        @Override
        public boolean requiresUpdateEveryTick() { return true; }
        @Override
        public void tick() {
            LivingEntity target = getTarget();
            if (target == null) return;
            getLookControl().setLookAt(target, 30, 30);
            ServerLevel level = (ServerLevel) level();
            if (tickCount % 20 == 0 && isWithinMeleeAttackRange(target)) {
                triggerAnim("attack", "attack");
                doHurtTarget(target);
            }
            if (charge > 0) {
                Vec3 s = orbitShard(shard);
                level.sendParticles(BEAM_DUST, s.x, s.y, s.z, 4, 0.3, 0.3, 0.3, 0);
                if (--charge == 0) fire(level, target, s);
                return;
            }
            if (--cooldown > 0) return;
            int phase = getPhase();
            cooldown = phase == 1 ? 50 : phase == 2 ? 80 : 35;
            charge = 20;
            shard = random.nextInt(4);
            playSound(SoundEvents.BEACON_AMBIENT, 3F, 1.8F);
        }

        private void fire(ServerLevel level, LivingEntity target, Vec3 shardPos) {
            // with the shards loose (phase 2+) the beam comes straight from the core
            Vec3 from = getPhase() >= 2 ? core() : shardPos;
            drawLine(level, core(), from);
            Vec3 aim = target.getEyePosition().add(0, -0.4, 0);
            var hit = level.clip(new ClipContext(from, aim, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, PrismSentinel.this));
            Vec3 end = hit.getType() == HitResult.Type.MISS ? aim : hit.getLocation();
            drawLine(level, from, end);
            playSound(SoundEvents.BEACON_POWER_SELECT, 3F, 1.6F);
            triggerAnim("attack", "attack");
            if (hit.getType() == HitResult.Type.MISS) {
                target.hurt(damageSources().mobAttack(PrismSentinel.this), BEAM_DAMAGE);
            } else if (level.getBlockState(hit.getBlockPos()).is(BEAM_BLOCKING)) {
                level.sendParticles(ParticleTypes.END_ROD, end.x, end.y, end.z, 14, 0.3, 0.3, 0.3, 0.15);
                level.playSound(null, hit.getBlockPos(), SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.HOSTILE, 2F, 1.5F);
            }
        }

        private void drawLine(ServerLevel level, Vec3 a, Vec3 b) {
            double len = a.distanceTo(b);
            for (double d = 0; d < len; d += 0.35) {
                Vec3 p = a.lerp(b, d / len);
                level.sendParticles(BEAM_DUST, p.x, p.y, p.z, 1, 0, 0, 0, 0);
            }
        }
    }
}
