package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.zerog.tweaks.storage.WoodStorageBlock;
import net.zerog.tweaks.storage.WoodStorageBlockEntity;

/** Retains original wood/trim faces; only the upper section moves about its hinge. */
public final class WoodStorageRenderer implements BlockEntityRenderer<WoodStorageBlockEntity> {
    private static final float HINGE=10.5F/16F,TOP=14F/16F;
    public WoodStorageRenderer(BlockEntityRendererProvider.Context context) {}
    @Override public void render(WoodStorageBlockEntity be,float partialTick,PoseStack poses,
                                 MultiBufferSource buffers,int light,int overlay) {
        if(!(be.getBlockState().getBlock() instanceof WoodStorageBlock.Chest))return;
        String id=BuiltInRegistries.BLOCK.getKey(be.getBlockState().getBlock()).getPath();
        poses.pushPose();
        poses.translate(.5,0,.5);
        poses.mulPose(Axis.YP.rotationDegrees(-be.getBlockState().getValue(BlockStateProperties.HORIZONTAL_FACING).toYRot()-180));
        poses.translate(-.5,0,-.5);
        box(id,poses,buffers,light,0,HINGE,.25F,1);
        poses.pushPose();
        poses.translate(0,HINGE,15F/16F);
        float open=be.lidOpenness(partialTick);
        open=1-(1-open)*(1-open)*(1-open);
        poses.mulPose(Axis.XP.rotationDegrees(90*open));
        poses.translate(0,-HINGE,-15F/16F);
        box(id,poses,buffers,light,HINGE,TOP,0,.25F);
        poses.popPose();
        poses.popPose();
    }
    private static void box(String id,PoseStack poses,MultiBufferSource buffers,int light,
                            float bottom,float top,float v0,float v1) {
        for(int face=0;face<6;face++){
            String suffix=face==0?"front":face==4?"top":face==5?"bottom":"side";
            var texture=ResourceLocation.fromNamespaceAndPath("zerog_tweaks","textures/block/"+id+"_"+suffix+".png");
            var out=buffers.getBuffer(RenderType.entityCutoutNoCull(texture));
            var n=StorageRenderGeometry.NORMALS[face];
            StorageRenderGeometry.quad(out,poses.last(),StorageRenderGeometry.face(face,1F/16F,bottom,1F/16F,15F/16F,top,15F/16F),
                0,face<4?v0:0,1,face<4?v1:1,0xffffffff,light,n[0],n[1],n[2]);
        }
    }
}
