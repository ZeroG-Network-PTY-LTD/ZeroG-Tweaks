package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.Difficulty;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.entity.Tidewraith;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.TidewraithItems;

@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class TidewraithGameTests {
    @GameTest(template = "tidewraith_empty", timeoutTicks = 160)
    public static void regular_and_boss_survive_flight_ticks(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        var regular = helper.spawn(EntityInit.TIDEWRAITH.get(), 4, 5, 4);
        var boss = helper.spawn(EntityInit.TIDEWRAITH_BOSS.get(), 10, 5, 10);
        helper.assertTrue(!regular.isBoss() && boss.isBoss(), "Boss roles reversed");
        helper.assertTrue(regular.getMaxHealth() == 30 && boss.getMaxHealth() == 180,
                "Entity attributes missing or wrong");
        helper.assertTrue(boss.getAttributeValue(Attributes.ATTACK_DAMAGE) == 8,
                "Boss damage attribute missing");
        helper.assertTrue(Math.abs(boss.getBbHeight() - 2.125) < 0.001,
                "Authored boss dimensions were scaled again");
        helper.runAfterDelay(110, () -> {
            helper.assertTrue(regular.isAlive() && boss.isAlive(), "Entity disappeared");
            helper.assertTrue(regular.isNoGravity() && boss.isNoGravity(), "Flight gravity changed");
            helper.assertTrue(regular.tickCount >= 100 && boss.tickCount >= 100, "Entities did not tick");
            regular.discard(); boss.discard(); helper.succeed();
        });
    }

    @GameTest(template = "tidewraith_empty", timeoutTicks = 40)
    public static void boss_variants_save_and_clamp(GameTestHelper helper) {
        var boss = EntityInit.TIDEWRAITH_BOSS.get().create(helper.getLevel());
        helper.assertTrue(boss != null, "Boss type could not create an entity");
        boss.setVariant(3);
        CompoundTag tag = new CompoundTag();
        boss.addAdditionalSaveData(tag);
        var restored = EntityInit.TIDEWRAITH_BOSS.get().create(helper.getLevel());
        restored.readAdditionalSaveData(tag);
        helper.assertTrue(restored.getVariant() == 3, "Storm variant lost on reload");
        restored.setVariant(999);
        helper.assertTrue(restored.getVariant() == 3, "Invalid high variant not clamped");
        restored.setVariant(-1);
        helper.assertTrue(restored.getVariant() == 0, "Invalid low variant not clamped");
        helper.succeed();
    }

    @GameTest(template = "tidewraith_empty", timeoutTicks = 40)
    public static void both_spawn_eggs_create_correct_mobs(GameTestHelper helper) {
        helper.getLevel().getServer().setDifficulty(Difficulty.NORMAL, true);
        var player = helper.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        for (int i = 0; i < 2; i++) {
            var item = i == 0 ? TidewraithItems.TIDEWRAITH_EGG.get() : TidewraithItems.BOSS_EGG.get();
            BlockPos relative = new BlockPos(3 + i * 7, 0, 3);
            helper.setBlock(relative, Blocks.STONE);
            BlockPos absolute = helper.absolutePos(relative);
            player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(item));
            var hit = new BlockHitResult(Vec3.atCenterOf(absolute).add(0, 0.5, 0),
                    Direction.UP, absolute, false);
            var result = item.useOn(new UseOnContext(player, InteractionHand.MAIN_HAND, hit));
            helper.assertTrue(result.consumesAction(), "Egg interaction did not succeed");
            AABB area = new AABB(absolute).inflate(2);
            final boolean expectedBoss = i == 1;
            var mobs = helper.getLevel().getEntitiesOfClass(Tidewraith.class, area,
                    mob -> mob.isBoss() == expectedBoss);
            helper.assertTrue(mobs.size() == 1, "Egg did not create exactly one correct mob");
            mobs.forEach(Tidewraith::discard);
        }
        helper.succeed();
    }
}
