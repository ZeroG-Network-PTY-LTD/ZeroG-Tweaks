"""Checks the Concord Vault in a running dev-server world: rooms, Key Altar pieces, altar blocks really placed, key spread.

usage: python tools/dev/vault_world_check.py WORLD    (dev server running with that level-name, RCON on)
"""
import collections, itertools, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcon
from worldscan import chunk, dimension_dir, section_blocks

world = sys.argv[1]
dim = dimension_dir(world, 'zerog_tweaks:cerulon')
r = rcon.Rcon()
loc = r.cmd("execute in zerog_tweaks:cerulon positioned 0 100 0 run locate structure zerog_tweaks:concord_vault")
x, z = [int(v) for v in loc.split('[')[1].split(']')[0].replace('~', '0').split(',')[0::2]]
r.cmd(f"execute in zerog_tweaks:cerulon run forceload add {x} {z}"); r.cmd("save-all flush")
st = chunk(dim, x >> 4, z >> 4)["structures"]["starts"]["zerog_tweaks:concord_vault"]
kinds = collections.Counter(); bbs = []; chamber = None
for ch in st["Children"]:
    bbs.append(ch["BB"])
    if ch.get("id") == "minecraft:jigsaw":
        name = ch["pool_element"].get("location", "?").split("concord_vault/")[-1]; kinds[name] += 1
        if name == "chamber": chamber = ((ch["BB"][0] + ch["BB"][3]) / 2, (ch["BB"][2] + ch["BB"][5]) / 2)
    else:
        kinds[ch["id"]] += 1
rooms = sum(v for k, v in kinds.items() if k.startswith("rooms/"))
x0 = min(b[0] for b in bbs); z0 = min(b[2] for b in bbs); x1 = max(b[3] for b in bbs); z1 = max(b[5] for b in bbs)
r.cmd(f"execute in zerog_tweaks:cerulon run forceload add {x0} {z0} {x1} {z1}"); r.cmd("save-all flush")
found = []
for cx in range(x0 >> 4, (x1 >> 4) + 1):
    for cz in range(z0 >> 4, (z1 >> 4) + 1):
        c = chunk(dim, cx, cz)
        if not c: continue
        for sec in c.get("sections", []):
            names = [p["Name"] for p in sec.get("block_states", {}).get("palette", [])]
            if "zerog_tweaks:vault_key_altar" not in names: continue
            for i, name, y in section_blocks(sec):
                if name == "zerog_tweaks:vault_key_altar": found.append((cx * 16 + (i & 15), y, cz * 16 + ((i >> 4) & 15)))
d_ch = [round(math.hypot(a[0] - chamber[0], a[2] - chamber[1])) for a in found]
pair = min((math.hypot(a[0] - b[0], a[2] - b[2]) for a, b in itertools.combinations(found, 2)), default=0)
print(f"{world}: vault at {x},{z} | rooms {rooms} | altar pieces {kinds['zerog_tweaks:vault_key_altar']} | altar blocks placed "
      f"{len(found)} | distance from chamber {sorted(d_ch)} | closest two keys {round(pair)} blocks")
