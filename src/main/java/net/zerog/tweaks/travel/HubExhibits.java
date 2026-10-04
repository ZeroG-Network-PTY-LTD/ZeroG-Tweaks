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

/** Bounded inspection district north of the explicit hub. Never clears player builds. */
public final class HubExhibits {
    public static final List<String> ROOMS=List.of("collapsed_mine","concord_shrine","crystal_garden","forge","observatory",
            "prismling_nest","star_library","starlight_pool","storage_hall","trap_hall");
    public static final List<String> VALIDATED_TIERS=List.of("tier3","tier5","tier6","tier7");
    public static BlockPos designOrigin(int index) {return new BlockPos(8+(index%4)*32,64,-42-(index/4)*32);}
    public static BlockPos formedOrigin(int index) {return new BlockPos(8+index*32,64,-102);}
    public static BlockPos roomOrigin(int index) {return new BlockPos(8+(index%5)*26,64,-134-(index/5)*30);}
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
            for(var layout:MultiblockGuides.layouts())for(var cell:layout.cells())part(prefix(layout.id())+"_"+cell.part());
            part("geno_station");part("genetic_splicer");
            for(var tier:VALIDATED_TIERS)for(String name:List.of("casing","roof","controller","energy_port","frame_housing"))part(tier+"_"+name);
            for(String room:ROOMS)if(level.getStructureManager().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","concord_vault/rooms/"+room)).isEmpty())
                return "Missing room template: "+room;
        } catch(IllegalStateException absent) {return absent.getMessage()+"; gallery not placed.";}
        // These previously unused northern plots must be empty above native ground.
        for(var pos:BlockPos.betweenClosed(new BlockPos(-2,63,-170),new BlockPos(136,77,-15))) {
            var state=level.getBlockState(pos);
            if(pos.getY()==63) {
                if(!state.isAir() && !state.is(Blocks.STONE) && !state.is(BlockInit.LANDING_PLATFORM.get()))
                    return "Gallery floor occupied at "+pos.toShortString()+"; nothing overwritten.";
            } else if(!state.isAir())return "Gallery plot occupied at "+pos.toShortString()+"; nothing overwritten.";
        }
        // Raised pads and 360-degree aisles; gates at Z>=17 are outside this district.
        for(int z=-170;z<=-15;z++)for(int x=-1;x<=1;x++)floor(level,new BlockPos(x,63,z));
        for(int x=0;x<=62;x++)for(int z=-18;z<=-16;z++)floor(level,new BlockPos(x,63,z));
        sign(level,new BlockPos(62,64,-17),"NORTH: EXHIBITS","8 authored designs","4 formed references","10 Vault rooms");
        int index=0;
        for(var layout:MultiblockGuides.layouts()) {
            var base=designOrigin(index++);pad(level,base,24,20);
            for(var cell:layout.cells())level.setBlock(base.offset(cell.x(),cell.y(),cell.z()),part(prefix(layout.id())+"_"+cell.part()),3);
            String name=layout.id().equals("cosmic_alveary")?"Cosmic Alveary":prefix(layout.id())+" "+layout.id().split("_")[1];
            sign(level,base.offset(2,0,layout.maxZ()+3),name,"AUTHORED DESIGN",layout.cells().size()+" block cells","G: layer/360 guide");
            sign(level,base.offset(7,0,layout.maxZ()+3),"Not a 5x5 validator","Front: controller","Frame housing slots","Ports: follow guide");
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
            for(int y=0;y<5;y++)for(int x=0;x<5;x++)for(int z=0;z<5;z++) {
                if((y==1||y==2)&&x>0&&x<4&&z>0&&z<4)continue;
                String name=y==4?"roof":"casing";
                if(y==0&&x==4&&z==4)name="controller";
                else if(y==0&&x==0&&z==0)name="energy_port";
                else if(y==1&&x==2&&z==4)name="frame_housing";
                level.setBlock(base.offset(x,y,z),part(tier+"_"+name),3);
            }
            sign(level,base.offset(2,0,7),tier+" 5x5x5", "FORMATION REFERENCE","Controller: SE base","Not auto-powered");
            sign(level,base.offset(8,0,7),"107 shell blocks","18 interior air","Energy: NW base","Frames: south wall");
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
        ledger.exhibitsBuilt=true;ledger.setDirty();return "Built 8 authored apiaries, 4 formation examples and 10 Vault rooms north of the hub.";
    }
    private static void floor(ServerLevel level,BlockPos pos) {level.setBlock(pos,BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);}
    private static void pad(ServerLevel level,BlockPos origin,int width,int depth) {
        for(int x=-3;x<width;x++)for(int z=-3;z<depth;z++)floor(level,origin.offset(x,-1,z));
        for(int x=0;x<=origin.getX();x++)for(int z=depth-2;z<depth;z++)floor(level,new BlockPos(x,63,origin.getZ()+z));
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
