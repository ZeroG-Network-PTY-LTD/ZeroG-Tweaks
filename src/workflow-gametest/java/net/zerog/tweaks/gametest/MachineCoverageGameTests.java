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
                ItemStack accepted=ItemStack.EMPTY;int inputSlot=-1;
                search:for(int slot=0;slot<cached.getSlots();slot++)for(var item:BuiltInRegistries.ITEM){
                    var candidate=new ItemStack(item);
                    if(!candidate.isEmpty()&&cached.isItemValid(slot,candidate)&&cached.insertItem(slot,candidate,true).isEmpty()){
                        accepted=candidate;inputSlot=slot;break search;
                    }
                }
                h.assertTrue(inputSlot>=0,"No actually insertable test input: "+id);
                h.assertTrue(LegacyMachineSides.command(be,player,503+side.ordinal()*4),"Off command rejected: "+id);
                h.assertTrue(cached.insertItem(inputSlot,accepted.copy(),false).getCount()==1,"Disabled cached face accepted valid input: "+id);
                h.assertTrue(LegacyMachineSides.command(be,player,500+side.ordinal()*4),"Restore command rejected: "+id);
                h.assertTrue(cached.insertItem(inputSlot,accepted.copy(),false).getCount()==1,"Restoring face revived stale handler: "+id);
                var restored=h.getLevel().getCapability(Capabilities.ItemHandler.BLOCK,be.getBlockPos(),side);
                h.assertTrue(restored!=null&&restored.insertItem(inputSlot,accepted.copy(),false).isEmpty(),"Restored face rejected valid input: "+id);
                var recovered=restored.extractItem(inputSlot,1,false);
                if(GeneticsRuntime.handles(id)){
                    var retained=restored.getStackInSlot(inputSlot);
                    h.assertTrue(recovered.isEmpty()&&retained.getCount()==1&&ItemStack.isSameItemSameComponents(retained,accepted),"Genetics specimen extraction/retention contract failed: "+id);
                    // Fixture cleanup: players can recover specimens, but automated input extraction stays forbidden.
                    GeneticsRuntime.inventory(be).extractItem(inputSlot,1,false);
                }else h.assertTrue(recovered.getCount()==1&&ItemStack.isSameItemSameComponents(recovered,accepted),"Input round-trip lost/changed an item: "+id);
                if(powered){h.assertTrue(LegacyMachineSides.command(be,player,527+side.ordinal()*4),"FE Off rejected: "+id);h.assertTrue(h.getLevel().getCapability(Capabilities.EnergyStorage.BLOCK,be.getBlockPos(),side)==null,"Disabled FE face still advertised: "+id);h.assertTrue(LegacyMachineSides.command(be,player,525+side.ordinal()*4),"FE Input rejected: "+id);}
            }
            h.assertTrue(LegacyMachineCards.supports(be)==powered,"Wrong upgrade contract: "+id);
            if(powered){var cards=LegacyMachineCards.inventory(be);h.assertTrue(!cards.isItemValid(0,new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("zerog_tweaks:void_upgrade_card")))),"Unsupported card accepted: "+id);}
            count++;
        }h.assertTrue(count==11,"Incomplete machine coverage");h.succeed();
    }
}
