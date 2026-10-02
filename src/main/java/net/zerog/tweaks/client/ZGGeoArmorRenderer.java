package net.zerog.tweaks.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.core.component.DataComponents;
import javax.annotation.Nullable;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.armortrim.ArmorTrim;
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
 * GeckoLib 4.9's HumanoidArmorLayer mixin renders GeoItem armor itself and skips vanilla's
 * renderArmorPiece, so vanilla's trim pass never runs. After drawing the shell we therefore draw the
 * trim ourselves, exactly as HumanoidArmorLayer#renderTrim would: the item's trim sprite (darker palette
 * on same-material armor, the _leggings texture for leggings) on a vanilla-shaped armor box (64x32 trim
 * layout) just above the shell's base plates. Every trim pattern and material, ZeroG or vanilla, renders.
 * If vanilla's own trim pass ever reaches us (buffer wrapped in a SpriteCoordinateExpander) it is
 * skipped, so the trim is never drawn twice.
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
        if (buffer instanceof SpriteCoordinateExpander) {
            return; // vanilla trim pass: the trim was already drawn below
        }
        // GeckoLib clears currentStack/currentSlot/baseModel/bufferSource at the end of its render, so read them first
        var stack = this.currentStack;
        var slot = this.currentSlot;
        var base = this.baseModel;
        var buffers = this.bufferSource;
        super.renderToBuffer(poseStack, buffer, packedLight, packedOverlay, colour);
        renderEquippedTrim(poseStack, packedLight, stack, slot, base, buffers);
    }

    /** Same lookup as HumanoidArmorLayer#renderTrim, using the stack/slot/buffers GeckoLib handed us. */
    private static void renderEquippedTrim(PoseStack poseStack, int packedLight, @Nullable ItemStack stack,
            @Nullable EquipmentSlot slot, @Nullable HumanoidModel<?> base, @Nullable MultiBufferSource buffers) {
        if (stack == null || slot == null || base == null || buffers == null) return;
        ArmorTrim trim = stack.get(DataComponents.TRIM);
        if (trim == null || !(stack.getItem() instanceof ArmorItem armor)) return;
        boolean leggings = slot == EquipmentSlot.LEGS;
        TextureAtlasSprite sprite = Minecraft.getInstance().getModelManager().getAtlas(Sheets.ARMOR_TRIMS_SHEET)
                .getSprite(leggings ? trim.innerTexture(armor.getMaterial()) : trim.outerTexture(armor.getMaterial()));
        VertexConsumer trimBuffer = sprite.wrap(buffers.getBuffer(Sheets.armorTrimsSheet(trim.pattern().value().decal())));
        renderTrim(poseStack, trimBuffer, packedLight, OverlayTexture.NO_OVERLAY, -1, slot, base);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void renderTrim(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay, int colour,
            EquipmentSlot slot, HumanoidModel<?> base) {
        HumanoidModel<LivingEntity> model = slot == EquipmentSlot.LEGS ? innerTrimModel() : outerTrimModel();
        ((HumanoidModel) base).copyPropertiesTo(model);
        model.setAllVisible(false);
        switch (slot) {
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
