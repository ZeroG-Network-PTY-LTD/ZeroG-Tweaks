package net.zerog.tweaks.travel;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.SignBlockEntity;

/** One-time, hub-only replacement of the authored northern legacy gate exhibits. */
public final class HubTieredGates {
    public static final String ADMIN="zerog_tweaks:hub_admin_gate";
    public static BlockPos centre(int tier){return new BlockPos(-22+((tier-1)%3)*22,64,-22-((tier-1)/3)*22);}
    public static BlockPos playerCentre(int tier){return centre(tier).offset(0,0,-44);}
    public static boolean controllerPosition(BlockPos pos){for(int t=1;t<=6;t++)if(centre(t).offset(0,1,-2).equals(pos))return true;return false;}
    /** Compact destination cluster for the twelve known hub gates only. Ordinary survival locations stay unchanged. */
    public static BlockPos landingColumn(BlockPos controller){
        for(int set=0;set<2;set++)for(int t=1;t<=6;t++){
            var c=set==0?centre(t):playerCentre(t);
            if(c.offset(0,1,-2).equals(controller)){int i=set*6+t-1;return new BlockPos(520+(i%3)*16,0,520+(i/3)*16);}
        }
        return null;
    }
    public static void build(ServerLevel level){
        if(level!=level.getServer().overworld()||!PlanetTestHub.isHub(level.getServer()))return;
        var ledger=GateLedger.get(level.getServer());if(ledger.tieredHubBuilt){buildPlayers(level);return;}
        // Remove only known legacy exhibits and matching authored parts, not arbitrary player blocks.
        for(int i=0;!ledger.compactHub&&i<net.zerog.tweaks.registry.ZGDimensionTerrain.dimensions().size();i++){
            var c=PlanetTestHub.hubCentre(i);
            for(var part:PlanetGate.parts()){var at=c.offset(part.offset());if(level.getBlockState(at).is(part.block()))level.setBlock(at,Blocks.AIR.defaultBlockState(),3);}
            var sign=c.offset(0,1,-8);if(level.getBlockEntity(sign) instanceof SignBlockEntity)level.removeBlock(sign,false);
            ledger.gates.remove(GateLedger.key("minecraft:overworld",c));
        }
        String[] targets={"moon","cerulon","skarn","eidolon","solvane","g5_moons"};
        for(int tier=1;tier<=6;tier++){
            var c=centre(tier);
            int radius=tier+1;
            for(var pos:BlockPos.betweenClosed(c.offset(-radius,-1,-radius),c.offset(radius,-1,radius)))level.setBlock(pos,net.zerog.tweaks.registry.BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
            var be=level.getBlockEntity(c.offset(0,1,-2));
            if(!(be instanceof SurvivalGateBlockEntity gate))throw new IllegalStateException("Missing tiered hub controller");
            gate.getPersistentData().putBoolean(ADMIN,true);gate.stored=gate.capacity();gate.selected=SurvivalGateBlockEntity.destinations().indexOf("zerog_tweaks:"+targets[tier-1]);gate.setChanged();
            if(gate.formedTier()!=tier)throw new IllegalStateException("Hub tier "+tier+" failed formation");
            var pos=c.offset(0,1,-10);level.setBlock(pos,Blocks.OAK_SIGN.defaultBlockState(),3);
            if(level.getBlockEntity(pos) instanceof SignBlockEntity sign){var text=sign.getFrontText();String[] lines={"CONCORD TIER "+tier,"ADMIN TEST POWER","Choose destination","Stand on pad"};for(int n=0;n<4;n++)text=text.setMessage(n,Component.literal(lines[n]));sign.setText(text,true);sign.setChanged();}
        }
        ledger.tieredHubBuilt=true;ledger.setDirty();buildPlayers(level);
    }
    /** Normal finite FE and tier rules, never marked ADMIN or entered in the legacy route ledger. */
    private static void buildPlayers(ServerLevel level){
        var ledger=GateLedger.get(level.getServer());if(ledger.playerHubBuilt)return;
        String[] targets={"moon","cerulon","skarn","eidolon","solvane","g5_moons"};
        for(int tier=1;tier<=6;tier++){
            var c=playerCentre(tier);int radius=tier+1;
            for(var pos:BlockPos.betweenClosed(c.offset(-radius,-1,-radius),c.offset(radius,-1,radius)))level.setBlock(pos,net.zerog.tweaks.registry.BlockInit.LANDING_PLATFORM.get().defaultBlockState(),2);
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
            var gate=(SurvivalGateBlockEntity)level.getBlockEntity(c.offset(0,1,-2));
            if(gate==null||gate.formedTier()!=tier||gate.adminTest())throw new IllegalStateException("Player gate tier "+tier+" failed formation");
            gate.selected=SurvivalGateBlockEntity.destinations().indexOf("zerog_tweaks:"+targets[tier-1]);gate.stored=0;gate.setChanged();
            String metal=net.zerog.tweaks.transport.TransportTier.ALL[tier-1].name();
            var cablePos=c.offset(3,1,0);var cellPos=c.offset(3,2,0);var generatorPos=c.offset(4,1,0);
            var cableBlock=net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",metal+"_energy_conduit"));
            var cellBlock=net.minecraft.core.registries.BuiltInRegistries.BLOCK.get(net.minecraft.resources.ResourceLocation.fromNamespaceAndPath("zerog_tweaks",metal+"_energy_cell"));
            level.setBlock(cablePos,cableBlock.defaultBlockState(),3);
            level.setBlock(cellPos,cellBlock.defaultBlockState(),3);
            level.setBlock(generatorPos,net.zerog.tweaks.registry.BlockInit.COMBUSTION_GENERATOR.get().defaultBlockState(),3);
            var cable=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(cablePos);
            var cell=(net.zerog.tweaks.transport.TransportBlockEntity)level.getBlockEntity(cellPos);
            java.util.Arrays.fill(cable.modes,3);cable.modes[net.minecraft.core.Direction.WEST.ordinal()]=1;cable.modes[net.minecraft.core.Direction.EAST.ordinal()]=2;cable.modes[net.minecraft.core.Direction.UP.ordinal()]=2;cable.setChanged();
            java.util.Arrays.fill(cell.modes,3);cell.modes[net.minecraft.core.Direction.DOWN.ordinal()]=1;cell.stored=Math.min(cell.capacity(),gate.capacity());cell.setChanged();
            var generator=(net.zerog.tweaks.machine.CombustionBlockEntity)level.getBlockEntity(generatorPos);
            generator.fuel.setStackInSlot(0,new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.COAL,64));generator.setChanged();
            var signPos=c.offset(0,1,-10);level.setBlock(signPos,Blocks.OAK_SIGN.defaultBlockState(),3);
            if(level.getBlockEntity(signPos) instanceof SignBlockEntity sign){var text=sign.getFrontText();String[] lines={"PLAYER TIER "+tier,"FINITE FE / NORMAL COST","Cell + coal -> PORT","Claim terminal; stand pad"};for(int n=0;n<4;n++)text=text.setMessage(n,Component.literal(lines[n]));sign.setText(text,true);sign.setText(text,false);sign.setChanged();}
        }
        for(int z=-99;z<=-54;z++)for(int x=-1;x<=1;x++)path(level,new BlockPos(x,63,z));
        for(int z:new int[]{-33,-55,-77,-99})for(int x=-31;x<=31;x++)for(int dz=0;dz<2;dz++)path(level,new BlockPos(x,63,z+dz));
        ledger.playerHubBuilt=true;ledger.setDirty();
    }
    private static void path(ServerLevel level,BlockPos pos){var state=level.getBlockState(pos);if(state.isAir()||state.is(Blocks.STONE))level.setBlock(pos,Blocks.STONE_BRICKS.defaultBlockState(),2);}
    private HubTieredGates(){}
}
