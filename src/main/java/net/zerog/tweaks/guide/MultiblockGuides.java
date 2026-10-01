package net.zerog.tweaks.guide;

import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/** Authored reference layouts, not formation rules or replacement recipes. */
public final class MultiblockGuides {
    public record Cell(int x, int y, int z, String part) {}
    public record Layout(String id, List<Cell> cells, List<String> externalModules) {
        public int maxY() { return cells.stream().mapToInt(Cell::y).max().orElse(0); }
        public int maxX() { return cells.stream().mapToInt(Cell::x).max().orElse(0); }
        public int maxZ() { return cells.stream().mapToInt(Cell::z).max().orElse(0); }
        public Map<String, Integer> quantities() {
            Map<String, Integer> result = new TreeMap<>();
            cells.forEach(cell -> result.merge(cell.part(), 1, Integer::sum));
            return result;
        }
    }
    private static final List<Layout> LAYOUTS = load();
    public static List<Layout> layouts() { return LAYOUTS; }
    private static List<Layout> load() {
        try (var stream = MultiblockGuides.class.getResourceAsStream(
                "/assets/zerog_tweaks/guides/multiblocks.json")) {
            if (stream == null) throw new IllegalStateException("Multiblock guide data missing");
            var json = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
            List<Layout> layouts = new ArrayList<>();
            for (var entry : json.getAsJsonArray("layouts")) {
                var item = entry.getAsJsonObject(); List<Cell> cells = new ArrayList<>();
                for (var block : item.getAsJsonArray("cells")) {
                    var c = block.getAsJsonObject();
                    cells.add(new Cell(c.get("x").getAsInt(), c.get("y").getAsInt(),
                            c.get("z").getAsInt(), c.get("part").getAsString()));
                }
                List<String> modules = new ArrayList<>();
                item.getAsJsonArray("external_modules").forEach(m -> modules.add(m.getAsString()));
                layouts.add(new Layout(item.get("id").getAsString(), List.copyOf(cells), List.copyOf(modules)));
            }
            return List.copyOf(layouts);
        } catch (Exception failure) {
            throw new IllegalStateException("Invalid authored multiblock guide", failure);
        }
    }
    private MultiblockGuides() {}
}
