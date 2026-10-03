package net.zerog.tweaks.client;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockAndTintGetter;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ModelEvent;
import net.neoforged.neoforge.client.model.BakedModelWrapper;
import net.neoforged.neoforge.client.model.data.ModelData;
import net.neoforged.neoforge.client.model.data.ModelProperty;
import net.zerog.tweaks.registry.ZGStarGlassBlock;

/** Shared galaxy projection for rectangular coplanar windows, no external CTM mod. */
@EventBusSubscriber(modid="zerog_tweaks",value=Dist.CLIENT)
public final class ConnectedStarGlassModel extends BakedModelWrapper<BakedModel> {
    private static final ModelProperty<int[][]> RECTANGLES=new ModelProperty<>();
    private static final int LIMIT=16;
    private ConnectedStarGlassModel(BakedModel base) {super(base);}
    @SubscribeEvent public static void bake(ModelEvent.ModifyBakingResult event) {
        event.getModels().replaceAll((key,model) -> key.id().getNamespace().equals("zerog_tweaks")
                && key.id().getPath().equals("star_glass") && !key.variant().equals("inventory")
                ? new ConnectedStarGlassModel(model):model);
    }
    private static Direction horizontal(Direction face) {return face.getAxis()==Direction.Axis.X?Direction.SOUTH:Direction.EAST;}
    private static Direction vertical(Direction face) {return face.getAxis()==Direction.Axis.Y?Direction.SOUTH:Direction.UP;}
    private static int run(BlockAndTintGetter level,BlockPos pos,BlockState state,Direction direction) {
        int distance=0;
        while(distance<LIMIT) {
            var other=level.getBlockState(pos.relative(direction,distance+1));
            if(!(other.getBlock() instanceof ZGStarGlassBlock) || other.getValue(ZGStarGlassBlock.NEBULA)!=state.getValue(ZGStarGlassBlock.NEBULA)) break;
            distance++;
        }
        return distance;
    }
    @Override public ModelData getModelData(BlockAndTintGetter level,BlockPos pos,BlockState state,ModelData original) {
        if(!(state.getBlock() instanceof ZGStarGlassBlock)) return original;
        var rectangles=new int[6][4];
        for(var face:Direction.values()) {
            var h=horizontal(face);var v=vertical(face);
            rectangles[face.ordinal()]=new int[]{run(level,pos,state,h.getOpposite()),run(level,pos,state,h),
                    run(level,pos,state,v.getOpposite()),run(level,pos,state,v)};
        }
        return original.derive().with(RECTANGLES,rectangles).build();
    }
    private static float coordinate(int[] vertices,int index,Direction direction) {
        return Float.intBitsToFloat(vertices[index+switch(direction.getAxis()){case X->0;case Y->1;case Z->2;}]);
    }
    @Override public List<BakedQuad> getQuads(BlockState state,Direction face,RandomSource random,ModelData data,RenderType type) {
        var original=super.getQuads(state,face,random,data,type);
        var rectangles=data.get(RECTANGLES);
        if(face==null || rectangles==null) return original;
        int[] r=rectangles[face.ordinal()];
        if(r[0]+r[1]+r[2]+r[3]==0) return original;
        var output=new ArrayList<BakedQuad>();
        for(var quad:original) {
            int[] vertices=quad.getVertices().clone();int stride=vertices.length/4;
            var sprite=quad.getSprite();
            for(int i=0;i<4;i++) {
                int at=i*stride;float h=coordinate(vertices,at,horizontal(face)),v=coordinate(vertices,at,vertical(face));
                float u=(r[0]+h)/(r[0]+r[1]+1F),w=1-(r[2]+v)/(r[2]+r[3]+1F);
                // Exclude the old per-block quartz border. Reapply only the outer
                // silhouette below, so internal joins show one larger universe.
                vertices[at+4]=Float.floatToRawIntBits(sprite.getU(.0625F+u*.875F));
                vertices[at+5]=Float.floatToRawIntBits(sprite.getV(.0625F+w*.875F));
            }
            output.add(new BakedQuad(vertices,quad.getTintIndex(),quad.getDirection(),sprite,quad.isShade(),quad.hasAmbientOcclusion()));
            for(int edge=0;edge<4;edge++) if(r[edge]==0) {
                int[] strip=quad.getVertices().clone();int axis=coordinateAxis(edge<2?horizontal(face):vertical(face));
                boolean upper=(edge&1)==1;
                for(int i=0;i<4;i++) {
                    int at=i*stride;float p=Float.intBitsToFloat(strip[at+axis]);
                    strip[at+axis]=Float.floatToRawIntBits(upper?.975F+p*.025F:p*.025F);
                    // Quartz sits just outside the galaxy pane, not coplanar.
                    int normal=coordinateAxis(face);
                    strip[at+normal]=Float.floatToRawIntBits(Float.intBitsToFloat(strip[at+normal])+face.getAxisDirection().getStep()*.001F);
                    // A narrow quartz-edge texel, without stretching the galaxy.
                    strip[at+4]=Float.floatToRawIntBits(sprite.getU(.018F));
                    strip[at+5]=Float.floatToRawIntBits(sprite.getV(.1F+i*.2F));
                }
                output.add(new BakedQuad(strip,-1,face,sprite,quad.isShade(),quad.hasAmbientOcclusion()));
            }
        }
        return output;
    }
    private static int coordinateAxis(Direction direction) {return switch(direction.getAxis()){case X->0;case Y->1;case Z->2;};}
}
