package net.zerog.tweaks.registry;

import java.util.Map;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.common.ItemAbilities;
import net.neoforged.neoforge.event.level.BlockEvent;
import net.zerog.tweaks.ZeroGTweaks;

/** Axe stripping for the ZeroG woods, like vanilla AxeItem.STRIPPABLES: log/wood to stripped, keeping the axis. */
@EventBusSubscriber(modid = ZeroGTweaks.MODID)
public final class ZGStripping {
    private static Map<Block, Block> strippables;

    private static Map<Block, Block> strippables() {
        if (strippables == null) strippables = Map.of(
                BlockInit.CHARWOOD_LOG.get(), BlockInit.STRIPPED_CHARWOOD_LOG.get(),
                BlockInit.CHARWOOD_WOOD.get(), BlockInit.STRIPPED_CHARWOOD_WOOD.get(),
                BlockInit.GILDWOOD_LOG.get(), BlockInit.STRIPPED_GILDWOOD_LOG.get(),
                BlockInit.GILDWOOD_WOOD.get(), BlockInit.STRIPPED_GILDWOOD_WOOD.get(),
                BlockInit.HOARWOOD_LOG.get(), BlockInit.STRIPPED_HOARWOOD_LOG.get(),
                BlockInit.HOARWOOD_WOOD.get(), BlockInit.STRIPPED_HOARWOOD_WOOD.get(),
                BlockInit.SHARDWOOD_LOG.get(), BlockInit.STRIPPED_SHARDWOOD_LOG.get(),
                BlockInit.SHARDWOOD_WOOD.get(), BlockInit.STRIPPED_SHARDWOOD_WOOD.get());
        return strippables;
    }

    @SubscribeEvent
    public static void strip(BlockEvent.BlockToolModificationEvent event) {
        if (event.getItemAbility() != ItemAbilities.AXE_STRIP) return;
        var state = event.getState();
        Block stripped = strippables().get(state.getBlock());
        if (stripped != null && state.hasProperty(RotatedPillarBlock.AXIS))
            event.setFinalState(stripped.defaultBlockState().setValue(RotatedPillarBlock.AXIS, state.getValue(RotatedPillarBlock.AXIS)));
    }

    private ZGStripping() {}
}
