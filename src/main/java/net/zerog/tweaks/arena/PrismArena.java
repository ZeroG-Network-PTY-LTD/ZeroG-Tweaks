package net.zerog.tweaks.arena;

/**
 * Measurements of the Prism Sentinel arena template (structure/prism_sentinel_arena.nbt, built by Design
 * structures/prism_sentinel_arena/build_prism_arena_v3.py), relative to the Concord Prism at the dais centre.
 * The Sentinel and the prism read the arena only through these, so they stay right for any rotation of the
 * structure; change them together with the template.
 */
public final class PrismArena {
    /** The prism sits on the 2-step dais: the fight floor surface is this far below it (blocks stand on floor + 1). */
    public static final int FLOOR_BELOW_PRISM = 3;
    /** Flat fight floor radius; the dais covers r <= 4, the 4 pylons stand on the diagonals at r ~18.4. */
    public static final double FLOOR_RADIUS = 22;
    public static final double DAIS_RADIUS = 4;
    /** Half the template footprint (67 x 67): the arena box. */
    public static final double HALF = 33.5;
    /** The wall ring the entrance cuts through, and the opening (7 wide, 9 tall above the floor). */
    public static final int ENTRANCE_NEAR = 28, ENTRANCE_FAR = 29, ENTRANCE_HALF_WIDTH = 3, ENTRANCE_HEIGHT = 9;
    /** Centre of the crystal oculus above the prism (shimmer glass, lit as a pulsar lamp after a victory). */
    public static final int OCULUS_ABOVE_PRISM = 32;
    /** The Sentinel appears this far from the prism on the entrance side, facing whoever opened the test. */
    public static final double SENTINEL_START = 10;

    private PrismArena() {}
}
