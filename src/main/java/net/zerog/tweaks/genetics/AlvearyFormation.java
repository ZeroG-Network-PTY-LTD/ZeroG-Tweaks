package net.zerog.tweaks.genetics;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.zerog.tweaks.transport.TransportBlock;
import net.zerog.tweaks.storage.StorageTankBlock;

/** Same authored 5³ shell, with explicit original ZeroG service-module substitutions. */
public final class AlvearyFormation {
    public enum Role {NONE,ENERGY,ITEM,FLUID}
    private static TagKey<Block> tag(String role){return TagKey.create(Registries.BLOCK,ResourceLocation.fromNamespaceAndPath("zerog_tweaks","alveary/"+role+"_modules"));}
    public static final TagKey<Block> ENERGY=tag("energy"),ITEM=tag("item"),FLUID=tag("fluid");
    public record Result(boolean formed,String error){}
    public static Role role(BlockState state){var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());if(!key.getNamespace().equals("zerog_tweaks"))return Role.NONE;if(state.getBlock() instanceof TransportBlock block){if((block.family.equals("energy_port")||block.family.equals("energy_cell"))&&state.is(ENERGY))return Role.ENERGY;if(block.family.equals("item_port")&&state.is(ITEM))return Role.ITEM;if(block.family.equals("fluid_port")&&state.is(FLUID))return Role.FLUID;}if(state.getBlock() instanceof StorageTankBlock&&state.is(FLUID))return Role.FLUID;return Role.NONE;}
    public static boolean frontOutside(BlockState state,BlockPos pos,BlockPos anchor){if(!(state.getBlock() instanceof TransportBlock block)||!block.family.endsWith("port"))return true;var front=pos.relative(state.getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING));return front.getX()<anchor.getX()-4||front.getX()>anchor.getX()||front.getZ()<anchor.getZ()-4||front.getZ()>anchor.getZ();}
    public static Result validate(ServerLevel level,BlockPos anchor,int tier){if(tier<1||tier>7||!AlvearyPorts.footprintLoaded(level,anchor))return new Result(false,"Structure footprint is not fully loaded");int energy=0;String prefix="tier"+tier;
        for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){var pos=anchor.offset(-x,y,-z);var state=level.getBlockState(pos);var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());String id=key.getNamespace().equals("aeroapiary")?key.getPath():"";boolean core=(y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3;if(core){if(!state.isAir())return new Result(false,"Keep the central flight chamber clear: "+pos.toShortString());continue;}if(y==4){if(!id.equals(prefix+"_roof"))return new Result(false,"Requires "+prefix+" roof: "+pos.toShortString());continue;}if(x==0&&y==0&&z==0){if(!id.equals(prefix+"_controller")&&!(tier==1&&id.equals("apiary_controller")))return new Result(false,"Controller must anchor the shell");continue;}var role=role(state);if(!id.startsWith(prefix+"_")&&role==Role.NONE)return new Result(false,"Unsupported shell part at "+pos.toShortString());if(role!=Role.NONE&&!frontOutside(state,pos,anchor))return new Result(false,"Service port front must face outside: "+pos.toShortString());if(id.equals(prefix+"_energy_port")||role==Role.ENERGY)energy++;}
        return energy>0?new Result(true,null):new Result(false,"No energy port/cell in structure");
    }
    private AlvearyFormation(){}
}
