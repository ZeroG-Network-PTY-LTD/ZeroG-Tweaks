package net.zerog.tweaks.gametest;
import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;
/** Narrow maintenance batch; no undefined climate or research rules are invented. */
@GameTestHolder("zerog_maintenance") @PrefixGameTestTemplate(false)
public final class MaintenanceBoundaryGameTests {
 @GameTest(templateNamespace="zerog_maintenance",template="equipment_empty",timeoutTicks=200)
 public static void loaded_combinations(GameTestHelper h){RecipeCatalogueGameTests.catalogue_shows_real_combinations_catalysts_and_upgrade_costs(h);}
 @GameTest(templateNamespace="zerog_maintenance",template="equipment_empty",timeoutTicks=200)
 public static void loaded_yields(GameTestHelper h){RecipeCatalogueGameTests.catalogue_preserves_seed_feed_salvage_and_refinery_yields(h);}
 @GameTest(templateNamespace="zerog_maintenance",template="equipment_empty",timeoutTicks=200)
 public static void frame_progression(GameTestHelper h){AlvearyRuntimeGameTests.real_27_frame_progression_migration_and_reload(h);}
 @GameTest(templateNamespace="zerog_maintenance",template="equipment_empty",timeoutTicks=200)
 public static void supported_bee_processing(GameTestHelper h){AlvearyRuntimeGameTests.formed_controller_uses_actual_pb_recipe_components_and_honey_save(h);}
 @GameTest(templateNamespace="zerog_maintenance",template="equipment_empty",timeoutTicks=200)
 public static void actual_module_ports(GameTestHelper h){AlvearyServiceGameTests.zerog_ports_form_transfer_buffers_and_expose_front_only(h);}
}
