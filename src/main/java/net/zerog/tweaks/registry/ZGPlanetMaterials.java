package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.zerog.tweaks.ZeroGTweaks;

/** Additive exploration/crafting minerals: no new tool tiers or gate shortcuts. */
public final class ZGPlanetMaterials {
    public static final List<String> METALS=List.of("lunarium","aresium","azurium","basaltine","rime_nickel","helion");
    public static final List<String> GEMS=List.of("eclipse_opal","redshift_garnet","tidal_sapphire","ember_spinel","wraith_quartz","corona_topaz");
    private static final DeferredRegister.Blocks BLOCKS=DeferredRegister.createBlocks(ZeroGTweaks.MODID);
    public static final Map<String,DeferredBlock<Block>> BLOCK_ITEMS=new LinkedHashMap<>();
    private static void block(String id,boolean ore,boolean gem){
        var holder=BLOCKS.register(id,()->{
            var props=BlockBehaviour.Properties.of().mapColor(MapColor.STONE).sound(SoundType.STONE)
                    .strength(ore?3.0F:5.0F,7.0F).requiresCorrectToolForDrops();
            return ore?new DropExperienceBlock(UniformInt.of(gem?2:0,gem?5:0),props):new Block(props);
        });
        BLOCK_ITEMS.put(id,holder);ItemInit.ITEMS.registerSimpleBlockItem(id,holder);
    }
    public static void register(IEventBus bus){
        for(var name:METALS){
            block(name+"_ore",true,false);block(name+"_block",false,false);block("raw_"+name+"_block",false,false);
            for(var id:List.of("raw_"+name,name+"_ingot",name+"_nugget",name+"_dust")) ItemInit.ITEMS.registerSimpleItem(id);
        }
        for(var name:GEMS){
            block(name+"_ore",true,true);block(name+"_block",false,true);
            ItemInit.ITEMS.registerSimpleItem(name);ItemInit.ITEMS.registerSimpleItem(name+"_dust");
        }
        BLOCKS.register(bus);
    }
    private ZGPlanetMaterials(){}
}
