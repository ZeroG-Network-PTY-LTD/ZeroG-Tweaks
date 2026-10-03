package net.zerog.tweaks.event;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.Block;

/** Even-diameter, bilaterally symmetric 10-block sphere: no radius rounding to 11. */
public final class CometRemnant {
    public static final int DIAMETER=10;
    public enum Layer { SHELL, MANTLE, CORE }
    public record Cell(int x,int y,int z,Layer layer,int distanceSquared) {}
    public record Palette(String rock,String commonOre,String rareOre,String gemOre) {}
    public static List<Cell> cells() {
        var cells=new ArrayList<Cell>();
        for(int x=0;x<DIAMETER;x++) for(int y=0;y<DIAMETER;y++) for(int z=0;z<DIAMETER;z++) {
            int dx=2*x-9,dy=2*y-9,dz=2*z-9,d=dx*dx+dy*dy+dz*dz;
            if(d<=100) cells.add(new Cell(x,y,z,d<=11?Layer.CORE:d<=49?Layer.MANTLE:Layer.SHELL,d));
        }
        return List.copyOf(cells);
    }
    private static final String[][] GALAXY_THEMES={
            {"cerulon","mars","skarn","eidolon","skarn","solvane"},
            {"eidolon","skarn","solvane","moon","cerulon","mars"},
            {"moon","cerulon","mars","skarn","eidolon","skarn"},
            {"skarn","eidolon","skarn","solvane","moon","cerulon"}};
    public static String theme(String dimension) {
        if(dimension.matches("g[2-5]_p[1-6]")) return GALAXY_THEMES[dimension.charAt(1)-'2'][dimension.charAt(4)-'1'];
        if(dimension.endsWith("_moons")) return "moon";
        return dimension;
    }
    public static Palette palette(String dimension) {
        return switch(theme(dimension)) {
            case "mars" -> new Palette("martian_stone","aresium_ore","olympium_ore","redshift_garnet_ore");
            case "cerulon" -> new Palette("cerulean_stone","azurium_ore","lumenite_ore","tidal_sapphire_ore");
            case "skarn" -> new Palette("skarn_rock","basaltine_ore","cinnabrite_ore","ember_spinel_ore");
            case "eidolon" -> new Palette("permafrost","rime_nickel_ore","rimeglass_ore","wraith_quartz_ore");
            case "solvane" -> new Palette("solar_stone","helion_ore","dawnstone_ore","corona_topaz_ore");
            default -> new Palette("lunar_stone","lunarium_ore","moonsteel_ore","eclipse_opal_ore");
        };
    }
    public static Block material(Cell cell,Palette palette,RandomSource random) {
        String id=switch(cell.layer()) {
            case CORE -> cell.distanceSquared()<=3?palette.gemOre():random.nextInt(3)==0?palette.rareOre():"meteorite_fragment";
            case MANTLE -> random.nextInt(7)==0?palette.commonOre():"meteorite_fragment";
            case SHELL -> cell.distanceSquared()<83&&random.nextInt(20)==0?palette.commonOre():random.nextInt(4)==0?"meteorite_fragment":palette.rock();
        };
        return BuiltInRegistries.BLOCK.get(ResourceLocation.fromNamespaceAndPath("zerog_tweaks",id));
    }
    private CometRemnant() {}
}
