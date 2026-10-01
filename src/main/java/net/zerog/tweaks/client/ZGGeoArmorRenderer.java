package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.renderer.SpriteCoordinateExpander;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.zerog.tweaks.ZeroGTweaks;
import net.zerog.tweaks.item.ZGGeoArmorItem;
import software.bernie.geckolib.model.DefaultedItemGeoModel;
import software.bernie.geckolib.renderer.GeoArmorRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

/**
 * GeckoLib armor renderer that keeps vanilla armor trims working.
 *
 * Vanilla's HumanoidArmorLayer draws a trim by calling renderToBuffer again with the trim sprite
 * wrapped around the buffer (a SpriteCoordinateExpander). The GeckoLib model would just redraw itself,
 * so on that pass we instead draw a vanilla-shaped armor box (64x32 trim layout) just above the
 * shell's base plates. Every trim pattern and material, ZeroG or vanilla, renders as on vanilla armor.
 */
public class ZGGeoArmorRenderer extends GeoArmorRenderer<ZGGeoArmorItem> {
    // a hair above the geo base boxes (outer 1.0-1.01, leggings 0.5) so trims don't z-fight
    private static HumanoidModel<LivingEntity> outerTrimModel;
    private static HumanoidModel<LivingEntity> innerTrimModel;

    public ZGGeoArmorRenderer(String setId) {
        super(new DefaultedItemGeoModel<>(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "armor/" + setId)));
        addRenderLayer(new AutoGlowingGeoLayer<>(this));
    }

    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay, int colour) {
        if (buffer instanceof SpriteCoordinateExpander && this.baseModel != null && this.currentSlot != null) {
            renderTrim(poseStack, buffer, packedLight, packedOverlay, colour);
            return;
        }
        super.renderToBuffer(poseStack, buffer, packedLight, packedOverlay, colour);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private void renderTrim(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay, int colour) {
        HumanoidModel<LivingEntity> model = this.currentSlot == EquipmentSlot.LEGS ? innerTrimModel() : outerTrimModel();
        ((HumanoidModel) this.baseModel).copyPropertiesTo(model);
        model.setAllVisible(false);
        switch (this.currentSlot) {
            case HEAD -> model.head.visible = true;
            case CHEST -> {
                model.body.visible = true;
                model.rightArm.visible = true;
                model.leftArm.visible = true;
            }
            // GeckoLib leggings have no body bone, so keep the trim on the legs only
            case LEGS, FEET -> {
                model.rightLeg.visible = true;
                model.leftLeg.visible = true;
            }
            default -> {}
        }
        model.renderToBuffer(poseStack, buffer, packedLight, packedOverlay, colour);
    }

    private static HumanoidModel<LivingEntity> outerTrimModel() {
        if (outerTrimModel == null) outerTrimModel = bake(1.05F);
        return outerTrimModel;
    }

    private static HumanoidModel<LivingEntity> innerTrimModel() {
        if (innerTrimModel == null) innerTrimModel = bake(0.55F);
        return innerTrimModel;
    }

    private static HumanoidModel<LivingEntity> bake(float inflate) {
        return new HumanoidModel<>(LayerDefinition.create(HumanoidModel.createMesh(new CubeDeformation(inflate), 0.0F), 64, 32).bakeRoot());
    }
}
