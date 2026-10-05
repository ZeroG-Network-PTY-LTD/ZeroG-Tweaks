package net.zerog.tweaks.transport;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.network.chat.Component;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

@EventBusSubscriber(modid="zerog_tweaks")
public final class TransportInteraction {
    @SubscribeEvent public static void open(PlayerInteractEvent.RightClickBlock event){
        if(event.getHand()!=InteractionHand.MAIN_HAND)return;
        // Generator blocks own their dedicated fuel/power menu; never intercept them as transport.
        var be=event.getLevel().getBlockEntity(event.getPos());if(!(be instanceof TransportBlockEntity))return;
        if(be instanceof TransportBlockEntity t&&!event.getItemStack().isEmpty()){
            var stack=event.getItemStack();boolean handled=false;
            if(stack.getItem() instanceof net.minecraft.world.item.DyeItem dye){handled=true;if(event.getLevel() instanceof net.minecraft.server.level.ServerLevel level){t.colour=dye.getDyeColor().getId();t.setChanged();level.invalidateCapabilities(event.getPos());if(!event.getEntity().getAbilities().instabuild)stack.shrink(1);}}
            else if(stack.is(net.minecraft.world.item.Items.POTION)&&stack.getOrDefault(net.minecraft.core.component.DataComponents.POTION_CONTENTS,net.minecraft.world.item.alchemy.PotionContents.EMPTY).is(net.minecraft.world.item.alchemy.Potions.WATER)){handled=true;if(!event.getLevel().isClientSide){t.colour=-1;t.setChanged();if(!event.getEntity().getAbilities().instabuild){stack.shrink(1);var bottle=new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.GLASS_BOTTLE);if(!event.getEntity().addItem(bottle))event.getEntity().drop(bottle,false);}}}
            else if(stack.getItem() instanceof net.minecraft.world.item.BlockItem item&&item.getBlock() instanceof TransportBlock replacement&&replacement.family.equals(t.block().family)&&replacement.tier>t.block().tier){handled=true;if(event.getLevel() instanceof net.minecraft.server.level.ServerLevel level){var old=upgrade(level,event.getPos(),replacement);if(!old.isEmpty()&&!event.getEntity().getAbilities().instabuild){stack.shrink(1);if(!event.getEntity().addItem(old))event.getEntity().drop(old,false);}}}
            if(handled){event.setCanceled(true);event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));}return;
        }
        if(!event.getItemStack().isEmpty())return;
        if(event.getEntity() instanceof ServerPlayer player)player.openMenu(new SimpleMenuProvider((id,inv,p)->new TransportMenu(id,inv,be),Component.literal("Transport Controls")),buf->buf.writeBlockPos(event.getPos()));
        event.setCanceled(true);event.setCancellationResult(InteractionResult.sidedSuccess(event.getLevel().isClientSide));
    }
    /** Upgrade transaction: new node owns the old saved state, never duplicate loose contents. */
    public static net.minecraft.world.item.ItemStack upgrade(net.minecraft.server.level.ServerLevel level,net.minecraft.core.BlockPos pos,TransportBlock replacement){if(!(level.getBlockEntity(pos) instanceof TransportBlockEntity old)||!replacement.family.equals(old.block().family)||replacement.tier<=old.block().tier)return net.minecraft.world.item.ItemStack.EMPTY;var tag=old.saveWithFullMetadata(level.registryAccess());var refund=new net.minecraft.world.item.ItemStack(old.block());for(int i=0;i<9;i++)old.items.setStackInSlot(i,net.minecraft.world.item.ItemStack.EMPTY);old.tank.setFluid(net.neoforged.neoforge.fluids.FluidStack.EMPTY);old.stored=0;if(!level.setBlock(pos,replacement.defaultBlockState(),3)){old.loadWithComponents(tag,level.registryAccess());return net.minecraft.world.item.ItemStack.EMPTY;}if(!(level.getBlockEntity(pos) instanceof TransportBlockEntity next))throw new IllegalStateException("Transport upgrade must create its registered block entity");next.loadWithComponents(tag,level.registryAccess());next.setChanged();level.invalidateCapabilities(pos);return refund;}
    private TransportInteraction(){}
}
