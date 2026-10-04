import java.util.Map;
import java.util.Arrays;
/** Read-only inspection of the installed addon's actual layout contract; no game launch. */
public final class ApiaryMachineLayoutProbe {
    public static void main(String[] args)throws Exception {
        var type=Class.forName("com.zerog.aeroapiary.MachineSlotLayouts");
        var field=type.getDeclaredField("LAYOUT");field.setAccessible(true);
        @SuppressWarnings("unchecked") var map=(Map<String,int[][]>)field.get(null);
        map.entrySet().stream().sorted(Map.Entry.comparingByKey()).forEach(e->{
            System.out.println(e.getKey()+" "+Arrays.deepToString(e.getValue()));
        });
    }
}
