package net.zerog.tweaks.gametest;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.event.PlanetStorms;

@GameTestHolder("zerog_gate_power")
@PrefixGameTestTemplate(false)
public final class WeatherPauseGameTests {
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void disabled_weather_cannot_override_native_strengths_or_spawn_bolts(GameTestHelper h) {
        var mars=h.getLevel().getServer().getLevel(ResourceKey.create(Registries.DIMENSION,ResourceLocation.parse("zerog_tweaks:mars")));
        h.assertTrue(mars!=null,"Mars fixture missing");
        float rain=mars.getRainLevel(1),thunder=mars.getThunderLevel(1);
        try {
            mars.setRainLevel(.37F);mars.setThunderLevel(.19F);
            // Native getThunderLevel returns thunder strength multiplied by rain.
            float expectedRain=mars.getRainLevel(1),expectedThunder=mars.getThunderLevel(1);
            for(var mode:PlanetStorms.Mode.values()) {
                PlanetStorms.override(mars,mode);
                h.assertTrue(Math.abs(mars.getRainLevel(1)-expectedRain)<.001F&&Math.abs(mars.getThunderLevel(1)-expectedThunder)<.001F,"Disabled mode overwrote native weather: "+mode);
            }
            h.assertTrue(!PlanetStorms.strike(mars,new BlockPos(0,mars.getMaxBuildHeight()-1,0)),"Disabled custom lightning spawned");
            for(String planet:new String[]{"moon","mars","eidolon","skarn","solvane","g2_p1"})
                for(long time:new long[]{0,1800,7200,24000})
                    h.assertTrue(PlanetStorms.automatic(planet,time,"toxic_acid_glacier")==PlanetStorms.Mode.CLEAR,"Automatic weather remained active");
        } finally { mars.setRainLevel(rain);mars.setThunderLevel(rain>0?thunder/rain:0); }
        h.succeed();
    }
    @GameTest(templateNamespace="zerog_gate_power",template="equipment_empty",timeoutTicks=100)
    public static void disabled_admin_command_rejects_activation_and_native_lightning_is_not_cancelled(GameTestHelper h) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var level=h.getLevel();var player=h.makeMockServerPlayerInLevel();
        player.getAbilities().instabuild=true;
        float rain=level.getRainLevel(1),thunder=level.getThunderLevel(1);
        int result=level.getServer().getCommands().getDispatcher().execute("zgweather electrical",player.createCommandSourceStack());
        h.assertTrue(result==0&&rain==level.getRainLevel(1)&&thunder==level.getThunderLevel(1),"Weather command bypassed build pause");
        var bolt=EntityType.LIGHTNING_BOLT.create(level);
        var event=new net.neoforged.neoforge.event.entity.EntityJoinLevelEvent(bolt,level);
        PlanetStorms.protectNativeStrikes(event);
        h.assertTrue(!event.isCanceled(),"Vanilla lightning was cancelled by disabled custom weather");
        player.discard();h.succeed();
    }
    private WeatherPauseGameTests() {}
}
