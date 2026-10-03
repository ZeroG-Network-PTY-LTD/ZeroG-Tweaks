package net.zerog.tweaks.item;

import java.util.Map;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.BlockItemStateProperties;
import net.minecraft.world.level.block.Block;
import net.zerog.tweaks.registry.ZGStarGlassBlock;

/** Variant entry must not replace the canonical block->item mapping. */
public final class StarGlassVariantItem extends BlockItem {
    private final String colour;
    public StarGlassVariantItem(Block block,ZGStarGlassBlock.Nebula colour) {
        super(block,new Item.Properties().component(DataComponents.BLOCK_STATE,
                BlockItemStateProperties.EMPTY.with(ZGStarGlassBlock.NEBULA,colour)));
        this.colour=colour.getSerializedName();
    }
    @Override public void registerBlocks(Map<Block,Item> map,Item item) {}
    @Override public String getDescriptionId() {return "item.zerog_tweaks.star_glass_"+colour;}
}
