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
        helper.assertTrue(spawns(shores, MobCategory.WATER_AMBIENT, EntityInit.GLIMMERFISH.get())
                && spawns(plains, MobCategory.MONSTER, EntityInit.PRISMLING_HOLDER.get()), "Fish and (underground) Prismlings");
        helper.succeed();
    }

    private static boolean spawns(Biome biome, MobCategory category, EntityType<?> type) {
        return biome.getMobSettings().getMobs(category).unwrap().stream().anyMatch(d -> d.type == type);
    }
}
