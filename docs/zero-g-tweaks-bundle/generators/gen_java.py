from food_data import F
E={'crawler_leg':[('HUNGER',10,0,.3)],'beetle_grub':[('CONFUSION',4,0,.3)],'lurker_leg':[('POISON',4,0,.6)],
'grilled_scorch_tail':[('FIRE_RESISTANCE',30,0,1)],'cooked_glimmerfish':[('NIGHT_VISION',30,0,1)],'cooked_hopper':[('JUMP',20,0,1)],'cooked_gildcrab':[('ABSORPTION',20,0,1)],
'shardwood_syrup':[('MOVEMENT_SPEED',10,0,1)],'cinder_cap_stew':[('FIRE_RESISTANCE',60,0,1)],'pyrefruit':[('GLOWING',10,0,1)],'nebula_pie':[('NIGHT_VISION',60,0,1)],
'ember_chili':[('FIRE_RESISTANCE',180,0,1),('DAMAGE_BOOST',30,0,1)],'cryo_chowder':[('DAMAGE_RESISTANCE',30,0,1)],'starfall_feast':[('REGENERATION',10,1,1),('ABSORPTION',120,1,1)],
'low_g_jelly':[('SLOW_FALLING',60,0,1),('JUMP',60,1,1)]}
FAST={'astronaut_ration','ration_pack'}; BOWL={'cinder_cap_stew','ember_chili','cryo_chowder','starfall_feast'}; BOTTLE={'shardwood_syrup','frostfern_tea','frost_milk'}
TODO={'scorch_tail':'sets the eater on fire for 2 s (ScorchTailItem)','frostfern_tea':'Freeze Ward 60 s (custom effect)','cryo_chowder':'Freeze Ward 180 s (custom effect)',
'frost_milk':'clears effects + Slowness immunity 30 s (FrostMilkItem + custom effect)'}
out=['package net.zerog.tweaks.item;','','import net.minecraft.world.effect.MobEffectInstance;','import net.minecraft.world.effect.MobEffects;','import net.minecraft.world.food.FoodProperties;','import net.minecraft.world.item.Items;','',
'/** Generated from the ZeroG Tweaks food table (NeoForge 1.21.1). Values are proposals for playtesting. */','public final class ZGFoods {','    private ZGFoods() {}','']
for it in F:
    if not it['hun']: continue
    k=it['k']; b=f"new FoodProperties.Builder().nutrition({it['hun']}).saturationModifier({it['sat']}f)"
    for (e,s,a,p) in E.get(k,[]): b+=f"\n            .effect(new MobEffectInstance(MobEffects.{e}, {s*20}, {a}), {p}f)"
    if k in FAST: b+="\n            .fast()"
    if k in BOWL: b+="\n            .usingConvertsTo(Items.BOWL)"
    if k in BOTTLE: b+="\n            .usingConvertsTo(Items.GLASS_BOTTLE).alwaysEdible()"
    if k in TODO: out.append(f"    // TODO: {TODO[k]}")
    out.append(f"    public static final FoodProperties {k.upper()} = {b}\n            .build();")
out+=['}','']
open('out_java/ZGFoods.java','w').write('\n'.join(out))
open('out_java/ZGInteractions.java','w').write('''package net.zerog.tweaks.event;

import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.registry.ZGBlocks;
import net.zerog.tweaks.registry.ZGEntities;
import net.zerog.tweaks.registry.ZGItems;

/**
 * Bottle interactions: milk a Frost Yak, tap a Shardwood log for syrup.
 * Shearing (Crystal Stag antlers, Frost Yak wool) lives in the entity classes via IShearable; see the notes at the bottom.
 */
@EventBusSubscriber(modid = ZeroGTweaks.MODID)
public final class ZGInteractions {
    private ZGInteractions() {}

    @SubscribeEvent
    public static void onEntityInteract(PlayerInteractEvent.EntityInteract event) {
        Player player = event.getEntity();
        ItemStack held = event.getItemStack();
        Entity target = event.getTarget();
        Level level = event.getLevel();
        if (target.getType() == ZGEntities.FROST_YAK.get() && held.is(Items.GLASS_BOTTLE)
                && target instanceof Animal yak && !yak.isBaby()) {
            if (!level.isClientSide) {
                ItemStack milk = new ItemStack(ZGItems.FROST_MILK.get());
                player.setItemInHand(event.getHand(), ItemUtils.createFilledResult(held, player, milk));
                level.playSound(null, target.blockPosition(), SoundEvents.COW_MILK, SoundSource.NEUTRAL, 1.0f, 1.2f);
            }
            event.setCancellationResult(InteractionResult.sidedSuccess(level.isClientSide));
            event.setCanceled(true);
        }
    }

    @SubscribeEvent
    public static void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        Player player = event.getEntity();
        ItemStack held = event.getItemStack();
        Level level = event.getLevel();
        BlockPos pos = event.getPos();
        if (held.is(Items.GLASS_BOTTLE) && level.getBlockState(pos).is(ZGBlocks.SHARDWOOD_LOG.get())
                && !player.getCooldowns().isOnCooldown(Items.GLASS_BOTTLE)) {
            if (!level.isClientSide) {
                ItemStack syrup = new ItemStack(ZGItems.SHARDWOOD_SYRUP.get());
                player.setItemInHand(event.getHand(), ItemUtils.createFilledResult(held, player, syrup));
                level.playSound(null, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, 1.0f, 1.0f);
                player.getCooldowns().addCooldown(Items.GLASS_BOTTLE, 100); // 5 s between taps
            }
            event.setCancellationResult(InteractionResult.sidedSuccess(level.isClientSide));
            event.setCanceled(true);
        }
    }
}

/*
 * Shearing, implemented on the entity (NeoForge IShearable):
 *
 * public class CrystalStag extends Animal implements IShearable {
 *     private static final EntityDataAccessor<Boolean> SHEARED = SynchedEntityData.defineId(CrystalStag.class, EntityDataSerializers.BOOLEAN);
 *     private int regrowTicks;
 *
 *     @Override public boolean isShearable(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
 *         return !isBaby() && !entityData.get(SHEARED);
 *     }
 *     @Override public List<ItemStack> onSheared(@Nullable Player player, ItemStack item, Level level, BlockPos pos) {
 *         entityData.set(SHEARED, true); regrowTicks = 6000;              // antlers regrow in 5 minutes
 *         level.playSound(null, this, SoundEvents.AMETHYST_BLOCK_BREAK, SoundSource.NEUTRAL, 1f, 1f);
 *         return List.of(new ItemStack(ZGItems.STARLITE.get(), 1 + random.nextInt(2)));
 *     }
 *     @Override public void aiStep() { super.aiStep(); if (!level().isClientSide && entityData.get(SHEARED) && --regrowTicks <= 0) entityData.set(SHEARED, false); }
 * }
 *
 * FrostYak: same pattern, returning 1-2 Yak Wool; wool regrows after eating (like sheep eating grass) or after a timer.
 */
''')
open('out_java/ZGFoodItems.java','w').write('''package net.zerog.tweaks.item;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
import net.minecraft.world.item.Item;

/** Small item classes for foods with behavior beyond FoodProperties. */
public final class ZGFoodItems {
    private ZGFoodItems() {}

    /** Drinks (Shardwood Syrup, Frostfern Tea, Frost Milk) use the drink animation. */
    public static class DrinkItem extends Item {
        public DrinkItem(Properties props) { super(props); }
        @Override public UseAnim getUseAnimation(ItemStack stack) { return UseAnim.DRINK; }
    }

    /** Frost Milk: clears all effects like milk. */
    public static class FrostMilkItem extends DrinkItem {
        public FrostMilkItem(Properties props) { super(props); }
        @Override public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
            if (!level.isClientSide) entity.removeAllEffects();
            return super.finishUsingItem(stack, level, entity);
        }
    }

    /** Raw Scorch Tail: sets the eater on fire for 2 seconds. */
    public static class ScorchTailItem extends Item {
        public ScorchTailItem(Properties props) { super(props); }
        @Override public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
            if (!level.isClientSide) entity.igniteForSeconds(2.0f);
            return super.finishUsingItem(stack, level, entity);
        }
    }
}
''')
open('out_java/README.md','w').write('''# ZeroG Tweaks Java helpers (NeoForge 1.21.1)

Package names (`net.zerog.tweaks...`) and registry classes (`ZGItems`, `ZGBlocks`, `ZGEntities`) are placeholders; rename to match your project.

- `ZGFoods.java`: every food's FoodProperties from the design table. Custom effects (Freeze Ward, slowness immunity) are marked TODO.
- `ZGFoodItems.java`: drink animation, Frost Milk (clears effects), raw Scorch Tail (sets you on fire).
- `ZGInteractions.java`: milking a Frost Yak and tapping Shardwood logs with a glass bottle; shearing notes for the Crystal Stag and Frost Yak.

Registration notes:
- Astronaut Ration: `new Item.Properties().food(ZGFoods.ASTRONAUT_RATION).stacksTo(16)`.
- Bowl dishes: `.stacksTo(1)` like vanilla stews.
- Crops: register `rust_tuber_crop` as a CropBlock (age 0-3) with Rust Tuber as its seed item, and `skyberry_bush` like SweetBerryBushBlock.
- Fluid: `acid_still.png` / `acid_flow.png` are the textures for the Acid fluid type.
- Emissive blocks: models with a second element carrying `neoforge_data` (block_light 15) render the `_emissive.png` overlay full-bright. Verify in game.
''')
print('ok')
