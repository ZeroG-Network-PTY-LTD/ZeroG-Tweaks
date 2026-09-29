package net.zerog.tweaks.item;

import java.util.function.Consumer;
import javax.annotation.Nullable;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.ZeroGTweaks;
import software.bernie.geckolib.animatable.GeoItem;
import software.bernie.geckolib.animatable.client.GeoRenderProvider;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.model.DefaultedItemGeoModel;
import software.bernie.geckolib.renderer.GeoArmorRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Armor piece that renders the set's GeckoLib model (with the 3D extras) instead of the flat vanilla layers.
 * Files per set (all in resources/): geckolib/models/item/armor/<set>.geo.json,
 * geckolib/animations/item/armor/<set>.animation.json, textures/item/armor/<set>.png (+ _glowmask.png).
 * Example: new ZGGeoArmorItem(ZGArmorMaterials.SOLVANITE, ArmorItem.Type.HELMET, new Item.Properties(), "solvanite")
 * Written against GeckoLib 4.7 for 1.21.1; check GeoRenderProvider's signature if your version differs.
 */
public class ZGGeoArmorItem extends ArmorItem implements GeoItem {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final String setId;

    public ZGGeoArmorItem(Holder<ArmorMaterial> material, Type type, Properties props, String setId) {
        super(material, type, props);
        this.setId = setId;
    }

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {
        consumer.accept(new GeoRenderProvider() {
            private GeoArmorRenderer<?> renderer;

            @Override
            public <T extends LivingEntity> HumanoidModel<?> getGeoArmorRenderer(@Nullable T entity, ItemStack stack, @Nullable EquipmentSlot slot, @Nullable HumanoidModel<T> original) {
                if (renderer == null) {
                    renderer = new GeoArmorRenderer<>(new DefaultedItemGeoModel<ZGGeoArmorItem>(ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, "armor/" + setId)));
                    renderer.addRenderLayer(new AutoGlowingGeoLayer<>(renderer));
                }
                return renderer;
            }
        });
    }

    @Override public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {}
    @Override public AnimatableInstanceCache getAnimatableInstanceCache() { return cache; }
}
