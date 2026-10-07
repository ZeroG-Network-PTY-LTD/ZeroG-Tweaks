package net.zerog.tweaks.gametest;

import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.ChunkPos;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.worldgen.KeyAltarPiece;

/** Real jigsaw generation, not natural chunk placement: ordinary-server audit covers that separately. */
@GameTestHolder("zerog_galaxy_access") @PrefixGameTestTemplate(false)
public final class VaultReferenceBoundsGameTests {
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=1200)
    public static void generated_vault_and_four_altars_fit_vanilla_reference_window(GameTestHelper h) {
        var level=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse("zerog_tweaks:cerulon")));
        h.assertTrue(level!=null,"Native Cerulon fixture is required");
        var vault=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(ResourceLocation.parse("zerog_tweaks:concord_vault"));
        var generator=level.getChunkSource().getGenerator();
        var origin=new ChunkPos(-2,-20);
        for(long seed=0;seed<32;seed++) {
            var start=vault.generate(level.registryAccess(),generator,generator.getBiomeSource(),level.getChunkSource().randomState(),level.getStructureManager(),seed,origin,0,level,biome->true);
            h.assertTrue(start.isValid(),"Bounded Vault failed to produce a layout seed"+seed);
            int keys=0;
            for(var piece:start.getPieces()) {
                var box=piece.getBoundingBox();
                h.assertTrue((box.minX()>>4)>=origin.x-8&&(box.maxX()>>4)<=origin.x+8
                    &&(box.minZ()>>4)>=origin.z-8&&(box.maxZ()>>4)<=origin.z+8,
                    "Generated piece escapes vanilla reference window seed"+seed+" "+box);
                if(piece instanceof KeyAltarPiece)keys++;
            }
            h.assertTrue(keys==4,"Generated Vault lacks four planned keys seed"+seed);
        }
        h.succeed();
    }
}
