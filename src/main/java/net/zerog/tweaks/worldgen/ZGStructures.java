package net.zerog.tweaks.worldgen;

import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/** Structure types used by data/zerog_tweaks/worldgen/structure (boss arenas etc.). */
public final class ZGStructures {
    private static final DeferredRegister<StructureType<?>> TYPES =
            DeferredRegister.create(Registries.STRUCTURE_TYPE, ZeroGTweaks.MODID);

    public static final Supplier<StructureType<DryLandJigsawStructure>> DRY_LAND_JIGSAW =
            TYPES.register("dry_land_jigsaw", () -> () -> DryLandJigsawStructure.CODEC);

    public static void register(IEventBus modBus) {
        TYPES.register(modBus);
    }

    private ZGStructures() {}
}
