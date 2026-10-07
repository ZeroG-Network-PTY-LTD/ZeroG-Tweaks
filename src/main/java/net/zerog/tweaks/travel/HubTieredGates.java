package net.zerog.tweaks.travel;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;

/** One-time, hub-only replacement of the authored northern legacy gate exhibits. */
public final class HubTieredGates {
    public static final String ADMIN="zerog_tweaks:hub_admin_gate";
    public static BlockPos centre(int tier){return PlanetTestHub.hubCentre(tier-1);}
    public static boolean controllerPosition(BlockPos pos){for(int t=1;t<=6;t++)if(centre(t).offset(0,1,-2).equals(pos))return true;return false;}
    public static void build(ServerLevel level){
        if(level!=level.getServer().overworld()||!PlanetTestHub.isHub(level.getServer()))return;
        var ledger=GateLedger.get(level.getServer());if(ledger.tieredHubBuilt)return;
        // Remove only known legacy exhibits and matching authored parts, not arbitrary player blocks.
        for(int i=0;i<net.zerog.tweaks.registry.ZGDimensionTerrain.dimensions().size();i++){
            var c=PlanetTestHub.hubCentre(i);
            for(var part:PlanetGate.parts()){var at=c.offset(part.offset());if(level.getBlockState(at).is(part.block()))level.setBlock(at,Blocks.AIR.defaultBlockState(),3);}
            var sign=c.offset(0,1,-8);if(level.getBlockEntity(sign) instanceof SignBlockEntity)level.removeBlock(sign,false);
            ledger.gates.remove(GateLedger.key("minecraft:overworld",c));
        }
        String[] targets={"moon","cerulon","skarn","eidolon","solvane","g5_moons"};
        for(int tier=1;tier<=6;tier++){
            var c=centre(tier);
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
            var be=level.getBlockEntity(c.offset(0,1,-2));
            if(!(be instanceof SurvivalGateBlockEntity gate))throw new IllegalStateException("Missing tiered hub controller");
            gate.getPersistentData().putBoolean(ADMIN,true);gate.stored=gate.capacity();gate.selected=SurvivalGateBlockEntity.destinations().indexOf("zerog_tweaks:"+targets[tier-1]);gate.setChanged();
            if(gate.formedTier()!=tier)throw new IllegalStateException("Hub tier "+tier+" failed formation");
            var pos=c.offset(0,1,-10);level.setBlock(pos,Blocks.OAK_SIGN.defaultBlockState(),3);
            if(level.getBlockEntity(pos) instanceof SignBlockEntity sign){var text=sign.getFrontText();String[] lines={"CONCORD TIER "+tier,"ADMIN TEST POWER","Choose destination","Stand on pad"};for(int n=0;n<4;n++)text=text.setMessage(n,Component.literal(lines[n]));sign.setText(text,true);sign.setChanged();}
        }
        ledger.tieredHubBuilt=true;ledger.setDirty();
    }
    private HubTieredGates(){}
}
