import java.util.Map;
/** Executes the installed addon slot table without starting Minecraft. */
public final class MachineWorkbenchContractCheck {
    public static void main(String[] args)throws Exception {
        var slotsFor=Class.forName("com.zerog.aeroapiary.MachineSlotLayouts").getMethod("slotsFor",String.class);
        var counts=Map.ofEntries(Map.entry("stardust_smelter",3),Map.entry("starmetal_smelter",4),
            Map.entry("silk_weaver",4),Map.entry("gravitational_centrifuge",7),Map.entry("centrifuge",7),
            Map.entry("frame_assembler",3),Map.entry("frame_component_assembler",3),Map.entry("frame_infusion_altar",4),
            Map.entry("infusion_altar",3),Map.entry("genetic_splicer",4),Map.entry("geno_station",2));
        for(var entry:counts.entrySet()) {
            var rows=(int[][])slotsFor.invoke(null,entry.getKey());
            if(rows.length!=entry.getValue())throw new AssertionError(entry.getKey()+" count mismatch");
            for(int i=0;i<rows.length;i++)if(rows[i][0]!=i)throw new AssertionError(entry.getKey()+" slot numbering");
            System.out.println("PASS "+entry.getKey()+": "+rows.length+" existing machine slots + 36 player slots");
        }
    }
}
