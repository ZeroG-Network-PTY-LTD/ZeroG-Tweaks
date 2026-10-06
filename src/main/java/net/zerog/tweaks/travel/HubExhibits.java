package net.zerog.tweaks.travel;

import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.DispenserBlockEntity;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.levelgen.structure.templatesystem.JigsawReplacementProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.zerog.tweaks.guide.MultiblockGuides;
import net.zerog.tweaks.registry.BlockInit;

/** Cardinal inspection districts in the explicit hub. Never clears player builds. */
public final class HubExhibits {
    public static final List<String> ROOMS=List.of("collapsed_mine","concord_shrine","crystal_garden","forge","observatory",
            "prismling_nest","star_library","starlight_pool","storage_hall","trap_hall");
    public static final List<String> VALIDATED_TIERS=List.of("tier3","tier5","tier6","tier7");
    public static BlockPos designOrigin(int index) {return new BlockPos(-62+(index%4)*32,64,40+(index/4)*32);}
    public static BlockPos formedOrigin(int index) {return new BlockPos(-62+index*32,64,110);}
    public static BlockPos roomOrigin(int index) {return new BlockPos(80+(index%5)*26,64,-25+(index/5)*30);}
    private static String prefix(String layout) {return layout.equals("cosmic_alveary")?"tier5":layout.substring(0,5);}
    private static BlockState part(String id) {
        var key=ResourceLocation.fromNamespaceAndPath("aeroapiary",id);
        if(!BuiltInRegistries.BLOCK.containsKey(key))throw new IllegalStateException("Missing bee add-on block "+key);
        var state=BuiltInRegistries.BLOCK.get(key).defaultBlockState();
        if(state.hasProperty(BlockStateProperties.HORIZONTAL_FACING))state=state.setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH);
        return state;
    }
    public static String build(ServerLevel level) {
        if(!PlanetTestHub.isHub(level.getServer()) || level!=level.getServer().overworld())return "Only available in the ZeroG Planet Test Hub.";
        var ledger=GateLedger.get(level.getServer());if(ledger.exhibitsBuilt)return "Hub exhibits already built; player edits preserved.";
        // Resolve all optional blocks/templates before any placement. Never substitute air.
        try {
            for(var layout:MultiblockGuides.layouts())for(String name:List.of("casing","roof","controller"))part(prefix(layout.id())+"_"+name);
            part("geno_station");part("genetic_splicer");
            for(var tier:VALIDATED_TIERS)for(String name:List.of("casing","roof","controller"))part(tier+"_"+name);
            for(String room:ROOMS)if(level.getStructureManager().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","concord_vault/rooms/"+room)).isEmpty())
                return "Missing room template: "+room;
        } catch(IllegalStateException absent) {return absent.getMessage()+"; gallery not placed.";}
        // All new district plots must be empty above native ground.
        var plots=new java.util.ArrayList<BlockPos>();
        for(int i=0;i<MultiblockGuides.layouts().size();i++)plots.add(designOrigin(i));
        for(int i=0;i<VALIDATED_TIERS.size();i++)plots.add(formedOrigin(i));
        for(int i=0;i<ROOMS.size();i++)plots.add(roomOrigin(i));
        for(var plot:plots)for(var pos:BlockPos.betweenClosed(plot.offset(-3,-1,-3),plot.offset(24,13,23))) {
            var state=level.getBlockState(pos);
            if(pos.getY()==63) {
                if(!state.isAir() && !state.is(Blocks.STONE) && !state.is(BlockInit.LANDING_PLATFORM.get()))
                    return "Gallery floor occupied at "+pos.toShortString()+"; nothing overwritten.";
            } else if(!state.isAir())return "Gallery plot occupied at "+pos.toShortString()+"; nothing overwritten.";
        }
        // Raised pads and 360-degree aisles; northern gate pads are separate.
        for(int z=0;z<=154;z++)for(int x=-2;x<=2;x++)floor(level,new BlockPos(x,63,z));
        for(int x=0;x<=210;x++)for(int z=-2;z<=2;z++)floor(level,new BlockPos(x,63,z));
        sign(level,new BlockPos(3,64,12),"SOUTH: BEE SYSTEMS","12 working shells","Ports face outward","Walk around all sides");
        sign(level,new BlockPos(12,64,3),"EAST: SCHEMATICS","10 Vault room designs","Inspection structures","Not active boss arenas");
        sign(level,new BlockPos(-3,64,-12),"NORTH: ALL GATES","34 destinations","Protected return pads","Test power enabled");
        int index=0;
        for(var layout:MultiblockGuides.layouts()) {
            var base=designOrigin(index++);pad(level,base,24,20);
            buildServiceShell(level,base,prefix(layout.id()));
            String name=layout.id().equals("cosmic_alveary")?"Cosmic Alveary":prefix(layout.id())+" "+layout.id().split("_")[1];
            sign(level,base.offset(2,0,8),name,"WORKING 5x5 SHELL","Controller: row 2","Right-click terminal");
            sign(level,base.offset(7,0,8),"ZEROG SERVICE BASE","2 item / 2 fluid","1 energy; outward","No terminal cables");
            // The earlier approved external-module rule: no invented service sockets.
            level.setBlock(base.offset(15,0,2),part("geno_station"),3);
            level.setBlock(base.offset(17,0,2),part("genetic_splicer"),3);
            level.setBlock(base.offset(19,0,2),BlockInit.CRYO_POD.get().defaultBlockState(),3);
            sign(level,base.offset(17,0,5),"EXTERNAL MODULES","Genetics / splicer","Cryo pod reference","Not formation sockets");
            for(int y=0;y<=layout.maxY();y++)sign(level,base.offset(12,0,7+y),"Layer Y="+y,"Count from base 0", "G: exact cells", "Inspect all sides");
        }
        index=0;
        for(String tier:VALIDATED_TIERS) {
            var base=formedOrigin(index++);pad(level,base,24,20);
            buildServiceShell(level,base,tier);
            sign(level,base.offset(2,0,8),tier+" 5x5x5", "FORMATION REFERENCE","Controller: row 2","Charged cell behind");
            sign(level,base.offset(8,0,7),"Base: 2 item ports","2 fluid / 1 energy","18 interior air","Terminal: no cable");
        }
        index=0;
        for(String name:ROOMS) {
            var base=roomOrigin(index++);pad(level,base,23,23);
            var template=level.getStructureManager().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","concord_vault/rooms/"+name)).orElseThrow();
            var settings=new StructurePlaceSettings().setIgnoreEntities(true).addProcessor(JigsawReplacementProcessor.INSTANCE);
            template.placeInWorld(level,base,base,settings,level.random,3);
            for(var pos:BlockPos.betweenClosed(base,base.offset(16,8,16))) {
                if(level.getBlockEntity(pos) instanceof SpawnerBlockEntity spawner) {
                    var data=spawner.saveWithoutMetadata(level.registryAccess());data.putShort("RequiredPlayerRange",(short)0);
                    data.putShort("SpawnCount",(short)0);data.putShort("Delay",(short)32767);spawner.loadWithComponents(data,level.registryAccess());spawner.setChanged();
                }
                if(level.getBlockEntity(pos) instanceof DispenserBlockEntity dispenser) {dispenser.clearContent();dispenser.setChanged();}
            }
            sign(level,base.offset(8,0,19),name.replace('_',' '),"CONCORD VAULT ROOM","17 x 9 x 17", "Inspection, not boss");
            sign(level,base.offset(14,0,19),"Original room design","Spawner disabled","Trap launchers empty","No entities placed");
        }
        HubTransportShowcase.build(level);
        ledger.exhibitsBuilt=true;ledger.setDirty();return "Built southern bee shells, eastern Vault schematics and western isolated transport lanes.";
    }
    public static void buildServiceShell(ServerLevel level,BlockPos base,String tier) {
        keepLoaded(level,base,base.offset(4,0,6));
        for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++) {
            var pos=base.offset(x,y,z);
            if((y==1||y==2)&&x>0&&x<4&&z>0&&z<4){level.setBlock(pos,Blocks.AIR.defaultBlockState(),3);continue;}
            var state=part(tier+"_"+(y==4?"roof":y==1&&x==2&&z==4?"controller":"casing"));
            if(y==0&&z==4) {
                String id=x<2?"item_port":x==2?"energy_port":"fluid_port";
                var key=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id);
                if(!BuiltInRegistries.BLOCK.containsKey(key))throw new IllegalStateException("Missing service port "+key);
                state=BuiltInRegistries.BLOCK.get(key).defaultBlockState()
                    .setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH);
                if(x==1||x==4)state=state.setValue(net.zerog.tweaks.transport.TransportBlock.MODE,
                    net.zerog.tweaks.transport.TransportBlock.PortMode.OUTPUT);
            }
            level.setBlock(pos,state,3);
        }
        var controller=base.offset(2,1,4);
        var result=net.zerog.tweaks.genetics.AlvearyFormation.locate(level,controller,Integer.parseInt(tier.substring(4)));
        if(!result.formed())throw new IllegalStateException("Hub service shell rejected: "+tier+": "+result.error());
        var cellPos=base.offset(2,0,6);
        var cell=BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","astrium_energy_cell"));
        level.setBlock(cellPos,cell.defaultBlockState(),3);
        if(level.getBlockEntity(cellPos) instanceof net.zerog.tweaks.transport.TransportBlockEntity be){be.stored=be.capacity();java.util.Arrays.fill(be.modes,1);be.setChanged();}
        var cable=BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","astrium_energy_conduit"));
        level.setBlock(base.offset(2,0,5),cable.defaultBlockState(),3);
    }
    private static void buildMachineStations(ServerLevel level) {
        String[] ids={"alloy_forge","crystal_growth_chamber","salvage_station","combustion_generator","solar_array","fusion_reactor"};
        for(int i=0;i<ids.length;i++) {
            var base=new BlockPos(8+(i%5)*26,64,-200-(i/5)*26);pad(level,base,23,23);
            keepLoaded(level,base.offset(0,0,-2),base.offset(4,0,0));
            var key=ResourceLocation.fromNamespaceAndPath("zerog_tweaks",ids[i]);
            if(!BuiltInRegistries.BLOCK.containsKey(key))throw new IllegalStateException("Missing inspection machine "+key);
            var state=BuiltInRegistries.BLOCK.get(key).defaultBlockState();
            if(state.hasProperty(BlockStateProperties.HORIZONTAL_FACING))state=state.setValue(BlockStateProperties.HORIZONTAL_FACING,Direction.SOUTH);
            level.setBlock(base,state,3);
            for(int z=1;z<=2;z++)level.setBlock(base.offset(0,0,-z),BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",z==1?"astrium_energy_conduit":"astrium_energy_cell")).defaultBlockState(),3);
            if(level.getBlockEntity(base.offset(0,0,-2)) instanceof net.zerog.tweaks.transport.TransportBlockEntity be){be.stored=be.capacity();java.util.Arrays.fill(be.modes,0);be.setChanged();}
            level.setBlock(base.offset(2,0,0),Blocks.CHEST.defaultBlockState(),3);
            if(level.getBlockEntity(base.offset(2,0,0)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity chest){
                chest.setItem(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.COAL,64));
                chest.setItem(1,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.OAK_LOG,64));
                var fuel=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","fusion_dust");
                if(BuiltInRegistries.ITEM.containsKey(fuel))chest.setItem(2,new net.minecraft.world.item.ItemStack(BuiltInRegistries.ITEM.get(fuel),64));
            }
            sign(level,base.offset(1,0,4),ids[i].replace('_',' '),"GUI / SIDE INSPECTION","Charged cell behind","Supply recipe inputs");
        }
        for(int i=0;i<6;i++) {
            var base=new BlockPos(60+i*10,64,-230);
            keepLoaded(level,base,base.offset(4,0,0));
            String tier=net.zerog.tweaks.storage.StorageTankRegistry.TIERS[i];
            for(int x=0;x<8;x++)floor(level,base.offset(x,-1,0));
            String[] family={"energy_cell","energy_conduit","item_tube","fluid_pipe","fluid_tank"};
            for(int x=0;x<family.length;x++)level.setBlock(base.offset(x,0,0),BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",tier+"_"+family[x])).defaultBlockState(),3);
            floor(level,base.offset(0,-1,3));
            sign(level,base.offset(0,0,3),tier+" transport","CELL / CABLE / TUBE","PIPE / TANK","Configure real faces");
        }
    }
    private static void keepLoaded(ServerLevel level,BlockPos min,BlockPos max) {
        if(!PlanetTestHub.isHub(level.getServer()))throw new IllegalStateException("Inspection tickets are test-hub only");
        for(int x=min.getX()>>4;x<=max.getX()>>4;x++)for(int z=min.getZ()>>4;z<=max.getZ()>>4;z++)level.setChunkForced(x,z,true);
    }
    private static void floor(ServerLevel level,BlockPos pos) {level.setBlock(pos,BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);}
    private static void pad(ServerLevel level,BlockPos origin,int width,int depth) {
        for(int x=-3;x<width;x++)for(int z=-3;z<depth;z++)floor(level,origin.offset(x,-1,z));
        for(int x=Math.min(0,origin.getX());x<=Math.max(0,origin.getX());x++)for(int z=depth-2;z<depth;z++)floor(level,new BlockPos(x,63,origin.getZ()+z));
        for(int x:List.of(-2,width-2))level.setBlock(origin.offset(x,0,depth-2),Blocks.END_ROD.defaultBlockState(),3);
    }
    private static void sign(ServerLevel level,BlockPos pos,String... lines) {
        level.setBlock(pos,Blocks.OAK_SIGN.defaultBlockState(),3);
        if(level.getBlockEntity(pos) instanceof SignBlockEntity sign) {
            var text=sign.getFrontText();for(int i=0;i<4;i++)text=text.setMessage(i,Component.literal(lines[i]));
            sign.setText(text,true);sign.setText(text,false);sign.setChanged();
        }
    }
    private HubExhibits() {}
}
