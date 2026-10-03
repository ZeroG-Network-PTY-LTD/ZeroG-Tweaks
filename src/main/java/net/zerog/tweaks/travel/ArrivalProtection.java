package net.zerog.tweaks.travel;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.event.level.BlockEvent;
import net.neoforged.neoforge.event.level.ExplosionEvent;
import net.neoforged.neoforge.event.level.PistonEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.living.MobSpawnEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/** Only authored test-hub/planet arrival pads, not survival player-built gates. */
public final class ArrivalProtection {
    public static final int RADIUS = 10;
    public static boolean contains(LevelAccessor level, BlockPos pos) {
        return intersects(level, pos, pos);
    }
    public static boolean intersects(LevelAccessor level, BlockPos min, BlockPos max) {
        if (!(level instanceof ServerLevel server)) return false;
        String dimension = server.dimension().location().toString();
        return GateLedger.get(server.getServer()).gates.values().stream().anyMatch(g ->
            g.testPower && g.dimension.equals(dimension)
            && max.getX() >= g.centre.getX()-RADIUS && min.getX() <= g.centre.getX()+RADIUS
            && max.getZ() >= g.centre.getZ()-RADIUS && min.getZ() <= g.centre.getZ()+RADIUS
            && max.getY() >= g.centre.getY()-4 && min.getY() <= g.centre.getY()+16);
    }
    public static void breaking(BlockEvent.BreakEvent event) {
        if (contains(event.getLevel(), event.getPos())) event.setCanceled(true);
    }
    public static void placing(BlockEvent.EntityPlaceEvent event) {
        boolean protectedPosition = contains(event.getLevel(), event.getPos());
        if (event instanceof BlockEvent.EntityMultiPlaceEvent multi)
            protectedPosition |= multi.getReplacedBlockSnapshots().stream().anyMatch(s -> contains(event.getLevel(),s.getPos()));
        if (protectedPosition) event.setCanceled(true);
    }
    public static void fluid(BlockEvent.FluidPlaceBlockEvent event) {
        if (contains(event.getLevel(),event.getPos())) event.setCanceled(true);
    }
    public static void piston(PistonEvent.Pre event) {
        // Twelve-block vanilla push range plus a block at either end, across all axes.
        if (intersects(event.getLevel(),event.getPos().offset(-14,-14,-14),event.getPos().offset(14,14,14)))
            event.setCanceled(true);
    }
    public static void explosion(ExplosionEvent.Detonate event) {
        event.getAffectedBlocks().removeIf(p -> contains(event.getLevel(),p));
        event.getAffectedEntities().removeIf(e -> contains(event.getLevel(),e.blockPosition()));
    }
    public static void damage(LivingIncomingDamageEvent event) {
        if (contains(event.getEntity().level(),event.getEntity().blockPosition())) event.setCanceled(true);
    }
    public static void spawn(MobSpawnEvent.PositionCheck event) {
        if (event.getEntity() instanceof net.minecraft.world.entity.monster.Enemy
                && contains(event.getEntity().level(),event.getEntity().blockPosition()))
            event.setResult(MobSpawnEvent.PositionCheck.Result.FAIL);
    }
    public static void tick(ServerTickEvent.Post event) {
        if (event.getServer().getTickCount()%20 != 0) return;
        repairLoaded(event.getServer());
    }
    public static void repairLoaded(net.minecraft.server.MinecraftServer server) {
        if(!server.isSameThread()) throw new IllegalStateException("Arrival repairs require the server thread");
        // Repair loaded pads only. This also upgrades existing saved test-gate records.
        for (var gate : GateLedger.get(server).gates.values()) {
            if (!gate.testPower) continue;
            var level = PlanetTestHub.planet(server,gate.dimension);
            if (level == null || !level.hasChunkAt(gate.centre.offset(-8,0,-8))
                    || !level.hasChunkAt(gate.centre.offset(8,0,8))) continue;
            var expected=new java.util.HashMap<BlockPos,net.minecraft.world.level.block.Block>();
            for (int x=-8;x<=8;x++) for (int z=-8;z<=8;z++) for(int y=-2;y<=0;y++)
                expected.put(new BlockPos(x,y,z),net.zerog.tweaks.registry.BlockInit.LANDING_PLATFORM.get());
            for(var part:PlanetGate.parts()) expected.put(part.offset(),part.block());
            for (var part:expected.entrySet()) {
                var pos=gate.centre.offset(part.getKey());
                if (!level.getBlockState(pos).is(part.getValue())) level.setBlock(pos,part.getValue().defaultBlockState(),2);
            }
            // Keep the central player landing column clear of fire, falling blocks and liquids.
            for (int x=-2;x<=2;x++) for(int z=-2;z<=2;z++) for(int y=1;y<=3;y++) {
                var pos=gate.centre.offset(x,y,z);
                if (!level.getBlockState(pos).isAir()) level.setBlock(pos,Blocks.AIR.defaultBlockState(),2);
            }
        }
    }
    private ArrivalProtection() {}
}
