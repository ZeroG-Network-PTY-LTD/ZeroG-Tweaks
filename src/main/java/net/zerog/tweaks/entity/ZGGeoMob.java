package net.zerog.tweaks.entity;

import java.util.Set;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;

/**
 * A ZeroG mob drawn by ZGGeoMobRenderer from geo/<id>.geo.json + animations/<id>.animation.json. Each clip set has
 * idle, a movement loop, blink and attack (animation.zerog_tweaks.<id>.<clip>).
 */
public interface ZGGeoMob {
    /** Bones the renderer may hide, and which of them are hidden right now. */
    default Set<String> toggleableBones() { return Set.of(); }
    default Set<String> hiddenBones() { return Set.of(); }

    /** The art set to draw this mob with (base = the renderer's id); styled mobs return e.g. "mossback_autumn". */
    default String assetId(String base) { return base; }

    /** body: idle/move loop; eyes: blink; action: attack (both triggered from the server with triggerAnim). */
    static void registerControllers(GeoEntity mob, AnimatableManager.ControllerRegistrar controllers, String id, String moveClip) {
        String p = "animation.zerog_tweaks." + id + ".";
        RawAnimation idle = RawAnimation.begin().thenLoop(p + "idle");
        RawAnimation move = RawAnimation.begin().thenLoop(p + moveClip);
        controllers.add(new AnimationController<>(mob, "body", 4, s -> s.setAndContinue(s.isMoving() ? move : idle)));
        controllers.add(new AnimationController<>(mob, "eyes", 0, s -> PlayState.STOP)
                .triggerableAnim("blink", RawAnimation.begin().thenPlay(p + "blink")));
        controllers.add(new AnimationController<>(mob, "action", 2, s -> PlayState.STOP)
                .triggerableAnim("attack", RawAnimation.begin().thenPlay(p + "attack")));
    }
}
