package net.zerog.tweaks.storage;

import java.util.List;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.fluids.FluidStack;

/** The same tank shell can store liquids or contained gases; contents are native BE data. */
public final class StorageTankItem extends BlockItem {
    private final int tier;
    public StorageTankItem(StorageTankBlock block, Properties properties, int tier) {
        super(block, properties); this.tier = tier;
    }
    @Override public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
        super.appendHoverText(stack, context, lines, flag);
        lines.add(Component.translatable("tooltip.zerog_tweaks.tank_capacity", tier + 1, StorageTankRegistry.CAPACITIES[tier]));
        var data = stack.get(DataComponents.BLOCK_ENTITY_DATA);
        if (data != null && context.registries() != null) {
            var contents = FluidStack.parseOptional(context.registries(), data.copyTag().getCompound("fluid").getCompound("Fluid"));
            if (!contents.isEmpty()) lines.add(Component.translatable("tooltip.zerog_tweaks.gas_contents", contents.getHoverName(), contents.getAmount(), StorageTankRegistry.CAPACITIES[tier]));
        }
    }
}
