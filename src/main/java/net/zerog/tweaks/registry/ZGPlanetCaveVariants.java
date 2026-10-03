package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.registries.DeferredBlock;

/** All 34 destinations get stable berry/vine/dripstone identities. */
public final class ZGPlanetCaveVariants {
    public record Family(DeferredBlock<Head> head,DeferredBlock<Body> body,DeferredBlock<AlienDripstone> point,DeferredBlock<Block> rock) {}
    public static final Map<String,Family> FAMILIES=new LinkedHashMap<>();
    public static class Head extends ZGCaveVinesBlock {
        private final String id;
        Head(Properties p,String id) {super(p);this.id=id;}
        @Override protected Block getBodyBlock() {return FAMILIES.get(id).body.get();}
        @Override public ItemStack getCloneItemStack(LevelReader l,BlockPos p,BlockState s) {return berry(id);}
        @Override protected InteractionResult useWithoutItem(BlockState s,Level l,BlockPos p,Player player,BlockHitResult hit) {return pick(id,s,l,p,player);}
    }
    public static class Body extends ZGCaveVinesPlantBlock {
        private final String id;
        Body(Properties p,String id) {super(p);this.id=id;}
        @Override protected GrowingPlantHeadBlock getHeadBlock() {return FAMILIES.get(id).head.get();}
        @Override public ItemStack getCloneItemStack(LevelReader l,BlockPos p,BlockState s) {return berry(id);}
        @Override protected InteractionResult useWithoutItem(BlockState s,Level l,BlockPos p,Player player,BlockHitResult hit) {return pick(id,s,l,p,player);}
    }
    public static ItemStack berry(String id) {return new ItemStack(net.minecraft.core.registries.BuiltInRegistries.ITEM.get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id+"_cave_berry")));}
    public static InteractionResult pick(String id,BlockState state,Level level,BlockPos pos,Player player) {
        if(!state.getValue(CaveVines.BERRIES)) return InteractionResult.PASS;
        if(!level.isClientSide) {
            Block.popResource(level,pos,berry(id));
            level.setBlock(pos,state.setValue(CaveVines.BERRIES,false),3);
            level.playSound(null,pos,net.minecraft.sounds.SoundEvents.CAVE_VINES_PICK_BERRIES,net.minecraft.sounds.SoundSource.BLOCKS,1,1);
            level.gameEvent(net.minecraft.world.level.gameevent.GameEvent.BLOCK_CHANGE,pos,net.minecraft.world.level.gameevent.GameEvent.Context.of(player,state));
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
    public static void init() {
        // The soil DeferredBlocks are populated later by BlockInit.register;
        // the stable dimension catalogue is available before that lifecycle.
        for(String id:ZGDimensionTerrain.dimensions()) {
            var head=BlockInit.BLOCKS.register(id+"_cave_vines",()->new Head(BlockBehaviour.Properties.ofFullCopy(Blocks.CAVE_VINES),id));
            var body=BlockInit.BLOCKS.register(id+"_cave_vines_plant",()->new Body(BlockBehaviour.Properties.ofFullCopy(Blocks.CAVE_VINES_PLANT),id));
            var point=BlockInit.BLOCKS.register(id+"_pointed_dripstone",()->new AlienDripstone(BlockBehaviour.Properties.ofFullCopy(Blocks.POINTED_DRIPSTONE).noOcclusion()));
            var rock=BlockInit.BLOCKS.registerSimpleBlock(id+"_dripstone_block",BlockBehaviour.Properties.ofFullCopy(Blocks.DRIPSTONE_BLOCK));
            FAMILIES.put(id,new Family(head,body,point,rock));
            ItemInit.ITEMS.register(id+"_cave_berry",()->new ItemNameBlockItem(head.get(),new Item.Properties().food(new FoodProperties.Builder().nutrition(2).saturationModifier(.15F).build())));
            ItemInit.ITEMS.registerSimpleBlockItem(id+"_pointed_dripstone",point);
            ItemInit.ITEMS.registerSimpleBlockItem(id+"_dripstone_block",rock);
        }
    }
    private ZGPlanetCaveVariants() {}
}
