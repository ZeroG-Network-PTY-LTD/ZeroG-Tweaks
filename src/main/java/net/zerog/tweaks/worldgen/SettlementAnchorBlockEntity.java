package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.zerog.tweaks.registry.BlockEntityInit;

public final class SettlementAnchorBlockEntity extends BlockEntity {
    private int residents;
    private int speciesResidents;
    private int layout;
    public SettlementAnchorBlockEntity(BlockPos pos,BlockState state) {super(BlockEntityInit.SETTLEMENT_ANCHOR.get(),pos,state);}
    public void configure(int layout) {this.layout=layout;setChanged();}
    public int residentsCreated() {return residents;}
    public int speciesResidentsCreated() {return speciesResidents;}
    public static void tick(Level world,BlockPos pos,BlockState state,SettlementAnchorBlockEntity anchor) {
        if(!(world instanceof ServerLevel server) || !server.getServer().isSameThread()
                || server.getGameTime()%20 != 0 || (anchor.residents>=6 && anchor.speciesResidents>=2)) return;
        anchor.populate(server);
    }
    public void populate(ServerLevel server) {
        if(!server.getServer().isSameThread()) throw new IllegalStateException("Residents must be created on the server thread");
        var anchor=this;var pos=worldPosition;
        for(int x=-20;x<=20;x+=20) for(int z=-20;z<=20;z+=20)
            if(!server.hasChunkAt(pos.offset(x,0,z))) return;
        var homes=PlanetSettlementFeature.homes(anchor.layout);
        for(;anchor.residents<6;anchor.residents++) {
            var home=homes.get(anchor.residents/2);
            var at=pos.offset(home.getX()+(anchor.residents%2==0?-1:1),1,home.getZ());
            if(!server.getBlockState(at).isAir() || !server.getBlockState(at.above()).isAir()) return;
            var id=java.util.UUID.nameUUIDFromBytes((server.dimension().location()+"/"+pos.asLong()+"/resident/"+anchor.residents)
                    .getBytes(java.nio.charset.StandardCharsets.UTF_8));
            if(server.getEntity(id)!=null) {anchor.setChanged();continue;}
            var villager=EntityType.VILLAGER.create(server);if(villager==null) return;
            villager.setUUID(id);villager.moveTo(at.getX()+.5,at.getY(),at.getZ()+.5,0,0);villager.setPersistenceRequired();
            String theme=PlanetEcologyProfile.theme(server.dimension().location().getPath());
            var clothing=net.zerog.tweaks.registry.ZGVillagerAttire.TYPES.get(theme+"_space_"+Math.floorMod(id.hashCode(),4)).get();
            villager.setVillagerData(villager.getVillagerData().setType(clothing));
            if(!server.addFreshEntity(villager)) return;anchor.setChanged();
        }
        String theme=PlanetEcologyProfile.theme(server.dimension().location().getPath());
        String species=net.zerog.tweaks.registry.ZGPlanetVillagers.THEMES.get(theme);
        if(species==null)return;
        for(;speciesResidents<2;speciesResidents++) {
            var at=pos.offset(speciesResidents==0?-3:3,1,0);
            if(!server.getBlockState(at).isAir() || !server.getBlockState(at.above()).isAir())return;
            var id=java.util.UUID.nameUUIDFromBytes((server.dimension().location()+"/"+pos.asLong()+"/species/"+speciesResidents)
                    .getBytes(java.nio.charset.StandardCharsets.UTF_8));
            if(server.getEntity(id)!=null){setChanged();continue;}
            var villager=net.zerog.tweaks.registry.ZGPlanetVillagers.TYPES.get(species).get().create(server);
            if(villager==null)return;
            villager.setUUID(id);villager.setStyle(id.hashCode());villager.moveTo(at.getX()+.5,at.getY(),at.getZ()+.5,0,0);
            villager.setPersistenceRequired();
            if(!server.addFreshEntity(villager))return;setChanged();
        }
        anchor.setChanged();
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider registries) {
        super.saveAdditional(tag,registries);tag.putInt("residents",residents);tag.putInt("layout",layout);tag.putInt("speciesResidents",speciesResidents);
    }
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider registries) {
        super.loadAdditional(tag,registries);residents=Math.max(0,Math.min(6,tag.getInt("residents")));layout=Math.floorMod(tag.getInt("layout"),4);
        speciesResidents=Math.max(0,Math.min(2,tag.getInt("speciesResidents")));
    }
}
