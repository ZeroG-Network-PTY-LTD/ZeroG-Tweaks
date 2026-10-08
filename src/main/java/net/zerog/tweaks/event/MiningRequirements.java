package net.zerog.tweaks.event;

import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

/** Read loaded mining tags; never maintain a second, conflicting ore ladder. */
@EventBusSubscriber(modid="zerog_tweaks")
public final class MiningRequirements {
    public static Component requirement(BlockState state) {
        if (!state.requiresCorrectToolForDrops()) return Component.empty();
        var required=state.getTags().map(tag->tag.location()).filter(id->
            id.getNamespace().equals("zerog_tweaks") && id.getPath().startsWith("needs_")
                && id.getPath().endsWith("_tool")).sorted().findFirst();
        if(required.isPresent()) {
            String path=required.get().getPath();
            String material=path.substring(6,path.length()-5);
            var id=net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                material.equals("netherite")?"minecraft":"zerog_tweaks",material+"_pickaxe");
            if(BuiltInRegistries.ITEM.containsKey(id))return Component.literal("Requires: ")
                .append(BuiltInRegistries.ITEM.get(id).getDescription()).append(" or better");
        }
        String tier=state.is(BlockTags.NEEDS_DIAMOND_TOOL)?"Diamond":state.is(BlockTags.NEEDS_IRON_TOOL)?"Iron":state.is(BlockTags.NEEDS_STONE_TOOL)?"Stone":"";
        String tool=state.is(BlockTags.MINEABLE_WITH_PICKAXE)?"pickaxe":state.is(BlockTags.MINEABLE_WITH_AXE)?"axe":state.is(BlockTags.MINEABLE_WITH_SHOVEL)?"shovel":state.is(BlockTags.MINEABLE_WITH_HOE)?"hoe":"correct tool";
        return Component.literal("Requires: "+(tier.isEmpty()?"":tier+" ")+tool+(tier.isEmpty()?"":" or better"));
    }
    @SubscribeEvent public static void tooltip(ItemTooltipEvent event) {
        if(event.getItemStack().getItem() instanceof BlockItem item
            && BuiltInRegistries.BLOCK.getKey(item.getBlock()).getNamespace().equals("zerog_tweaks")) {
            var line=requirement(item.getBlock().defaultBlockState());
            if(!line.getString().isEmpty())event.getToolTip().add(line.copy().withStyle(ChatFormatting.GRAY));
        }
    }
    @SubscribeEvent public static void mining(PlayerInteractEvent.LeftClickBlock event) {
        if(!event.getLevel().isClientSide || event.getEntity().isCreative() || event.getEntity().isSpectator())return;
        var state=event.getLevel().getBlockState(event.getPos());
        if(!BuiltInRegistries.BLOCK.getKey(state.getBlock()).getNamespace().equals("zerog_tweaks")
            || event.getEntity().hasCorrectToolForDrops(state))return;
        var line=requirement(state);
        if(!line.getString().isEmpty())event.getEntity().displayClientMessage(line.copy().withStyle(ChatFormatting.RED),true);
    }
    private MiningRequirements(){}
}
