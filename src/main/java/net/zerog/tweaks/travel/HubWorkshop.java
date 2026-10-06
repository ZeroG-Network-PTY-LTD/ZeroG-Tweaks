package net.zerog.tweaks.travel;

import java.util.*;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.*;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.transport.TransportBlockEntity;

/** Additive, once-only test supplies. Never changes survival recipes or existing exhibits. */
public final class HubWorkshop {
    public static final List<String> MACHINES=List.of("ore_refinery","alloy_forge","crystal_growth_chamber","salvage_station",
        "combustion_generator","solar_array","fusion_reactor","geno_station","genetic_splicer","centrifuge",
        "starmetal_smelter","silk_weaver","frame_infusion_altar");
    public static BlockPos origin(int i){return new BlockPos(-100+(i%4)*24,64,-20-(i/4)*26);}
    private static ResourceLocation key(String id){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id);}
    private static ItemStack stack(String id,int n){var k=ResourceLocation.parse(id);return BuiltInRegistries.ITEM.containsKey(k)?new ItemStack(BuiltInRegistries.ITEM.get(k),n):ItemStack.EMPTY;}
    private static void add(Map<String,ItemStack> kit,ItemStack stack){if(!stack.isEmpty())kit.merge(BuiltInRegistries.ITEM.getKey(stack.getItem()).toString(),stack,(old,next)->old.getCount()>=next.getCount()?old:next);}
    public static String build(ServerLevel level){
        if(!PlanetTestHub.isHub(level.getServer())||level!=level.getServer().overworld())return "Workshop is hub-only.";
        var ledger=GateLedger.get(level.getServer());if(ledger.workshopBuilt)return "Supplied workshop already built; player edits and supplies preserved.";
        var kits=new ArrayList<List<ItemStack>>();var blocks=new ArrayList<ResourceLocation>();
        for(int i=0;i<MACHINES.size();i++){
            var id=MACHINES.get(i);var block=ResourceLocation.fromNamespaceAndPath(i<7?"zerog_tweaks":"aeroapiary",id);blocks.add(block);
            var kit=new LinkedHashMap<String,ItemStack>();
            if(i<4){
                var kind=ProcessingRegistry.Kind.values()[i];
                var recipes=level.getRecipeManager().getAllRecipesFor(ProcessingRegistry.TYPES_BY_KIND.get(kind).get()).stream().sorted(Comparator.comparing(h->h.id().toString())).toList();
                if(recipes.isEmpty())return "No loaded "+kind.id+" recipes; workshop not placed.";
                for(var recipe:recipes){var entries=new ArrayList<>(recipe.value().inputs());recipe.value().catalyst().ifPresent(entries::add);
                    for(var entry:entries){var options=entry.ingredient().getItems();if(options.length==0)return "Unresolved ingredient in "+recipe.id()+"; workshop not placed.";
                        Arrays.sort(options,Comparator.comparing(s->BuiltInRegistries.ITEM.getKey(s.getItem()).toString()));
                        add(kit,options[0].copyWithCount(Math.min(options[0].getMaxStackSize(),entry.consumed()?entry.count()*16:entry.count())));
                    }
                }
                for(String upgrade:List.of("cyrrium_casing","tectium_casing","wraithsteel_casing","astrium_casing","cryo_core","pulsar_dust","tremor_dust","spectral_dust","fusion_dust"))add(kit,stack("zerog_tweaks:"+upgrade,1));
            }else if(i==4){add(kit,new ItemStack(Items.COAL,64));add(kit,new ItemStack(Items.OAK_LOG,64));}
            else if(i==6)add(kit,stack("zerog_tweaks:fusion_dust",64));
            else if((i==7||i==8)&&BuiltInRegistries.BLOCK.containsKey(block)){
                var cage=sampleBee(level);if(cage.isEmpty())return "Productive Bees sample unavailable; genetics workshop not placed.";
                if(i==8)cage=net.zerog.tweaks.genetics.ProductiveBeeGenes.analyse(cage);
                add(kit,cage);
                add(kit,stack("aeroapiary:serum_vial",16));add(kit,new ItemStack(Items.HONEY_BOTTLE,16));
                if(i==8){
                    var serum=stack("aeroapiary:trait_serum",1);var tag=new net.minecraft.nbt.CompoundTag();var trait=new net.minecraft.nbt.CompoundTag();
                    trait.putString("gene","productivity");trait.putString("value",net.zerog.tweaks.genetics.ProductiveBeeGenes.read(cage).get("productivity"));tag.put("zerog_tweaks:trait",trait);
                    serum.set(net.minecraft.core.component.DataComponents.CUSTOM_DATA,net.minecraft.world.item.component.CustomData.of(tag));add(kit,serum);
                    add(kit,stack("aeroapiary:royal_jelly",16));add(kit,stack("aeroapiary:cosmic_jelly",16));
                    add(kit,stack("zerog_tweaks:royal_jelly_bucket",1));add(kit,stack("zerog_tweaks:cosmic_jelly_bucket",1));
                }
            }
            else if(i>=9&&BuiltInRegistries.BLOCK.containsKey(block)){
                try {var filter=Class.forName("com.zerog.aeroapiary.ZeroGMachines").getMethod("mayPlaceIn",String.class,int.class,ItemStack.class);
                    for(var item:BuiltInRegistries.ITEM){var sample=new ItemStack(item);if(sample.isEmpty())continue;
                        for(int slot=0;slot<3;slot++)if((Boolean)filter.invoke(null,id,slot,sample)){add(kit,sample.copyWithCount(Math.min(16,sample.getMaxStackSize())));break;}
                    }
                }catch(ReflectiveOperationException ex){return "Addon ingredient contract unavailable; workshop not placed.";}
            }
            if(i<7&&!BuiltInRegistries.BLOCK.containsKey(block))return "Missing machine "+block+"; workshop not placed.";
            if(kit.size()>108)return "Supply kit exceeds four chests: "+id+"; workshop not placed.";
            kits.add(List.copyOf(kit.values()));
        }
        var serviceKit=new LinkedHashMap<String,ItemStack>();
        for(var item:BuiltInRegistries.ITEM){var sample=new ItemStack(item);
            if(net.zerog.tweaks.genetics.AlvearyRuntime.isFrame(sample)||!net.zerog.tweaks.genetics.AlvearyRuntime.species(sample).isEmpty())add(serviceKit,sample.copyWithCount(Math.min(16,sample.getMaxStackSize())));
        }
        add(serviceKit,sampleBee(level));
        for(String id:List.of("liquid_starlight_bucket","moon_honey_bucket","mars_honey_bucket","cerulon_honey_bucket","skarn_honey_bucket","eidolon_honey_bucket","solvane_honey_bucket","royal_jelly_bucket","cosmic_jelly_bucket","flux_wrench","item_filter_card","fluid_filter_card","generator_flux_module","storage_expansion_module","item_port","fluid_port","energy_port"))add(serviceKit,stack("zerog_tweaks:"+id,1));
        add(serviceKit,new ItemStack(Items.BUCKET,16));
        for(String tier:net.zerog.tweaks.storage.StorageTankRegistry.TIERS)for(String family:List.of("energy_cell","energy_conduit","item_tube","fluid_pipe","fluid_tank"))add(serviceKit,stack("zerog_tweaks:"+tier+"_"+family,1));
        if(serviceKit.size()>108)return "Alveary kit exceeds four chests; workshop not placed.";
        // All plots checked before any modification. Native flat ground is the only replaceable floor.
        for(var p:BlockPos.betweenClosed(new BlockPos(-103,63,-102),new BlockPos(-10,69,-1))){
            var state=level.getBlockState(p);
            if(p.getY()==63? !state.isAir()&&!state.is(Blocks.STONE)&&!state.is(BlockInit.LANDING_PLATFORM.get()):!state.isAir())return "Workshop plot occupied at "+p.toShortString()+"; nothing overwritten.";
        }
        for(int x=-100;x<=0;x++)for(int z=-6;z<=-4;z++){
            var pos=new BlockPos(x,63,z);var state=level.getBlockState(pos);
            if(!state.isAir()&&!state.is(Blocks.STONE)&&!state.is(BlockInit.LANDING_PLATFORM.get()))return "Workshop access floor occupied at "+pos.toShortString()+"; nothing overwritten.";
        }
        var serviceBase=origin(13);var supplies=List.copyOf(serviceKit.values());
        for(int x=-2;x<=18;x++)for(int z=-3;z<=9;z++)level.setBlock(serviceBase.offset(x,-1,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
        for(int x=serviceBase.getX()>>4;x<=serviceBase.offset(18,0,0).getX()>>4;x++)for(int z=serviceBase.offset(0,0,-3).getZ()>>4;z<=serviceBase.offset(0,0,9).getZ()>>4;z++)level.setChunkForced(x,z,true);
        for(int c=0;c<4;c++){var pos=serviceBase.offset(3+c*2,0,0);level.setBlock(pos,Blocks.CHEST.defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH),3);
            if(level.getBlockEntity(pos) instanceof ChestBlockEntity chest){for(int s=0;s<27&&c*27+s<supplies.size();s++)chest.setItem(s,supplies.get(c*27+s).copy());chest.setChanged();}
        }
        sign(level,serviceBase.offset(0,0,4),"ALVEARY SERVICE KIT","Bees / frames / buckets","Ports / six-tier lines","Load tier slots manually");
        sign(level,serviceBase.offset(5,0,4),"SHELLS IN NORTH GALLERY","Charged cell at each","Honey alongside combs","Client review remains");
        for(int i=0;i<MACHINES.size();i++){
            var base=origin(i);for(int x=-2;x<=18;x++)for(int z=-3;z<=9;z++)level.setBlock(base.offset(x,-1,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
            for(int x=base.getX()>>4;x<=base.offset(18,0,0).getX()>>4;x++)for(int z=base.offset(0,0,-3).getZ()>>4;z<=base.offset(0,0,9).getZ()>>4;z++)level.setChunkForced(x,z,true);
            if(!BuiltInRegistries.BLOCK.containsKey(blocks.get(i))){sign(level,base,"Optional machine",MACHINES.get(i),"Addon not installed","No substitute placed");continue;}
            var state=BuiltInRegistries.BLOCK.get(blocks.get(i)).defaultBlockState();if(state.hasProperty(BlockStateProperties.HORIZONTAL_FACING))state=state.setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH);
            level.setBlock(base,state,3);
            boolean generator=i>=4&&i<=6;
            level.setBlock(base.offset(0,0,-1),BuiltInRegistries.BLOCK.get(key("astrium_energy_conduit")).defaultBlockState(),3);
            level.setBlock(base.offset(0,0,-2),BuiltInRegistries.BLOCK.get(key("astrium_energy_cell")).defaultBlockState(),3);
            if(level.getBlockEntity(base.offset(0,0,-2)) instanceof TransportBlockEntity cell){cell.stored=generator?0:cell.capacity();Arrays.fill(cell.modes,generator?2:1);cell.setChanged();}
            for(int c=0;c<4;c++){var p=base.offset(3+c*2,0,0);level.setBlock(p,Blocks.CHEST.defaultBlockState().setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH),3);
                if(level.getBlockEntity(p) instanceof ChestBlockEntity chest){for(int s=0;s<27&&c*27+s<kits.get(i).size();s++)chest.setItem(s,kits.get(i).get(c*27+s).copy());chest.setChanged();}
            }
            sign(level,base.offset(0,0,4),MACHINES.get(i).replace('_',' '),generator?"OUTPUT TO EMPTY CELL":"CHARGED CELL INPUT",i==5?"Daylight / open sky":"Ingredients in chests","No recipe costs changed");
            sign(level,base.offset(5,0,4),"SUPPLIES: MANUAL LOAD","Recipe inputs + catalysts","Outputs stay in machine","No automatic restocking");
        }
        for(int x=-100;x<=0;x++)for(int z=-6;z<=-4;z++)level.setBlock(new BlockPos(x,63,z),BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
        sign(level,new BlockPos(-12,64,-5),"WEST: WORKSHOP","13 machine stations","Test materials / power","Recipes balanced later");
        ledger.workshopBuilt=true;ledger.setDirty();return "Built supplied workshop west of hub; original exhibits and gates preserved.";
    }
    private static ItemStack sampleBee(ServerLevel level){
        var type=ResourceLocation.parse("productivebees:configurable_bee");if(!BuiltInRegistries.ENTITY_TYPE.containsKey(type))return ItemStack.EMPTY;
        try {
            var bee=(net.minecraft.world.entity.animal.Bee)BuiltInRegistries.ENTITY_TYPE.get(type).create(level);if(bee==null)return ItemStack.EMPTY;
            bee.getClass().getMethod("setBeeType",String.class).invoke(bee,"productivebees:iron");
            String root="cy.jdkdigital.productivebees.";var attr=Class.forName(root+"util.GeneAttribute");var value=Class.forName(root+"util.GeneValue");var set=bee.getClass().getMethod("setAttributeValue",attr,value);
            String[] values={"PRODUCTIVITY_HIGH","ENDURANCE_STRONG","TEMPER_PASSIVE","BEHAVIOR_DIURNAL","WEATHER_TOLERANCE_ANY"};
            for(int i=0;i<5;i++)set.invoke(bee,attr.getField(net.zerog.tweaks.genetics.ProductiveBeeGenes.GENES[i].toUpperCase(Locale.ROOT)).get(null),value.getField(values[i]).get(null));
            var cage=stack("productivebees:bee_cage",1);Class.forName(root+"common.item.BeeCage").getMethod("captureEntity",net.minecraft.world.entity.animal.Bee.class,ItemStack.class).invoke(null,bee,cage);bee.discard();
            return net.zerog.tweaks.genetics.ProductiveBeeGenes.read(cage).size()==5?cage:ItemStack.EMPTY;
        }catch(ReflectiveOperationException|LinkageError ex){return ItemStack.EMPTY;}
    }
    private static void sign(ServerLevel level,BlockPos pos,String... lines){level.setBlock(pos,Blocks.OAK_SIGN.defaultBlockState(),3);if(level.getBlockEntity(pos) instanceof SignBlockEntity sign){var text=sign.getFrontText();for(int i=0;i<4;i++)text=text.setMessage(i,Component.literal(lines[i]));sign.setText(text,true);sign.setText(text,false);sign.setChanged();}}
    private HubWorkshop(){}
}
