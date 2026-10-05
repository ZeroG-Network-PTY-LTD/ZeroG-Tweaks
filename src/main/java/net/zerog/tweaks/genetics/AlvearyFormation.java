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
    public record Result(boolean formed,String error,BlockPos anchor){public Result(boolean formed,String error){this(formed,error,null);}}
    /** A controller is a terminal; the geometric anchor is the southeast bottom corner. */
    public static BlockPos anchor(net.minecraft.world.level.block.entity.BlockEntity owner){var state=AlvearyRuntime.state(owner);return state.contains("shell_anchor")?BlockPos.of(state.getLong("shell_anchor")):owner.getBlockPos();}
    public static Result locate(ServerLevel level,BlockPos controller,int tier){
        Result nearest=null;
        for(int x=0;x<5;x++)for(int z=0;z<5;z++){
            if(x!=0&&x!=4&&z!=0&&z!=4)continue;
            var base=controller.offset(x,-1,z);
            if(!AlvearyPorts.footprintLoaded(level,base))continue;
            var roof=BuiltInRegistries.BLOCK.getKey(level.getBlockState(base.above(4)).getBlock());
            if(!roof.toString().equals("aeroapiary:tier"+tier+"_roof"))continue;
            var result=serviceBase(level,base,controller,tier);
            if(result.formed())return result;
            nearest=result;
        }
        // Save compatibility only: existing corner-controller shells are not erased.
        var legacy=validate(level,controller,tier);
        if(legacy.formed())return new Result(true,null,controller);
        return nearest!=null?nearest:new Result(false,"Second-row wall controller; bottom requires 2 item, 2 fluid and 1 energy port");
    }
    private static Result serviceBase(ServerLevel level,BlockPos base,BlockPos controller,int tier){
        int items=0,fluids=0,energy=0;String prefix="tier"+tier+"_";
        for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){
            var pos=base.offset(-x,y,-z);var state=level.getBlockState(pos);var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());
            String id=key.getNamespace().equals("aeroapiary")?key.getPath():"";
            if((y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3){if(!state.isAir())return new Result(false,"Keep central flight chamber clear",base);continue;}
            if(y==4){if(!id.equals(prefix+"roof"))return new Result(false,"Requires matching tier roof",base);continue;}
            if(pos.equals(controller)){if(!id.equals(prefix+"controller")&&!(tier==1&&id.equals("apiary_controller")))return new Result(false,"Wrong controller tier",base);continue;}
            if(id.endsWith("_controller")||id.equals("apiary_controller"))return new Result(false,"Only one controller per shell",base);
            var role=role(state);
            if(id.equals(prefix+"energy_port"))role=Role.ENERGY;
            if(id.equals(prefix+"input_hatch")||id.equals(prefix+"output_hatch"))role=Role.ITEM;
            if(id.equals(prefix+"fluid_port")||id.equals(prefix+"honey_port"))role=Role.FLUID;
            if(role!=Role.NONE){
                if(y!=0||x!=0&&x!=4&&z!=0&&z!=4)return new Result(false,"Service ports belong on bottom perimeter",base);
                if(!frontOutside(state,pos,base))return new Result(false,"Port front must face outside",base);
                if(role==Role.ENERGY)energy++;else if(role==Role.ITEM)items++;else fluids++;
            }else if(!id.startsWith(prefix))return new Result(false,"Unsupported shell block",base);
        }
        return items==2&&fluids==2&&energy==1?new Result(true,null,base):new Result(false,"Bottom ports: items "+items+"/2, fluids "+fluids+"/2, energy "+energy+"/1",base);
    }
    public static Role role(BlockState state){var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());if(!key.getNamespace().equals("zerog_tweaks"))return Role.NONE;if(state.getBlock() instanceof TransportBlock block){if((block.family.equals("energy_port")||block.family.equals("energy_cell"))&&state.is(ENERGY))return Role.ENERGY;if(block.family.equals("item_port")&&state.is(ITEM))return Role.ITEM;if(block.family.equals("fluid_port")&&state.is(FLUID))return Role.FLUID;}if(state.getBlock() instanceof StorageTankBlock&&state.is(FLUID))return Role.FLUID;return Role.NONE;}
    public static boolean frontOutside(BlockState state,BlockPos pos,BlockPos anchor){if(!(state.getBlock() instanceof TransportBlock block)||!block.family.endsWith("port"))return true;var front=pos.relative(state.getValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING));return front.getX()<anchor.getX()-4||front.getX()>anchor.getX()||front.getZ()<anchor.getZ()-4||front.getZ()>anchor.getZ();}
    public static Result validate(ServerLevel level,BlockPos anchor,int tier){if(tier<1||tier>7||!AlvearyPorts.footprintLoaded(level,anchor))return new Result(false,"Structure footprint is not fully loaded");int energy=0;String prefix="tier"+tier;
        for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++){var pos=anchor.offset(-x,y,-z);var state=level.getBlockState(pos);var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());String id=key.getNamespace().equals("aeroapiary")?key.getPath():"";boolean core=(y==1||y==2)&&x>=1&&x<=3&&z>=1&&z<=3;if(core){if(!state.isAir())return new Result(false,"Keep the central flight chamber clear: "+pos.toShortString());continue;}if(y==4){if(!id.equals(prefix+"_roof"))return new Result(false,"Requires "+prefix+" roof: "+pos.toShortString());continue;}if(x==0&&y==0&&z==0){if(!id.equals(prefix+"_controller")&&!(tier==1&&id.equals("apiary_controller")))return new Result(false,"Controller must anchor the shell");continue;}var role=role(state);if(!id.startsWith(prefix+"_")&&role==Role.NONE)return new Result(false,"Unsupported shell part at "+pos.toShortString());if(role!=Role.NONE&&!frontOutside(state,pos,anchor))return new Result(false,"Service port front must face outside: "+pos.toShortString());if(id.equals(prefix+"_energy_port")||role==Role.ENERGY)energy++;}
        return energy>0?new Result(true,null):new Result(false,"No energy port/cell in structure");
    }
    private AlvearyFormation(){}
}
