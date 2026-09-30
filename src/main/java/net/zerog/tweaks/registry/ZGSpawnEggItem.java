package net.zerog.tweaks.registry;

import java.util.Objects;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.gameevent.GameEvent;

/**
 * Spawn egg that finds its entity type by id when used, instead of holding a registry reference.
 * Works like the vanilla spawn egg (clicked face placement, consumes one outside creative) once the
 * entity is registered; before that it tells the player the mob isn't in the game yet.
 * Colours: base = layer 0, spots = layer 1 of minecraft:item/template_spawn_egg (see client/ZGItemColors).
 */
public class ZGSpawnEggItem extends Item {
    private final int base;
    private final int spots;
    private final String[] entityIds;

    public ZGSpawnEggItem(int base, int spots, String[] entityIds, Item.Properties props) {
        super(props);
        this.base = base;
        this.spots = spots;
        this.entityIds = entityIds;
    }

    public int color(int tintIndex) {
        return tintIndex == 0 ? base : tintIndex == 1 ? spots : 0xFFFFFF;
    }

    /** The entity type this egg spawns, or null while no mod has registered it. */
    public EntityType<?> entityType() {
        for (String id : entityIds) {
            var type = BuiltInRegistries.ENTITY_TYPE.getOptional(ResourceLocation.parse(id));
            if (type.isPresent()) return type.get();
        }
        return null;
    }

    @Override
    public InteractionResult useOn(UseOnContext ctx) {
        Level level = ctx.getLevel();
        if (!(level instanceof ServerLevel server)) return InteractionResult.SUCCESS;
        Player player = ctx.getPlayer();
        EntityType<?> type = entityType();
        if (type == null) {
            if (player != null) player.displayClientMessage(Component.translatable("item.zerog_tweaks.spawn_egg.not_ready", getDescription()), true);
            return InteractionResult.FAIL;
        }
        BlockPos pos = ctx.getClickedPos();
        Direction face = ctx.getClickedFace();
        BlockState state = level.getBlockState(pos);
        BlockPos at = state.getCollisionShape(level, pos).isEmpty() ? pos : pos.relative(face);
        ItemStack stack = ctx.getItemInHand();
        Entity spawned = type.spawn(server, stack, player, at, MobSpawnType.SPAWN_EGG, true, !Objects.equals(pos, at) && face == Direction.UP);
        if (spawned != null) {
            stack.consume(1, player);
            level.gameEvent(player, GameEvent.ENTITY_PLACE, pos);
        }
        return InteractionResult.CONSUME;
    }
}
