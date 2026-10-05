package net.zerog.tweaks.storage;

import com.mojang.serialization.MapCodec;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;

public final class StorageTankBlock extends BaseEntityBlock {
    public static final IntegerProperty LEVEL=IntegerProperty.create("level",0,8);
    public final int tier;
    public StorageTankBlock(Properties props,int tier){super(props);this.tier=tier;registerDefaultState(stateDefinition.any().setValue(BlockStateProperties.HORIZONTAL_FACING,net.minecraft.core.Direction.NORTH).setValue(LEVEL,0));}
    @Override protected MapCodec<? extends BaseEntityBlock> codec(){return simpleCodec(p->new StorageTankBlock(p,0));}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<net.minecraft.world.level.block.Block,BlockState> builder){builder.add(BlockStateProperties.HORIZONTAL_FACING,LEVEL);}
    @Override public BlockState getStateForPlacement(BlockPlaceContext context){return defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,context.getHorizontalDirection().getOpposite());}
    @Override protected RenderShape getRenderShape(BlockState state){return RenderShape.MODEL;}
    @Override public BlockEntity newBlockEntity(BlockPos pos,BlockState state){return new StorageTankBlockEntity(pos,state);}
    public static ItemStack contentsItem(StorageTankBlockEntity be){var item=new ItemStack(be.getBlockState().getBlock());item.set(DataComponents.BLOCK_ENTITY_DATA,CustomData.of(be.saveWithFullMetadata(be.getLevel().registryAccess())));return item;}
    @Override protected List<ItemStack> getDrops(BlockState state,LootParams.Builder builder){var entity=builder.getOptionalParameter(LootContextParams.BLOCK_ENTITY);return List.of(entity instanceof StorageTankBlockEntity be?contentsItem(be):new ItemStack(this));}
    @Override public BlockState playerWillDestroy(Level level,BlockPos pos,BlockState state,Player player){if(!level.isClientSide&&player.getAbilities().instabuild&&level.getBlockEntity(pos) instanceof StorageTankBlockEntity be&&!be.tank.isEmpty())popResource(level,pos,contentsItem(be));return super.playerWillDestroy(level,pos,state,player);}
}
