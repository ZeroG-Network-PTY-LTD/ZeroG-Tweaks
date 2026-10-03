package net.zerog.tweaks.arena;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.LongArrayTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.zerog.tweaks.arena.ConcordPrismBlock.State;
import net.zerog.tweaks.entity.PrismSentinel;
import net.zerog.tweaks.registry.BlockEntityInit;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.EntityInit;

/**
 * Runs the Prism Sentinel fight for one arena (Design briefs/prism_sentinel_arena.md, section 5).
 *
 * IDLE: right-click asks "Are you Concord?", seals the entrance with prism barriers and, 3 s later, the Sentinel forms
 * on the fight floor between the dais and the entrance (ACTIVE). If every player leaves or dies for 10 s, the Sentinel withdraws, the barrier opens and the
 * prism goes back to IDLE. When the Sentinel dies: the heir line, the barrier opens, the oculus lights and the prism
 * goes DEFEATED. A DEFEATED prism re-arms with a Sentinel Prism (rematch: no gate key).
 *
 * Arena geometry is read relative to the prism ({@link PrismArena}), so it works for any rotation of the structure:
 * doorways are wall sides open just above the floor; the fight seals all of them (the Concord Vault chamber has four).
 */
public class ConcordPrismBlockEntity extends BlockEntity {
    public static final int SUMMON_DELAY = 60;
    public static final int EMPTY_RESET = 200;
    private static final int MISSING_GRACE = 100;

    @Nullable private UUID sentinel;
    private final List<BlockPos> barrier = new ArrayList<>();
    private boolean rematch;
    private int countdown;        // ticks until the Sentinel rises (ACTIVE, before it exists)
    private int emptyTicks;       // ticks with no player inside the arena
    private int missingTicks;     // ticks the Sentinel could not be found

    public ConcordPrismBlockEntity(BlockPos pos, BlockState state) {
        super(BlockEntityInit.CONCORD_PRISM.get(), pos, state);
    }

    public State state() { return getBlockState().getValue(ConcordPrismBlock.STATE); }
    public boolean isRematch() { return rematch; }
    @Nullable public UUID sentinelId() { return sentinel; }
    public List<BlockPos> barrierBlocks() { return List.copyOf(barrier); }

    // ---- player actions ----------------------------------------------------------------------------------------------

    /** Right-click on an IDLE prism: the test begins. Returns false if it can't start now. */
    public boolean start(ServerLevel level) {
        if (state() != State.IDLE) return false;
        setState(level, State.ACTIVE);
        countdown = SUMMON_DELAY;
        emptyTicks = 0;
        missingTicks = 0;
        tell(level, PrismSentinel.speech(Component.translatable("chat.zerog_tweaks.prism_sentinel.ask")));
        level.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 3F, 0.8F);
        seal(level);
        setChanged();
        return true;
    }

    /** A Sentinel Prism used on a DEFEATED prism: arm it for a rematch (no gate key from a rematch). */
    public boolean rearm(ServerLevel level) {
        if (state() != State.DEFEATED) return false;
        rematch = true;
        setState(level, State.IDLE);
        setOculus(level, false);
        tell(level, Component.translatable("chat.zerog_tweaks.prism_sentinel.rearmed").withStyle(ChatFormatting.AQUA));
        level.playSound(null, worldPosition, SoundEvents.RESPAWN_ANCHOR_CHARGE, SoundSource.BLOCKS, 2F, 1.2F);
        setChanged();
        return true;
    }

    /** Called by the Sentinel from its die(). */
    public void onSentinelDefeated(PrismSentinel boss) {
        if (!(level instanceof ServerLevel server) || state() != State.ACTIVE) return;
        sentinel = null;
        tell(server, PrismSentinel.speech(Component.translatable("chat.zerog_tweaks.prism_sentinel.heir")));
        unseal(server);
        setOculus(server, true);
        setState(server, State.DEFEATED);
        server.playSound(null, worldPosition, SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.BLOCKS, 2F, 1F);
        setChanged();
    }

    // ---- ticking -----------------------------------------------------------------------------------------------------

    public static void serverTick(Level level, BlockPos pos, BlockState state, ConcordPrismBlockEntity be) {
        if (level instanceof ServerLevel server) be.tick(server);
    }

    private void tick(ServerLevel level) {
        State st = state();
        if (st == State.DEFEATED) {
            // the oculus beam: light falling from the skylight onto the prism
            if (level.getGameTime() % 5 == 0) {
                double y = worldPosition.getY() + 1 + level.random.nextDouble() * (PrismArena.OCULUS_ABOVE_PRISM - 1);
                level.sendParticles(ParticleTypes.END_ROD, worldPosition.getX() + 0.5, y, worldPosition.getZ() + 0.5,
                        1, 0.15, 0.4, 0.15, 0.0);
            }
            return;
        }
        if (st != State.ACTIVE) return;
        if (countdown > 0) {
            level.sendParticles(ParticleTypes.END_ROD, worldPosition.getX() + 0.5, worldPosition.getY() + 1.2,
                    worldPosition.getZ() + 0.5, 3, 0.3, 0.3, 0.3, 0.02);
            if (--countdown == 0) summon(level);
            return;
        }
        emptyTicks = playersInside(level).isEmpty() ? emptyTicks + 1 : 0;
        PrismSentinel boss = sentinel != null && level.getEntity(sentinel) instanceof PrismSentinel s && s.isAlive() ? s : null;
        missingTicks = boss == null ? missingTicks + 1 : 0;
        if (emptyTicks >= EMPTY_RESET || missingTicks >= MISSING_GRACE) reset(level, boss);
    }

    private void summon(ServerLevel level) {
        PrismSentinel boss = EntityInit.PRISM_SENTINEL.get().create(level);
        if (boss == null) { reset(level, null); return; }
        // on the floor between the dais and the entrance, facing the way in
        Direction d = entrance(level);
        Direction toward = d != null ? d : Direction.SOUTH;
        double x = worldPosition.getX() + 0.5 + toward.getStepX() * PrismArena.SENTINEL_START;
        double z = worldPosition.getZ() + 0.5 + toward.getStepZ() * PrismArena.SENTINEL_START;
        double y = worldPosition.getY() - PrismArena.FLOOR_BELOW_PRISM + 1;
        boss.moveTo(x, y, z, toward.toYRot(), 0);
        boss.setYHeadRot(toward.toYRot());
        level.sendParticles(ParticleTypes.END_ROD, x, y + 5, z, 120, 1.5, 4, 1.5, 0.05);
        boss.bindToPrism(worldPosition, rematch);
        boss.finalizeSpawn(level, level.getCurrentDifficultyAt(worldPosition), MobSpawnType.EVENT, null);
        level.addFreshEntity(boss);
        sentinel = boss.getUUID();
        level.playSound(null, worldPosition, SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.HOSTILE, 4F, 0.5F);
        setChanged();
    }

    /** Everyone left or died (or the Sentinel vanished): withdraw and wait for the next challenger. */
    private void reset(ServerLevel level, @Nullable PrismSentinel boss) {
        if (boss != null) boss.discard();
        sentinel = null;
        unseal(level);
        setState(level, State.IDLE);
        tell(level, Component.translatable("chat.zerog_tweaks.prism_sentinel.reset").withStyle(ChatFormatting.GRAY));
        setChanged();
    }

    // ---- arena geometry ----------------------------------------------------------------------------------------------

    public AABB arenaBox() {
        double h = PrismArena.HALF + 4;   // the boss bar and chat reach a little past the walls
        return new AABB(worldPosition.getX() + 0.5 - h, worldPosition.getY() - 10, worldPosition.getZ() + 0.5 - h,
                worldPosition.getX() + 0.5 + h, worldPosition.getY() + 32, worldPosition.getZ() + 0.5 + h);
    }

    private List<ServerPlayer> playersInside(ServerLevel level) {
        AABB hall = arenaBox().deflate(4, 0, 4);   // the hall itself, not the apron outside
        return level.getEntitiesOfClass(ServerPlayer.class, hall, p -> p.isAlive() && !p.isSpectator());
    }

    /** The side of the wall that is open just above the floor: the entrance. */
    @Nullable
    Direction entrance(Level level) {
        BlockPos above = worldPosition.below(PrismArena.FLOOR_BELOW_PRISM - 2);
        for (Direction d : Direction.Plane.HORIZONTAL) {
            if (level.getBlockState(above.relative(d, PrismArena.ENTRANCE_NEAR)).isAir()
                    && level.getBlockState(above.relative(d, PrismArena.ENTRANCE_FAR)).isAir()) return d;
        }
        return null;
    }

    private void seal(ServerLevel level) {
        for (Direction d : Direction.Plane.HORIZONTAL) {
            if (isOpen(level, d)) sealSide(level, d);
        }
    }

    /** True if the wall is open on this side just above the floor (a doorway). */
    private boolean isOpen(Level level, Direction d) {
        BlockPos above = worldPosition.below(PrismArena.FLOOR_BELOW_PRISM - 2);
        return level.getBlockState(above.relative(d, PrismArena.ENTRANCE_NEAR)).isAir()
                && level.getBlockState(above.relative(d, PrismArena.ENTRANCE_FAR)).isAir();
    }

    private void sealSide(ServerLevel level, Direction d) {
        Direction side = d.getClockWise();
        BlockState wall = BlockInit.PRISM_BARRIER.get().defaultBlockState();
        int floor = -PrismArena.FLOOR_BELOW_PRISM;
        for (int out = PrismArena.ENTRANCE_NEAR; out <= PrismArena.ENTRANCE_FAR; out++) {
            for (int lateral = -PrismArena.ENTRANCE_HALF_WIDTH; lateral <= PrismArena.ENTRANCE_HALF_WIDTH; lateral++) {
                for (int dy = floor + 1; dy <= floor + PrismArena.ENTRANCE_HEIGHT; dy++) {
                    BlockPos p = worldPosition.relative(d, out).relative(side, lateral).above(dy);
                    if (level.getBlockState(p).isAir()) {
                        level.setBlock(p, wall, Block.UPDATE_ALL);
                        barrier.add(p);
                    }
                }
            }
        }
    }

    private void unseal(ServerLevel level) {
        for (BlockPos p : barrier) {
            if (level.getBlockState(p).is(BlockInit.PRISM_BARRIER.get())) level.removeBlock(p, false);
        }
        barrier.clear();
    }

    /** Lit oculus after a victory: the shimmer-glass core over the dais becomes a pulsar lamp. */
    private void setOculus(ServerLevel level, boolean lit) {
        BlockPos p = worldPosition.above(PrismArena.OCULUS_ABOVE_PRISM);
        BlockState now = level.getBlockState(p);
        if (lit && now.is(BlockInit.SHIMMER_GLASS.get())) {
            level.setBlock(p, BlockInit.PULSAR_LAMP.get().defaultBlockState(), Block.UPDATE_ALL);
        } else if (!lit && now.is(BlockInit.PULSAR_LAMP.get())) {
            level.setBlock(p, BlockInit.SHIMMER_GLASS.get().defaultBlockState(), Block.UPDATE_ALL);
        }
    }

    private void setState(ServerLevel level, State st) {
        level.setBlock(worldPosition, getBlockState().setValue(ConcordPrismBlock.STATE, st), Block.UPDATE_ALL);
    }

    private void tell(ServerLevel level, Component msg) {
        for (ServerPlayer p : level.getEntitiesOfClass(ServerPlayer.class, arenaBox())) p.sendSystemMessage(msg);
    }

    // ---- save --------------------------------------------------------------------------------------------------------

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        if (sentinel != null) tag.putUUID("Sentinel", sentinel);
        tag.put("Barrier", new LongArrayTag(barrier.stream().mapToLong(BlockPos::asLong).toArray()));
        tag.putBoolean("Rematch", rematch);
        tag.putInt("Countdown", countdown);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        sentinel = tag.hasUUID("Sentinel") ? tag.getUUID("Sentinel") : null;
        barrier.clear();
        for (long l : tag.getLongArray("Barrier")) barrier.add(BlockPos.of(l));
        rematch = tag.getBoolean("Rematch");
        countdown = tag.getInt("Countdown");
    }
}
