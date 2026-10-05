package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;

/** Original six-face cuboid helper. Clockwise winding is deliberately avoided. */
final class StorageRenderGeometry {
    private StorageRenderGeometry() {}
    static void quad(VertexConsumer out, PoseStack.Pose pose, float[][] points,
                     float u0, float v0, float u1, float v1, int color, int light,
                     float nx, float ny, float nz) {
        float[][] uv={{u0,v1},{u1,v1},{u1,v0},{u0,v0}};
        for(int i=0;i<4;i++) out.addVertex(pose,points[i][0],points[i][1],points[i][2])
            .setColor((color>>>16)&255,(color>>>8)&255,color&255,(color>>>24)&255)
            .setUv(uv[i][0],uv[i][1]).setOverlay(net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY)
            .setLight(light).setNormal(pose,nx,ny,nz);
    }
    static float[][] face(int face,float x0,float y0,float z0,float x1,float y1,float z1) {
        return switch(face) {
            case 0 -> new float[][]{{x1,y0,z0},{x0,y0,z0},{x0,y1,z0},{x1,y1,z0}};
            case 1 -> new float[][]{{x0,y0,z1},{x1,y0,z1},{x1,y1,z1},{x0,y1,z1}};
            case 2 -> new float[][]{{x0,y0,z0},{x0,y0,z1},{x0,y1,z1},{x0,y1,z0}};
            case 3 -> new float[][]{{x1,y0,z1},{x1,y0,z0},{x1,y1,z0},{x1,y1,z1}};
            case 4 -> new float[][]{{x0,y1,z1},{x1,y1,z1},{x1,y1,z0},{x0,y1,z0}};
            default -> new float[][]{{x0,y0,z0},{x1,y0,z0},{x1,y0,z1},{x0,y0,z1}};
        };
    }
    static final float[][] NORMALS={{0,0,-1},{0,0,1},{-1,0,0},{1,0,0},{0,1,0},{0,-1,0}};
}
