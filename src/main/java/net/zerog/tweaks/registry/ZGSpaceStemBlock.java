package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.StemBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;

/** Vanilla gourd mechanics when lit; slow growth and fruit setting in darkness. */
public final class ZGSpaceStemBlock extends StemBlock {
    private final ResourceKey<Block> fruit,attached;
    public ZGSpaceStemBlock(ResourceKey<Block> fruit,ResourceKey<Block> attached,ResourceKey<Item> seed,BlockBehaviour.Properties properties){
        super(fruit,attached,seed,properties);this.fruit=fruit;this.attached=attached;
    }
    @Override protected void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource random){
        if(!level.isAreaLoaded(pos,1))return;
        if(level.getRawBrightness(pos,0)>=9){super.randomTick(state,level,pos,random);return;}
        if(!state.canSurvive(level,pos))return;
        if(!net.neoforged.neoforge.common.CommonHooks.canCropGrow(level,pos,state,random.nextInt(ZGCropBlock.darkGrowthChance(state,level,pos))==0))return;
        int age=state.getValue(AGE);
        if(age<7)level.setBlock(pos,state.setValue(AGE,age+1),2);
        else{
            var direction=Direction.Plane.HORIZONTAL.getRandomDirection(random);var at=pos.relative(direction);var soil=level.getBlockState(at.below());
            if(level.isEmptyBlock(at)&&(soil.getBlock() instanceof FarmBlock||soil.is(BlockTags.DIRT))){
                var registry=level.registryAccess().registryOrThrow(Registries.BLOCK);var fruitBlock=registry.getOptional(fruit);var attachedBlock=registry.getOptional(attached);
                if(fruitBlock.isPresent()&&attachedBlock.isPresent()){
                    level.setBlockAndUpdate(at,fruitBlock.get().defaultBlockState());
                    level.setBlockAndUpdate(pos,attachedBlock.get().defaultBlockState().setValue(HorizontalDirectionalBlock.FACING,direction));
                }
            }
        }
        net.neoforged.neoforge.common.CommonHooks.fireCropGrowPost(level,pos,state);
    }
}
