package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.DripstoneThickness;
import net.minecraft.world.level.material.Fluids;

/** Native shape, placement, waterlogging and injury; own-family support chains.
 * Decorative mineral formations do not run vanilla's hard-coded dripstone growth
 * or cauldron conversion, which would silently create vanilla blocks.
 */
public class AlienDripstone extends PointedDripstoneBlock {
    public AlienDripstone(Properties p) {super(p);}
    @Override protected boolean canSurvive(BlockState s,LevelReader level,BlockPos pos) {
        var direction=s.getValue(TIP_DIRECTION);var support=pos.relative(direction.getOpposite());var state=level.getBlockState(support);
        return state.isFaceSturdy(level,support,direction) || state.is(this)&&state.getValue(TIP_DIRECTION)==direction;
    }
    @Override protected BlockState updateShape(BlockState s,Direction side,BlockState neighbour,LevelAccessor level,BlockPos pos,BlockPos other) {
        if(s.getValue(WATERLOGGED)) level.scheduleTick(pos,Fluids.WATER,Fluids.WATER.getTickDelay(level));
        if(!canSurvive(s,level,pos)) level.scheduleTick(pos,this,1);
        var dir=s.getValue(TIP_DIRECTION);var ahead=level.getBlockState(pos.relative(dir));var behind=level.getBlockState(pos.relative(dir.getOpposite()));
        boolean next=ahead.is(this)&&ahead.getValue(TIP_DIRECTION)==dir;
        var thickness=!next?DripstoneThickness.TIP:ahead.getValue(THICKNESS)==DripstoneThickness.TIP?DripstoneThickness.FRUSTUM:
                behind.is(this)?DripstoneThickness.MIDDLE:DripstoneThickness.BASE;
        return s.setValue(THICKNESS,thickness);
    }
    @Override protected void tick(BlockState s,ServerLevel level,BlockPos pos,RandomSource random) {if(!canSurvive(s,level,pos)) level.destroyBlock(pos,true);}
    @Override protected void randomTick(BlockState s,ServerLevel level,BlockPos pos,RandomSource random) {}
    @Override public void animateTick(BlockState s,Level level,BlockPos pos,RandomSource random) {}
}
