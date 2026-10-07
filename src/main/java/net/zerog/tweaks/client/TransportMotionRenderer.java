package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.*;
import net.minecraft.client.renderer.blockentity.*;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemDisplayContext;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.zerog.tweaks.transport.TransportBlockEntity;

/** One small content preview following a real server-committed route; no inventory ownership. */
public final class TransportMotionRenderer implements BlockEntityRenderer<TransportBlockEntity> {
    public TransportMotionRenderer(BlockEntityRendererProvider.Context context){}
    @Override public void render(TransportBlockEntity be,float partial,PoseStack poses,MultiBufferSource buffers,int light,int overlay){
        if(be.getLevel()==null)return;float elapsed=be.getLevel().getGameTime()-be.motionTick+partial;
        if(elapsed<0||elapsed>=10||be.motionItem.isEmpty()&&be.motionFluid.isEmpty()&&be.motionEnergy<=0)return;
        float t=elapsed/10;var from=Direction.values()[be.motionFrom];var to=Direction.values()[be.motionTo];
        // Travel through the junction centre, rather than cutting diagonally through its casing.
        float incoming=Math.max(0,1-2*t),outgoing=Math.max(0,2*t-1);
        float x=.5F+.45F*(incoming*from.getStepX()+outgoing*to.getStepX());
        float y=.5F+.45F*(incoming*from.getStepY()+outgoing*to.getStepY());
        float z=.5F+.45F*(incoming*from.getStepZ()+outgoing*to.getStepZ());
        poses.pushPose();poses.translate(x,y,z);
        if(!be.motionItem.isEmpty()) {
            poses.scale(.28F,.28F,.28F);
            Minecraft.getInstance().getItemRenderer().renderStatic(be.motionItem,ItemDisplayContext.FIXED,light,overlay,poses,buffers,be.getLevel(),0);
        }else if(be.motionEnergy>0) {
            var sprite=Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(ResourceLocation.withDefaultNamespace("block/white_concrete"));
            var out=buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS));
            float radius=.035F+.015F*(float)Math.sin(t*Math.PI);
            for(int f=0;f<6;f++){var n=StorageRenderGeometry.NORMALS[f];StorageRenderGeometry.quad(out,poses.last(),StorageRenderGeometry.face(f,-radius,-radius,-radius,radius,radius,radius),sprite.getU0(),sprite.getV0(),sprite.getU1(),sprite.getV1(),0xff9af3ff,LightTexture.FULL_BRIGHT,n[0],n[1],n[2]);}
        }else {
            var fluid=be.motionFluid;var ext=IClientFluidTypeExtensions.of(fluid.getFluid());var texture=ext.getFlowingTexture(fluid);
            if(texture==null)texture=ext.getStillTexture(fluid);
            if(texture!=null){var sprite=Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(texture);
                int tint=ext.getTintColor(fluid);if((tint>>>24)==0)tint|=0xff000000;
                light=LightTexture.pack(Math.max(LightTexture.block(light),fluid.getFluid().getFluidType().getLightLevel(fluid)),LightTexture.sky(light));
                var out=buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS));
                // Short, independently undulating ribbons retain the actual fluid's flowing texture.
                for(int band=0;band<3;band++){
                    float wave=.018F*(float)Math.sin((t*2+band*.35F)*Math.PI*2);
                    float offset=(band-1)*.055F;
                    float minX=-.025F,minY=-.05F+wave,minZ=-.09F,maxX=.025F,maxY=.025F+wave,maxZ=.09F;
                    if(to.getAxis()==Direction.Axis.X){minX=-.09F;maxX=.09F;minZ=offset-.025F;maxZ=offset+.025F;}
                    else if(to.getAxis()==Direction.Axis.Z){minX=offset-.025F;maxX=offset+.025F;}
                    else {minX=offset-.025F;maxX=offset+.025F;minY=-.09F;maxY=.09F;minZ=-.025F;maxZ=.025F;}
                    for(int f=0;f<6;f++){var n=StorageRenderGeometry.NORMALS[f];StorageRenderGeometry.quad(out,poses.last(),StorageRenderGeometry.face(f,minX,minY,minZ,maxX,maxY,maxZ),sprite.getU0(),sprite.getV0(),sprite.getU1(),sprite.getV1(),tint,light,n[0],n[1],n[2]);}
                }
            }
        }
        poses.popPose();
    }
}
