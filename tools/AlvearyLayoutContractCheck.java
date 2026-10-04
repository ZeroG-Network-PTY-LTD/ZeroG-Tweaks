import net.zerog.tweaks.guide.AlvearyLayout;
import java.util.HashSet;

/** No game launch: validates the actual addon's public static slot table against our layout. */
public final class AlvearyLayoutContractCheck {
    public static void main(String[] args)throws Exception {
        var layouts=Class.forName("com.zerog.aeroapiary.MachineSlotLayouts");
        var slotsFor=layouts.getMethod("slotsFor",String.class);
        String[] ids={"tier1_controller","tier2_controller","tier3_controller","tier4_controller",
            "tier5_controller","tier6_controller","tier7_controller","apiary_controller","zero_g_hive"};
        for(String id:ids) {
            int tier=AlvearyLayout.tier(id);int[][] slots=(int[][])slotsFor.invoke(null,id);
            if(slots.length!=AlvearyLayout.machineSlots(tier))throw new AssertionError(id+" count "+slots.length);
            for(int page=0;page<(AlvearyLayout.products(tier)+8)/9;page++) {
              var positions=new HashSet<String>();
              for(int i=0;i<slots.length+36;i++) {
                if(i<slots.length && slots[i][0]!=i)throw new AssertionError(id+" reordered slot "+i);
                int[] pos=AlvearyLayout.position(tier,i,page);
                if(!AlvearyLayout.visible(tier,i,page))continue;
                if(pos[0]<0||pos[0]+16>256||pos[1]<0||pos[1]+16>250)throw new AssertionError(id+" out of bounds");
                if(!positions.add(pos[0]+","+pos[1]))throw new AssertionError(id+" duplicate position");
            }
            }
            System.out.println("PASS "+id+": "+slots.length+" machine + 36 player slots; stable IDs and unique visible positions across product pages");
        }
    }
}
