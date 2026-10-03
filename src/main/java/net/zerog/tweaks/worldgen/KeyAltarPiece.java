package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import net.zerog.tweaks.registry.BlockInit;

/** A Key Altar (holding its Concord Key) on a black plinth in the middle of a vault room; see ConcordVaultStructure. */
public class KeyAltarPiece extends StructurePiece {
    private final BlockPos altar;

    public KeyAltarPiece(BlockPos altar) {
        super(ZGStructures.KEY_ALTAR_PIECE.get(), 0, new BoundingBox(altar.below()).encapsulate(altar));
        this.altar = altar;
    }

    public KeyAltarPiece(CompoundTag tag) {
        super(ZGStructures.KEY_ALTAR_PIECE.get(), tag);
        this.altar = NbtUtils.readBlockPos(tag, "Altar").orElseThrow();
    }

    public BlockPos altarPos() { return altar; }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        tag.put("Altar", NbtUtils.writeBlockPos(altar));
    }

    @Override
    public void postProcess(WorldGenLevel level, StructureManager structures, ChunkGenerator generator, RandomSource random,
                            BoundingBox box, ChunkPos chunk, BlockPos pivot) {
        if (box.isInside(altar)) {
            level.setBlock(altar, BlockInit.VAULT_KEY_ALTAR.get().defaultBlockState(), Block.UPDATE_CLIENTS);
        }
        if (box.isInside(altar.below())) {
            level.setBlock(altar.below(), BlockInit.CHISELED_POLISHED_BLACK_CERULEAN_STONE.get().defaultBlockState(), Block.UPDATE_CLIENTS);
        }
    }
}
