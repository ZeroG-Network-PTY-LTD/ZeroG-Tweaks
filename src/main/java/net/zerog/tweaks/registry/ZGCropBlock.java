package net.zerog.tweaks.registry;

import net.minecraft.world.level.block.CropBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.item.ItemStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.LevelReader;

/** Base crop: age 0..3 (shipped blockstates). Subclasses bind their produce item. */
public abstract class ZGCropBlock extends CropBlock {
    /** Dormant-space growth is sixteen times slower than the same hydrated, lit crop. */
    public static final int DARK_GROWTH_FACTOR=16;
    public static final IntegerProperty AGE = IntegerProperty.create("age", 0, 3);
    public ZGCropBlock(Properties props) { super(props); }
    @Override public int getMaxAge() { return 3; }
    @Override public IntegerProperty getAgeProperty() { return AGE; }
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) { b.add(AGE); }
    public abstract ItemStack produce();
    @Override protected boolean canSurvive(BlockState state,LevelReader level,BlockPos pos){
        var below=pos.below();var soil=level.getBlockState(below);
        var decision=soil.canSustainPlant(level,below,Direction.UP,state);
        return decision.isDefault()?mayPlaceOn(soil,level,below):decision.isTrue();
    }
    public static int darkGrowthChance(BlockState state,BlockGetter level,BlockPos pos){
        return ((int)(25F/getGrowthSpeed(state,level,pos))+1)*DARK_GROWTH_FACTOR;
    }
    @Override protected void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource random){
        if(!level.isAreaLoaded(pos,1))return;
        if(level.getRawBrightness(pos,0)>=9){super.randomTick(state,level,pos,random);return;}
        if(!state.canSurvive(level,pos)||isMaxAge(state))return;
        if(net.neoforged.neoforge.common.CommonHooks.canCropGrow(level,pos,state,random.nextInt(darkGrowthChance(state,level,pos))==0)){
            level.setBlock(pos,getStateForAge(getAge(state)+1),2);
            net.neoforged.neoforge.common.CommonHooks.fireCropGrowPost(level,pos,state);
        }
    }
}
