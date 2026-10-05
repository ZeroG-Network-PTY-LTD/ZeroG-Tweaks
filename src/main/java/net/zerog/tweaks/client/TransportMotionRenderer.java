package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.*;
import net.minecraft.client.renderer.blockentity.*;
import net.minecraft.core.Direction;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemDisplayContext;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.zerog.tweaks.transport.TransportBlockEntity;

/** One small content preview following a real server-committed route; no inventory ownership. */
public final class TransportMotionRenderer implements BlockEntityRenderer<TransportBlockEntity> {
    public TransportMotionRenderer(BlockEntityRendererProvider.Context context){}
    @Override public void render(TransportBlockEntity be,float partial,PoseStack poses,MultiBufferSource buffers,int light,int overlay){
        if(be.getLevel()==null)return;float elapsed=be.getLevel().getGameTime()-be.motionTick+partial;
        if(elapsed<0||elapsed>=10||be.motionItem.isEmpty()&&be.motionFluid.isEmpty())return;
        float t=elapsed/10;var from=Direction.values()[be.motionFrom];var to=Direction.values()[be.motionTo];
        float x=.5F+.45F*((1-t)*from.getStepX()+t*to.getStepX());
        float y=.5F+.45F*((1-t)*from.getStepY()+t*to.getStepY());
        float z=.5F+.45F*((1-t)*from.getStepZ()+t*to.getStepZ());
        poses.pushPose();poses.translate(x,y,z);
        if(!be.motionItem.isEmpty()) {
            poses.scale(.28F,.28F,.28F);
            Minecraft.getInstance().getItemRenderer().renderStatic(be.motionItem,ItemDisplayContext.FIXED,light,overlay,poses,buffers,be.getLevel(),0);
        }else {
            var fluid=be.motionFluid;var ext=IClientFluidTypeExtensions.of(fluid.getFluid());var texture=ext.getStillTexture(fluid);
            if(texture!=null){var sprite=Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(texture);
                int tint=ext.getTintColor(fluid);if((tint>>>24)==0)tint|=0xff000000;
                light=LightTexture.pack(Math.max(LightTexture.block(light),fluid.getFluid().getFluidType().getLightLevel(fluid)),LightTexture.sky(light));
                var out=buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS));
                for(int f=0;f<6;f++){var n=StorageRenderGeometry.NORMALS[f];StorageRenderGeometry.quad(out,poses.last(),StorageRenderGeometry.face(f,-.09F,-.09F,-.09F,.09F,.09F,.09F),sprite.getU0(),sprite.getV0(),sprite.getU1(),sprite.getV1(),tint,light,n[0],n[1],n[2]);}
            }
        }
        poses.popPose();
    }
}
