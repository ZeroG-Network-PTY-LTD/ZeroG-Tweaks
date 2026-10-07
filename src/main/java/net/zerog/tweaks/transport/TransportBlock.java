package net.zerog.tweaks.transport;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;

public class TransportBlock extends BaseEntityBlock {
    public enum Connection implements net.minecraft.util.StringRepresentable {NONE,PIPE,NORMAL,PUSH,PULL;public String getSerializedName(){return name().toLowerCase(java.util.Locale.ROOT);}}
    public enum PortMode implements net.minecraft.util.StringRepresentable {INPUT,OUTPUT,BOTH;public String getSerializedName(){return name().toLowerCase(java.util.Locale.ROOT);}}
    public static final java.util.Map<net.minecraft.core.Direction,net.minecraft.world.level.block.state.properties.EnumProperty<Connection>> SIDES=new java.util.EnumMap<>(net.minecraft.core.Direction.class);
    public static final net.minecraft.world.level.block.state.properties.IntegerProperty GAUGE=net.minecraft.world.level.block.state.properties.IntegerProperty.create("level",0,8);
    public static final net.minecraft.world.level.block.state.properties.EnumProperty<PortMode> MODE=net.minecraft.world.level.block.state.properties.EnumProperty.create("mode",PortMode.class);
    static{for(var direction:net.minecraft.core.Direction.values())SIDES.put(direction,net.minecraft.world.level.block.state.properties.EnumProperty.create(direction.getName(),Connection.class));}
    public final String family;public final int tier;
    public TransportBlock(Properties props,String family,int tier){super(props);this.family=family;this.tier=tier;var state=stateDefinition.any();for(var property:SIDES.values())if(state.hasProperty(property))state=state.setValue(property,Connection.NONE);if(state.hasProperty(GAUGE))state=state.setValue(GAUGE,0);if(state.hasProperty(MODE))state=state.setValue(MODE,PortMode.BOTH);if(state.hasProperty(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING))state=state.setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,net.minecraft.core.Direction.NORTH);registerDefaultState(state);}
    public static final class Wire extends TransportBlock {public Wire(Properties p,String f,int t){super(p,f,t);}@Override protected void createBlockStateDefinition(net.minecraft.world.level.block.state.StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> b){for(var prop:SIDES.values())b.add(prop);}}
    public static final class Cell extends TransportBlock {public Cell(Properties p,String f,int t){super(p,f,t);}@Override protected void createBlockStateDefinition(net.minecraft.world.level.block.state.StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> b){b.add(GAUGE,net.minecraft.world.level.block.state.properties.BlockStateProperties.FACING);}}
    public static final class Port extends TransportBlock {public Port(Properties p,String f,int t){super(p,f,t);}@Override protected void createBlockStateDefinition(net.minecraft.world.level.block.state.StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> b){b.add(MODE,net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING);}}
    @Override public BlockState getStateForPlacement(net.minecraft.world.item.context.BlockPlaceContext context){var state=defaultBlockState();if(state.hasProperty(net.minecraft.world.level.block.state.properties.BlockStateProperties.FACING))return state.setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.FACING,context.getClickedFace().getOpposite());return state.hasProperty(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING)?state.setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,context.getHorizontalDirection().getOpposite()):state;}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(p->new TransportBlock(p,"energy",0));}
    @Override protected RenderShape getRenderShape(BlockState state){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos pos,BlockState state){return new TransportBlockEntity(pos,state);}
    private static void invalidateAround(Level level,BlockPos pos){
        if(level.isClientSide)return;
        if(level.getBlockEntity(pos) instanceof TransportBlockEntity be)be.invalidateTopology();
        for(var side:net.minecraft.core.Direction.values()){
            var next=pos.relative(side);
            if(level.hasChunkAt(next)&&level.getBlockEntity(next) instanceof TransportBlockEntity be)be.invalidateTopology();
        }
    }
    @Override protected void onPlace(BlockState state,Level level,BlockPos pos,BlockState previous,boolean moving){
        super.onPlace(state,level,pos,previous,moving);
        if(!state.is(previous.getBlock()))invalidateAround(level,pos);
    }
    @Override protected void neighborChanged(BlockState state,Level level,BlockPos pos,net.minecraft.world.level.block.Block neighbor,BlockPos neighborPos,boolean moving){
        invalidateAround(level,pos);
        super.neighborChanged(state,level,pos,neighbor,neighborPos,moving);
    }
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type){return level.isClientSide?null:createTickerHelper(type,TransportRegistry.TYPE.get(),TransportBlockEntity::tick);}
    @Override protected void onRemove(BlockState state,Level level,BlockPos pos,BlockState next,boolean moving){
        if(!state.is(next.getBlock()))invalidateAround(level,pos);
        if(!state.is(next.getBlock())&&level.getBlockEntity(pos) instanceof TransportBlockEntity be){if(be.block().family.equals("null_link"))be.unlink();for(int i=0;i<be.items.getSlots();i++)net.minecraft.world.Containers.dropItemStack(level,pos.getX()+.5,pos.getY()+.5,pos.getZ()+.5,be.items.getStackInSlot(i));}
        super.onRemove(state,level,pos,next,moving);
    }
}
