package net.zerog.tweaks.gametest;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.regex.Pattern;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.zerog.tweaks.travel.SurvivalGateLayout;

@GameTestHolder("zerog_codex_art") @PrefixGameTestTemplate(false)
public final class CodexIllustratedGameTests {
    private static String read(String name) throws java.io.IOException {
        try(var in=CodexIllustratedGameTests.class.getClassLoader().getResourceAsStream("assets/zerog_tweaks/guides/zerog_tweaks/concord_codex/"+name)){
            if(in==null)throw new java.io.IOException("Missing guide page "+name);
            return new String(in.readAllBytes(),StandardCharsets.UTF_8);
        }
    }
    @GameTest(templateNamespace="zerog_codex_art",template="equipment_empty",timeoutTicks=500)
    public static void parser_and_exact_gate_layers(GameTestHelper h) throws java.io.IOException {
        var tag=Pattern.compile("<Block id=\"([^\"]+)\" x=\"(-?\\d+)\" y=\"(-?\\d+)\" z=\"(-?\\d+)\" />");
        for(int tier=1;tier<=6;tier++){
            var name="gate_t"+tier+".md";var source=read(name);
            h.assertTrue(guideme.compiler.PageCompiler.parse("test",ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name),source)!=null,"GuideME parse failed");
            var expected=new HashMap<BlockPos,String>();
            for(var p:SurvivalGateLayout.parts(tier))expected.put(p.offset().offset(tier+1,2,tier+1),BuiltInRegistries.BLOCK.getKey(p.block()).toString());
            int start=source.lastIndexOf("<GameScene");
            var matches=tag.matcher(source.substring(start));var actual=new HashMap<BlockPos,String>();
            while(matches.find())h.assertTrue(actual.put(new BlockPos(Integer.parseInt(matches.group(2)),Integer.parseInt(matches.group(3)),Integer.parseInt(matches.group(4))),matches.group(1))==null,"Duplicate pictured cell");
            h.assertTrue(actual.equals(expected),"Tier "+tier+" illustration differs from live formation");
            var layers=new HashMap<BlockPos,String>();matches=tag.matcher(source.substring(0,start));
            while(matches.find())h.assertTrue(layers.put(new BlockPos(Integer.parseInt(matches.group(2)),Integer.parseInt(matches.group(3)),Integer.parseInt(matches.group(4))),matches.group(1))==null,"Duplicate layer cell");
            h.assertTrue(layers.equals(expected),"Tier "+tier+" layers omit/change live parts");
        }
        var names=new java.util.ArrayList<String>(java.util.List.of("index.md","16_gate_atlas.md","17_machine_fieldbook.md","18_impacts.md"));
        for(int t=1;t<=6;t++)names.add("gate_t"+t+".md");
        names.addAll(java.util.List.of("01_signal.md","03_power.md","04_launch.md","07_mining.md","09_tier2.md"));
        for(var name:names){
            var source=read(name);
            h.assertTrue(guideme.compiler.PageCompiler.parse("test",ResourceLocation.fromNamespaceAndPath("zerog_tweaks",name),source)!=null,"Page parse failed: "+name);
            var ids=Pattern.compile("<(?:ItemImage|BlockImage|ItemLink) id=\"(zerog_tweaks:[^\"]+)\"").matcher(source);
            while(ids.find())h.assertTrue(BuiltInRegistries.ITEM.containsKey(ResourceLocation.parse(ids.group(1))),"Missing illustration item: "+ids.group(1));
        }
        h.succeed();
    }
}
