package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.CaveVines;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;

/** Native climbing/support growth with six planet palettes. Venom is visual only. */
public final class ZGAlienVines {
    public static final List<String> KINDS=List.of("ivy","glow_ivy","venom_ivy","fruit_ivy");
    public static final Map<String,DeferredBlock<AlienVine>> VINES=new LinkedHashMap<>();
    public static final Map<String,DeferredItem<Item>> FRUITS=new LinkedHashMap<>();
    public static void init() {
        for(String theme:List.of("moon","mars","cerulon","skarn","eidolon","solvane")) {
            FRUITS.put(theme,ItemInit.ITEMS.register(theme+"_vine_fruit",()->new Item(new Item.Properties()
                    .food(new FoodProperties.Builder().nutrition(3).saturationModifier(.4F).build()))));
            for(String kind:KINDS) {
                String id=theme+"_"+kind;
                var block=BlockInit.BLOCKS.register(id,()->new AlienVine(theme,kind));
                VINES.put(id,block);ItemInit.ITEMS.registerSimpleBlockItem(id,block);
            }
        }
    }
    public static final class AlienVine extends ZGVineBlock implements BonemealableBlock {
        private final String theme,kind;
        AlienVine(String theme,String kind) {
            super(Block.Properties.ofFullCopy(Blocks.VINE).lightLevel(state->kind.equals("glow_ivy")?8:
                    kind.equals("venom_ivy")?6:kind.equals("fruit_ivy")&&state.getValue(CaveVines.BERRIES)?7:0));
            this.theme=theme;this.kind=kind;
            registerDefaultState(defaultBlockState().setValue(CaveVines.BERRIES,false));
        }
        @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block,BlockState> builder) {
            super.createBlockStateDefinition(builder);builder.add(CaveVines.BERRIES);
        }
        @Override protected void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource random) {
            super.randomTick(state,level,pos,random);
            if(kind.equals("fruit_ivy") && !state.getValue(CaveVines.BERRIES) && random.nextInt(8)==0
                    && level.getBlockState(pos).is(this))
                level.setBlock(pos,level.getBlockState(pos).setValue(CaveVines.BERRIES,true),2);
        }
        @Override protected InteractionResult useWithoutItem(BlockState state,Level level,BlockPos pos,Player player,BlockHitResult hit) {
            if(!kind.equals("fruit_ivy") || !state.getValue(CaveVines.BERRIES))return InteractionResult.PASS;
            if(!level.isClientSide()) {
                popResource(level,pos,new ItemStack(FRUITS.get(theme).get()));
                level.setBlock(pos,state.setValue(CaveVines.BERRIES,false),2);
            }
            return InteractionResult.sidedSuccess(level.isClientSide());
        }
        @Override public boolean isValidBonemealTarget(LevelReader level,BlockPos pos,BlockState state) {
            return kind.equals("fruit_ivy") && !state.getValue(CaveVines.BERRIES);
        }
        @Override public boolean isBonemealSuccess(Level level,RandomSource random,BlockPos pos,BlockState state) {return true;}
        @Override public void performBonemeal(ServerLevel level,RandomSource random,BlockPos pos,BlockState state) {
            level.setBlock(pos,state.setValue(CaveVines.BERRIES,true),2);
        }
    }
    private ZGAlienVines() {}
}
