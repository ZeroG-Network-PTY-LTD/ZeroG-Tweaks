package net.zerog.tweaks.travel;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;

/** Gate pylon. Controller sets powered-idle/launch LIT; client renders pillar-top beam lamps. */
public final class GatePylonBlock extends Block {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;
    public GatePylonBlock(Properties properties){super(properties);registerDefaultState(defaultBlockState().setValue(LIT,false));}
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> builder){builder.add(LIT);}
}
