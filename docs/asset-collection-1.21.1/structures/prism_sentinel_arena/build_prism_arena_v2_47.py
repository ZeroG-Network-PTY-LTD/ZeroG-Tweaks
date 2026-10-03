"""Prism Sentinel arena v2 ("Keeper's Proving Hall", Cerulon) per Design briefs/prism_sentinel_arena.md.

usage: python build_prism_arena_v2.py OUT.nbt
Template 47 x 32 x 47, centre column (23, *, 23), fight floor surface at y = 3 (foundation y 0-2 below), entrance south (+z).
Rings (radius from centre): dais r0-4, fight floor r5-15 (flat, recessed pulsar lamp lines), 4 refractor pylons on the
diagonals at r~12.7, tiered stands r16-19, outer wall r19.6-21.6 with buttresses every 45 degrees out to r23, open
lattice dome (8 ribs) to a ring + crystal oculus at y 28-30. Nothing over the fight floor below y 21 (floor + 18).
Only Cerulon decor blocks: no ores, storage blocks, gate/machine parts, vanilla amethyst, sea lanterns or Prismstone.
"""
import gzip, math, random, struct, sys

rng = random.Random(4242)
Z = "zerog_tweaks:"
SX, SY, SZ = 47, 32, 47
C = 23
FLOOR = 3
B = {}        # (x, y, z) -> block state string, template-local
ENTITIES = []


def put(dx, y, dz, block):
    x, z = C + dx, C + dz
    if 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ:
        B[(x, y, z)] = block


def r_of(dx, dz):
    return math.hypot(dx, dz)


def ang_of(dx, dz):
    return (math.degrees(math.atan2(dz, dx)) + 360) % 360


def entrance(dx, dz):
    return dz > 0 and abs(dx) <= 2


def cells(rmax):
    for dx in range(-23, 24):
        for dz in range(-23, 24):
            if r_of(dx, dz) <= rmax:
                yield dx, dz


# ---- clear the inside (so terrain doesn't fill the hall) ----------------------------------------------------------------
for dx, dz in cells(21.6):
    for y in range(FLOOR + 1, SY):
        put(dx, y, dz, "minecraft:air")

# ---- foundation and fight floor ---------------------------------------------------------------------------------------
for dx, dz in cells(23.6):
    r = r_of(dx, dz)
    for y in range(0, FLOOR):
        put(dx, y, dz, Z + ("cobbled_cerulean_stone" if y == 0 else "cerulean_stone"))
    b = Z + "polished_cerulean_stone"
    if 9.6 <= r <= 10.5:
        b = Z + "smooth_cerulean_stone"                       # inner trim ring
    if 15.0 <= r <= 15.9:
        b = Z + "polished_black_cerulean_stone_bricks"        # floor edge
    if 5.5 <= r <= 14.9 and (dx == 0 or dz == 0 or abs(dx) == abs(dz)):
        b = Z + "pulsar_lamp"                                 # 8 radial light lines, flush with the floor
    if r > 15.9:
        b = Z + "cerulean_stone_bricks"
    put(dx, FLOOR, dz, b)

# ---- dais r0-4: two steps, black trim, crystal inlay, Concord Prism at the centre ---------------------------------------
for dx, dz in cells(4.0):
    r = r_of(dx, dz)
    put(dx, FLOOR + 1, dz, Z + ("chiseled_polished_black_cerulean_stone" if r > 3.2 else "polished_black_cerulean_stone"))
    if r <= 2.9:
        top = Z + "polished_cerulean_stone"
        if abs(dx) == abs(dz) and r >= 1.4:
            top = Z + "crystal_glass"                          # inlay pointing at the 4 pylons
        if r > 2.2 and (dx == 0 or dz == 0):
            top = Z + "pulsar_lamp"
        put(dx, FLOOR + 2, dz, top)
put(0, FLOOR + 2, 0, Z + "polished_black_cerulean_stone")
put(0, FLOOR + 3, 0, Z + "concord_prism[state=idle]")

# ---- 4 refractor pylons on the diagonals (beam cover) -------------------------------------------------------------------
for sx, sz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
    px, pz = 9 * sx, 9 * sz
    for ox in (-1, 0, 1):
        for oz in (-1, 0, 1):
            for y in range(FLOOR + 1, FLOOR + 7):
                b = Z + "polished_black_cerulean_stone_bricks"
                if y in (FLOOR + 1, FLOOR + 6):
                    b = Z + "chiseled_polished_black_cerulean_stone"
                if ox == 0 and oz == 0 or (ox == 0 or oz == 0) and FLOOR + 2 <= y <= FLOOR + 5:
                    b = Z + "crystal_glass"                    # glowing crystal core, visible through the slots
                if ox == 0 and oz == 0 and y == FLOOR + 3:
                    b = Z + "spectral_lantern"
                put(px + ox, y, pz + oz, b)
    put(px, FLOOR + 7, pz, Z + "cerulite_cluster[facing=up,waterlogged=false]")

# ---- tiered stands r16-19: 3 steps rising outward ----------------------------------------------------------------------
STAND = [(15.9, 16.9, 1), (16.9, 17.9, 2), (17.9, 19.6, 3)]
for dx, dz in cells(19.6):
    r = r_of(dx, dz)
    if r < 15.9 or entrance(dx, dz):
        continue
    for lo, hi, h in STAND:
        if lo <= r < hi:
            for y in range(FLOOR + 1, FLOOR + h + 1):
                b = Z + "cerulean_stone_bricks"
                if y == FLOOR + h:
                    b = Z + "smooth_cerulean_stone"
                put(dx, y, dz, b)

# lit risers: a spectral lantern every 30 degrees on each step face, and one in the wall's inner face
for k in range(12):
    a = math.radians(30 * k + 15)
    for rr, y in ((16.4, FLOOR + 1), (17.4, FLOOR + 2), (19.8, FLOOR + 4)):
        dx, dz = round(rr * math.cos(a)), round(rr * math.sin(a))
        if not entrance(dx, dz):
            put(dx, y, dz, Z + "spectral_lantern")

# old rail line on the top step (4-connected ring at r ~18.8), with a few parked minecarts
ring = []
for i in range(720):
    a = math.radians(i / 2)
    p = (round(18.8 * math.cos(a)), round(18.8 * math.sin(a)))
    if not ring or ring[-1] != p:
        if ring and abs(p[0] - ring[-1][0]) == 1 and abs(p[1] - ring[-1][1]) == 1:
            ring.append((p[0], ring[-1][1]))                  # fill the diagonal step: rails need edge neighbours
        ring.append(p)
while ring[-1] == ring[0]:
    ring.pop()
DIR = {(0, -1): "north", (0, 1): "south", (1, 0): "east", (-1, 0): "west"}
for i, (dx, dz) in enumerate(ring):
    if entrance(dx, dz):
        continue
    a = ring[i - 1]; b = ring[(i + 1) % len(ring)]
    d1 = DIR[(a[0] - dx, a[1] - dz)]; d2 = DIR[(b[0] - dx, b[1] - dz)]
    pair = {d1, d2}
    if pair == {"north", "south"}: shape = "north_south"
    elif pair == {"east", "west"}: shape = "east_west"
    else:
        shape = ("south" if "south" in pair else "north") + "_" + ("east" if "east" in pair else "west")
    put(dx, FLOOR + 4, dz, f"minecraft:rail[shape={shape},waterlogged=false]")
for k, ang in enumerate((200, 290, 340)):
    a = math.radians(ang)
    dx, dz = round(18.8 * math.cos(a)), round(18.8 * math.sin(a))
    if (dx, dz) in ring:
        ENTITIES.append((C + dx + 0.5, FLOOR + 4.0625, C + dz + 0.5, C + dx, FLOOR + 4, C + dz))

# ---- outer wall r19.6-21.6, 9 tall, crystal-vein windows, chiseled band -------------------------------------------------
WALL_TOP = FLOOR + 9
for dx, dz in cells(21.6):
    r = r_of(dx, dz)
    if r < 19.6:
        continue
    ang = ang_of(dx, dz)
    for y in range(FLOOR + 1, WALL_TOP + 1):
        if entrance(dx, dz) and y <= FLOOR + 7:
            continue
        b = Z + "cerulean_stone_bricks"
        if y <= FLOOR + 2 and rng.random() < 0.18:
            b = Z + "cracked_cerulean_stone_bricks"
        if y == FLOOR + 5:
            b = Z + "chiseled_cerulean_stone"
        if y == WALL_TOP:
            b = Z + "polished_black_cerulean_stone_bricks"
        # crystal vein slits halfway between buttresses: crystal glass behind chiseled stone
        if abs((ang % 45) - 22.5) < 2.2 and FLOOR + 3 <= y <= FLOOR + 8 and y != FLOOR + 5:
            b = Z + ("crystal_glass" if r < 20.6 else "shimmer_glass")
        put(dx, y, dz, b)
# half-cut crystal on the outer face, as if the miners stopped mid-job
for k in range(6):
    a = math.radians(rng.choice([10, 55, 100, 145, 235, 325]) + rng.uniform(-6, 6))
    dx, dz = round(21.6 * math.cos(a)), round(21.6 * math.sin(a))
    y = FLOOR + rng.randint(2, 5)
    put(dx, y, dz, Z + "cerulean_geode_shell")
    put(dx, y + 1, dz, Z + "cerulean_geode_shell")

CROWNS = []
# ---- buttresses every 45 degrees (not on the entrance), cluster crowns -------------------------------------------------
for k in range(8):
    a = math.radians(45 * k)
    if k == 2:      # 90 degrees = south = entrance: the arch takes that spot
        continue
    for rr in (21.6, 22.6, 23.4):
        for side in (-1, 0, 1):
            dx = round(rr * math.cos(a) - side * math.sin(a))
            dz = round(rr * math.sin(a) + side * math.cos(a))
            top = WALL_TOP + 1 if rr < 22 else (WALL_TOP - 2 if rr < 23 else FLOOR + 4)
            for y in range(FLOOR + 1, top + 1):
                b = Z + ("polished_black_cerulean_stone_bricks" if y >= top - 1 else "cerulean_stone_bricks")
                put(dx, y, dz, b)
            if rr < 22 and side == 0:
                CROWNS.append((dx, top + 1, dz))
    # azure moss creeping at the foot of the buttress
    for side in (-2, 2):
        dx = round(22.6 * math.cos(a) - side * math.sin(a)); dz = round(22.6 * math.sin(a) + side * math.cos(a))
        put(dx, FLOOR, dz, Z + "azure_moss")

# ---- entrance arch (south): carved stone arch, Concord mark, pulsar-lamp pillars, walkway -------------------------------
for dz in range(16, 24):
    for dx in range(-2, 3):
        put(dx, FLOOR, dz, Z + ("polished_black_cerulean_stone" if abs(dx) == 2 else "polished_cerulean_stone"))
for dz in range(19, 23):
    for dx in (-3, 3):
        for y in range(FLOOR + 1, FLOOR + 8):
            put(dx, y, dz, Z + ("pulsar_lamp" if dz == 22 and y in (FLOOR + 2, FLOOR + 5) else "polished_black_cerulean_stone_bricks"))
    for dx in range(-3, 4):
        put(dx, FLOOR + 8, dz, Z + "chiseled_polished_black_cerulean_stone")
        put(dx, FLOOR + 9, dz, Z + "polished_black_cerulean_stone_bricks")
for dx in (-2, -1, 1, 2):
    put(dx, FLOOR + 7, 22, Z + "polished_black_cerulean_stone_bricks")   # arch shoulders
put(0, FLOOR + 8, 23, Z + "pulsar_lamp")                                    # the Concord mark: a lit keystone
put(-1, FLOOR + 8, 23, Z + "chiseled_polished_black_cerulean_stone")
put(1, FLOOR + 8, 23, Z + "chiseled_polished_black_cerulean_stone")
# crystal-sand apron and starbloom planters by the door
for dx in range(-6, 7):
    for dz in (22, 23):
        if abs(dx) > 3:
            put(dx, FLOOR, dz, Z + "crystal_sand")
for dx in (-5, 5):
    put(dx, FLOOR, 23, Z + "azure_moss")
    put(dx, FLOOR + 1, 23, Z + "starbloom")

# ---- dome: 8 thin ribs from the buttresses up to a ring and crystal oculus ---------------------------------------------
RING_Y = FLOOR + 25
for k in range(8):
    a = math.radians(45 * k)
    for i in range(0, 121):
        t = i / 120
        rr = 21.0 - 15.0 * t
        y = round(WALL_TOP + 1 + (RING_Y - WALL_TOP - 1) * math.sin(t * math.pi / 2))
        dx, dz = round(rr * math.cos(a)), round(rr * math.sin(a))
        b = Z + "polished_black_cerulean_stone_bricks"
        if 0.35 < t < 0.75 and i % 9 == 0:
            b = Z + "crystal_glass"                          # crystal vein in each rib
        put(dx, y, dz, b)
for dx, dz in cells(6.6):
    r = r_of(dx, dz)
    if r >= 5.5:
        put(dx, RING_Y, dz, Z + "polished_black_cerulean_stone_bricks")
        put(dx, RING_Y + 1, dz, Z + "chiseled_polished_black_cerulean_stone" if r < 6.2 else "minecraft:air")
    else:
        put(dx, RING_Y + 1, dz, Z + ("shimmer_glass" if r < 2.2 else "crystal_glass"))   # the oculus
for dx, y, dz in CROWNS:                                     # after the ribs, which start on the buttresses
    put(dx, y, dz, Z + "cerulite_cluster[facing=up,waterlogged=false]")
put(0, RING_Y + 2, 0, Z + "pulsar_lamp")                     # beam source above the oculus (lights the dais)
for dx, dz in ((3, 0), (-3, 0), (0, 3), (0, -3)):
    put(dx, RING_Y + 2, dz, Z + "spectral_lantern")


# ---- NBT --------------------------------------------------------------------------------------------------------------
def s(v):
    b = v.encode("utf-8"); return struct.pack(">H", len(b)) + b
def tag(t, name, payload): return bytes([t]) + s(name) + payload
def p_int(v): return struct.pack(">i", v)
def p_double(v): return struct.pack(">d", v)
def p_compound(items): return b"".join(tag(t, n, p) for t, n, p in items) + b"\x00"
def p_list(et, payloads): return bytes([et]) + struct.pack(">i", len(payloads)) + b"".join(payloads)
TAG_INT, TAG_DOUBLE, TAG_STR, TAG_LIST, TAG_COMPOUND = 3, 6, 8, 9, 10


def parse_state(state):
    if "[" not in state:
        return state, {}
    name, props = state[:-1].split("[", 1)
    return name, dict(p.split("=") for p in props.split(","))


palette, index, blocks = [], {}, []
for (x, y, z), st in sorted(B.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
    if st not in index:
        index[st] = len(palette); palette.append(st)
    blocks.append((x, y, z, index[st]))
pal = []
for st in palette:
    name, props = parse_state(st)
    items = [(TAG_STR, "Name", s(name))]
    if props:
        items.append((TAG_COMPOUND, "Properties", p_compound([(TAG_STR, k, s(v)) for k, v in props.items()])))
    pal.append(p_compound(items))
blk = [p_compound([(TAG_LIST, "pos", p_list(TAG_INT, [p_int(x), p_int(y), p_int(z)])), (TAG_INT, "state", p_int(i))])
       for x, y, z, i in blocks]
ents = []
for ex, ey, ez, bx, by, bz in ENTITIES:
    nbt = p_compound([(TAG_STR, "id", s("minecraft:minecart")),
                      (TAG_LIST, "Pos", p_list(TAG_DOUBLE, [p_double(ex), p_double(ey), p_double(ez)]))])
    ents.append(p_compound([(TAG_LIST, "pos", p_list(TAG_DOUBLE, [p_double(ex), p_double(ey), p_double(ez)])),
                            (TAG_LIST, "blockPos", p_list(TAG_INT, [p_int(bx), p_int(by), p_int(bz)])),
                            (TAG_COMPOUND, "nbt", nbt)]))
root = p_compound([(TAG_INT, "DataVersion", p_int(3955)),
                   (TAG_LIST, "size", p_list(TAG_INT, [p_int(SX), p_int(SY), p_int(SZ)])),
                   (TAG_LIST, "palette", p_list(TAG_COMPOUND, pal)),
                   (TAG_LIST, "blocks", p_list(TAG_COMPOUND, blk)),
                   (TAG_LIST, "entities", p_list(TAG_COMPOUND, ents))])
with gzip.open(sys.argv[1], "wb") as fh:
    fh.write(bytes([TAG_COMPOUND]) + s("") + root)
solid = {}
for st in B.values():
    if st != "minecraft:air":
        n = parse_state(st)[0]; solid[n] = solid.get(n, 0) + 1
print(f"wrote {sys.argv[1]}: {len(B)} cells, {sum(solid.values())} solid, {len(palette)} states, {len(ENTITIES)} minecarts")
for n, c in sorted(solid.items(), key=lambda kv: -kv[1]):
    print(f"  {c:6d}  {n}")
