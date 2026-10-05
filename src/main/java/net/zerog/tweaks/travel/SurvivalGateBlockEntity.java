package net.zerog.tweaks.travel;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.zerog.tweaks.config.ZGProgressionConfig;
import net.zerog.tweaks.registry.BlockInit;
import net.zerog.tweaks.registry.ZGDimensionTerrain;

/** Persistent survival controller. Every launch is checked again after the ready countdown. */
public final class SurvivalGateBlockEntity extends BlockEntity {
    public UUID owner;
    public int stored,selected=-1,countdown;
    public boolean returnPlatform;
    public String homeDimension="";
    public BlockPos homeController=BlockPos.ZERO;
    private final Set<UUID> ready=new HashSet<>();
    private Set<UUID> expected=Set.of();
    private long receiveTick=Long.MIN_VALUE;
    private int receivedThisTick;
    public final ItemStackHandler upgrades=new ItemStackHandler(4){
        @Override public boolean isItemValid(int slot,ItemStack stack){var id=BuiltInRegistries.ITEM.getKey(stack.getItem());return slot<upgradeSlots()&&id.getNamespace().equals("zerog_tweaks")&&List.of("refracting_lens","cryo_core","star_map_fragment","capacity_coil").contains(id.getPath());}
        @Override public int getSlotLimit(int slot){return 1;}
        @Override protected void onContentsChanged(int slot){setChanged();}
    };
    public SurvivalGateBlockEntity(BlockPos pos,BlockState state){super(SurvivalGates.CONTROLLER.get(),pos,state);}
    public Direction facing(){return getBlockState().getValue(BlockStateProperties.HORIZONTAL_FACING);}
    public BlockPos centre(){return SurvivalGateLayout.centre(worldPosition,facing());}
    public int formedTier(){return level instanceof ServerLevel server?SurvivalGateLayout.formedTier(server,worldPosition,facing()):0;}
    public int upgradeSlots(){int t=formedTier();return t>=6?4:t>=5?3:t>=3?2:t>=1?1:0;}
    public boolean has(String id){for(int i=0;i<upgradeSlots();i++)if(BuiltInRegistries.ITEM.getKey(upgrades.getStackInSlot(i).getItem()).equals(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id)))return true;return false;}
    public int capacity(){return ZGProgressionConfig.baseCost(Math.max(1,formedTier()))*2;}
    public IEnergyStorage energy(){return new IEnergyStorage(){
        public int receiveEnergy(int amount,boolean simulate){int tier=formedTier();if(tier==0||amount<=0)return 0;long tick=level.getGameTime();int used=receiveTick==tick?receivedThisTick:0;int rate=(1000<<(tier-1))*(has("cryo_core")?2:1);int accepted=Math.max(0,Math.min(amount,Math.min(capacity()-stored,rate-used)));if(!simulate&&accepted>0){if(receiveTick!=tick){receiveTick=tick;receivedThisTick=0;}receivedThisTick+=accepted;stored+=accepted;setChanged();}return accepted;}
        public int extractEnergy(int amount,boolean simulate){return 0;} public int getEnergyStored(){return stored;} public int getMaxEnergyStored(){return capacity();} public boolean canExtract(){return false;} public boolean canReceive(){return formedTier()>0;}
    };}
    public boolean isPort(BlockPos pos){for(var part:SurvivalGateLayout.parts(Math.max(1,formedTier())))if(part.block()==BlockInit.GATE_ENERGY_PORT.get()&&centre().offset(SurvivalGateLayout.rotate(part.offset(),facing())).equals(pos))return true;return false;}
    public void claim(ServerPlayer player){if(owner==null){owner=player.getUUID();setChanged();}}
    public boolean mayControl(ServerPlayer player){return owner!=null&&owner.equals(player.getUUID());}
    public static List<String> destinations(){var list=new ArrayList<String>();list.add("minecraft:overworld");for(String name:ZGDimensionTerrain.dimensions())list.add("zerog_tweaks:"+name);return List.copyOf(list);}
    public boolean canReach(String id){int tier=formedTier(),galaxy=SurvivalGateLayout.galaxy(id);return tier>0&&galaxy>0&&galaxy<=Math.min(5,tier)&&(!id.endsWith("_moons")||tier==6)&&!id.equals(level.dimension().location().toString());}
    public AABB pad(){int r=SurvivalGateLayout.padRadius(Math.max(1,formedTier()));BlockPos c=centre();return new AABB(Vec3.atLowerCornerOf(c.offset(-r,1,-r)),Vec3.atLowerCornerOf(c.offset(r+1,4,r+1)));}
    public List<ServerPlayer> passengers(){if(!(level instanceof ServerLevel server))return List.of();return server.getEntitiesOfClass(ServerPlayer.class,pad(),p->p.isAlive()&&!p.isSpectator());}
    public int cost(int passengers){String target=returnPlatform?homeDimension:selected>=0&&selected<destinations().size()?destinations().get(selected):"";return SurvivalGateLayout.cost(ZGProgressionConfig.baseCost(Math.max(1,formedTier())),level.dimension().location().toString(),target,passengers,has("refracting_lens"));}
    public boolean engage(ServerPlayer player){
        if(!mayControl(player)||countdown>0||formedTier()==0)return false;
        var group=passengers();if(!group.contains(player)||group.size()>SurvivalGateLayout.passengers(formedTier())+(has("capacity_coil")?2:0)||stored<cost(group.size()))return false;
        if(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))return false;
        expected=group.stream().map(ServerPlayer::getUUID).collect(java.util.stream.Collectors.toSet());ready.clear();ready.add(player.getUUID());countdown=100;setChanged();
        for(var passenger:group)passenger.displayClientMessage(Component.literal("Concord gate ready check: right-click the controller and select Ready, or step off the pad to cancel."),false);
        return true;
    }
    public void confirm(ServerPlayer player){if(countdown>0&&expected.contains(player.getUUID())&&pad().contains(player.position()))ready.add(player.getUUID());}
    public void cancel(){countdown=0;ready.clear();expected=Set.of();setChanged();}
    public void preview(ServerPlayer player){if(!(level instanceof ServerLevel server)||!mayControl(player))return;int tier=Math.min(6,Math.max(1,formedTier()+1));for(var part:SurvivalGateLayout.parts(tier)){BlockPos at=centre().offset(SurvivalGateLayout.rotate(part.offset(),facing()));if(server.hasChunkAt(at)&&!server.getBlockState(at).is(part.block()))server.sendParticles(player,ParticleTypes.END_ROD,true,at.getX()+.5,at.getY()+.5,at.getZ()+.5,2,.1,.1,.1,0);}}
    public void tick(){
        if(!(level instanceof ServerLevel server))return;
        // Return platforms trickle-charge only with their explicitly built crystal cell.
        if(returnPlatform&&server.getGameTime()%20==0&&server.getBlockState(centre().offset(0,-2,0)).is(BlockInit.CRYSTAL_CELL.get())){stored=Math.min(capacity(),stored+1000);setChanged();}
        if(countdown<=0)return;
        var group=passengers();var present=group.stream().map(ServerPlayer::getUUID).collect(java.util.stream.Collectors.toSet());
        int tier=formedTier();
        if(tier==0||group.size()>SurvivalGateLayout.passengers(tier)+(has("capacity_coil")?2:0)||!present.equals(expected)||(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))){cancel();return;}
        BlockPos c=centre();double phase=(100-countdown)*.16,radius=Math.max(.6,SurvivalGateLayout.padRadius(tier)*.75);
        for(int point=0;point<8;point++){double angle=phase+point*Math.PI/4;server.sendParticles(ParticleTypes.PORTAL,c.getX()+.5+Math.cos(angle)*radius,c.getY()+1.15+Math.sin(phase)*.12,c.getZ()+.5+Math.sin(angle)*radius,1,.04,.04,.04,.02);}
        if(countdown%10==0){
            for(var part:SurvivalGateLayout.parts(tier))if(part.block()==BlockInit.GATE_PYLON.get()&&part.offset().getY()==tier+1){BlockPos at=c.offset(SurvivalGateLayout.rotate(part.offset(),facing()));server.sendParticles(ParticleTypes.END_ROD,at.getX()+.5,at.getY()+1.05,at.getZ()+.5,2,.12,.08,.12,.005);}
            server.sendParticles(ParticleTypes.END_ROD,c.getX()+.5,c.getY()+1.2,c.getZ()+.5,4,radius,.1,radius,.04);
        }
        if(--countdown==0){if(ready.containsAll(expected))launch(group);else for(var p:group)p.displayClientMessage(Component.literal("Launch cancelled: not everyone confirmed Ready."),false);ready.clear();expected=Set.of();setChanged();}
    }
    private void launch(List<ServerPlayer> group){
        if(!(level instanceof ServerLevel source)||group.isEmpty())return;
        int tier=formedTier();if(tier==0||group.size()>SurvivalGateLayout.passengers(tier)+(has("capacity_coil")?2:0))return;
        if(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))return;
        int fee=cost(group.size());if(stored<fee)return;
        String id=returnPlatform?homeDimension:destinations().get(selected);
        ServerLevel target=PlanetTestHub.planet(source.getServer(),id);if(target==null)return;
        SurvivalGateBlockEntity landing;
        if(returnPlatform){target.getChunkAt(homeController);if(!(target.getBlockEntity(homeController) instanceof SurvivalGateBlockEntity home))return;SurvivalGateLayout.loadFootprint(target,homeController,home.facing());if(home.formedTier()==0)return;landing=home;}
        else landing=prepareArrival(target,this);
        BlockPos c=landing.centre();var pets=source.getEntitiesOfClass(Mob.class,pad(),mob->(mob instanceof TamableAnimal tame&&tame.isTame()&&group.stream().anyMatch(p->p.getUUID().equals(tame.getOwnerUUID())))||(mob.isLeashed()&&mob.getLeashHolder() instanceof ServerPlayer p&&group.contains(p)));
        // All validation and destination preparation completes before charging or moving anything.
        stored-=fee;setChanged();
        for(Mob pet:pets){pet.dropLeash(true,false);pet.changeDimension(transition(target,c));}
        for(ServerPlayer player:group){bindHome(player);var moved=player.changeDimension(transition(target,c));if(moved instanceof LivingEntity living)living.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING,100,0,false,false));}
        target.sendParticles(ParticleTypes.FLASH,c.getX()+.5,c.getY()+1.5,c.getZ()+.5,1,0,0,0,0);
        target.sendParticles(ParticleTypes.REVERSE_PORTAL,c.getX()+.5,c.getY()+1.5,c.getZ()+.5,24,1,.4,1,.04);
    }
    public void bindHome(ServerPlayer player){if(returnPlatform)return;var tag=player.getPersistentData().getCompound("zerog_home_gate");tag.putString("dimension",level.dimension().location().toString());tag.putLong("controller",worldPosition.asLong());player.getPersistentData().put("zerog_home_gate",tag);}
    public static DimensionTransition transition(ServerLevel target,BlockPos centre){return new DimensionTransition(target,new Vec3(centre.getX()+.5,centre.getY()+1,centre.getZ()+.5),Vec3.ZERO,180,0,DimensionTransition.PLAY_PORTAL_SOUND.then(DimensionTransition.PLACE_PORTAL_TICKET));}
    public static SurvivalGateBlockEntity prepareArrival(ServerLevel target,SurvivalGateBlockEntity home){
        // Deterministic gate-specific landing location; never overwrite a previous platform.
        int x=512+Math.floorMod(home.worldPosition.getX(),16)*32,z=512+Math.floorMod(home.worldPosition.getZ(),16)*32;
        target.getChunk(x>>4,z>>4);int y=Math.min(target.getMaxBuildHeight()-10,Math.max(target.getSeaLevel()+4,target.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,x,z)+3));
        BlockPos c=new BlockPos(x,y,z),controller=c.offset(0,1,-2);
        // Locate persisted platforms in the loaded column instead of rebuilding above the old one.
        for(int scan=target.getMinBuildHeight();scan<target.getMaxBuildHeight();scan++)if(target.getBlockEntity(new BlockPos(x,scan,z-2)) instanceof SurvivalGateBlockEntity existing&&existing.returnPlatform&&existing.homeController.equals(home.worldPosition)&&existing.homeDimension.equals(home.level.dimension().location().toString()))return existing;
        for(var p:BlockPos.betweenClosed(c.offset(-3,-2,-3),c.offset(3,-1,3)))target.setBlock(p,BlockInit.LANDING_PLATFORM.get().defaultBlockState(),3);
        for(var part:SurvivalGateLayout.parts(1))target.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
        target.setBlock(c.offset(0,-2,0),BlockInit.CRYSTAL_CELL.get().defaultBlockState(),3);
        var landing=(SurvivalGateBlockEntity)target.getBlockEntity(controller);landing.returnPlatform=true;landing.owner=home.owner;landing.homeController=home.worldPosition;landing.homeDimension=home.level.dimension().location().toString();landing.stored=0;landing.setChanged();return landing;
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider registries){super.saveAdditional(tag,registries);tag.putInt("FE",stored);tag.putInt("selected",selected);if(owner!=null)tag.putUUID("owner",owner);tag.putBoolean("return",returnPlatform);tag.putString("homeDimension",homeDimension);tag.putLong("homeController",homeController.asLong());tag.put("upgrades",upgrades.serializeNBT(registries));}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider registries){super.loadAdditional(tag,registries);stored=Math.max(0,Math.min(200000000,tag.getInt("FE")));selected=tag.getInt("selected");owner=tag.hasUUID("owner")?tag.getUUID("owner"):null;returnPlatform=tag.getBoolean("return");homeDimension=tag.getString("homeDimension");homeController=BlockPos.of(tag.getLong("homeController"));upgrades.deserializeNBT(registries,tag.getCompound("upgrades"));cancel();}
}
