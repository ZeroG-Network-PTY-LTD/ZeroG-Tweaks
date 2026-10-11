package net.zerog.tweaks.gametest;
import net.minecraft.gametest.framework.*;
import net.neoforged.neoforge.gametest.*;
import net.zerog.tweaks.machine.RecipeBrowserLayout;
@GameTestHolder("zerog_recipe_browser") @PrefixGameTestTemplate(false)
public final class RecipeBrowserLayoutGameTests {
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void back_and_escape_keep_overlay_mouse_releases_out_of_inventory(GameTestHelper h){
        var input=new net.zerog.tweaks.machine.RecipeBrowserInput();input.open();input.press(0);input.close();
        h.assertTrue(input.consumeRelease(0),"Back release fell through to the underlying carried-item slot");
        h.assertTrue(!input.consumeRelease(0),"An unrelated later inventory release was swallowed");
        input.open();input.press(0);input.press(1);input.close();
        h.assertTrue(input.consumeRelease(0)&&input.consumeRelease(1)&&!input.consumeRelease(2),"Closing during a drag lost overlay press ownership");
        input.open();h.assertTrue(input.consumeRelease(0),"Opening-button release reached hidden slots");
        input.close();h.assertTrue(!input.consumeRelease(0),"Closed idle browser blocked inventory forever");h.succeed();
    }
    @GameTest(templateNamespace="zerog_workflow_optional",template="equipment_empty",timeoutTicks=100)
    public static void recipes_and_back_button_fit_and_input_coordinates_match(GameTestHelper h){
        for(int[] viewport:new int[][]{{320,240},{384,216},{427,240},{640,360},{854,480}})
            for(int content:new int[]{208,224,250}){
                int width=viewport[0],height=viewport[1];var b=RecipeBrowserLayout.fit(width,height,content);
                double right=b.left()+174*b.scale(),bottom=b.top()+content*b.scale();
                h.assertTrue(b.left()>=0&&right<=width&&b.top()>=18,"Recipe panel clipped header/viewport");
                h.assertTrue(bottom+3<=b.backTop()&&b.backTop()+18<=height,"Back button overlaps recipes or falls outside screen");
                h.assertTrue(b.backLeft()>=0&&b.backLeft()+140<=width,"Back button clipped horizontally");
                double x=b.left()+87*b.scale(),y=b.top()+content/2.0*b.scale();
                h.assertTrue(Math.abs(b.localX(x)-87)<.001&&Math.abs(b.localY(y)-content/2.0)<.001,"Scaled pointer no longer matches recipe row");
            }
        h.succeed();
    }
}
