package net.zerog.tweaks.arena;

import net.minecraft.util.StringRepresentable;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;

/**
 * Concord Prism: the altar at the centre of the Prism Sentinel arena (briefs/prism_sentinel_arena.md, section 5).
 * Unbreakable in survival and drops nothing. Its state is IDLE -> ACTIVE (fight running) -> DEFEATED (glowing, inert);
 * a DEFEATED prism re-arms with a Sentinel Prism for a rematch. The fight wiring arrives with the Sentinel entity.
 */
public class ConcordPrismBlock extends Block {
    public enum State implements StringRepresentable {
        IDLE("idle"), ACTIVE("active"), DEFEATED("defeated");

        private final String name;
        State(String name) { this.name = name; }
        @Override public String getSerializedName() { return name; }
    }

    public static final EnumProperty<State> STATE = EnumProperty.create("state", State.class);

    public ConcordPrismBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(STATE, State.IDLE));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(STATE);
    }

    /** Light level per state, for Properties.lightLevel. */
    public static int light(BlockState state) {
        return switch (state.getValue(STATE)) {
            case IDLE -> 10;
            case ACTIVE -> 13;
            case DEFEATED -> 15;
        };
    }
}
