package net.zerog.tweaks.registry;

import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.world.level.block.*;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.registries.DeferredBlock;

/** Six themed water-source plants, with paired heads/bodies and vanilla kelp growth. */
public final class ZGPlanetAquatic {
    public record Family(DeferredBlock<Head> head, DeferredBlock<Body> body) {}
    public static final Map<String, Family> FAMILIES = new LinkedHashMap<>();
    public static final class Head extends ZGKelpBlock {
        private final String theme;
        Head(Properties properties, String theme) { super(properties); this.theme=theme; }
        @Override protected Block getBodyBlock() { return FAMILIES.get(theme).body.get(); }
    }
    public static final class Body extends ZGKelpPlantBlock {
        private final String theme;
        Body(Properties properties,String theme) { super(properties); this.theme=theme; }
        @Override protected GrowingPlantHeadBlock getHeadBlock() { return FAMILIES.get(theme).head.get(); }
    }
    public static void init() {
        for (String theme : new String[]{"moon","mars","cerulon","skarn","eidolon","solvane"}) {
            var head=BlockInit.BLOCKS.register(theme+"_kelp",()->new Head(Block.Properties.ofFullCopy(Blocks.KELP).lightLevel(s->4),theme));
            var body=BlockInit.BLOCKS.register(theme+"_kelp_plant",()->new Body(Block.Properties.ofFullCopy(Blocks.KELP_PLANT).lightLevel(s->4),theme));
            FAMILIES.put(theme,new Family(head,body));
            ItemInit.ITEMS.register(theme+"_kelp",()->new ItemNameBlockItem(head.get(),new Item.Properties()));
        }
    }
    private ZGPlanetAquatic() {}
}
