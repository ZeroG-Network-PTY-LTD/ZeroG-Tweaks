"""Read saved chunks of a dev-server world straight from its region files (no Minecraft needed) and count blocks.

Used to check what world generation really placed, e.g. "is any vanilla dripstone generating on the planets?".

usage: python tools/dev/worldscan.py WORLD DIMENSION [CX CZ RADIUS]
         WORLD      folder name under run-server/ (level-name in server.properties)
         DIMENSION  e.g. zerog_tweaks:cerulon, or minecraft:overworld
         CX CZ      centre chunk (default 0 0), RADIUS in chunks (default 4)
       Prints every block type in the area with its count and height range; only chunks that were saved are read.
       Generate the area first, e.g. with tools/dev/rcon.py:
         python tools/dev/rcon.py "execute in zerog_tweaks:cerulon run forceload add -64 -64 63 63"
         python tools/dev/rcon.py "save-all flush"

As a library: from worldscan import chunk, dimension_dir, section_blocks
"""
import collections, os, struct, sys, zlib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def _read(b, i, t):
    if t == 1: return b[i], i + 1
    if t == 2: return struct.unpack_from(">h", b, i)[0], i + 2
    if t == 3: return struct.unpack_from(">i", b, i)[0], i + 4
    if t == 4: return struct.unpack_from(">q", b, i)[0], i + 8
    if t == 5: return struct.unpack_from(">f", b, i)[0], i + 4
    if t == 6: return struct.unpack_from(">d", b, i)[0], i + 8
    if t == 7: n = struct.unpack_from(">i", b, i)[0]; return b[i + 4:i + 4 + n], i + 4 + n
    if t == 8: n = struct.unpack_from(">H", b, i)[0]; return b[i + 2:i + 2 + n].decode('utf-8', 'replace'), i + 2 + n
    if t == 9:
        et = b[i]; n = struct.unpack_from(">i", b, i + 1)[0]; i += 5; out = []
        for _ in range(n):
            v, i = _read(b, i, et); out.append(v)
        return out, i
    if t == 10:
        d = {}
        while True:
            tt = b[i]; i += 1
            if tt == 0: return d, i
            n = struct.unpack_from(">H", b, i)[0]; name = b[i + 2:i + 2 + n].decode(); i += 2 + n
            d[name], i = _read(b, i, tt)
    if t == 11: n = struct.unpack_from(">i", b, i)[0]; return list(struct.unpack_from(f">{n}i", b, i + 4)), i + 4 + 4 * n
    if t == 12: n = struct.unpack_from(">i", b, i)[0]; return list(struct.unpack_from(f">{n}q", b, i + 4)), i + 4 + 8 * n
    raise ValueError(f"NBT tag {t}")


def dimension_dir(world, dimension):
    """Folder holding region/ for a dimension of run-server/<world>."""
    base = os.path.join(REPO, 'run-server', world)
    ns, path = dimension.split(':') if ':' in dimension else ('zerog_tweaks', dimension)
    if (ns, path) == ('minecraft', 'overworld'): return base
    if (ns, path) == ('minecraft', 'the_nether'): return os.path.join(base, 'DIM-1')
    if (ns, path) == ('minecraft', 'the_end'): return os.path.join(base, 'DIM1')
    return os.path.join(base, 'dimensions', ns, path)


def chunk(dim_dir, cx, cz):
    """The chunk's NBT as nested dicts/lists, or None if it was never saved."""
    path = os.path.join(dim_dir, 'region', f"r.{cx >> 5}.{cz >> 5}.mca")
    if not os.path.exists(path): return None
    f = open(path, "rb").read()
    off = struct.unpack_from(">I", f, 4 * ((cx & 31) + (cz & 31) * 32))[0]
    if off == 0: return None
    s = (off >> 8) * 4096; ln = struct.unpack_from(">I", f, s)[0]
    data = zlib.decompress(f[s + 5:s + 4 + ln])
    return _read(data, 3 + struct.unpack_from(">H", data, 1)[0], 10)[0]


def section_blocks(section):
    """Yields (local_index, block_name, y) for the 4096 cells of a chunk section (index: x + z*16 + (y&15)*256)."""
    bs = section.get('block_states')
    if not bs: return
    pal = [p['Name'] for p in bs['palette']]
    y0 = ((section['Y'] + 128) % 256 - 128) * 16          # Y is a signed byte
    if len(pal) == 1:
        for i in range(4096): yield i, pal[0], y0 + (i >> 8)
        return
    bits = max(4, (len(pal) - 1).bit_length()); per = 64 // bits; mask = (1 << bits) - 1
    data = bs['data']
    for i in range(4096):
        yield i, pal[((data[i // per] & 0xFFFFFFFFFFFFFFFF) >> ((i % per) * bits)) & mask], y0 + (i >> 8)


def count_blocks(dim_dir, cx0, cz0, cx1, cz1):
    counts = collections.Counter(); low = {}; high = {}; chunks = 0
    for cx in range(cx0, cx1 + 1):
        for cz in range(cz0, cz1 + 1):
            c = chunk(dim_dir, cx, cz)
            if not c or not c.get('sections'): continue
            chunks += 1
            for sec in c['sections']:
                for _, name, y in section_blocks(sec):
                    counts[name] += 1
                    low[name] = min(low.get(name, y), y); high[name] = max(high.get(name, y), y)
    return chunks, counts, low, high


if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    world, dimension = sys.argv[1], sys.argv[2]
    cx, cz, radius = (int(v) for v in (sys.argv[3:6] + ['0', '0', '4'][len(sys.argv[3:6]):]))
    d = dimension_dir(world, dimension)
    chunks, counts, low, high = count_blocks(d, cx - radius, cz - radius, cx + radius - 1, cz + radius - 1)
    print(f"{dimension} in {world}: {chunks} saved chunks around chunk {cx},{cz}")
    for name, n in counts.most_common():
        flag = '  <- vanilla' if name.startswith('minecraft:') and name not in (
            'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:bedrock') else ''
        print(f"{n:>9}  {name:45} y {low[name]}..{high[name]}{flag}")
