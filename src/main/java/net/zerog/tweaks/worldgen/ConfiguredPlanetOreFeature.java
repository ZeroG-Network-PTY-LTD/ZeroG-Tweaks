package net.zerog.tweaks.worldgen;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.OreFeature;
import net.minecraft.world.level.levelgen.feature.configurations.OreConfiguration;
import net.zerog.tweaks.config.ZGProgressionConfig;

/** Rarity multiplier applies only to ZeroG configured ores, never vanilla ores. */
public final class ConfiguredPlanetOreFeature extends OreFeature {
    public ConfiguredPlanetOreFeature() { super(OreConfiguration.CODEC); }
    @Override public boolean place(FeaturePlaceContext<OreConfiguration> context) {
        double attempts=1.0/ZGProgressionConfig.ORE_MULTIPLIER.get();
        int count=(int)attempts;
        if(context.random().nextDouble()<attempts-count)count++;
        boolean changed=false;
        for(int i=0;i<count;i++) {
            var origin=context.origin();
            // Extra attempts stay in the same owning chunk at the configured height.
            if(i>0)origin=new BlockPos((origin.getX()&~15)+context.random().nextInt(16),origin.getY(),
                (origin.getZ()&~15)+context.random().nextInt(16));
            changed |= super.place(new FeaturePlaceContext<>(context.topFeature(),context.level(),
                context.chunkGenerator(),context.random(),origin,context.config()));
        }
        return changed;
    }
}
