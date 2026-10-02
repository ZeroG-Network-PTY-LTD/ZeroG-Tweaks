"""Write the Prism Sentinel arena as a vanilla structure template (.nbt), like a structure block's SAVE button.

usage: python export_arena_nbt.py OUT.nbt
Box origin is the arena's min corner (-23, Y0, -23); size 47 x 22 x 47. Air is stored for the open space inside the
arena (so placing it in terrain clears the hall); everything outside the walls is left out (keeps the terrain).
"""
import gzip, io, math, struct, sys, contextlib

with contextlib.redirect_stdout(io.StringIO()):
    import build_prism_arena as arena  # builds arena.B: {(x, y, z): "id[props]"}

DATA_VERSION = 3955  # Minecraft 1.21.1
OX, OY, OZ = -23, arena.Y0, -23
SX, SY, SZ = 47, 22, 47


# ---- tiny NBT writer -------------------------------------------------------------------------------
def s(v):
    b = v.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def tag(t, name, payload):
    return bytes([t]) + s(name) + payload


def p_int(v): return struct.pack(">i", v)
def p_str(v): return s(v)


def p_compound(items):  # items: list of (type, name, payload)
    return b"".join(tag(t, n, p) for t, n, p in items) + b"\x00"


def p_list(elem_type, payloads):
    return bytes([elem_type]) + struct.pack(">i", len(payloads)) + b"".join(payloads)


TAG_INT, TAG_STR, TAG_LIST, TAG_COMPOUND = 3, 8, 9, 10


def parse_state(state):
    if "[" not in state:
        return state, {}
    name, props = state[:-1].split("[", 1)
    return name, dict(p.split("=") for p in props.split(","))


# ---- collect blocks ---------------------------------------------------------------------------------
cells = dict(arena.B)
for x in range(-21, 22):
    for z in range(-21, 22):
        if math.hypot(x, z) <= 20.6:
            for y in range(1, SY):
                cells.setdefault((x, OY + y, z), "minecraft:air")
palette, blocks = [], []
index = {}
for (x, y, z), state in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
    if state not in index:
        index[state] = len(palette)
        palette.append(state)
    blocks.append((x - OX, y - OY, z - OZ, index[state]))
assert all(0 <= bx < SX and 0 <= by < SY and 0 <= bz < SZ for bx, by, bz, _ in blocks), "block outside the box"

pal_payloads = []
for state in palette:
    name, props = parse_state(state)
    items = [(TAG_STR, "Name", p_str(name))]
    if props:
        items.append((TAG_COMPOUND, "Properties", p_compound([(TAG_STR, k, p_str(v)) for k, v in props.items()])))
    pal_payloads.append(p_compound(items))
blk_payloads = [p_compound([(TAG_LIST, "pos", p_list(TAG_INT, [p_int(bx), p_int(by), p_int(bz)])),
                            (TAG_INT, "state", p_int(st))]) for bx, by, bz, st in blocks]
root = p_compound([
    (TAG_INT, "DataVersion", p_int(DATA_VERSION)),
    (TAG_LIST, "size", p_list(TAG_INT, [p_int(SX), p_int(SY), p_int(SZ)])),
    (TAG_LIST, "palette", p_list(TAG_COMPOUND, pal_payloads)),
    (TAG_LIST, "blocks", p_list(TAG_COMPOUND, blk_payloads)),
    (TAG_LIST, "entities", p_list(TAG_COMPOUND, [])),
])
data = bytes([TAG_COMPOUND]) + s("") + root
with gzip.open(sys.argv[1], "wb") as fh:
    fh.write(data)
print(f"wrote {sys.argv[1]}: {len(blocks)} blocks ({len(arena.B)} solid + air), {len(palette)} palette states, size {SX}x{SY}x{SZ}")
