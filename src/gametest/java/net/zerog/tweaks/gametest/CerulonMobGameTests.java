package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.level.biome.Biome;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.registry.EntityInit;
import net.zerog.tweaks.registry.ItemInit;
import net.zerog.tweaks.registry.ZGSpawnRules;

/** Cerulon's natural mobs: they exist, behave per the mob spec, and spawn only where they belong. */
@GameTestHolder("zerog_tweaks")
@PrefixGameTestTemplate(false)
public final class CerulonMobGameTests {
    private static ResourceLocation rl(String path) {
        return ResourceLocation.fromNamespaceAndPath("zerog_tweaks", path);
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void cerulon_mobs_exist_with_spec_health(GameTestHelper helper) {
        var stag = helper.spawn(EntityInit.CRYSTAL_STAG.get(), 4, 2, 4);
        var prismling = helper.spawn(EntityInit.PRISMLING_HOLDER.get(), 8, 2, 4);
        var fowl = helper.spawn(EntityInit.AZURE_FOWL.get(), 4, 2, 8);
        var fish = helper.spawn(EntityInit.GLIMMERFISH.get(), 8, 2, 8);
        helper.assertTrue(stag.getMaxHealth() == 20 && prismling.getMaxHealth() == 8 && fowl.getMaxHealth() == 4
                && fish.getMaxHealth() == 3, "Mob health differs from the mob spec");
        helper.assertTrue(fish.getBucketItemStack().is(ItemInit.GLIMMERFISH_BUCKET.get()), "Glimmerfish should bucket");
        stag.discard(); prismling.discard(); fowl.discard(); fish.discard();
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 60)
    public static void azure_fowl_lays_blue_eggs(GameTestHelper helper) {
        var fowl = EntityInit.AZURE_FOWL.get().create(helper.getLevel());
        CompoundTag tag = new CompoundTag();
        fowl.addAdditionalSaveData(tag);
        tag.putInt("EggLayTime", 2);
        fowl.readAdditionalSaveData(tag);
        var pos = helper.absoluteVec(new net.minecraft.world.phys.Vec3(8.5, 2, 8.5));
        fowl.moveTo(pos.x, pos.y, pos.z);
        helper.getLevel().addFreshEntity(fowl);
        helper.runAfterDelay(10, () -> {
            boolean egg = !helper.getLevel().getEntitiesOfClass(ItemEntity.class, fowl.getBoundingBox().inflate(3),
                    e -> e.getItem().is(ItemInit.BLUE_EGG.get())).isEmpty();
            helper.assertTrue(egg, "The Azure Fowl should lay a Blue Egg");
            fowl.discard();
            helper.succeed();
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void sheared_stag_hides_its_antlers(GameTestHelper helper) {
        var stag = helper.spawn(EntityInit.CRYSTAL_STAG.get(), 8, 2, 8);
        helper.assertTrue(stag.hiddenBones().isEmpty(), "Antlers hidden before shearing");
        stag.onSheared(null, net.minecraft.world.item.ItemStack.EMPTY, helper.getLevel(), stag.blockPosition());
        helper.assertTrue(stag.isSheared() && stag.hiddenBones().contains("antlers"), "Sheared stag should hide its antlers");
        stag.discard();
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void spawn_rules_are_registered(GameTestHelper helper) {
        helper.assertTrue(SpawnPlacements.getPlacementType(EntityInit.CRYSTAL_STAG.get()) == SpawnPlacementTypes.ON_GROUND
                && SpawnPlacements.getPlacementType(EntityInit.AZURE_FOWL.get()) == SpawnPlacementTypes.ON_GROUND
                && SpawnPlacements.getPlacementType(EntityInit.PRISMLING_HOLDER.get()) == SpawnPlacementTypes.ON_GROUND
                && SpawnPlacements.getPlacementType(EntityInit.GLIMMERFISH.get()) == SpawnPlacementTypes.IN_WATER,
                "Spawn placements missing");
        var level = helper.getLevel();
        var surface = new BlockPos(0, level.getSeaLevel() + 5, 0);
        helper.assertFalse(ZGSpawnRules.prismling(EntityInit.PRISMLING_HOLDER.get(), level, MobSpawnType.NATURAL, surface,
                level.random), "Prismlings must not spawn naturally at the surface");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void cerulon_biomes_list_the_right_mobs(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        Biome plains = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("azure_plains")));
        Biome grove = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("shardwood_grove")));
        Biome shores = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("crystal_shores")));
        helper.assertTrue(spawns(plains, MobCategory.CREATURE, EntityInit.CRYSTAL_STAG.get())
                && spawns(plains, MobCategory.CREATURE, EntityInit.AZURE_FOWL.get()), "Plains: stags and fowl");
        helper.assertTrue(spawns(grove, MobCategory.CREATURE, EntityInit.AZURE_FOWL.get())
                && spawns(grove, MobCategory.CREATURE, EntityInit.CRYSTAL_STAG.get()), "Grove: fowl and a few stags");
        helper.assertTrue(spawns(shores, MobCategory.CREATURE, EntityInit.AZURE_FOWL.get())
                && !spawns(shores, MobCategory.CREATURE, EntityInit.CRYSTAL_STAG.get()), "Shores: fowl only, no stags");
        Biome sea = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("glimmer_sea")));
        Biome caverns = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("starlight_caverns")));
        Biome peaks = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("cerulean_peaks")));
        helper.assertTrue(spawns(sea, MobCategory.WATER_AMBIENT, EntityInit.GLIMMERFISH.get()), "Glimmerfish live in the Glimmer Sea");
        helper.assertTrue(spawns(caverns, MobCategory.MONSTER, EntityInit.PRISMLING_HOLDER.get())
                && spawns(peaks, MobCategory.MONSTER, EntityInit.PRISMLING_HOLDER.get()), "Prismlings: caves, and peaks at night");
        helper.assertFalse(spawns(plains, MobCategory.MONSTER, EntityInit.PRISMLING_HOLDER.get()), "No Prismlings on the plains");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void mossback_styles_and_stats(GameTestHelper helper) {
        int[] hits = new int[net.zerog.tweaks.entity.Mossback.Style.values().length];
        for (int roll = 0; roll < 100; roll++) hits[net.zerog.tweaks.entity.Mossback.Style.forRoll(roll).ordinal()]++;
        helper.assertTrue(hits[0] == 65 && hits[1] == 20 && hits[2] == 10 && hits[3] == 5,
                "Mossback styles should be 65/20/10/5, got " + java.util.Arrays.toString(hits));
        var moss = EntityInit.MOSSBACK.get().create(helper.getLevel());
        helper.assertTrue(moss.getMaxHealth() == 40
                && moss.getAttributeValue(net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE) == 7,
                "Mossback should have 40 HP and 7 damage");
        helper.assertTrue(Math.abs(moss.getBbWidth() - 2.5) < 0.001 && Math.abs(moss.getBbHeight() - 2.0) < 0.001, "Hitbox 2.5 x 2");
        moss.setStyle(net.zerog.tweaks.entity.Mossback.Style.BLOSSOM);
        helper.assertTrue("mossback_blossom".equals(moss.assetId("mossback")), "Style should pick its own art set");
        CompoundTag tag = new CompoundTag();
        moss.addAdditionalSaveData(tag);
        var back = EntityInit.MOSSBACK.get().create(helper.getLevel());
        back.readAdditionalSaveData(tag);
        helper.assertTrue(back.getStyle() == net.zerog.tweaks.entity.Mossback.Style.BLOSSOM, "Style lost on reload");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void mossback_calf_keeps_a_parent_style(GameTestHelper helper) {
        var a = EntityInit.MOSSBACK.get().create(helper.getLevel());
        var b = EntityInit.MOSSBACK.get().create(helper.getLevel());
        a.setStyle(net.zerog.tweaks.entity.Mossback.Style.RUINBACK);
        b.setStyle(net.zerog.tweaks.entity.Mossback.Style.AUTUMN);
        for (int i = 0; i < 20; i++) {
            var calf = (net.zerog.tweaks.entity.Mossback) a.getBreedOffspring(helper.getLevel(), b);
            var st = calf.getStyle();
            helper.assertTrue(st == net.zerog.tweaks.entity.Mossback.Style.RUINBACK || st == net.zerog.tweaks.entity.Mossback.Style.AUTUMN,
                    "Calf style should come from a parent, got " + st);
        }
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 100)
    public static void mossback_is_neutral_until_hit(GameTestHelper helper) {
        var moss = helper.spawn(EntityInit.MOSSBACK.get(), 8, 2, 8);
        var player = helper.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);
        player.moveTo(helper.absoluteVec(new net.minecraft.world.phys.Vec3(10.5, 2, 8.5)));
        helper.runAfterDelay(30, () -> {
            helper.assertTrue(moss.getTarget() == null, "A Mossback should ignore a player who didn't hit it");
            moss.hurt(helper.getLevel().damageSources().playerAttack(player), 1.0F);
            helper.runAfterDelay(20, () -> {
                helper.assertTrue(moss.isAngry() || moss.getTarget() == player, "A hit Mossback should fight back");
                moss.discard();
                helper.succeed();
            });
        });
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 20)
    public static void mossback_roams_the_azure_plains(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        Biome plains = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("azure_plains")));
        Biome shores = biomes.getOrThrow(ResourceKey.create(Registries.BIOME, rl("crystal_shores")));
        helper.assertTrue(spawns(plains, MobCategory.CREATURE, EntityInit.MOSSBACK.get()), "Mossbacks belong on the plains");
        // the colleague's expanded_habitat_cerulon_mossback lists it in every Cerulon biome; the spawn rule (Azure Moss + light)
        // is what keeps it on the moss, so check the rule instead of the biome list
        var level = helper.getLevel();
        var air = helper.absolutePos(new net.minecraft.core.BlockPos(4, 3, 4));
        helper.setBlock(new net.minecraft.core.BlockPos(4, 2, 4), net.zerog.tweaks.registry.BlockInit.CRYSTAL_SAND.get());
        helper.assertFalse(net.zerog.tweaks.registry.ZGSpawnRules.landAnimal(EntityInit.MOSSBACK.get(), level,
                net.minecraft.world.entity.MobSpawnType.NATURAL, air, level.random), "Mossbacks must not spawn on sand");
        helper.assertTrue(SpawnPlacements.getPlacementType(EntityInit.MOSSBACK.get()) == SpawnPlacementTypes.ON_GROUND, "Mossback spawn rule");
        helper.succeed();
    }

    private static boolean spawns(Biome biome, MobCategory category, EntityType<?> type) {
        return biome.getMobSettings().getMobs(category).unwrap().stream().anyMatch(d -> d.type == type);
    }
}
