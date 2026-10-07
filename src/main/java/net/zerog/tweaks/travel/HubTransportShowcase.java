package net.zerog.tweaks.travel;

import java.util.Arrays;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.fluids.FluidStack;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.storage.*;
import net.zerog.tweaks.transport.*;

/** Separated, conserved demonstration lanes. Finite supplies; no automatic refill. */
public final class HubTransportShowcase {
    public static BlockPos origin(int tier){return new BlockPos(-108+(tier%2)*24,64,-62+(tier/2)*16);}
    private static ResourceLocation id(String name){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name);}
    public static void build(ServerLevel level){
        if(!PlanetTestHub.isHub(level.getServer()))throw new IllegalStateException("Hub-only transport exhibition");
        for(int tier=0;tier<6;tier++){
            var base=origin(tier);String metal=StorageTankRegistry.TIERS[tier];
            for(int x=-1;x<=13;x++)for(int z=-1;z<=12;z++)level.setBlock(base.offset(x,-1,z),Blocks.STONE_BRICKS.defaultBlockState(),2);
            for(int z=0;z<=8;z+=4){
                String family=z==0?"energy":z==4?"item":"fluid";
                String line=family.equals("energy")?"energy_conduit":family.equals("item")?"item_tube":"fluid_pipe";
                for(int x=0;x<=8;x++){
                    var pos=base.offset(x,0,z);
                    var block=BuiltInRegistries.BLOCK.get(id(x==0||x==8?family+"_port":metal+"_"+line));
                    var state=block.defaultBlockState();
                    if(x==0||x==8)state=state.setValue(BlockStateProperties.HORIZONTAL_FACING,x==0?Direction.EAST:Direction.WEST)
                        .setValue(TransportBlock.MODE,x==0?TransportBlock.PortMode.OUTPUT:TransportBlock.PortMode.INPUT);
                    level.setBlock(pos,state,3);
                    var node=(TransportBlockEntity)level.getBlockEntity(pos);
                    Arrays.fill(node.modes,3);
                    if(x==0)node.modes[Direction.EAST.ordinal()]=1;
                    else if(x==8)node.modes[Direction.WEST.ordinal()]=2;
                    else {node.modes[Direction.WEST.ordinal()]=2;node.modes[Direction.EAST.ordinal()]=1;}
                    if(x==0){if(family.equals("energy"))node.stored=64000;
                        else if(family.equals("item"))node.items.setStackInSlot(0,new ItemStack(Items.IRON_INGOT,64));
                        else node.tank.setFluid(new FluidStack(BuiltInRegistries.FLUID.get(id("liquid_starlight")),8000));}
                    node.setChanged();
                }
            }
            var tankPos=base.offset(12,0,8);
            level.setBlock(tankPos,BuiltInRegistries.BLOCK.get(id(metal+"_fluid_tank")).defaultBlockState(),3);
            var tank=(StorageTankBlockEntity)level.getBlockEntity(tankPos);
            tank.tank.setFluid(new FluidStack(BuiltInRegistries.FLUID.get(id("liquid_starlight")),Math.min(4000,tank.capacity())));
            var signPos=base.offset(1,0,11);level.setBlock(signPos,Blocks.OAK_SIGN.defaultBlockState(),3);
            if(level.getBlockEntity(signPos) instanceof SignBlockEntity sign){var text=sign.getFrontText();
                String[] lines={metal+" TRANSFER LANES","Left OUT -> right IN","Power / items / fluid","Tank: bucket example"};
                for(int i=0;i<4;i++)text=text.setMessage(i,Component.literal(lines[i]));sign.setText(text,true);sign.setText(text,false);sign.setChanged();}
            for(int x=-108;x<=-44;x++)for(int z=base.getZ()+11;z<=base.getZ()+12;z++)level.setBlock(new BlockPos(x,63,z),Blocks.STONE_BRICKS.defaultBlockState(),2);
        }
    }
    private HubTransportShowcase(){}
}
