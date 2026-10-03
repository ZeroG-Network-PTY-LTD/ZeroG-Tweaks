package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.Difficulty;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.arena.ConcordPrismBlock;
import net.zerog.tweaks.arena.ConcordPrismBlockEntity;
import net.zerog.tweaks.entity.PrismSentinel;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;

/** Prism Sentinel boss (mob spec prism_sentinel) and the Concord Prism that runs its fight. */
@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class PrismSentinelGameTests {
    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void sentinel_matches_the_mob_spec(GameTestHelper helper) {
        var boss = helper.spawn(EntityInit.PRISM_SENTINEL.get(), 8, 2, 8);
        helper.assertTrue(boss.getMaxHealth() == 300, "Max health should be 300");
        helper.assertTrue(boss.getAttributeValue(Attributes.ATTACK_DAMAGE) == 10, "Attack damage should be 10");
        helper.assertTrue(boss.getAttributeValue(Attributes.ARMOR) == 15, "Armor should be 15");
        helper.assertTrue(boss.getAttributeValue(Attributes.KNOCKBACK_RESISTANCE) == 1, "Knockback resistance should be 1");
        helper.assertTrue(boss.getAttributeValue(Attributes.FOLLOW_RANGE) == 48, "Follow range should be 48");
        helper.assertTrue(Math.abs(boss.getBbWidth() - 3.6) < 0.001 && Math.abs(boss.getBbHeight() - 10.8) < 0.001,
                "Hitbox should be 3.6 x 10.8");
        helper.assertTrue(boss.isNoGravity(), "The Sentinel floats");
        boss.discard();
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void phases_follow_health_thirds(GameTestHelper helper) {
        helper.assertTrue(PrismSentinel.phaseFor(300, 300) == 1, "Full health is phase 1");
        helper.assertTrue(PrismSentinel.phaseFor(201, 300) == 1, "Above 2/3 is phase 1");
        helper.assertTrue(PrismSentinel.phaseFor(199, 300) == 2, "Below 2/3 is phase 2");
        helper.assertTrue(PrismSentinel.phaseFor(101, 300) == 2, "Above 1/3 is phase 2");
        helper.assertTrue(PrismSentinel.phaseFor(99, 300) == 3, "Below 1/3 is phase 3");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 120)
    public static void intro_is_invulnerable_then_phase_one(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        var boss = helper.spawn(EntityInit.PRISM_SENTINEL.get(), 8, 2, 8);
        helper.assertTrue(boss.getPhase() == 0, "Spawns in the intro phase");
        helper.assertFalse(boss.hurt(helper.getLevel().damageSources().generic(), 5), "Hurt during the rise");
        helper.runAfterDelay(PrismSentinel.INTRO_TICKS + 5, () -> {
            helper.assertTrue(boss.getPhase() == 1, "Phase 1 after the intro, got " + boss.getPhase());
            helper.assertTrue(boss.hurt(helper.getLevel().damageSources().generic(), 5), "Can't be hurt after the intro");
            boss.discard();
            helper.succeed();
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 120)
    public static void dying_sentinel_does_not_change_phase(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        var boss = helper.spawn(EntityInit.PRISM_SENTINEL.get(), 8, 2, 8);
        helper.runAfterDelay(PrismSentinel.INTRO_TICKS + 5, () -> {
            helper.assertTrue(boss.getPhase() == 1, "Phase 1 after the intro");
            boss.kill();
            helper.runAfterDelay(5, () -> {
                helper.assertTrue(boss.getPhase() == 1, "A dying Sentinel jumped to phase " + boss.getPhase());
                helper.succeed();
            });
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void anchor_and_rematch_survive_reload(GameTestHelper helper) {
        var boss = EntityInit.PRISM_SENTINEL.get().create(helper.getLevel());
        BlockPos prism = new BlockPos(100, 70, -40);
        boss.bindToPrism(prism, true);
        CompoundTag tag = new CompoundTag();
        boss.addAdditionalSaveData(tag);
        helper.assertTrue(tag.getBoolean("Rematch"), "Rematch flag not written (the loot table reads {Rematch:1b})");
        var restored = EntityInit.PRISM_SENTINEL.get().create(helper.getLevel());
        restored.readAdditionalSaveData(tag);
        helper.assertTrue(prism.equals(restored.getAnchor()) && restored.isRematch(), "Anchor or rematch lost on reload");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 60)
    public static void first_win_drops_the_gate_key_rematch_does_not(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        var first = helper.spawn(EntityInit.PRISM_SENTINEL.get(), 3, 2, 3);
        var again = helper.spawn(EntityInit.PRISM_SENTINEL.get(), 12, 2, 12);
        again.bindToPrism(helper.absolutePos(new BlockPos(12, 1, 12)), true);
        first.kill();
        again.kill();
        helper.runAfterDelay(5, () -> {
            helper.assertTrue(dropped(helper, ItemInit.GALAXY_3_GATE_KEY.get(), 0, 7), "First win must drop the gate key");
            helper.assertTrue(dropped(helper, ItemInit.SENTINEL_PRISM.get(), 0, 7), "First win must drop the Sentinel Prism");
            helper.assertFalse(dropped(helper, ItemInit.GALAXY_3_GATE_KEY.get(), 9, 16), "A rematch must not drop a gate key");
            helper.assertTrue(dropped(helper, ItemInit.SENTINEL_PRISM.get(), 9, 16), "A rematch still drops its loot");
            helper.succeed();
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 400)
    public static void prism_summons_then_resets_when_nobody_is_inside(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        BlockPos rel = new BlockPos(8, 2, 8);
        helper.setBlock(rel, BlockInit.CONCORD_PRISM.get());
        var prism = (ConcordPrismBlockEntity) helper.getBlockEntity(rel);
        helper.assertTrue(prism.start(helper.getLevel()), "An idle prism should start");
        helper.assertTrue(prism.state() == ConcordPrismBlock.State.ACTIVE, "Starting should make the prism ACTIVE");
        helper.assertFalse(prism.start(helper.getLevel()), "An active prism must not start twice");
        helper.runAfterDelay(ConcordPrismBlockEntity.SUMMON_DELAY + 5, () -> {
            var bosses = ownSentinels(helper, prism);
            helper.assertTrue(bosses.size() == 1, "Expected 1 Sentinel after the countdown, found " + bosses.size());
            var boss = bosses.get(0);
            helper.assertTrue(Math.abs(boss.getY() - (helper.absolutePos(rel).getY() - 2)) < 1.5,
                    "The Sentinel should stand on the fight floor, 3 below the prism; y=" + boss.getY());
        });
        // no player inside: after EMPTY_RESET ticks the Sentinel withdraws and the prism re-opens
        helper.runAfterDelay(ConcordPrismBlockEntity.SUMMON_DELAY + ConcordPrismBlockEntity.EMPTY_RESET + 20, () -> {
            helper.assertTrue(prism.state() == ConcordPrismBlock.State.IDLE, "Prism should reset to IDLE, is " + prism.state());
            helper.assertTrue(ownSentinels(helper, prism).isEmpty(), "The Sentinel should withdraw on reset");
            helper.succeed();
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void defeated_prism_rearms_for_a_rematch(GameTestHelper helper) {
        BlockPos rel = new BlockPos(8, 2, 8);
        helper.setBlock(rel, BlockInit.CONCORD_PRISM.get().defaultBlockState()
                .setValue(ConcordPrismBlock.STATE, ConcordPrismBlock.State.DEFEATED));
        var prism = (ConcordPrismBlockEntity) helper.getBlockEntity(rel);
        helper.assertTrue(prism.rearm(helper.getLevel()), "A defeated prism should accept a Sentinel Prism");
        helper.assertTrue(prism.state() == ConcordPrismBlock.State.IDLE && prism.isRematch(), "Re-arm should give IDLE + rematch");
        helper.assertFalse(prism.rearm(helper.getLevel()), "Only a DEFEATED prism re-arms");
        helper.succeed();
    }

    /** Sentinels bound to this prism (tests run side by side, so the arena box can hold other tests' bosses). */
    private static java.util.List<PrismSentinel> ownSentinels(GameTestHelper helper, ConcordPrismBlockEntity prism) {
        return helper.getLevel().getEntitiesOfClass(PrismSentinel.class, prism.arenaBox(),
                s -> prism.getBlockPos().equals(s.getAnchor()));
    }

    private static boolean dropped(GameTestHelper helper, Item item, int from, int to) {
        var box = new AABB(helper.absolutePos(new BlockPos(from, 0, from)).getCenter(),
                helper.absolutePos(new BlockPos(to, 6, to)).getCenter()).inflate(1);
        return !helper.getLevel().getEntitiesOfClass(ItemEntity.class, box, e -> e.getItem().is(item)).isEmpty();
    }
}
