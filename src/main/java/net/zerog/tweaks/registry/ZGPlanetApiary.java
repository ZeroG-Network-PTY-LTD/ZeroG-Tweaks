package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.BeehiveBlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.BlockEntityTypeAddBlocksEvent;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.*;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.level.material.FlowingFluid;

/** Vanilla bee AI and hive storage, with hive-specific products. Not a replacement for Productive Bees. */
public final class ZGPlanetApiary {
    public static final Map<String,Family> FAMILIES=new LinkedHashMap<>();
    public static final class Family {
        public final String id;
        public DeferredBlock<PlanetHive> hive;
        public DeferredItem<Item> comb;
        public DeferredItem<HoneyBottleItem> bottle;
        public DeferredHolder<FluidType,FluidType> type;
        public DeferredHolder<Fluid,FlowingFluid> source,flowing;
        public DeferredBlock<LiquidBlock> liquid;
        public DeferredItem<BucketItem> bucket;
        private Family(String id){this.id=id;}
    }
    public static void init(IEventBus bus){
        for(String key:ZGGlowbugs.HOMES.keySet()){
            Family f=new Family(key); FAMILIES.put(key,f);
            f.comb=ItemInit.ITEMS.register(key+"_honeycomb",()->new Item(new Item.Properties()));
            f.bottle=ItemInit.ITEMS.register(key+"_honey_bottle",()->new HoneyBottleItem(new Item.Properties()
                    .food(net.minecraft.world.food.Foods.HONEY_BOTTLE).stacksTo(16).craftRemainder(Items.GLASS_BOTTLE)));
            f.hive=BlockInit.BLOCKS.register(key+"_hive",()->new PlanetHive(key,Block.Properties.ofFullCopy(Blocks.BEEHIVE)));
            ItemInit.ITEMS.registerSimpleBlockItem(key+"_hive",f.hive);
            f.type=ZGFluids.TYPES.register(key+"_honey",()->new FluidType(FluidType.Properties.create()
                    .descriptionId("fluid_type.zerog_tweaks."+key+"_honey").density(1400).viscosity(6000)
                    .canConvertToSource(false).canHydrate(false).canSwim(true).canDrown(true).motionScale(.004)));
            java.util.function.Supplier<BaseFlowingFluid.Properties> properties=()->new BaseFlowingFluid.Properties(f.type,f.source,f.flowing)
                    .block(f.liquid).bucket(f.bucket).tickRate(30).slopeFindDistance(2).levelDecreasePerBlock(2);
            f.source=ZGFluids.FLUIDS.register(key+"_honey",()->new BaseFlowingFluid.Source(properties.get()));
            f.flowing=ZGFluids.FLUIDS.register("flowing_"+key+"_honey",()->new BaseFlowingFluid.Flowing(properties.get()));
            f.liquid=BlockInit.BLOCKS.register(key+"_honey",()->new LiquidBlock(f.source.get(),Block.Properties.ofFullCopy(Blocks.WATER)));
            f.bucket=ItemInit.ITEMS.register(key+"_honey_bucket",()->new BucketItem(f.source.get(),new Item.Properties().stacksTo(1).craftRemainder(Items.BUCKET)));
        }
        bus.addListener(BlockEntityTypeAddBlocksEvent.class,event->FAMILIES.values().forEach(f->event.modify(BlockEntityType.BEEHIVE,f.hive.get())));
    }
    public static final class PlanetHive extends BeehiveBlock {
        public final String variant;
        PlanetHive(String variant,Properties properties){super(properties);this.variant=variant;}
        @Override protected ItemInteractionResult useItemOn(ItemStack stack,BlockState state,Level level,BlockPos pos,Player player,InteractionHand hand,BlockHitResult hit){
            if(state.getValue(HONEY_LEVEL)<5) return super.useItemOn(stack,state,level,pos,player,hand,hit);
            boolean shears=stack.canPerformAction(net.neoforged.neoforge.common.ItemAbilities.SHEARS_HARVEST);
            if(!shears&&!stack.is(Items.GLASS_BOTTLE)&&!stack.is(Items.BUCKET)) return super.useItemOn(stack,state,level,pos,player,hand,hit);
            if(!level.isClientSide){
                Family f=FAMILIES.get(variant);
                if(shears){popResource(level,pos,new ItemStack(f.comb.get(),3));stack.hurtAndBreak(1,player,LivingEntity.getSlotForHand(hand));}
                else{
                    ItemStack result=new ItemStack(stack.is(Items.BUCKET)?f.bucket.get():f.bottle.get());
                    player.setItemInHand(hand,ItemUtils.createFilledResult(stack,player,result));
                }
                level.playSound(null,pos,shears?net.minecraft.sounds.SoundEvents.BEEHIVE_SHEAR:net.minecraft.sounds.SoundEvents.BOTTLE_FILL,net.minecraft.sounds.SoundSource.BLOCKS,1,1);
                if(CampfireBlock.isSmokeyPos(level,pos)) resetHoneyLevel(level,state,pos);
                else{
                    for(var bee:level.getEntitiesOfClass(net.minecraft.world.entity.animal.Bee.class,new net.minecraft.world.phys.AABB(pos).inflate(8,6,8))) if(bee.getTarget()==null) bee.setTarget(player);
                    releaseBeesAndResetHoneyLevel(level,state,pos,player,BeehiveBlockEntity.BeeReleaseStatus.EMERGENCY);
                }
            }
            return ItemInteractionResult.sidedSuccess(level.isClientSide);
        }
    }
    private ZGPlanetApiary(){}
}
