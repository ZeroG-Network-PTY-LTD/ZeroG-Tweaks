package net.zerog.tweaks.registry;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HalfTransparentBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;

/** Animated cosmic glass; the nebula colour can be changed with vanilla dyes. */
public class ZGStarGlassBlock extends HalfTransparentBlock {
    public static final MapCodec<ZGStarGlassBlock> CODEC = simpleCodec(ZGStarGlassBlock::new);
    public enum Nebula implements StringRepresentable {
        PURPLE, BLUE, TEAL;
        @Override public String getSerializedName() { return name().toLowerCase(java.util.Locale.ROOT); }
    }
    public static final EnumProperty<Nebula> NEBULA = EnumProperty.create("nebula", Nebula.class);

    public ZGStarGlassBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(NEBULA, Nebula.PURPLE));
    }

    @Override public MapCodec<ZGStarGlassBlock> codec() { return CODEC; }
    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) { builder.add(NEBULA); }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos,
            Player player, InteractionHand hand, BlockHitResult hit) {
        if (!(stack.getItem() instanceof DyeItem dye) || !player.getAbilities().mayBuild)
            return super.useItemOn(stack, state, level, pos, player, hand, hit);
        Nebula colour = switch (dye.getDyeColor()) {
            case PURPLE, MAGENTA -> Nebula.PURPLE;
            case BLUE, LIGHT_BLUE -> Nebula.BLUE;
            case CYAN, GREEN -> Nebula.TEAL;
            default -> null;
        };
        if (colour == null || colour == state.getValue(NEBULA))
            return super.useItemOn(stack, state, level, pos, player, hand, hit);
        if (!level.isClientSide) {
            level.setBlockAndUpdate(pos, state.setValue(NEBULA, colour));
            if (!player.getAbilities().instabuild) stack.shrink(1);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }
}
