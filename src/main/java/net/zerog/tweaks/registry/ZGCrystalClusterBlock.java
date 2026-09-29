package net.zerog.tweaks.registry;

import net.minecraft.world.level.block.AmethystClusterBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.PushReaction;

/**
 * Standing crystal spike (Brine / Frost / Cerulite / Prism).
 *
 * The shipped art is a 5-spike sprite, so the block renders as an X-billboard
 * like vanilla amethyst clusters — but a plain full cube gives it a full
 * invisible hitbox, no support attachment, and a grass-like silhouette.
 *
 * Extending AmethystClusterBlock (vanilla 1.21.1) gives:
 * - thin cross hitbox (7px tall column, 3px off-center spikes)
 * - placement on the clicked face (floor or wall, like vanilla clusters)
 * - pops off when the supporting block is removed
 * - pistons shear it instead of dragging it (DESTROY)
 */
public class ZGCrystalClusterBlock extends AmethystClusterBlock {
    public ZGCrystalClusterBlock(BlockBehaviour.Properties props) {
        super(7.0F, 3.0F, props
                .sound(SoundType.AMETHYST_CLUSTER)
                .noOcclusion()
                .pushReaction(PushReaction.DESTROY)
        );
    }
}