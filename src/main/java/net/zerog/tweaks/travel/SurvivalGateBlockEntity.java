package net.zerog.tweaks.travel;

import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
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
    /** Launch sequence (design doc): lock-on 0-2s, rift 2-3.5s, lift 3.5-5s over the 100-tick countdown. */
    private static final int RIFT_AT=40,LIFT_AT=70;
    private static final DustParticleOptions RIFT=new DustParticleOptions(new org.joml.Vector3f(.32F,.08F,.55F),1.4F);
    private int litTier,litColumns;
    private boolean lifting;
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
    public boolean adminTest(){return level instanceof ServerLevel server&&getPersistentData().getBoolean(HubTieredGates.ADMIN)&&PlanetTestHub.isHub(server.getServer())&&(!returnPlatform?server==server.getServer().overworld()&&HubTieredGates.controllerPosition(worldPosition):homeDimension.equals("minecraft:overworld")&&HubTieredGates.controllerPosition(homeController));}
    public boolean mayControl(ServerPlayer player){return adminTest()||owner!=null&&owner.equals(player.getUUID());}
    public static List<String> destinations(){var list=new ArrayList<String>();list.add("minecraft:overworld");for(String name:ZGDimensionTerrain.dimensions())list.add("zerog_tweaks:"+name);return List.copyOf(list);}
    public boolean canReach(String id){int tier=formedTier(),galaxy=SurvivalGateLayout.galaxy(id);return tier>0&&galaxy>0&&(adminTest()||galaxy<=Math.min(5,tier))&&!id.equals(level.dimension().location().toString());}
    public AABB pad(){int r=SurvivalGateLayout.padRadius(Math.max(1,formedTier()));BlockPos c=centre();return new AABB(Vec3.atLowerCornerOf(c.offset(-r,1,-r)),Vec3.atLowerCornerOf(c.offset(r+1,4,r+1)));}
    public List<ServerPlayer> passengers(){if(!(level instanceof ServerLevel server))return List.of();return server.getEntitiesOfClass(ServerPlayer.class,pad(),p->p.isAlive()&&!p.isSpectator());}
    public int cost(int passengers){if(adminTest())return 0;String target=returnPlatform?homeDimension:selected>=0&&selected<destinations().size()?destinations().get(selected):"";return SurvivalGateLayout.cost(ZGProgressionConfig.baseCost(Math.max(1,formedTier())),level.dimension().location().toString(),target,passengers,has("refracting_lens"));}
    public boolean engage(ServerPlayer player){
        if(!mayControl(player)||countdown>0||formedTier()==0)return false;
        var group=passengers();if(!group.contains(player)||group.size()>SurvivalGateLayout.passengers(formedTier())+(has("capacity_coil")?2:0)||stored<cost(group.size()))return false;
        if(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))return false;
        expected=group.stream().map(ServerPlayer::getUUID).collect(java.util.stream.Collectors.toSet());ready.clear();ready.add(player.getUUID());countdown=100;setChanged();
        for(var passenger:group)passenger.displayClientMessage(Component.literal("Concord gate ready check: right-click the controller and select Ready, or step off the pad to cancel."),false);
        return true;
    }
    public void confirm(ServerPlayer player){if(countdown>0&&expected.contains(player.getUUID())&&pad().contains(player.position()))ready.add(player.getUUID());}
    public void cancel(){if(lifting&&level instanceof ServerLevel server)stopLift(server);countdown=0;lifting=false;ready.clear();expected=Set.of();setChanged();}
    /** Drop anyone already floating and clear their white-out. Pylons go dark on the next idle tick. */
    private void stopLift(ServerLevel server){
        for(UUID id:expected){var p=server.getServer().getPlayerList().getPlayer(id);if(p!=null){p.removeEffect(MobEffects.LEVITATION);GateLaunchSync.sendLift(p,0);}}
        lifting=false;
    }
    /** Pylon columns of a tier (world positions, bottom to top), in order around the pad. */
    private List<List<BlockPos>> pylonColumns(int tier){
        BlockPos c=centre();var columns=new LinkedHashMap<Long,List<BlockPos>>();
        for(var part:SurvivalGateLayout.parts(tier))if(part.block()==BlockInit.GATE_PYLON.get()){BlockPos at=c.offset(SurvivalGateLayout.rotate(part.offset(),facing()));columns.computeIfAbsent(BlockPos.asLong(at.getX(),0,at.getZ()),k->new ArrayList<>()).add(at);}
        var list=new ArrayList<>(columns.values());list.forEach(column->column.sort(Comparator.comparingInt(BlockPos::getY)));
        list.sort(Comparator.comparingDouble(column->Math.atan2(column.get(0).getZ()-c.getZ(),column.get(0).getX()-c.getX())));
        return list;
    }
    /** Light the first {@code count} pylon columns of {@code tier}; 0 puts them all out. */
    private void lightPylons(ServerLevel server,int tier,int count){
        var columns=pylonColumns(tier);
        for(int i=0;i<columns.size();i++)for(BlockPos at:columns.get(i)){var state=server.getBlockState(at);boolean lit=i<count;if(state.is(BlockInit.GATE_PYLON.get())&&state.getValue(GatePylonBlock.LIT)!=lit)server.setBlock(at,state.setValue(GatePylonBlock.LIT,lit),3);}
        litTier=count>0?tier:0;litColumns=count;setChanged();
    }
    public boolean align(ServerPlayer player){
        if(!(level instanceof ServerLevel server)||!mayControl(player)||countdown>0||formedTier()>0)return false;
        var best=SurvivalGateLayout.closestFacing(server,worldPosition,facing());
        if(best!=facing()){
            server.setBlock(worldPosition,getBlockState().setValue(net.minecraft.world.level.block.state.properties.BlockStateProperties.HORIZONTAL_FACING,best),3);
            setChanged();server.invalidateCapabilities(worldPosition);
        }
        preview(player);return true;
    }
    public void preview(ServerPlayer player){
        if(!(level instanceof ServerLevel server)||!mayControl(player))return;
        int formed=formedTier(),tier=Math.min(6,Math.max(1,formed+1));
        var orientation=formed==0?SurvivalGateLayout.closestFacing(server,worldPosition,facing()):facing();
        if(formed==0&&orientation!=facing())player.sendSystemMessage(Component.literal("Controller faces "+facing().getName()+"; the closest matching gate faces "+orientation.getName()+". Use Align."));
        var missing=SurvivalGateLayout.missingParts(server,worldPosition,orientation,tier);
        if(formed>0)player.sendSystemMessage(Component.literal("Current gate: Tier "+formed+" complete. Alignment is valid."));
        if(formed==6)player.sendSystemMessage(Component.literal("Maximum tier reached; no further upgrade is required."));
        else player.sendSystemMessage(Component.literal((formed>0?"Optional next-tier upgrade: ":"Incomplete gate: ")+"Tier "+tier+" needs "+missing.size()+" missing/mismatched blocks."));
        if(!missing.isEmpty())player.sendSystemMessage(Component.literal("Front/left/right are relative to the gate plan; the tall arches are at the rear."));
        for(var requirement:SurvivalGateLayout.missingRequirements(server,worldPosition,orientation,tier))
            player.sendSystemMessage(Component.literal(requirement.section()+": "+requirement.count()+" × ").append(requirement.expected().getName()));
        for(var part:missing)if(server.hasChunkAt(part.pos()))server.sendParticles(player,ParticleTypes.END_ROD,true,part.pos().getX()+.5,part.pos().getY()+.5,part.pos().getZ()+.5,2,.1,.1,.1,0);
    }
    public void tick(){
        if(!(level instanceof ServerLevel server))return;
        if(adminTest())stored=capacity();
        // Return platforms trickle-charge only with their explicitly built crystal cell.
        if(returnPlatform&&server.getGameTime()%20==0&&server.getBlockState(centre().offset(0,-2,0)).is(BlockInit.CRYSTAL_CELL.get())){stored=Math.min(capacity(),stored+1000);setChanged();}
        if(countdown<=0){if(litTier>0)lightPylons(server,litTier,0);return;}
        var group=passengers();var present=group.stream().map(ServerPlayer::getUUID).collect(java.util.stream.Collectors.toSet());
        int tier=formedTier();
        if(tier==0||group.size()>SurvivalGateLayout.passengers(tier)+(has("capacity_coil")?2:0)||!present.equals(expected)||(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))){cancel();return;}
        BlockPos c=centre();double phase=(100-countdown)*.16,radius=Math.max(.6,SurvivalGateLayout.padRadius(tier)*.75);
        for(int point=0;point<8;point++){double angle=phase+point*Math.PI/4;server.sendParticles(ParticleTypes.PORTAL,c.getX()+.5+Math.cos(angle)*radius,c.getY()+1.15+Math.sin(phase)*.12,c.getZ()+.5+Math.sin(angle)*radius,1,.04,.04,.04,.02);}
        if(countdown%10==0){
            for(var part:SurvivalGateLayout.parts(tier))if(part.block()==BlockInit.GATE_PYLON.get()&&part.offset().getY()==tier+1){BlockPos at=c.offset(SurvivalGateLayout.rotate(part.offset(),facing()));server.sendParticles(ParticleTypes.END_ROD,at.getX()+.5,at.getY()+1.05,at.getZ()+.5,2,.12,.08,.12,.005);}
            server.sendParticles(ParticleTypes.END_ROD,c.getX()+.5,c.getY()+1.2,c.getZ()+.5,4,radius,.1,radius,.04);
        }
        int elapsed=100-countdown;Vec3 core=new Vec3(c.getX()+.5,c.getY()+1.6,c.getZ()+.5);
        // Lock-on: pylon columns light one at a time; particle streams spiral from the lit tops into the core.
        var columns=pylonColumns(tier);int lit=Math.min(columns.size(),1+elapsed*columns.size()/RIFT_AT);
        if(lit!=litColumns||litTier!=tier)lightPylons(server,tier,lit);
        if(elapsed%2==0)for(int i=0;i<lit;i++){
            var column=columns.get(i);Vec3 from=Vec3.atCenterOf(column.get(column.size()-1)).add(0,.6,0);
            for(int s=0;s<4;s++){double f=((elapsed/2+s*3)%12)/12.0,swirl=phase*2+i+f*Math.PI*2,r=.3*(1-f);Vec3 at=from.lerp(core,f);
                server.sendParticles(ParticleTypes.END_ROD,at.x+Math.cos(swirl)*r,at.y,at.z+Math.sin(swirl)*r,1,0,0,0,0);}
        }
        // Rift: a void crack opens in the core, across the gate's facing.
        if(elapsed==RIFT_AT)server.playSound(null,c,SoundEvents.RESPAWN_ANCHOR_CHARGE,SoundSource.BLOCKS,1.2F,.6F);
        if(elapsed>=RIFT_AT&&elapsed%2==0){
            double open=Math.min(1,(elapsed-RIFT_AT)/(double)(LIFT_AT-RIFT_AT));Direction side=facing().getClockWise();
            for(int k=-4;k<=4;k++){double jag=Math.sin(k*2.3+elapsed*.05)*.2*open;server.sendParticles(RIFT,core.x+side.getStepX()*jag,core.y+k*.22*open,core.z+side.getStepZ()*jag,1,.02,.02,.02,0);}
            server.sendParticles(ParticleTypes.REVERSE_PORTAL,core.x,core.y,core.z,3,.15*open,.5*open,.15*open,.02);
        }
        // Lift: once everyone is Ready, passengers float up while their clients stretch the view and white out.
        if(elapsed>=LIFT_AT&&!lifting&&ready.containsAll(expected)){
            lifting=true;server.playSound(null,c,SoundEvents.BEACON_ACTIVATE,SoundSource.BLOCKS,1.0F,1.4F);
            for(var p:group){p.addEffect(new MobEffectInstance(MobEffects.LEVITATION,countdown+5,0,false,false));GateLaunchSync.sendLift(p,countdown);}
        }
        if(--countdown==0){
            if(ready.containsAll(expected)){if(!launch(group)&&lifting)stopLift(server);}
            else{if(lifting)stopLift(server);for(var p:group)p.displayClientMessage(Component.literal("Launch cancelled: not everyone confirmed Ready."),false);}
            lifting=false;ready.clear();expected=Set.of();setChanged();
        }
    }
    private boolean launch(List<ServerPlayer> group){
        if(!(level instanceof ServerLevel source)||group.isEmpty())return false;
        int tier=formedTier();if(tier==0||group.size()>SurvivalGateLayout.passengers(tier)+(has("capacity_coil")?2:0))return false;
        if(!returnPlatform&&(selected<0||selected>=destinations().size()||!canReach(destinations().get(selected))))return false;
        int fee=cost(group.size());if(stored<fee)return false;
        String id=returnPlatform?homeDimension:destinations().get(selected);
        ServerLevel target=PlanetTestHub.planet(source.getServer(),id);if(target==null)return false;
        SurvivalGateBlockEntity landing;
        if(returnPlatform){target.getChunkAt(homeController);if(!(target.getBlockEntity(homeController) instanceof SurvivalGateBlockEntity home))return false;SurvivalGateLayout.loadFootprint(target,homeController,home.facing());if(home.formedTier()==0)return false;landing=home;}
        else landing=prepareArrival(target,this);
        BlockPos c=landing.centre();var pets=source.getEntitiesOfClass(Mob.class,pad(),mob->(mob instanceof TamableAnimal tame&&tame.isTame()&&group.stream().anyMatch(p->p.getUUID().equals(tame.getOwnerUUID())))||(mob.isLeashed()&&mob.getLeashHolder() instanceof ServerPlayer p&&group.contains(p)));
        // All validation and destination preparation completes before charging or moving anything.
        stored-=fee;setChanged();
        var arrive=arrival(target,c);
        for(Mob pet:pets){pet.dropLeash(true,false);var moved=pet.changeDimension(arrive);if(moved instanceof LivingEntity living)living.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING,100,0,false,false));}
        for(ServerPlayer player:group){bindHome(player);player.removeEffect(MobEffects.LEVITATION);GateLaunchSync.sendDestination(player,target);var moved=player.changeDimension(arrive);if(moved instanceof LivingEntity living)living.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING,100,0,false,false));}
        target.sendParticles(ParticleTypes.FLASH,c.getX()+.5,c.getY()+1.5,c.getZ()+.5,1,0,0,0,0);
        target.sendParticles(ParticleTypes.REVERSE_PORTAL,c.getX()+.5,c.getY()+1.5,c.getZ()+.5,24,1,.4,1,.04);
        return true;
    }
    /** Arrive up to four blocks above the pad, as high as the headroom allows, then drift down with Slow Falling. */
    public static DimensionTransition arrival(ServerLevel target,BlockPos centre){
        int clear=0;while(clear<5&&target.getBlockState(centre.above(clear+1)).isAir())clear++;
        int lift=Math.max(1,Math.min(4,clear-1));
        return new DimensionTransition(target,new Vec3(centre.getX()+.5,centre.getY()+lift,centre.getZ()+.5),Vec3.ZERO,180,0,DimensionTransition.PLAY_PORTAL_SOUND.then(DimensionTransition.PLACE_PORTAL_TICKET));
    }
    public void bindHome(ServerPlayer player){if(returnPlatform)return;var tag=player.getPersistentData().getCompound("zerog_home_gate");tag.putString("dimension",level.dimension().location().toString());tag.putLong("controller",worldPosition.asLong());player.getPersistentData().put("zerog_home_gate",tag);}
    public static DimensionTransition transition(ServerLevel target,BlockPos centre){return new DimensionTransition(target,new Vec3(centre.getX()+.5,centre.getY()+1,centre.getZ()+.5),Vec3.ZERO,180,0,DimensionTransition.PLAY_PORTAL_SOUND.then(DimensionTransition.PLACE_PORTAL_TICKET));}
    public static SurvivalGateBlockEntity prepareArrival(ServerLevel target,SurvivalGateBlockEntity home){
        // Deterministic gate-specific landing location; never overwrite a previous platform.
        var hubColumn=PlanetTestHub.isHub(home.level.getServer())&&home.level.dimension()==net.minecraft.world.level.Level.OVERWORLD?HubTieredGates.landingColumn(home.worldPosition):null;
        int x=hubColumn==null?512+Math.floorMod(home.worldPosition.getX(),16)*32:hubColumn.getX(),z=hubColumn==null?512+Math.floorMod(home.worldPosition.getZ(),16)*32:hubColumn.getZ();
        target.getChunk(x>>4,z>>4);int y=Math.min(target.getMaxBuildHeight()-10,Math.max(target.getSeaLevel()+4,target.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,x,z)+3));
        BlockPos c=new BlockPos(x,y,z),controller=c.offset(0,1,-2);
        // Locate persisted platforms in the loaded column instead of rebuilding above the old one.
        for(int scan=target.getMinBuildHeight();scan<target.getMaxBuildHeight();scan++)if(target.getBlockEntity(new BlockPos(x,scan,z-2)) instanceof SurvivalGateBlockEntity existing&&existing.returnPlatform&&existing.homeController.equals(home.worldPosition)&&existing.homeDimension.equals(home.level.dimension().location().toString())){
            SurvivalGateLayout.loadFootprint(target,existing.worldPosition,existing.facing());
            if(home.owner!=null&&!home.owner.equals(existing.owner)){existing.owner=home.owner;existing.setChanged();}
            if(home.adminTest()){existing.getPersistentData().putBoolean(HubTieredGates.ADMIN,true);existing.setChanged();}
            return existing;
        }
        if(hubColumn!=null)for(var p:BlockPos.betweenClosed(c.offset(-3,1,-3),c.offset(3,5,3)))target.setBlock(p,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),2);
        for(var p:BlockPos.betweenClosed(c.offset(-3,-2,-3),c.offset(3,-1,3)))target.setBlock(p,BlockInit.LANDING_PLATFORM.get().defaultBlockState(),3);
        for(var part:SurvivalGateLayout.parts(1))target.setBlock(c.offset(part.offset()),part.block().defaultBlockState(),3);
        target.setBlock(c.offset(0,-2,0),BlockInit.CRYSTAL_CELL.get().defaultBlockState(),3);
        var landing=(SurvivalGateBlockEntity)target.getBlockEntity(controller);landing.returnPlatform=true;landing.owner=home.owner;landing.homeController=home.worldPosition;landing.homeDimension=home.level.dimension().location().toString();landing.getPersistentData().putBoolean(HubTieredGates.ADMIN,home.adminTest());landing.stored=0;landing.setChanged();return landing;
    }
    @Override protected void saveAdditional(CompoundTag tag,HolderLookup.Provider registries){super.saveAdditional(tag,registries);tag.putInt("FE",stored);tag.putInt("selected",selected);if(owner!=null)tag.putUUID("owner",owner);tag.putBoolean("return",returnPlatform);tag.putString("homeDimension",homeDimension);tag.putLong("homeController",homeController.asLong());tag.put("upgrades",upgrades.serializeNBT(registries));tag.putInt("litTier",litTier);}
    @Override protected void loadAdditional(CompoundTag tag,HolderLookup.Provider registries){super.loadAdditional(tag,registries);stored=Math.max(0,Math.min(200000000,tag.getInt("FE")));selected=tag.getInt("selected");owner=tag.hasUUID("owner")?tag.getUUID("owner"):null;returnPlatform=tag.getBoolean("return");homeDimension=tag.getString("homeDimension");homeController=BlockPos.of(tag.getLong("homeController"));upgrades.deserializeNBT(registries,tag.getCompound("upgrades"));litTier=Math.max(0,Math.min(6,tag.getInt("litTier")));cancel();}
}
