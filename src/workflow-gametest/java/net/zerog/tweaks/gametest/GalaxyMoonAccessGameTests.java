package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.travel.*;

/** Ordinary formed gates, not the unrestricted admin showcase. */
@GameTestHolder("zerog_galaxy_access") @PrefixGameTestTemplate(false)
public final class GalaxyMoonAccessGameTests {
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=100)
    public static void vent_smoke_checks_cover_and_uses_supplied_animation_random(GameTestHelper h){
        var vent=net.zerog.tweaks.registry.BlockInit.VENT_ROCK.get();
        h.assertTrue(vent instanceof net.zerog.tweaks.registry.VentRockBlock,"Vent Rock is still a plain block");
        class AnimationRandom extends net.minecraft.world.level.levelgen.LegacyRandomSource {
            int calls;AnimationRandom(){super(14);}
            @Override public int nextInt(int bound){calls++;return 0;}
            @Override public double nextDouble(){calls++;return .5;}
        }
        var random=new AnimationRandom();var pos=h.absolutePos(new net.minecraft.core.BlockPos(2,2,2));
        h.getLevel().setBlock(pos.above(),net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),3);
        vent.animateTick(vent.defaultBlockState(),h.getLevel(),pos,random);
        h.assertTrue(random.calls==0,"Covered vent still attempted smoke animation");
        h.getLevel().removeBlock(pos.above(),false);
        vent.animateTick(vent.defaultBlockState(),h.getLevel(),pos,random);
        h.assertTrue(random.calls==3,"Open vent did not use supplied animation random");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=100)
    public static void glacial_ice_matches_approved_slip_and_glass_sound(GameTestHelper h){
        var ice=net.zerog.tweaks.registry.BlockInit.GLACIAL_ICE.get();
        h.assertTrue(ice.getFriction()==0.98F,"Glacial Ice lacks approved slippery friction");
        h.assertTrue(ice.defaultBlockState().getSoundType()==net.minecraft.world.level.block.SoundType.GLASS,"Glacial Ice still sounds like stone");
        h.assertTrue(ice.getExplosionResistance()==7.0F,"Ice repair changed existing resistance");
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_galaxy_access",template="equipment_empty",timeoutTicks=200)
    public static void galaxy_moons_follow_their_galaxy_tier_and_downgrade(GameTestHelper h){
        var level=h.getLevel();var centre=h.absolutePos(new BlockPos(8,4,8));
        for(int tier=1;tier<=6;tier++){
            for(var part:SurvivalGateLayout.parts(tier))level.setBlock(centre.offset(part.offset()),part.block().defaultBlockState(),3);
            var at=centre.offset(0,1,-2);var gate=(SurvivalGateBlockEntity)level.getBlockEntity(at);
            h.assertTrue(gate.formedTier()==tier,"Gate geometry did not form tier "+tier);
            h.assertTrue(!gate.adminTest(),"Progression test accidentally used an admin gate");
            for(int galaxy=2;galaxy<=5;galaxy++){
                boolean expected=galaxy<=tier;
                for(String suffix:new String[]{"_moons","_p1","_p6"}){
                    String target="zerog_tweaks:g"+galaxy+suffix;
                    h.assertTrue(gate.canReach(target)==expected,"Wrong survival access at tier "+tier+" to "+target);
                }
            }
            h.assertTrue(gate.canReach("zerog_tweaks:moon")&&gate.canReach("zerog_tweaks:mars"),"Sol access was lost");
            h.assertTrue(!gate.canReach("minecraft:overworld")&&!gate.canReach("minecraft:the_end"),"Self/unknown route exposed");
            var loaded=new SurvivalGateBlockEntity(at,gate.getBlockState());loaded.setLevel(level);
            loaded.loadWithComponents(gate.saveWithFullMetadata(level.registryAccess()),level.registryAccess());
            h.assertTrue(loaded.canReach("zerog_tweaks:g2_moons")== (tier>=2),"Reload changed moon access");
            if(tier>1){
                var edge=centre.offset(tier+1,-1,0);var state=level.getBlockState(edge);
                level.setBlock(edge,net.minecraft.world.level.block.Blocks.AIR.defaultBlockState(),3);
                h.assertTrue(gate.formedTier()==tier-1,"Broken frame did not downgrade");
                if(tier<=5)h.assertTrue(!gate.canReach("zerog_tweaks:g"+tier+"_moons"),"Downgrade retained higher moon access");
                level.setBlock(edge,state,3);
            }
        }
        h.succeed();
    }
}
