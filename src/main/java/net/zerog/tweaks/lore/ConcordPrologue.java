package net.zerog.tweaks.lore;

import java.util.*;
import net.minecraft.core.*;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.*;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.*;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.*;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.level.storage.loot.*;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;
import net.neoforged.fml.ModList;
import net.neoforged.neoforge.event.LootTableLoadEvent;
import net.neoforged.neoforge.event.entity.player.ItemEntityPickupEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.level.BlockEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.zerog.tweaks.registry.*;
import net.zerog.tweaks.travel.ArrivalProtection;

/** Persisted, server-thread-only Courier delivery. Never edits an existing save offline. */
public final class ConcordPrologue {
    public static final ResourceLocation COURIER=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","concord_courier");
    public static final long RECOVERY_TICKS=7*24000L;
    public static final class Signal {
        public long due, deliveredAt=-1; public int deliveries; public boolean moonGreeted;
        public final List<BlockPos> pods=new ArrayList<>();
        public final Map<String,BlockPos> controllers=new LinkedHashMap<>();
    }
    public static final class Ledger extends SavedData {
        public final Map<UUID,Signal> signals=new LinkedHashMap<>();
        public static Ledger load(CompoundTag tag,HolderLookup.Provider registries) {
            var ledger=new Ledger();
            for(var value:tag.getList("signals",Tag.TAG_COMPOUND)) {
                var data=(CompoundTag)value;var signal=new Signal();signal.due=data.getLong("due");
                signal.deliveries=data.getInt("deliveries");signal.deliveredAt=data.getLong("deliveredAt");
                signal.moonGreeted=data.getBoolean("moonGreeted");
                for(long pos:data.getLongArray("pods"))signal.pods.add(BlockPos.of(pos));
                for(var v:data.getList("controllers",Tag.TAG_COMPOUND)) {var c=(CompoundTag)v;signal.controllers.put(c.getString("key"),BlockPos.of(c.getLong("pos")));}
                ledger.signals.put(data.getUUID("player"),signal);
            } return ledger;
        }
        @Override public CompoundTag save(CompoundTag tag,HolderLookup.Provider registries) {
            var list=new ListTag();signals.forEach((id,s)->{var data=new CompoundTag();data.putUUID("player",id);
                data.putLong("due",s.due);data.putLong("deliveredAt",s.deliveredAt);data.putInt("deliveries",s.deliveries);
                data.putBoolean("moonGreeted",s.moonGreeted);
                data.putLongArray("pods",s.pods.stream().mapToLong(BlockPos::asLong).toArray());var controllers=new ListTag();
                s.controllers.forEach((key,pos)->{var c=new CompoundTag();c.putString("key",key);c.putLong("pos",pos.asLong());controllers.add(c);});
                data.put("controllers",controllers);list.add(data);});tag.put("signals",list);return tag;
        }
    }
    public static Ledger ledger(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(Ledger::new,Ledger::load),"zerog_concord_signal");
    }
    public static long nextNight(long dayTime) {
        long base=Math.floorDiv(dayTime,24000L)*24000L;
        return base+(Math.floorMod(dayTime,24000L)<13000?13000:37000);
    }
    public static void pickup(ItemEntityPickupEvent.Post event) {
        if(event.getPlayer() instanceof ServerPlayer player && event.getOriginalStack().is(ItemInit.RAW_NULLIFITE.get())) begin(player);
    }
    public static void begin(ServerPlayer player) {
        var ledger=ledger(player.server);if(ledger.signals.containsKey(player.getUUID()))return;
        var signal=new Signal();signal.due=nextNight(player.server.overworld().getDayTime());
        ledger.signals.put(player.getUUID(),signal);ledger.setDirty();
        player.sendSystemMessage(Component.translatable("message.zerog_tweaks.signal_heard"));
        if(!claimSystemsSupported())player.sendSystemMessage(Component.translatable("message.zerog_tweaks.courier_claim_adapter"));
    }
    public static void tick(ServerTickEvent.Post event) {
        var server=event.getServer();if(server.getTickCount()%100!=0)return;
        var world=server.overworld();var ledger=ledger(server);
        for(var player:server.getPlayerList().getPlayers()) {
            var signal=ledger.signals.get(player.getUUID());if(signal==null)continue;
            // Pickup hook is authoritative; carrying an ore from an old save does not retro-trigger.
            long time=world.getDayTime(), age=world.getGameTime();
            boolean recovery=recoveryDue(age,signal) && !hasRecoveryItems(player,signal);
            if(signal.deliveries>=2 || (signal.deliveries>0&&!recovery) || time<signal.due || player.serverLevel()!=world
                    || Math.floorMod(time,24000L)<13000 || Math.floorMod(time,24000L)>23000)continue;
            if(!claimSystemsSupported())continue;
            for(int attempt=0;attempt<12;attempt++) {
                double angle=world.random.nextDouble()*Math.PI*2;int distance=48+world.random.nextInt(49);
                int x=player.blockPosition().getX()+(int)(Math.cos(angle)*distance),z=player.blockPosition().getZ()+(int)(Math.sin(angle)*distance);
                if(!world.hasChunkAt(new BlockPos(x,64,z)))continue;
                var origin=new BlockPos(x-3,world.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,x,z)-1,z-3);
                if(deliver(world,origin,player,signal)) {signal.deliveries++;signal.deliveredAt=age;ledger.setDirty();
                    player.sendSystemMessage(Component.translatable("message.zerog_tweaks.courier_arrived",x,z));break;}
            }
        }
    }
    public static boolean recoveryDue(long age,Signal signal) {
        return signal.deliveries==1 && signal.deliveredAt>=0 && age-signal.deliveredAt>=RECOVERY_TICKS;
    }
    /** No supported claim adapter yet: refuse on detected claim systems rather than bypassing them. */
    public static boolean claimSystemsSupported() {
        return ModList.get().getMods().stream().noneMatch(mod->{String id=mod.getModId();return id.contains("claim")
            || id.equals("ftbchunks") || id.equals("flan") || id.equals("argonauts") || id.equals("cadmus")
            || id.equals("landprotect") || id.equals("griefdefender");});
    }
    public static boolean hasRecoveryItems(ServerPlayer player,Signal signal) {
        if(has(player.getInventory()) || has(player.getEnderChestInventory()))return true;
        for(var entry:signal.controllers.entrySet()) {
            var dimension=ResourceLocation.tryParse(entry.getKey().split("@",2)[0]);if(dimension==null)continue;
            var world=player.server.getLevel(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.DIMENSION,dimension));
            if(world!=null && (!world.hasChunkAt(entry.getValue()) || world.getBlockState(entry.getValue()).is(BlockInit.GATE_CONTROLLER.get())))return true;
        }return false;
    }
    private static boolean has(net.minecraft.world.Container inventory) {
        for(int i=0;i<inventory.getContainerSize();i++)if(inventory.getItem(i).is(ItemInit.DORMANT_WISP.get())
                ||inventory.getItem(i).is(ItemInit.GATE_CONTROLLER_ITEM.get()))return true;return false;
    }
    public static void placed(BlockEvent.EntityPlaceEvent event) {
        if(event.isCanceled() || !(event.getEntity() instanceof ServerPlayer player)
                || !event.getPlacedBlock().is(BlockInit.GATE_CONTROLLER.get()))return;
        var ledger=ledger(player.server);var signal=ledger.signals.get(player.getUUID());if(signal==null)return;
        signal.controllers.put(player.serverLevel().dimension().location()+"@"+event.getPos().asLong(),event.getPos().immutable());ledger.setDirty();
    }
    public static boolean safeSite(ServerLevel world,BlockPos origin) {
        if(!world.getServer().isSameThread() || !claimSystemsSupported() || origin.getY()<world.getMinBuildHeight()+1
                ||origin.getY()+4>=world.getMaxBuildHeight() || !world.getWorldBorder().isWithinBounds(origin)
                ||!world.getWorldBorder().isWithinBounds(origin.offset(6,4,6))
                || ArrivalProtection.intersects(world,origin,origin.offset(6,4,6)))return false;
        for(var pos:BlockPos.betweenClosed(origin,origin.offset(6,4,6))) {
            if(!world.hasChunkAt(pos)||world.getBlockEntity(pos)!=null||!world.getFluidState(pos).isEmpty())return false;
            var state=world.getBlockState(pos);
            if(pos.getY()==origin.getY()) {if(!(state.is(BlockTags.DIRT)||state.is(BlockTags.SAND)||state.is(BlockTags.BASE_STONE_OVERWORLD)))return false;}
            else if(!(state.isAir()||state.is(Blocks.SHORT_GRASS)||state.is(Blocks.TALL_GRASS)||state.is(Blocks.SNOW)))return false;
        }return world.canSeeSky(origin.offset(3,1,3));
    }
    public static boolean deliver(ServerLevel world,BlockPos origin,ServerPlayer player,Signal signal) {
        if(!safeSite(world,origin))return false;
        var template=world.getStructureManager().get(COURIER);if(template.isEmpty())return false;
        if(!template.get().placeInWorld(world,origin,origin,new StructurePlaceSettings().setIgnoreEntities(true),world.random,2))return false;
        if(!(world.getBlockEntity(origin.offset(3,1,3)) instanceof ChestBlockEntity chest))throw new IllegalStateException("Courier chest template invariant");
        chest.setItem(0,new ItemStack(ItemInit.DORMANT_WISP.get()));chest.setItem(1,new ItemStack(ItemInit.CONCORD_CODEX.get()));chest.setChanged();
        signal.pods.add(origin.immutable());
        world.sendParticles(net.minecraft.core.particles.ParticleTypes.END_ROD,origin.getX()+3.5,origin.getY()+12,origin.getZ()+3.5,80,1,8,1,.12);
        world.playSound(null,origin,net.minecraft.sounds.SoundEvents.GENERIC_EXPLODE.value(),net.minecraft.sounds.SoundSource.BLOCKS,2,.6F);
        ledger(world.getServer()).setDirty();return true;
    }
    public static void interact(PlayerInteractEvent.RightClickBlock event) {
        if(!(event.getEntity() instanceof ServerPlayer player)||player.serverLevel()!=player.server.overworld())return;
        var ledger=ledger(player.server);boolean found=false;
        for(var signal:ledger.signals.values())for(var origin:signal.pods)if(event.getPos().distSqr(origin.offset(3,1,3))<=25) {
            found=true;
            if(event.getPos().equals(origin.offset(3,1,1)) && player.serverLevel().getBlockState(event.getPos()).is(BlockInit.BROKEN_CONSOLE.get()))
                player.sendSystemMessage(Component.translatable("message.zerog_tweaks.courier_console"));
        }
        if(found)grant(player,"falling_star","found_pod");
    }
    public static void greeting(PlayerInteractEvent.EntityInteract event) {
        if(event.getHand()!=net.minecraft.world.InteractionHand.MAIN_HAND || !(event.getEntity() instanceof ServerPlayer player)
                || !(event.getTarget() instanceof net.zerog.tweaks.entity.PlanetVillager villager)
                || !villager.species().equals("lunari")
                || !player.serverLevel().dimension().location().equals(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","moon")))return;
        var ledger=ledger(player.server);var signal=ledger.signals.get(player.getUUID());
        if(signal!=null && signal.deliveries>0 && !signal.moonGreeted) {
            player.sendSystemMessage(Component.translatable("message.zerog_tweaks.lunari_signal_greeting"));
            signal.moonGreeted=true;ledger.setDirty();
        }
    }
    public static void grant(ServerPlayer player,String advancement,String criterion) {
        var holder=player.server.getAdvancements().get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks","codex/"+advancement));
        if(holder!=null)player.getAdvancements().award(holder,criterion);
    }
    public static void loot(LootTableLoadEvent event) {
        if(event.getName().equals(ResourceLocation.withDefaultNamespace("chests/ancient_city"))
                && event.getTable().getPool("zerog_dormant_wisp_backup")==null)
            event.getTable().addPool(LootPool.lootPool().name("zerog_dormant_wisp_backup").setRolls(ConstantValue.exactly(1))
                .when(LootItemRandomChanceCondition.randomChance(.05F)).add(LootItem.lootTableItem(ItemInit.DORMANT_WISP.get())).build());
    }
    private ConcordPrologue() {}
}
