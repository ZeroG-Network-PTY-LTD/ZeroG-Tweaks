package net.zerog.tweaks.client;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import com.google.gson.JsonParser;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;

/** Resource-reload-friendly profile; coordinates are bound to verified addon slot counts. */
public record MachineGuiProfile(String id,String namespace,List<String> roles,List<int[]> positions,List<String> metrics,
                                int outputStart,String purpose,boolean pending,boolean designOnly) {
    public static Optional<MachineGuiProfile> read(String namespace,String id) {
        var resource=Minecraft.getInstance().getResourceManager().getResource(
            ResourceLocation.fromNamespaceAndPath("zerog_tweaks","gui/machine_profiles.json"));
        if(resource.isEmpty())return Optional.empty();
        try(var stream=resource.get().open();var reader=new InputStreamReader(stream,StandardCharsets.UTF_8)) {
            var all=JsonParser.parseReader(reader).getAsJsonObject();var key=namespace+":"+id;
            if(!all.has(key))return Optional.empty();var obj=all.getAsJsonObject(key);
            var roles=new ArrayList<String>();obj.getAsJsonArray("slots").forEach(v->roles.add(v.getAsString()));
            var positions=new ArrayList<int[]>();obj.getAsJsonArray("positions").forEach(v->{
                var xy=v.getAsJsonArray();positions.add(new int[]{xy.get(0).getAsInt(),xy.get(1).getAsInt()});
            });
            var metrics=new ArrayList<String>();obj.getAsJsonArray("metrics").forEach(v->metrics.add(v.getAsString()));
            int output=obj.get("outputStart").getAsInt();
            if(roles.size()!=positions.size()||roles.size()>9||output<0||output>roles.size())return Optional.empty();
            for(var xy:positions)if(xy[0]<1||xy[0]+16>255||xy[1]<19||xy[1]+16>75)return Optional.empty();
            return Optional.of(new MachineGuiProfile(id,namespace,List.copyOf(roles),List.copyOf(positions),List.copyOf(metrics),
                output,obj.get("purpose").getAsString(),obj.get("pending").getAsBoolean(),obj.get("designOnly").getAsBoolean()));
        } catch(Exception ex) {return Optional.empty();} // Bad optional pack keeps the original screen.
    }
    public ResourceLocation background(){return ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/gui/workbench/"+id+".png");}
}
