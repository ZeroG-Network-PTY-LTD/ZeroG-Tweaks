package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.world.inventory.InventoryMenu;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.zerog.tweaks.storage.StorageTankBlockEntity;

/** Actual synchronized contents use the registered sprite, tint and luminosity. */
public final class StorageTankRenderer implements BlockEntityRenderer<StorageTankBlockEntity> {
    public StorageTankRenderer(BlockEntityRendererProvider.Context context) {}
    @Override public void render(StorageTankBlockEntity be,float partialTick,PoseStack poses,
                                 MultiBufferSource buffers,int light,int overlay) {
        var stack=be.tank.getFluid();
        if(stack.isEmpty())return;
        var extension=IClientFluidTypeExtensions.of(stack.getFluid());
        var still=extension.getStillTexture(stack);
        if(still==null)return;
        var sprite=Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(still);
        int tint=extension.getTintColor(stack);
        if((tint>>>24)==0)tint|=0xff000000;
        int emitted=stack.getFluid().getFluidType().getLightLevel(stack);
        light=LightTexture.pack(Math.max(LightTexture.block(light),emitted),LightTexture.sky(light));
        float fill=Math.max(0,Math.min(1,(float)stack.getAmount()/be.capacity()));
        float bottom=.125F,top=bottom+.75F*fill;
        if(net.zerog.tweaks.registry.ZGGases.isGas(stack.getFluid())) {
            // Contained gas occupies the chamber, not a falsely depicted liquid pool.
            top=.875F;tint=(tint&0x00ffffff)|((int)(32+96*fill)<<24);
        }
        var out=buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS));
        for(int f=0;f<6;f++){
            var n=StorageRenderGeometry.NORMALS[f];
            StorageRenderGeometry.quad(out,poses.last(),StorageRenderGeometry.face(f,.125F,bottom,.125F,.875F,top,.875F),
                sprite.getU0(),sprite.getV0(),sprite.getU1(),sprite.getV1(),tint,light,n[0],n[1],n[2]);
        }
    }
}
