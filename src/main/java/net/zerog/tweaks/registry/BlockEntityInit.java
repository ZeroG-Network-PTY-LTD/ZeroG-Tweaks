package net.zerog.tweaks.registry;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import net.zerog.tweaks.ZeroGTweaks;

/** BlockEntity types for ZeroG-Tweaks machines (aeroapiary ModBlockEntities pattern). */
public final class BlockEntityInit {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, ZeroGTweaks.MODID);

    @SuppressWarnings("unchecked")
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<OreRefineryBlockEntity>> ORE_REFINERY =
            BLOCK_ENTITIES.register("ore_refinery", () -> BlockEntityType.Builder.of(
                    (pos, state) -> new OreRefineryBlockEntity(BlockEntityInit.ORE_REFINERY.get(), pos, state),
                    BlockInit.ORE_REFINERY.get()).build(null));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<net.zerog.tweaks.arena.ConcordPrismBlockEntity>> CONCORD_PRISM =
            BLOCK_ENTITIES.register("concord_prism", () -> BlockEntityType.Builder.of(
                    net.zerog.tweaks.arena.ConcordPrismBlockEntity::new, BlockInit.CONCORD_PRISM.get()).build(null));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity>> SETTLEMENT_ANCHOR =
            BLOCK_ENTITIES.register("settlement_anchor", () -> BlockEntityType.Builder.of(
                    net.zerog.tweaks.worldgen.SettlementAnchorBlockEntity::new, BlockInit.SETTLEMENT_ANCHOR.get()).build(null));

    private BlockEntityInit() {}

    public static void register(IEventBus modBus) {
        BLOCK_ENTITIES.register(modBus);
    }
}
