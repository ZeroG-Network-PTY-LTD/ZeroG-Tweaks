package net.zerog.tweaks.genetics;

import java.util.ArrayList;
import java.util.List;

/** Read-only operation descriptions. Metrics use the same quarter-work budget as live jobs. */
public final class GeneticsRecipeCatalogue {
    public record Page(String title, List<String> lines, int ticks, int energy) {}
    public static Page page(String id, int mode, int speed, int coilTier) {
        if (!GeneticsRuntime.handles(id)) return new Page("Unsupported machine", List.of(), 0, 0);
        boolean splice = id.equals("genetic_splicer"), sample = !splice && mode == 1;
        int duration = GeneticsRuntime.duration(id, mode);
        speed = Math.clamp(speed, 100, 4000); coilTier = Math.clamp(coilTier, 0, 6);
        int ticks = (duration * 100 + speed - 1) / speed;
        int energy = net.zerog.tweaks.machine.MachineUpgradeConfig.recipeEnergy((long)duration * GeneticsRuntime.cost(id),coilTier);
        var lines = new ArrayList<String>();
        lines.add("Slot 0: 1 filled bee cage");
        lines.add("Requires five saved, valid bee traits");
        if (splice || sample) lines.add("Specimen must already be analysed");
        lines.add(splice ? "Slot 1: 1 valid trait serum, consumed" : sample
                ? "Slot 1: 1 serum vial, consumed" : "Slot 1: no reagent required");
        if (splice) {
            lines.add("Choose ONE catalyst route:");
            lines.add("Slot 2: 1 Royal Jelly OR 1 Cosmic Jelly");
            lines.add("OR tank: " + GeneticsTank.DOSE + " mB Royal/Cosmic Jelly");
            lines.add("Royal: 75% success; Cosmic: 100%");
            lines.add("Valid item catalyst takes priority over tank");
            lines.add("Slot 3: 1 changed cage on success");
            lines.add("Failure: original cage; reagents still consumed");
            lines.add("Slot 4: 1 empty serum vial on either outcome");
            lines.add("Only serum's single gene is changed");
            lines.add("Both outcomes must fit before starting");
        } else {
            lines.add("Choose ONE catalyst route:");
            lines.add("Slot 2: 1 Honey Drop OR 1 Honey Bottle");
            lines.add("OR tank: " + GeneticsTank.DOSE + " mB supported honey");
            lines.add("Valid item catalyst takes priority over tank");
            lines.add("Slot 3: 1 analysed cage, traits retained");
            if (sample) {
                lines.add("Slot 4: 1 serum of the selected gene/value");
                lines.add("Choose one of the five trait buttons");
                lines.add("Honey Bottle: 1 bottle to recovery slots 5-15");
            } else lines.add("Honey Bottle: 1 bottle to slot 4");
            lines.add("Honey Drop/fluid route: no bottle return");
            lines.add("Without power: " + duration * 4 + " ticks, 0 FE");
            lines.add("Mixed power: time and FE vary with powered work");
        }
        lines.add("Fully powered: " + ticks + " ticks / " + energy + " FE");
        lines.add("Base: " + duration + " ticks / " + duration * GeneticsRuntime.cost(id) + " FE");
        lines.add("Acceleration / Energy Coil: tiers 1-6");
        lines.add("Compact / Void unsupported");
        lines.add("Read-only guide; no autofill or job start");
        return new Page(splice ? "Splice" : sample ? "Sample" : "Analyse", List.copyOf(lines), ticks, energy);
    }
    private GeneticsRecipeCatalogue() {}
}
