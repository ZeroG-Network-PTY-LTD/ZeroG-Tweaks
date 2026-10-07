package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredBlock;

public final class ZGGasVents {
    public static final Map<String,Integer> COLOURS=Map.of("moon",0xB799ED,"mars",0xED985D,"cerulon",0x71CEE6,"skarn",0xEA6546,"eidolon",0xBDEBFF,"solvane",0xFFDB79);
    public static final Map<String,DeferredHolder<net.minecraft.core.particles.ParticleType<?>,SimpleParticleType>> SMOKE=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<GasVentBlock>> VENTS=new LinkedHashMap<>();
    public static final Map<String,DeferredBlock<GasVentBlock>> AMBIENT_VENTS=new LinkedHashMap<>();
    private static final DeferredRegister<net.minecraft.core.particles.ParticleType<?>> PARTICLES=DeferredRegister.create(Registries.PARTICLE_TYPE,"zerog_tweaks");
    public static void init(IEventBus bus) {
        for(String planet:java.util.List.of("moon","mars","cerulon","skarn","eidolon","solvane")) {
            SMOKE.put(planet,PARTICLES.register(planet+"_gas_smoke",()->new SimpleParticleType(false)));
            VENTS.put(planet,BlockInit.BLOCKS.register(planet+"_gas_vent",()->new GasVentBlock(planet,
                    Block.Properties.ofFullCopy(Blocks.STONE).randomTicks().lightLevel(s->planet.equals("solvane")?8:2))));
            ItemInit.ITEMS.registerSimpleBlockItem(planet+"_gas_vent",VENTS.get(planet));
            AMBIENT_VENTS.put(planet,BlockInit.BLOCKS.register(planet+"_ambient_vent",()->new GasVentBlock(planet,
                    Block.Properties.ofFullCopy(Blocks.STONE).lightLevel(s->planet.equals("solvane")?6:2),true)));
            ItemInit.ITEMS.registerSimpleBlockItem(planet+"_ambient_vent",AMBIENT_VENTS.get(planet));
        }
        PARTICLES.register(bus);
    }
    public static final class GasVentBlock extends Block {
        private final String planet;
        private final boolean ambientOnly;
        GasVentBlock(String planet,Properties properties){this(planet,properties,false);}
        GasVentBlock(String planet,Properties properties,boolean ambientOnly){super(properties);this.planet=planet;this.ambientOnly=ambientOnly;}
        @Override public void animateTick(BlockState state,Level level,BlockPos pos,RandomSource random) {
            if(ambientOnly&&!net.zerog.tweaks.event.PlanetStorms.enabled())return;
            if(!level.getBlockState(pos.above()).isAir()) return;
            for(int i=0;i<(ambientOnly?4:2);i++) level.addParticle(SMOKE.get(planet).get(),pos.getX()+.5+random.nextGaussian()*.12,pos.getY()+1.1,pos.getZ()+.5+random.nextGaussian()*.12,0,ambientOnly?.10:.04,0);
        }
        @Override protected void randomTick(BlockState state,ServerLevel level,BlockPos pos,RandomSource random) {
            if(ambientOnly)return;
            if(!level.getBlockState(pos.above()).isAir()) return;
            for(var living:level.getEntitiesOfClass(LivingEntity.class,new AABB(pos.above()).inflate(1.5,2,1.5))) {
                switch(planet) {
                    case "moon"->living.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING,80));
                    case "mars"->living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS,60));
                    case "cerulon"->living.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION,260));
                    case "eidolon"->living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN,60,1));
                    case "skarn","solvane"->{if(!living.fireImmune()) living.igniteForSeconds(2);}
                    default->{ }
                }
            }
        }
    }
    private ZGGasVents(){}
}
