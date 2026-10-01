package net.zerog.tweaks.gametest;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TieredItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.EquipmentSlot;
import net.neoforged.neoforge.common.damagesource.DamageContainer;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SnowLayerBlock;
import net.minecraft.world.level.block.FenceBlock;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGArmorMaterials;
import net.zerog.tweaks.registry.ZGToolTiers;
import net.zerog.tweaks.item.ZGArmorSetBonuses;

/** Registry-backed tests, compiled separately; running them needs human launch approval. */
@GameTestHolder(ZeroGTweaks.MODID)
@PrefixGameTestTemplate(false)
public final class EquipmentGameTests {
    private static final ArmorItem.Type[] TYPES = {ArmorItem.Type.HELMET,
            ArmorItem.Type.CHESTPLATE, ArmorItem.Type.LEGGINGS, ArmorItem.Type.BOOTS};

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void wooden_fences_use_boolean_connection_states(GameTestHelper helper) {
        for (String wood : new String[]{"charwood", "gildwood", "hoarwood", "shardwood"}) {
            var block = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, wood + "_fence"));
            helper.assertTrue(block instanceof FenceBlock, wood + " fence is a wall");
            var state = block.defaultBlockState();
            for (var property : new net.minecraft.world.level.block.state.properties.BooleanProperty[]{
                    FenceBlock.NORTH, FenceBlock.EAST, FenceBlock.SOUTH, FenceBlock.WEST}) {
                helper.assertTrue(state.hasProperty(property) && !state.getValue(property), "Invalid fence model property");
            }
            helper.assertTrue(block.getStateDefinition().getPossibleStates().size() == 32, "Unexpected fence states");
        }
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void deposits_have_eight_layers_and_stack_like_snow(GameTestHelper helper) {
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        BlockPos relative = new BlockPos(1, 1, 1);
        BlockPos absolute = helper.absolutePos(relative);
        helper.setBlock(relative.below(), Blocks.STONE);
        for (String name : new String[]{"ashfall", "crater_dust", "snowpack"}) {
            var block = BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, name));
            helper.assertTrue(block instanceof SnowLayerBlock, name + " is not a layered deposit");
            helper.assertTrue(block.getStateDefinition().getPossibleStates().size() == 8, "Wrong layer count");
            for (int layers = 1; layers <= 8; layers++) {
                var state = block.defaultBlockState().setValue(SnowLayerBlock.LAYERS, layers);
                helper.assertTrue(Math.abs(state.getShape(helper.getLevel(), absolute, CollisionContext.empty())
                        .max(Direction.Axis.Y) - layers / 8.0) < 0.001, "Wrong visible deposit height");
            }
            helper.setBlock(relative, block.defaultBlockState());
            player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(block));
            var hit = new BlockHitResult(Vec3.atCenterOf(absolute).add(0, 0.5, 0), Direction.UP, absolute, false);
            var placement = new BlockPlaceContext(player, InteractionHand.MAIN_HAND,
                    player.getMainHandItem(), hit);
            var stacked = block.getStateForPlacement(placement);
            helper.assertTrue(stacked != null && stacked.getValue(SnowLayerBlock.LAYERS) == 2,
                    "Deposit did not stack onto its first layer");
        }
        helper.succeed();
    }

    private static ArmorItem armor(GameTestHelper helper, String material, ArmorItem.Type type) {
        var id = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, material + "_" + type.getName());
        var item = BuiltInRegistries.ITEM.get(id);
        helper.assertTrue(item instanceof ArmorItem, id + " is not wearable armour");
        return (ArmorItem)item;
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void all_eighty_have_slots_durability_repairs_and_trims(GameTestHelper helper) {
        int count = 0;
        for (var entry : ZGArmorMaterials.profiles().entrySet()) {
            for (var type : TYPES) {
                var item = armor(helper, entry.getKey(), type);
                var stack = new ItemStack(item);
                helper.assertTrue(item.getEquipmentSlot() == type.getSlot(), "Wrong equipment slot");
                helper.assertTrue(item.getMaterial() == entry.getValue().material(), "Wrong armour material");
                helper.assertTrue(stack.getMaxStackSize() == 1, "Armour can stack");
                helper.assertTrue(stack.getMaxDamage() == type.getDurability(entry.getValue().durabilityFactor()),
                        "Wrong durability for " + entry.getKey() + " " + type.getName());
                helper.assertTrue(stack.is(ItemTags.TRIMMABLE_ARMOR), "Not tagged for smithing trims");
                helper.assertTrue(stack.is(ItemTags.ARMOR_ENCHANTABLE), "Not tagged for armour enchantments");
                helper.assertTrue(stack.is(ItemTags.DURABILITY_ENCHANTABLE), "Not tagged for durability enchantments");
                var repair = item.getMaterial().value().repairIngredient().get().getItems();
                helper.assertTrue(repair.length == 1 && item.isValidRepairItem(stack, repair[0]), "Repair ingredient missing");
                helper.assertTrue(!item.isValidRepairItem(stack, new ItemStack(Items.DIRT)), "Dirt repairs armour");
                helper.assertTrue(item.getDefense() > 0 && item.getEnchantmentValue() > 0, "Protection/enchantability missing");
                count++;
            }
        }
        helper.assertTrue(count == 80, "Expected all 20 four-piece sets, got " + count);
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void all_eighty_right_click_equip(GameTestHelper helper) {
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        for (var entry : ZGArmorMaterials.profiles().entrySet()) {
            for (var type : TYPES) {
                var item = armor(helper, entry.getKey(), type);
                player.setItemSlot(type.getSlot(), ItemStack.EMPTY);
                player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(item));
                var result = item.use(helper.getLevel(), player, InteractionHand.MAIN_HAND);
                helper.assertTrue(result.getResult().consumesAction(), "Right-click equip failed");
                helper.assertTrue(player.getItemBySlot(type.getSlot()).is(item), "Item not in intended slot");
                player.setItemSlot(type.getSlot(), ItemStack.EMPTY);
            }
        }
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void armour_attributes_are_slot_bound(GameTestHelper helper) {
        for (var entry : ZGArmorMaterials.profiles().entrySet()) {
            for (var type : TYPES) {
                var item = armor(helper, entry.getKey(), type);
                var attrs = item.getDefaultAttributeModifiers();
                // Check individual entries rather than summing unlike attribute kinds.
                long protection = attrs.modifiers().stream().filter(mod ->
                        mod.attribute().equals(Attributes.ARMOR)
                        && mod.slot().test(type.getSlot())
                        && mod.modifier().amount() == item.getDefense()).count();
                helper.assertTrue(protection == 1, "Missing/duplicate slot-bound protection");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void all_hundred_tools_have_behavior_and_repairs(GameTestHelper helper) {
        String[] kinds = {"sword", "pickaxe", "axe", "shovel", "hoe"};
        Class<?>[] classes = {SwordItem.class, PickaxeItem.class, AxeItem.class, ShovelItem.class, HoeItem.class};
        int count = 0;
        for (var entry : ZGToolTiers.profiles().entrySet()) {
            for (int i = 0; i < kinds.length; i++) {
                var id = ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, entry.getKey() + "_" + kinds[i]);
                var item = BuiltInRegistries.ITEM.get(id);
                helper.assertTrue(classes[i].isInstance(item), id + " has no intended tool behavior");
                var tiered = (TieredItem)item;
                var stack = new ItemStack(item);
                helper.assertTrue(tiered.getTier() == entry.getValue().tier(), "Wrong tool tier");
                helper.assertTrue(stack.getMaxDamage() == tiered.getTier().getUses(), "Wrong tool durability");
                helper.assertTrue(stack.getMaxStackSize() == 1, "Tools stack");
                helper.assertTrue(stack.is(ItemTags.DURABILITY_ENCHANTABLE), "Tool cannot receive durability enchantments");
                var repair = tiered.getTier().getRepairIngredient().getItems();
                helper.assertTrue(repair.length == 1 && tiered.isValidRepairItem(stack, repair[0]), "Tool repair missing");
                helper.assertTrue(!tiered.isValidRepairItem(stack, new ItemStack(Items.DIRT)), "Dirt repairs tools");
                count++;
            }
        }
        helper.assertTrue(count == 100, "Expected 20 five-tool sets");
        helper.succeed();
    }

    private static void equip(GameTestHelper helper, Player player, String material) {
        for (var type : TYPES) player.setItemSlot(type.getSlot(), new ItemStack(armor(helper, material, type)));
    }

    private static LivingIncomingDamageEvent damage(Player player, net.minecraft.world.damagesource.DamageSource source) {
        var event = new LivingIncomingDamageEvent(player, new DamageContainer(source, 8));
        ZGArmorSetBonuses.incomingDamage(event);
        return event;
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void bonuses_require_complete_matching_sets(GameTestHelper helper) {
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        equip(helper, player, "nullifite");
        helper.assertTrue(ZGArmorSetBonuses.wearsFullSet(player, "nullifite"), "Complete set not recognized");
        helper.assertTrue(damage(player, player.damageSources().fall()).isCanceled(), "Null Step did not block fall damage");
        player.setItemSlot(EquipmentSlot.FEET, ItemStack.EMPTY);
        helper.assertTrue(!damage(player, player.damageSources().fall()).isCanceled(), "Partial set still grants immunity");
        equip(helper, player, "moonsteel");
        helper.assertTrue(damage(player, player.damageSources().fall()).getAmount() == 4, "Lunar Stride not 50%");
        equip(helper, player, "ruskite");
        helper.assertTrue(damage(player, player.damageSources().inFire()).getAmount() == 6, "Heat Scale not 25%");
        equip(helper, player, "skarnite");
        helper.assertTrue(damage(player, player.damageSources().lava()).isCanceled(), "Ember Walk did not block lava damage");
        helper.assertTrue(!damage(player, player.damageSources().fall()).isCanceled(), "Ember Walk blocks unrelated damage");
        equip(helper, player, "eidolite");
        helper.assertTrue(damage(player, player.damageSources().freeze()).isCanceled(), "Phantom Veil did not block freezing");
        equip(helper, player, "cobaltium");
        var speed = new PlayerEvent.BreakSpeed(player, Blocks.STONE.defaultBlockState(), 10, null);
        ZGArmorSetBonuses.breakSpeed(speed);
        helper.assertTrue(Math.abs(speed.getNewSpeed() - 11) < 0.001, "Quick Hands is not +10%");
        helper.succeed();
    }

    @GameTest(template = "equipment_empty", timeoutTicks = 40)
    public static void attribute_bonuses_do_not_stack_or_leak_after_unequip(GameTestHelper helper) {
        var player = helper.makeMockPlayer(GameType.SURVIVAL);
        double baseHealth = player.getAttributeValue(Attributes.MAX_HEALTH);
        double baseToughness = player.getAttributeValue(Attributes.ARMOR_TOUGHNESS);
        equip(helper, player, "astrium");
        for (int i = 0; i < 50; i++) ZGArmorSetBonuses.updateSetAttributes(player);
        helper.assertTrue(player.getAttributeValue(Attributes.MAX_HEALTH) == baseHealth + 2, "Health bonus stacks");
        player.setItemSlot(EquipmentSlot.HEAD, ItemStack.EMPTY);
        ZGArmorSetBonuses.updateSetAttributes(player);
        helper.assertTrue(player.getAttributeValue(Attributes.MAX_HEALTH) == baseHealth, "Health bonus leaked after unequip");
        equip(helper, player, "ferrox");
        for (int i = 0; i < 50; i++) ZGArmorSetBonuses.updateSetAttributes(player);
        helper.assertTrue(player.getAttributeValue(Attributes.ARMOR_TOUGHNESS) == baseToughness + 1, "Sturdy is not +1 total");
        player.setItemSlot(EquipmentSlot.FEET, ItemStack.EMPTY);
        ZGArmorSetBonuses.updateSetAttributes(player);
        helper.assertTrue(player.getAttributeValue(Attributes.ARMOR_TOUGHNESS) == baseToughness, "Sturdy leaked after unequip");
        helper.succeed();
    }

    private EquipmentGameTests() {}
}
