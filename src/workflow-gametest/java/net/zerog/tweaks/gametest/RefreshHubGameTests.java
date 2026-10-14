package net.zerog.tweaks.gametest;

import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;

/** Fresh hub verification without placing the rejected planetary showcase templates. */
@GameTestHolder("zerog_refresh_hub") @PrefixGameTestTemplate(false)
public final class RefreshHubGameTests {
    @GameTest(templateNamespace="zerog_refresh_hub",template="equipment_empty",timeoutTicks=1200)
    public static void gate_tiers_and_return_routes(GameTestHelper h){
        HubTieredGateGameTests.six_admin_gate_tiers_form_route_reload_and_preserve_hub(h);
    }
    @GameTest(templateNamespace="zerog_refresh_hub",template="equipment_empty",timeoutTicks=1200)
    public static void supplied_workshop_and_unforced_hub(GameTestHelper h){
        HubTieredGateGameTests.compact_hub_is_supplied_unforced_and_does_not_sweep_planets(h);
        var level=h.getLevel().getServer().overworld();
        for(int station:new int[]{0,1,2,3,14}){
            var found=new java.util.HashSet<String>();var base=net.zerog.tweaks.travel.HubWorkshop.origin(station);
            for(int chest=0;chest<4;chest++)if(level.getBlockEntity(base.offset(3+chest*2,0,0)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity inventory)
                for(int slot=0;slot<27;slot++)found.add(net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(inventory.getItem(slot).getItem()).getPath());
            for(String family:java.util.List.of("acceleration","energy_coil","item_compact"))for(int tier:new int[]{1,6})
                h.assertTrue(found.contains(family+"_upgrade_card_t"+tier),"Missing compatible workshop card at station "+station);
            h.assertTrue(found.contains("void_upgrade_card"),"Missing void-card example");
        }
    }
    @GameTest(templateNamespace="zerog_refresh_hub",template="equipment_empty",timeoutTicks=1200)
    public static void player_gate_power_and_port_controls(GameTestHelper h){
        HubTieredGateGameTests.six_player_gates_charge_through_ports_and_show_exact_menu_energy(h);
    }
}
