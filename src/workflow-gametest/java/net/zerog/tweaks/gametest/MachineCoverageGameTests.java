package net.zerog.tweaks.gametest;
import net.minecraft.core.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.gametest.*;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.zerog.tweaks.machine.*;
import net.zerog.tweaks.genetics.*;
/** Explicit loaded-machine coverage: missing addons are a failure, not an empty successful audit. */
@GameTestHolder("zerog_machine_coverage") @PrefixGameTestTemplate(false)
public final class MachineCoverageGameTests {
    @GameTest(templateNamespace="zerog_recipe_legacy",template="equipment_empty",timeoutTicks=120)
    public static void all_eleven_live_machines_have_supported_faces_and_card_contracts(GameTestHelper h){
        int count=0;
        for(String id:new String[]{"stardust_smelter","starmetal_smelter","silk_weaver","gravitational_centrifuge","centrifuge","frame_assembler","frame_component_assembler","frame_infusion_altar","infusion_altar","geno_station","genetic_splicer"}){
            var key=ResourceLocation.parse("aeroapiary:"+id);h.assertTrue(BuiltInRegistries.BLOCK.containsKey(key),"Audit cannot skip missing registered machine: "+id);
            var pos=new BlockPos(2,2,2);h.setBlock(pos,BuiltInRegistries.BLOCK.get(key));var be=h.getBlockEntity(pos);h.assertTrue(be!=null&&LegacyMachineSides.supports(be),"Machine has no side controller: "+id);
            boolean powered=GeneticsRuntime.handles(id)||GeneticsRuntime.legacyPowered(id);
            h.assertTrue(LegacyMachineSides.supportsFamily(be,1)==powered&&LegacyMachineSides.supportsFamily(be,2)==GeneticsRuntime.handles(id),"Invented/missing FE or fluid faces: "+id);
            if(!GeneticsRuntime.handles(id))h.assertTrue(!LegacyRecipeCatalogue.basePages(id).isEmpty(),"Missing exact combinations: "+id);
            var player=h.makeMockPlayer(net.minecraft.world.level.GameType.SURVIVAL);player.setPos(be.getBlockPos().getCenter());
            for(var side:Direction.values()){
                var cached=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),side);h.assertTrue(cached!=null,"No default item face: "+id);
                h.assertTrue(LegacyMachineSides.command(be,player,503+side.ordinal()*4),"Off command rejected: "+id);
                h.assertTrue(cached.insertItem(0,new ItemStack(Items.DIRT),false).is(Items.DIRT),"Disabled cached face accepted input: "+id);
                h.assertTrue(LegacyMachineSides.command(be,player,500+side.ordinal()*4),"Restore command rejected: "+id);
                if(powered){h.assertTrue(LegacyMachineSides.command(be,player,527+side.ordinal()*4),"FE Off rejected: "+id);h.assertTrue(h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),side)==null,"Disabled FE face still advertised: "+id);h.assertTrue(LegacyMachineSides.command(be,player,525+side.ordinal()*4),"FE Input rejected: "+id);}
            }
            h.assertTrue(LegacyMachineCards.supports(be)==powered,"Wrong upgrade contract: "+id);
            if(powered){var cards=LegacyMachineCards.inventory(be);h.assertTrue(!cards.isItemValid(0,new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:void_upgrade_card")))),"Unsupported card accepted: "+id);}
            count++;
        }h.assertTrue(count==11,"Incomplete machine coverage");h.succeed();
    }
}
