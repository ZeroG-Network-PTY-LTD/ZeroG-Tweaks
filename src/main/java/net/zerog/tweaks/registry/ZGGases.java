package net.zerog.tweaks.registry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.*;
import net.minecraft.world.level.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.*;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.*;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.capabilities.*;
import net.neoforged.neoforge.fluids.*;
import net.neoforged.neoforge.fluids.capability.templates.FluidHandlerItemStack;
import net.neoforged.neoforge.registries.*;

/** Contained gases use the standard mB capability; never placeable liquid blocks. */
public final class ZGGases {
    public static final DeferredRegister<DataComponentType<?>> COMPONENTS=DeferredRegister.create(Registries.DATA_COMPONENT_TYPE,"zerog_tweaks");
    public static final DeferredHolder<DataComponentType<?>,DataComponentType<SimpleFluidContent>> CONTENT=COMPONENTS.register("gas_content",
        ()->DataComponentType.<SimpleFluidContent>builder().persistent(SimpleFluidContent.CODEC).networkSynchronized(SimpleFluidContent.STREAM_CODEC).build());
    public record Gas(String id, DeferredHolder<FluidType,FluidType> type, DeferredHolder<Fluid,ContainedGas> fluid) {}
    public static final Gas OXYGEN=make("oxygen",-1000),HYDROGEN=make("hydrogen",-2000);
    public static final List<Gas> ALL=List.of(OXYGEN,HYDROGEN);
    public static final DeferredItem<Item> CANISTER=ItemInit.ITEMS.register("gas_canister",()->new Item(new Item.Properties().stacksTo(1)) {
        @Override public void appendHoverText(ItemStack stack,TooltipContext context,List<Component> tooltip,TooltipFlag flag) {
            var gas=stack.getOrDefault(CONTENT.get(),SimpleFluidContent.EMPTY).copy();
            tooltip.add(gas.isEmpty()?Component.translatable("tooltip.zerog_tweaks.gas_empty"):
                Component.translatable("tooltip.zerog_tweaks.gas_contents",gas.getHoverName(),gas.getAmount(),1000));
        }
    });
    private static Gas make(String id,int density) {
        var type=ZGFluids.TYPES.register(id,()->new FluidType(FluidType.Properties.create()
            .descriptionId("fluid_type.zerog_tweaks."+id).density(density).viscosity(100)
            .canHydrate(false).canSwim(false).canDrown(false).canConvertToSource(false)));
        var fluid=ZGFluids.FLUIDS.register(id,()->new ContainedGas(type));
        return new Gas(id,type,fluid);
    }
    public static boolean isGas(Fluid fluid){return fluid instanceof ContainedGas;}
    public static ItemStack filled(Gas gas){var stack=new ItemStack(CANISTER.get());stack.set(CONTENT.get(),SimpleFluidContent.copyOf(new FluidStack(gas.fluid.get(),1000)));return stack;}
    public static void init(IEventBus bus){COMPONENTS.register(bus);bus.addListener(ZGGases::capabilities);}
    private static void capabilities(RegisterCapabilitiesEvent event){
        event.registerItem(Capabilities.FluidHandler.ITEM,(stack,context)->new FluidHandlerItemStack(CONTENT,stack,1000){
            @Override public boolean isFluidValid(int index,FluidStack gas){return index==0&&isGas(gas.getFluid());}
            @Override public boolean canFillFluidType(FluidStack gas){return isGas(gas.getFluid());}
        },CANISTER.get());
    }
    public static final class ContainedGas extends Fluid {
        private final Supplier<FluidType> type;
        private ContainedGas(Supplier<FluidType> type){this.type=type;}
        @Override public FluidType getFluidType(){return type.get();}
        @Override public Item getBucket(){return Items.AIR;}
        @Override protected boolean canBeReplacedWith(FluidState s,BlockGetter l,BlockPos p,Fluid f,Direction d){return false;}
        @Override protected Vec3 getFlow(BlockGetter l,BlockPos p,FluidState s){return Vec3.ZERO;}
        @Override public int getTickDelay(LevelReader l){return 0;}
        @Override protected float getExplosionResistance(){return 0;}
        @Override public float getHeight(FluidState s,BlockGetter l,BlockPos p){return 0;}
        @Override public float getOwnHeight(FluidState s){return 0;}
        @Override protected BlockState createLegacyBlock(FluidState s){return Blocks.AIR.defaultBlockState();}
        @Override public boolean isSource(FluidState s){return false;}
        @Override public int getAmount(FluidState s){return 0;}
        @Override public VoxelShape getShape(FluidState s,BlockGetter l,BlockPos p){return Shapes.empty();}
    }
    private ZGGases(){}
}
