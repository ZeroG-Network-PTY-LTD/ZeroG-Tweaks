package net.zerog.tweaks.travel;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.saveddata.SavedData;
import net.neoforged.neoforge.energy.IEnergyStorage;

/** Persisted routes and FE buffers; unlimited power is opt-in on test-world records only. */
public final class GateLedger extends SavedData {
    public static final int CAPACITY=50_000_000,TRAVEL_COST=50_000_000;
    public final Map<String,Gate> gates=new LinkedHashMap<>();
    public boolean hubBuilt;
    public boolean tieredHubBuilt;
    public boolean playerHubBuilt;
    public boolean compactHub;
    public boolean exhibitsBuilt;
    public boolean workshopBuilt;
    public int prepared;
    // Absent in older saves: never retrofit preview settlements automatically.
    public boolean inspectionEnabled;
    public int inspectionPrepared;
    public final Map<String,java.util.List<BlockPos>> inspectionVillages=new LinkedHashMap<>();
    public static final class Gate {
        public final String dimension,target;public final BlockPos centre;public final boolean testPower;
        public int energy;
        public Gate(String dimension,BlockPos centre,String target,boolean testPower) {
            this.dimension=dimension;this.centre=centre;this.target=target;this.testPower=testPower;
        }
    }
    public static GateLedger get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(GateLedger::new,GateLedger::load),"zerog_planet_gates");
    }
    public static String key(String dimension,BlockPos centre) {return dimension+"@"+centre.asLong();}
    public void add(Gate gate) {gates.put(key(gate.dimension,gate.centre),gate);setDirty();}
    public static GateLedger load(CompoundTag tag,HolderLookup.Provider registries) {
        var ledger=new GateLedger();ledger.hubBuilt=tag.getBoolean("hubBuilt");ledger.prepared=tag.getInt("prepared");
        ledger.tieredHubBuilt=tag.getBoolean("tieredHubBuilt");
        ledger.playerHubBuilt=tag.getBoolean("playerHubBuilt");
        ledger.compactHub=tag.getBoolean("compactHub");
        ledger.exhibitsBuilt=tag.getBoolean("exhibitsBuilt");
        ledger.workshopBuilt=tag.getBoolean("workshopBuilt");
        ledger.inspectionEnabled=tag.getBoolean("inspectionEnabled");ledger.inspectionPrepared=tag.getInt("inspectionPrepared");
        for(var value:tag.getList("inspectionVillages",Tag.TAG_COMPOUND)) {
            var data=(CompoundTag)value;
            ledger.inspectionVillages.computeIfAbsent(data.getString("dimension"),k->new java.util.ArrayList<>()).add(BlockPos.of(data.getLong("centre")));
        }
        for(var value:tag.getList("gates",Tag.TAG_COMPOUND)) {
            var data=(CompoundTag)value;
            var gate=new Gate(data.getString("dimension"),BlockPos.of(data.getLong("centre")),data.getString("target"),data.getBoolean("testPower"));
            gate.energy=Math.max(0,Math.min(CAPACITY,data.getInt("energy")));ledger.gates.put(key(gate.dimension,gate.centre),gate);
        }
        return ledger;
    }
    @Override public CompoundTag save(CompoundTag tag,HolderLookup.Provider registries) {
        tag.putBoolean("hubBuilt",hubBuilt);tag.putInt("prepared",prepared);var list=new ListTag();
        tag.putBoolean("tieredHubBuilt",tieredHubBuilt);
        tag.putBoolean("playerHubBuilt",playerHubBuilt);
        tag.putBoolean("compactHub",compactHub);
        tag.putBoolean("exhibitsBuilt",exhibitsBuilt);
        tag.putBoolean("workshopBuilt",workshopBuilt);
        tag.putBoolean("inspectionEnabled",inspectionEnabled);tag.putInt("inspectionPrepared",inspectionPrepared);
        var villages=new ListTag();inspectionVillages.forEach((dimension,positions)->positions.forEach(position->{
            var data=new CompoundTag();data.putString("dimension",dimension);data.putLong("centre",position.asLong());villages.add(data);
        }));tag.put("inspectionVillages",villages);
        for(var gate:gates.values()) {
            var data=new CompoundTag();data.putString("dimension",gate.dimension);data.putLong("centre",gate.centre.asLong());
            data.putString("target",gate.target);data.putBoolean("testPower",gate.testPower);data.putInt("energy",gate.energy);list.add(data);
        }
        tag.put("gates",list);return tag;
    }
    public Gate controller(ServerLevel level,BlockPos pos) {
        return gates.values().stream().filter(g->g.dimension.equals(level.dimension().location().toString())
                && PlanetGate.controller(g.centre).equals(pos)).findFirst().orElse(null);
    }
    public IEnergyStorage input(ServerLevel level,BlockPos pos) {
        var gate=gates.values().stream().filter(g->g.dimension.equals(level.dimension().location().toString())
                && PlanetGate.parts().stream().anyMatch(p->p.block()==net.zerog.tweaks.registry.BlockInit.GATE_ENERGY_PORT.get()
                &&g.centre.offset(p.offset()).equals(pos))).findFirst().orElse(null);
        if(gate==null)return null;
        return new IEnergyStorage() {
            public int receiveEnergy(int max,boolean simulate) {
                if(gate.testPower||max<=0||PlanetGate.missing(level,gate.centre)!=null)return 0;
                int accepted=Math.min(max,CAPACITY-gate.energy);
                if(!simulate&&accepted>0){gate.energy+=accepted;setDirty();}return accepted;
            }
            public int extractEnergy(int max,boolean simulate){return 0;}
            public int getEnergyStored(){return gate.testPower?CAPACITY:gate.energy;}
            public int getMaxEnergyStored(){return CAPACITY;}
            public boolean canExtract(){return false;}
            public boolean canReceive(){return !gate.testPower;}
        };
    }
}
