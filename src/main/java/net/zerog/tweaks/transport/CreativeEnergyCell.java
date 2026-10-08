package net.zerog.tweaks.transport;

import net.minecraft.core.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.*;
import net.minecraft.world.item.*;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.energy.IEnergyStorage;

/** Admin source, not a rechargeable survival buffer. All faces share one quota. */
public final class CreativeEnergyCell extends Block implements EntityBlock {
    @net.neoforged.fml.common.EventBusSubscriber(modid="zerog_tweaks")
    public static final class PickupGuard {
        @net.neoforged.bus.api.SubscribeEvent public static void pickup(net.neoforged.neoforge.event.entity.player.ItemEntityPickupEvent.Pre e){
            if(!e.getPlayer().isCreative()&&e.getItemEntity().getItem().is(TransportRegistry.CREATIVE_CELL.get().asItem()))e.setCanPickup(net.neoforged.neoforge.common.util.TriState.FALSE);
        }
    }
    public CreativeEnergyCell(Properties p){super(p);}
    @Override public BlockEntity newBlockEntity(BlockPos p,BlockState s){return new Cell(p,s);}
    @Override public void setPlacedBy(Level l,BlockPos p,BlockState s,LivingEntity placer,ItemStack item){
        super.setPlacedBy(l,p,s,placer,item);
        if(!l.isClientSide&&l.getBlockEntity(p) instanceof Cell cell){cell.enabled=placer instanceof net.minecraft.world.entity.player.Player player&&player.isCreative();cell.setChanged();}
    }
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level l,BlockState s,BlockEntityType<T> type){return l.isClientSide?null:(world,p,state,be)->{if(be instanceof Cell cell)cell.tick();};}
    public static final class CreativeItem extends BlockItem {
        public CreativeItem(Block b,Item.Properties p){super(b,p);}
        @Override public InteractionResult place(BlockPlaceContext c){return c.getPlayer()!=null&&c.getPlayer().isCreative()?super.place(c):InteractionResult.FAIL;}
        @Override public void appendHoverText(ItemStack s,Item.TooltipContext c,java.util.List<net.minecraft.network.chat.Component> lines,TooltipFlag f){
            lines.add(net.minecraft.network.chat.Component.literal("ADMIN • Unlimited GFE • 300,000 FE/tick total"));
            lines.add(net.minecraft.network.chat.Component.literal("Creative placement only; all six faces share output limit."));
        }
    }
    public static final class Cell extends BlockEntity {
        public static final int RATE=300000;public boolean enabled;
        private long lastTick=Long.MIN_VALUE;private int used;
        public Cell(BlockPos p,BlockState s){super(TransportRegistry.CREATIVE_TYPE.get(),p,s);}
        private boolean active(){return enabled&&level!=null&&!level.isClientSide&&!isRemoved()&&level.getBlockEntity(worldPosition)==this;}
        public IEnergyStorage energy(){return new IEnergyStorage(){
            public int receiveEnergy(int n,boolean sim){return 0;}
            public int extractEnergy(int n,boolean sim){
                if(n<=0||!active())return 0;long tick=level.getGameTime();int spent=tick==lastTick?used:0;int out=Math.min(n,RATE-spent);
                if(!sim&&out>0){if(lastTick!=tick){lastTick=tick;used=0;}used+=out;}return out;
            }
            public int getEnergyStored(){return active()?Integer.MAX_VALUE:0;}
            public int getMaxEnergyStored(){return Integer.MAX_VALUE;}
            public boolean canExtract(){return active();}public boolean canReceive(){return false;}
        };}
        public void tick(){if(!active())return;var from=energy();for(var side:Direction.values()){
            var pos=worldPosition.relative(side);if(!level.hasChunkAt(pos))continue;
            var to=level.getCapability(Capabilities.EnergyStorage.BLOCK,pos,side.getOpposite());if(to==null||!to.canReceive())continue;
            int n=to.receiveEnergy(from.extractEnergy(RATE,true),true);if(n>0)to.receiveEnergy(from.extractEnergy(n,false),false);
        }}
        @Override protected void saveAdditional(CompoundTag t,HolderLookup.Provider r){super.saveAdditional(t,r);t.putBoolean("creativeEnabled",enabled);}
        @Override protected void loadAdditional(CompoundTag t,HolderLookup.Provider r){super.loadAdditional(t,r);enabled=t.getBoolean("creativeEnabled");}
    }
}
