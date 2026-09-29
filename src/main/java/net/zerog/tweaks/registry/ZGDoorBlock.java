package net.zerog.tweaks.registry;

import net.minecraft.world.level.block.DoorBlock;
import net.minecraft.world.level.block.state.properties.BlockSetType;

/** Standard door with vanilla sound set. */
public class ZGDoorBlock extends DoorBlock {
    public ZGDoorBlock(Properties props) { super(BlockSetType.OAK, props); }
}