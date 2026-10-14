package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.blockentity.*;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.zerog.tweaks.machine.*;

/** Actual synchronized press jobs; preview visuals never create inventory items. */
public final class CompressorRenderer implements BlockEntityRenderer<ProcessingBlockEntity> {
    public CompressorRenderer(BlockEntityRendererProvider.Context context){}
    @Override public void render(ProcessingBlockEntity be,float partial,PoseStack poses,MultiBufferSource buffers,int light,int overlay){
        if(be.kind!=ProcessingRegistry.Kind.PRESSING)return;
        var mc=Minecraft.getInstance();
        float phase=Math.clamp((float)be.displayProgress/be.displayDuration,0,1);
        float compression=(float)Math.sin(Math.PI*phase);
        poses.pushPose();
        poses.translate(.5,0,.5);
        poses.mulPose(Axis.YP.rotationDegrees(-be.getBlockState().getValue(BlockStateProperties.HORIZONTAL_FACING).toYRot()-180));
        poses.translate(-.5,0,-.5);
        // Silver ram and telescoping shaft stay inside the one-block chassis.
        box(poses,buffers,light,overlay,.20F,.65F-.30F*compression,.12F,.60F,.10F,.60F);
        box(poses,buffers,light,overlay,.44F,.75F-.30F*compression,.36F,.12F,.20F+.30F*compression,.12F);
        item(be.displayDie,poses,buffers,light,overlay,.30F,.48F,.48F,false);
        boolean result=be.displayInput.isEmpty()||phase>.75F;
        item(result?be.displayResult:be.displayInput,poses,buffers,light,overlay,.345F,.45F,result?.13F:.24F*(1-.7F*compression),true);
        poses.popPose();
    }
    private static void box(PoseStack p,MultiBufferSource b,int light,int overlay,float x,float y,float z,float sx,float sy,float sz){
        p.pushPose();p.translate(x,y,z);p.scale(sx,sy,sz);Minecraft.getInstance().getBlockRenderer().renderSingleBlock(Blocks.IRON_BLOCK.defaultBlockState(),p,b,light,overlay);p.popPose();
    }
    private static void item(ItemStack stack,PoseStack p,MultiBufferSource b,int light,int overlay,float y,float scale,float thickness,boolean flatSprite){
        if(stack.isEmpty())return;p.pushPose();p.translate(.5,y,.43);if(flatSprite)p.mulPose(Axis.XP.rotationDegrees(90));p.scale(scale,scale,thickness);
        Minecraft.getInstance().getItemRenderer().renderStatic(stack,ItemDisplayContext.FIXED,light,overlay,p,b,null,0);p.popPose();
    }
}
