package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.zerog.tweaks.registry.BlockEntityInit;

/** Outpost foundation; residents are created only by the server tick. */
public final class SettlementAnchorBlock extends Block implements EntityBlock {
    public SettlementAnchorBlock(Properties properties) { super(properties); }
    @Override public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {return new SettlementAnchorBlockEntity(pos,state);}
    @Override public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level,BlockState state,BlockEntityType<T> type) {
        if(level.isClientSide || type != BlockEntityInit.SETTLEMENT_ANCHOR.get()) return null;
        return (world,pos,block,be) -> SettlementAnchorBlockEntity.tick(world,pos,block,(SettlementAnchorBlockEntity)be);
    }
}
