package net.zerog.tweaks.item;

import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.zerog.tweaks.config.ZGProgressionConfig;
import net.zerog.tweaks.travel.PlanetTestHub;
import net.zerog.tweaks.travel.SurvivalGateBlockEntity;
import net.zerog.tweaks.travel.SurvivalGateLayout;

/** Deliberately requires a bound, owned, intact, charged survival gate. */
public final class RecallAnchorItem extends Item {
    private final boolean group;
    public RecallAnchorItem(Properties properties,boolean group){super(properties);this.group=group;}
    @Override public InteractionResult useOn(UseOnContext context){
        if(context.getPlayer() instanceof ServerPlayer p&&context.getLevel().getBlockEntity(context.getClickedPos()) instanceof SurvivalGateBlockEntity gate){
            if(!gate.mayControl(p)||gate.formedTier()==0||gate.returnPlatform)return InteractionResult.FAIL;
            CompoundTag tag=context.getItemInHand().getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();
            tag.putString("homeDimension",p.level().dimension().location().toString());tag.putLong("homeController",context.getClickedPos().asLong());
            context.getItemInHand().set(DataComponents.CUSTOM_DATA,CustomData.of(tag));p.displayClientMessage(Component.literal("Anchor bound to this home gate."),false);return InteractionResult.SUCCESS;
        }return InteractionResult.PASS;
    }
    @Override public InteractionResultHolder<ItemStack> use(Level level,Player user,InteractionHand hand){
        ItemStack stack=user.getItemInHand(hand);if(!(user instanceof ServerPlayer player))return InteractionResultHolder.pass(stack);
        CompoundTag tag=stack.getOrDefault(DataComponents.CUSTOM_DATA,CustomData.EMPTY).copyTag();
        long now=player.getServer().overworld().getGameTime();
        if(tag.getString("homeDimension").isEmpty()||player.getPersistentData().getLong("zerog_recall_until")>now)return InteractionResultHolder.fail(stack);
        var home=PlanetTestHub.planet(player.getServer(),tag.getString("homeDimension"));if(home==null)return InteractionResultHolder.fail(stack);
        BlockPos at=BlockPos.of(tag.getLong("homeController"));home.getChunkAt(at);
        if(!(home.getBlockEntity(at) instanceof SurvivalGateBlockEntity gate)||!gate.mayControl(player))return InteractionResultHolder.fail(stack);
        SurvivalGateLayout.loadFootprint(home,at,gate.facing());
        if(gate.formedTier()==0)return InteractionResultHolder.fail(stack);
        var passengers=group?player.serverLevel().getEntitiesOfClass(ServerPlayer.class,player.getBoundingBox().inflate(8),p->p==player||player.getTeam()!=null&&player.isAlliedTo(p)):List.of(player);
        if(passengers.size()>SurvivalGateLayout.passengers(gate.formedTier()))return InteractionResultHolder.fail(stack);
        int fee=(int)Math.ceil(SurvivalGateLayout.cost(ZGProgressionConfig.baseCost(gate.formedTier()),player.level().dimension().location().toString(),home.dimension().location().toString(),passengers.size(),gate.has("refracting_lens"))*1.5);
        if(gate.stored<fee){player.displayClientMessage(Component.literal("Recall needs "+fee+" FE at the home gate."),false);return InteractionResultHolder.fail(stack);}
        gate.stored-=fee;gate.setChanged();
        for(ServerPlayer p:passengers){p.getPersistentData().putLong("zerog_recall_until",now+ZGProgressionConfig.RECALL_COOLDOWN.get());net.zerog.tweaks.travel.GateLaunchSync.sendDestination(p,home);p.changeDimension(SurvivalGateBlockEntity.transition(home,gate.centre()));}
        return InteractionResultHolder.success(stack);
    }
    @Override public void appendHoverText(ItemStack stack,TooltipContext context,List<Component> tooltip,TooltipFlag flag){tooltip.add(Component.literal("Bind to your home controller. Recall costs 150% of normal travel FE."));if(group)tooltip.add(Component.literal("Recalls nearby scoreboard teammates within 8 blocks."));}
}
