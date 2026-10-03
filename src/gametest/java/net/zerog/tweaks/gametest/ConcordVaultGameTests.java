package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameType;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.arena.ConcordLockBlock;
import net.zerog.tweaks.arena.VaultKeyAltarBlock;
import net.zerog.tweaks.entity.Prismling;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ItemInit;

/** Concord Vault: Key Altars hand out keys, the Concord Lock builds the Sentinel chamber one key at a time. */
@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class ConcordVaultGameTests {
    private static BlockHitResult hit(GameTestHelper helper, BlockPos rel) {
        return new BlockHitResult(Vec3.atCenterOf(helper.absolutePos(rel)), Direction.UP, helper.absolutePos(rel), false);
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void key_altar_gives_one_key_and_wakes_guardians(GameTestHelper helper) {
        BlockPos rel = new BlockPos(8, 2, 8);
        helper.setBlock(rel, BlockInit.VAULT_KEY_ALTAR.get());
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        var state = helper.getBlockState(rel);
        state.useWithoutItem(helper.getLevel(), player, hit(helper, rel));
        helper.assertTrue(player.getInventory().countItem(ItemInit.CONCORD_VAULT_KEY.get()) == 1, "The altar should give one Concord Key");
        helper.assertFalse(helper.getBlockState(rel).getValue(VaultKeyAltarBlock.HAS_KEY), "The altar should be empty now");
        helper.getBlockState(rel).useWithoutItem(helper.getLevel(), player, hit(helper, rel));
        helper.assertTrue(player.getInventory().countItem(ItemInit.CONCORD_VAULT_KEY.get()) == 1, "An empty altar gives nothing");
        int guardians = helper.getLevel().getEntitiesOfClass(Prismling.class, new net.minecraft.world.phys.AABB(helper.absolutePos(rel)).inflate(5)).size();
        helper.assertTrue(guardians > 0, "Taking the key should wake Prismling guardians");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 60, batch = "concord_vault_lock")
    public static void four_keys_build_the_chamber_and_form_the_prism(GameTestHelper helper) {
        BlockPos rel = new BlockPos(8, 6, 8);
        helper.setBlock(rel, BlockInit.CONCORD_LOCK.get().defaultBlockState());
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(ItemInit.CONCORD_VAULT_KEY.get(), 4));
        BlockPos lock = helper.absolutePos(rel);
        for (int key = 1; key <= ConcordLockBlock.KEYS; key++) {
            var state = helper.getLevel().getBlockState(lock);
            state.useItemOn(player.getMainHandItem(), helper.getLevel(), player, InteractionHand.MAIN_HAND, hit(helper, rel));
            if (key == 1) {
                // stage 1 lights the floor: a radial pulsar-lamp line runs from r6 out to r21 (floor = lock - 3)
                helper.assertTrue(helper.getLevel().getBlockState(lock.offset(0, -3, 10)).is(BlockInit.PULSAR_LAMP.get()),
                        "The first key should light the chamber floor");
            }
            if (key == 2) {
                helper.assertTrue(helper.getLevel().getBlockState(lock.offset(14, -2, 14)).is(BlockInit.CHISELED_POLISHED_BLACK_CERULEAN_STONE.get()),
                        "The second key should raise the refractor pylons");
            }
            if (key < ConcordLockBlock.KEYS) {
                helper.assertTrue(helper.getLevel().getBlockState(lock).getValue(ConcordLockBlock.STAGE) == key, "Lock stage should be " + key);
            }
        }
        helper.assertTrue(helper.getLevel().getBlockState(lock).is(BlockInit.CONCORD_PRISM.get()), "The fourth key should form the Concord Prism");
        helper.assertTrue(player.getMainHandItem().isEmpty(), "All four keys should be used up");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void lock_rotation_matches_the_structure(GameTestHelper helper) {
        helper.assertTrue(ConcordLockBlock.rotationOf(Direction.SOUTH) == net.minecraft.world.level.block.Rotation.NONE
                && ConcordLockBlock.rotationOf(Direction.WEST) == net.minecraft.world.level.block.Rotation.CLOCKWISE_90
                && ConcordLockBlock.rotationOf(Direction.NORTH) == net.minecraft.world.level.block.Rotation.CLOCKWISE_180
                && ConcordLockBlock.rotationOf(Direction.EAST) == net.minecraft.world.level.block.Rotation.COUNTERCLOCKWISE_90,
                "Lock facing -> rotation");
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        helper.assertTrue(structures.containsKey(ResourceLocation.fromNamespaceAndPath("zerog_tweaks", "concord_vault")), "Vault structure missing");
        var templates = helper.getLevel().getStructureManager();
        for (String t : new String[] {"chamber", "chamber_stage_1", "chamber_stage_2", "chamber_stage_3", "entrance_shaft",
                "corridor_straight", "rooms/storage_hall", "rooms/concord_shrine"}) {
            helper.assertTrue(templates.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks", "concord_vault/" + t)).isPresent(), "Missing template " + t);
        }
        helper.succeed();
    }
}
