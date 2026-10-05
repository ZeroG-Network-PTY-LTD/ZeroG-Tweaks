package net.zerog.tweaks.storage;

import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.fluids.FluidUtil;

@EventBusSubscriber(modid="zerog_tweaks")
public final class StorageTankInteraction {
    @SubscribeEvent public static void use(PlayerInteractEvent.RightClickBlock event){if(event.getHand()!=InteractionHand.MAIN_HAND||!(event.getLevel().getBlockEntity(event.getPos()) instanceof StorageTankBlockEntity be))return;var stack=event.getItemStack();var player=event.getEntity();
        boolean client=event.getLevel().isClientSide;InteractionResult result=InteractionResult.sidedSuccess(client);
        if(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem()).toString().equals("zerog_tweaks:flux_wrench")){if(!client){if(player.isShiftKeyDown()){var saved=StorageTankBlock.contentsItem(be);be.tank.setFluid(net.neoforged.neoforge.fluids.FluidStack.EMPTY);event.getLevel().removeBlock(event.getPos(),false);if(!player.addItem(saved))player.drop(saved,false);}else be.cycle(event.getFace());}}
        else if(stack.getItem() instanceof BlockItem item&&item.getBlock() instanceof StorageTankBlock replacement){if(!client){if(stack.has(DataComponents.BLOCK_ENTITY_DATA))result=InteractionResult.FAIL;else{var refund=upgrade((ServerLevel)event.getLevel(),event.getPos(),replacement);if(refund.isEmpty())result=InteractionResult.FAIL;else if(!player.getAbilities().instabuild){stack.shrink(1);if(!player.addItem(refund))player.drop(refund,false);}}}}
        else if(FluidUtil.getFluidHandler(stack).isPresent()){if(!client&&!FluidUtil.interactWithFluidHandler(player,event.getHand(),event.getLevel(),event.getPos(),event.getFace()))result=InteractionResult.FAIL;}
        else if(stack.isEmpty()&&!player.isShiftKeyDown()){if(player instanceof ServerPlayer server)server.openMenu(new SimpleMenuProvider((id,inv,p)->new StorageTankMenu(id,inv,be),Component.literal("Fluid Storage Tank")),buf->buf.writeBlockPos(be.getBlockPos()));}
        else return;event.setCanceled(true);event.setCancellationResult(result);
    }
    /** Only an empty new shell is consumed; the old shell refund never carries fluid. */
    public static ItemStack upgrade(ServerLevel level,BlockPos pos,StorageTankBlock replacement){if(!(level.getBlockEntity(pos) instanceof StorageTankBlockEntity old)||replacement.tier<=((StorageTankBlock)old.getBlockState().getBlock()).tier)return ItemStack.EMPTY;var saved=old.saveWithFullMetadata(level.registryAccess());var refund=new ItemStack(old.getBlockState().getBlock());var facing=old.getBlockState().getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING);if(!level.setBlock(pos,replacement.defaultBlockState().setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,facing),3))return ItemStack.EMPTY;var next=(StorageTankBlockEntity)level.getBlockEntity(pos);if(next==null)throw new IllegalStateException("Tank upgrade did not create its block entity");next.loadWithComponents(saved,level.registryAccess());next.changed();level.invalidateCapabilities(pos);return refund;}
    private StorageTankInteraction(){}
}
