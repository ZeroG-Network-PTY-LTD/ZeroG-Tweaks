package net.zerog.tweaks.travel;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;

/** Gate pylon. LIT is set column by column by SurvivalGateBlockEntity during a launch; it only adds light. */
public final class GatePylonBlock extends Block {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;
    public GatePylonBlock(Properties properties){super(properties);registerDefaultState(defaultBlockState().setValue(LIT,false));}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> builder){builder.add(LIT);}
}
