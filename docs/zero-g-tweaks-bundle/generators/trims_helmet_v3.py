"""Trim patterns v3 - helmets. Clean raised line-work like vanilla trims: shapes are drawn as '#' lines and 'o' gems,
then auto-embossed (light top edge, mid body, dark drop-shadow underneath) so they read as inlaid metal on any armor.
Each pattern is one clear idea built from helmet parts: brow band, cheek guards, nose guard, crown crest.
Usage: python3 trims_helmet_v3.py <in_trim_dir> <out_trim_dir>"""
import sys, os
from PIL import Image

KEY = [(236, 236, 236), (212, 212, 212), (188, 188, 188), (164, 164, 164), (140, 140, 140), (116, 116, 116), (92, 92, 92), (68, 68, 68)]
# top: row 0 = back edge, row 7 = front edge.  side: player's RIGHT side, col 7 = front edge (mirrored for the left).  back: col 0 = player's left.
H = {
 'fracture': dict(  # a brow band split by a lightning crack that runs over the crown
  top=['...#....', '....#...', '....#...', '...#....', '...#....', '....#...', '....#...', '...#....'],
  front=['###..###', '...##...', '....#...', '........', '........', '........', '........', '........'],
  side=['########', '.....#..', '....#...', '........', '........', '........', '........', '........'],
  back=['###..###', '...##...', '....#...', '...#....', '...#....', '....#...', '........', '........']),
 'crater': dict(  # a rim band with two dents, and an impact ring on the crown
  top=['........', '..####..', '.#....#.', '.#.oo.#.', '.#.oo.#.', '.#....#.', '..####..', '........'],
  front=['########', '.o....o.', '........', '........', '........', '........', '........', '........'],
  side=['########', '........', '...##...', '..#..#..', '...##...', '........', '........', '........'],
  back=['########', '........', '...##...', '..#..#..', '..#..#..', '...##...', '........', '........']),
 'olympus': dict(  # a single ridge crest and a mountain peak rising off the brow; ranges on the sides
  top=['...##...', '...##...', '...##...', '...##...', '...##...', '...##...', '...##...', '...##...'],
  front=['...##...', '..#..#..', '.#....#.', '#......#', '........', '........', '........', '........'],
  side=['........', '........', '........', '........', '....#...', '...#.#..', '..#...#.', '.#.....#'],
  back=['...##...', '..#..#..', '.#....#.', '#..##..#', '..#..#..', '.#....#.', '#......#', '........']),
 'geode': dict(  # a cut gem set in the brow, a faceted diamond on the crown
  top=['...##...', '..#..#..', '.#....#.', '#..oo..#', '#..oo..#', '.#....#.', '..#..#..', '...##...'],
  front=['..#oo#..', '...##...', '........', '........', '........', '........', '........', '........'],
  side=['........', '...#....', '..#.#...', '.#.o.#..', '..#.#...', '...#....', '........', '........'],
  back=['...##...', '..#..#..', '.#.oo.#.', '..#..#..', '...##...', '........', '........', '........']),
 'rift': dict(  # two long claw tears across the crown that rake down both sides
  top=['#.......', '.#....#.', '..#....#', '...#....', '....#...', '.....#..', '......#.', '.......#'],
  front=['#.......', '.#......', '........', '........', '........', '........', '........', '........'],
  side=['#...#...', '.#...#..', '..#...#.', '...#...#', '........', '........', '........', '........'],
  back=['.#....#.', '..#....#', '...#....', '....#...', '........', '........', '........', '........']),
 'hull': dict(  # armored plates: brow and neck bands, cheek plates, rivets, a seam over the crown
  top=['...o....', '...#....', '...#....', '...#....', '...#....', '...#....', '...#....', '...o....'],
  front=['########', '#......#', '#......#', '#......#', '#......#', '#......#', 'o......o', '........'],
  side=['########', '........', '....#...', '....#...', '....#...', '....#...', '........', '########'],
  back=['########', '.o....o.', '...##...', '...##...', '...##...', '...##...', '.o....o.', '########']),
 'corona': dict(  # a sun on the crown with four rays, and a sunrise arc over the brow
  top=['...##...', '...##...', '..####..', '##.oo.##', '##.oo.##', '..####..', '...##...', '...##...'],
  front=['...##...', '.#.##.#.', '..####..', '........', '........', '........', '........', '........'],
  side=['....##..', '....##..', '........', '........', '........', '........', '........', '........'],
  back=['...##...', '.#.##.#.', '..####..', '........', '........', '........', '........', '........']),
 'surge': dict(  # one wave line wrapping the helmet, and a wave crest over the crown
  top=['..#.....', '...#....', '...#....', '..#.....', '..#.....', '...#....', '...#....', '..#.....'],
  front=['........', '........', '........', '........', '........', '##....##', '..#..#..', '...##...'],
  side=['........', '........', '........', '........', '........', '.##...##', '#..#.#..', '....#...'],
  back=['........', '........', '........', '........', '........', '##....##', '..#..#..', '...##...']),
 'prism': dict(  # a triangle crest on the forehead, an arrow on the crown, stacked prisms on the back
  top=['........', '........', '.######.', '..#..#..', '...##...', '...##...', '...##...', '...##...'],
  front=['...##...', '..#..#..', '.######.', '........', '........', '........', '........', '........'],
  side=['........', '........', '........', '....#...', '...#.#..', '..#####.', '........', '........'],
  back=['...##...', '..#..#..', '.######.', '........', '...##...', '..#..#..', '.######.', '........']),
 'meteor': dict(  # a meteor streaks over the crown and its glowing head lands on the brow
  top=['#.......', '.#......', '..#.....', '...#....', '....#...', '.....#..', '......##', '......oo'],
  front=['......oo', '.....##.', '........', '........', '........', '........', '........', '........'],
  side=['........', '.#......', '..#.....', '........', '........', '........', '........', '........'],
  back=['#.......', '.#......', '........', '........', '........', '........', '........', '........']),
}
FACES = {'top': (8, 0), 'right': (0, 8), 'front': (8, 8), 'left': (16, 8), 'back': (24, 8)}

def emboss(rows):
    """'#'/'o' grid -> {(x,y): key}. Light where the pixel above is empty, mid elsewhere; gems bright;
    a dark drop shadow under each line where there is room."""
    on = {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c in '#o'}
    out = {}
    for (x, y) in on:
        c = rows[y][x]
        if c == 'o': out[(x, y)] = 0
        else: out[(x, y)] = 1 if (x, y - 1) not in on else 3
    for (x, y) in on:
        if rows[y][x] == '#' and y + 1 < 8 and (x, y + 1) not in on and (x, y + 1) not in out:
            out[(x, y + 1)] = 6
    return out

def paint(im, pid):
    g = H[pid]; p = im.load()
    for k, rows in g.items(): assert len(rows) == 8 and all(len(r) == 8 for r in rows), (pid, k)
    for x in range(32):
        for y in range(16):
            if (8 <= x < 24 and y < 8) or y >= 8: p[x, y] = (0, 0, 0, 0)
    def put(face, rows, mirror=False):
        ox, oy = FACES[face]
        for (x, y), k in emboss(rows).items():
            p[ox + (7 - x if mirror else x), oy + y] = KEY[k] + (255,)
    put('top', g['top']); put('front', g['front']); put('back', g['back']); put('right', g['side']); put('left', g['side'], True)
    return im

if __name__ == '__main__':
    src, dst = sys.argv[1:3]; os.makedirs(dst, exist_ok=True)
    for pid in H: paint(Image.open(f'{src}/{pid}.png').convert('RGBA'), pid).save(f'{dst}/{pid}.png')
    print('helmets v3:', len(H))
