package net.zerog.tweaks.item;

import java.util.function.Consumer;
import javax.annotation.Nullable;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.core.Holder;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.zerog.tweaks.client.ZGGeoArmorRenderer;
import software.bernie.geckolib.animatable.GeoItem;
import software.bernie.geckolib.animatable.client.GeoRenderProvider;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Armor piece that renders the set's GeckoLib model (chunky shell cubes) instead of the flat vanilla layers.
 * Files per set: geckolib/models/item/armor/<set>.geo.json, geckolib/animations/item/armor/<set>.animation.json,
 * textures/item/armor/<set>.png and <set>_glowmask.png. Rendering (glow layer, trims) lives in ZGGeoArmorRenderer.
 */
public class ZGGeoArmorItem extends ZGArmorItem implements GeoItem {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final String setId;

    public ZGGeoArmorItem(String setId, Holder<ArmorMaterial> material, Type type, Properties properties) {
        super(setId, material, type, properties);
        this.setId = setId;
    }

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {
        consumer.accept(new GeoRenderProvider() {
            private ZGGeoArmorRenderer renderer;

            @Override
            public <T extends LivingEntity> HumanoidModel<?> getGeoArmorRenderer(@Nullable T entity, ItemStack stack,
                    @Nullable EquipmentSlot slot, @Nullable HumanoidModel<T> original) {
                if (this.renderer == null) {
                    this.renderer = new ZGGeoArmorRenderer(setId);
                }
                return this.renderer;
            }
        });
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {}

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }
}
