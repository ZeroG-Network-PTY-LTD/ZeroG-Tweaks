package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.PlanetTestHub;

/** Native collision checks; no client visuals or automatic natural placement. */
@GameTestHolder("zerog_gallery_clearance") @PrefixGameTestTemplate(false)
public final class StructureGalleryCollisionGameTests {
    @GameTest(templateNamespace="zerog_gallery_clearance",template="equipment_empty",timeoutTicks=2000)
    public static void gallery_stairs_have_native_headroom_loot_and_spawners(GameTestHelper h) {
        String[] planets={"cerulon","skarn","eidolon"};
        String[] structures={"water_bio_habitat","hot_ring_monolith","ice_spire_outpost"};
        var origin=new BlockPos(768,160,768);
        for(int index=0;index<3;index++) {
            var level=PlanetTestHub.planet(h.getLevel().getServer(),"zerog_tweaks:"+planets[index]);
            h.assertTrue(level!=null,"Missing planet fixture");
            for(int x=48;x<=51;x++)for(int z=48;z<=51;z++)level.getChunk(x,z);
            var template=level.getStructureManager().getOrCreate(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","planetary_showcase/"+structures[index]));
            h.assertTrue(template.placeInWorld(level,origin,origin,new StructurePlaceSettings(),level.random,2),"Template did not place");
            int width=net.zerog.tweaks.travel.PlanetShowcaseSites.width(structures[index]),depth=net.zerog.tweaks.travel.PlanetShowcaseSites.surface(structures[index]),c=width/2;
            for(int step=0;step<depth-1;step++)for(int x=c-1;x<=c+1;x++) {
                var floor=origin.offset(x,1+step,c+2+step);
                h.assertTrue(!level.getBlockState(floor).getCollisionShape(level,floor).isEmpty(),"Missing stair support");
                for(int dy=1;dy<=3;dy++) {
                    var cell=floor.above(dy);
                    h.assertTrue(level.getBlockState(cell).getCollisionShape(level,cell).isEmpty(),"Native stair collision at "+structures[index]+" step="+step);
                }
            }
            for(int x:new int[]{8,width-9})for(int z:new int[]{8,width-9}) {
                var pos=origin.offset(x,2,z);
                h.assertTrue(level.getBlockEntity(pos) instanceof ChestBlockEntity,"Missing loot-room chest");
                var chest=(ChestBlockEntity)level.getBlockEntity(pos);
                boolean present=false;for(int slot=0;slot<27;slot++)present|=!chest.getItem(slot).isEmpty();
                h.assertTrue(present,"No generated loot");
                for(int dy=0;dy<2;dy++) {
                    var at=origin.offset(x-1,2+dy,z);
                    h.assertTrue(level.getBlockState(at).getCollisionShape(level,at).isEmpty(),"Blocked chest approach");
                }
            }
            h.assertTrue(level.getBlockEntity(origin.offset(c-4,2,c-4)) instanceof SpawnerBlockEntity,"Missing hostile spawner");
        }
        h.succeed();
    }
}
